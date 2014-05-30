# -*- coding: utf-8 -*-
'''
Created on 2014-2-17
@author: CL.lam
'''
import os
import random
import traceback
import transaction
import shutil
import json
from datetime import datetime as dt
from tg import expose, redirect, flash, request, config, session
from tg.decorators import paginate
from repoze.what import authorize
from repoze.what.predicates import has_permission
from sqlalchemy.sql.expression import and_, desc

from rpac.lib.base import BaseController
from rpac.util.common import tabFocus, logError, serveFile, \
    ReportGenerationException, sendEmail
import rpac.model as DBModel
from rpac.model import qry, DBSession, OrderHeader, PrintShop, AddressBook, \
                        Product, Option, CO, Care, DateCode, DotPantone, Category, Fibers
from rpac.widgets.ordering import order_search_form
from rpac.util.excel_helper import FDReport, getExcelVersion, FDOrder
from rpac.model.ordering import ORDER_INPROCESS, ORDER_COMPLETE, ORDER_NEW, \
    OrderDetail, ORDER_CANCEL, ORDER_MANUAL
from rpac.util.layout_pdf import gen_pdf



__all__ = ['OrderingController', ]


DEFAULT_SENDER = 'r-pac-fd-order-system@r-pac.com.hk'


class OrderingController(BaseController):
    allow_only = authorize.not_anonymous()

    @expose('rpac.templates.ordering.index')
    @paginate("result", items_per_page = 20)
    @tabFocus(tab_type = "main")
    def index(self , **kw):
        ws = [OrderHeader.active == 0]
        if kw.get("no", False) : ws.append(OrderHeader.no.op("ilike")("%%%s%%" % kw["no"]))
        if kw.get("customerpo", False) : ws.append(OrderHeader.customerpo.op("ilike")("%%%s%%" % kw["customerpo"]))
        if kw.get("vendorpo", False) : ws.append(OrderHeader.vendorpo.op("ilike")("%%%s%%" % kw["vendorpo"]))
        if kw.get("status", False) : ws.append(OrderHeader.status == kw["status"])
        if kw.get("printShopId", False) : ws.append(OrderHeader.printShopId == kw["printShopId"])
        if not has_permission("MAIN_ORDERING_CHECKING_ALL"): ws.append(OrderHeader.createById == request.identity["user"].user_id)

        result = qry(OrderHeader).filter(and_(*ws)).order_by(desc(OrderHeader.createTime)).all()
        ps = qry(PrintShop).filter(and_(PrintShop.active == 0)).order_by(PrintShop.name)
        return { "result" : result , "values" : kw, "widget" : order_search_form , "printshops" : ps}


    @expose()
    def export(self, **kw):
        ws = [OrderHeader.active == 0]
        if kw.get("no", False) : ws.append(OrderHeader.no.op("ilike")("%%%s%%" % kw["no"]))
        if kw.get("customerpo", False) : ws.append(OrderHeader.customerpo.op("ilike")("%%%s%%" % kw["customerpo"]))
        if kw.get("vendorpo", False) : ws.append(OrderHeader.vendorpo.op("ilike")("%%%s%%" % kw["vendorpo"]))
        if kw.get("status", False) : ws.append(OrderHeader.status == kw["status"])
        if kw.get("printShopId", False) : ws.append(OrderHeader.printShopId == kw["printShopId"])
        if not has_permission("MAIN_ORDERING_CHECKING_ALL"): ws.append(OrderHeader.createById == request.identity["user"].user_id)

        data = []
        for h in  qry(OrderHeader).filter(and_(*ws)).order_by(desc(OrderHeader.createTime)):
            data.append(map(unicode, [ h.no, h.customerpo, h.vendorpo, h.createTime.strftime("%Y/%m/%d %H:%M"),
                                      h.createBy, h.printShop, h.showStatus(),
                                      h.completeDate.strftime("%Y/%m/%d %H:%M") if h.completeDate else '',
                                      h.shipQty or '',
                                     ]))

        try:
            v = getExcelVersion()
            if not v : raise ReportGenerationException()
            if v <= "2003" :  # version below 2003
                templatePath = os.path.join(config.get("public_dir"), "TEMPLATE", "FD_REPORT_TEMPLATE.xls")
            else :  # version above 2003
                templatePath = os.path.join(config.get("public_dir"), "TEMPLATE", "FD_REPORT_TEMPLATE.xlsx")

            tempFileName, realFileName = self._getReportFilePath(templatePath)
            sdexcel = FDReport(templatePath = tempFileName, destinationPath = realFileName)
            sdexcel.inputData(data)
            sdexcel.outputData()
        except:
            traceback.print_exc()
            logError()
            if sdexcel:sdexcel.clearData()
            raise ReportGenerationException()
        else:
            return serveFile(realFileName)



    def _getReportFilePath(self, templatePath):
        current = dt.now()
        dateStr = current.strftime("%Y%m%d")
        fileDir = os.path.join(config.get("public_dir"), "fd", dateStr)
        if not os.path.exists(fileDir): os.makedirs(fileDir)
        v = getExcelVersion()
        if not v : raise ReportGenerationException()
        if v <= "2003" :  # version below 2003
            tempFileName = os.path.join(fileDir, "%s_%s_%d.xls" % (request.identity["user"].user_name,
                                                               current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
            realFileName = os.path.join(fileDir, "%s_%s.xls" % (request.identity["user"].user_name, current.strftime("%Y%m%d%H%M%S")))
        else:
            tempFileName = os.path.join(fileDir, "%s_%s_%d.xlsx" % (request.identity["user"].user_name,
                                                               current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
            realFileName = os.path.join(fileDir, "%s_%s.xlsx" % (request.identity["user"].user_name, current.strftime("%Y%m%d%H%M%S")))
        shutil.copy(templatePath, tempFileName)
        return tempFileName, realFileName



    @expose('rpac.templates.ordering.detail')
    @paginate("result", items_per_page = 20)
    @tabFocus(tab_type = "main")
    def detail(self, **kw):
        hid = kw.get('id', None)
        if not hid :
            flash("No ID provides!", "warn")
            return redirect('/ordering/index')

        try:
            obj = qry(OrderHeader).filter(and_(OrderHeader.active == 0 , OrderHeader.id == hid)).one()
        except:
            flash("The record does not exist!", "warn")
            return redirect('/ordering/index')


        return {
                'obj' : obj ,

                }




    @expose('rpac.templates.ordering.placeorder')
    @tabFocus(tab_type = "main")
    def placeorder(self , **kw):
        locations = qry(PrintShop).filter(and_(PrintShop.active == 0)).order_by(PrintShop.name)
        address = qry(AddressBook).filter(and_(AddressBook.active == 0, AddressBook.createById == request.identity['user'].user_id)).order_by(AddressBook.createTime).all()
        values = {}
        if len(address) > 0 :
            for f in ['shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3',
                      'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax', 'shipEmail', 'shipRemark',
                      'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3',
                      'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax', 'billEmail', 'billRemark'] :
                values[f] = unicode(getattr(address[0], f) or '')

        products = []
        for p in session.get('items', []) :
            p['productobj'] = qry(Product).get(p['id'])
            products.append(p)

        return {'locations' : locations ,
                'products' : products, 'address' : address,
                'values' : values,
                'address' : address,
                }


    @expose()
    def saveorder(self, **kw):
        try:
            addressFields = [
                              'shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3', 'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax', 'shipEmail', 'shipRemark',
                              'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3', 'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax', 'billEmail', 'billRemark',
                             ]
            fields = [ 'customerpo', 'vendorpo', 'printShopId', 'shipInstructions']
            params = {}
            for f in addressFields: params[f] = kw.get(f, None) or None
            if kw.get('addressID', None) == 'OTHER': DBSession.add(AddressBook(**params))
            for f in fields: params[f] = kw.get(f, None) or None
            if params['printShopId'] : params['printShopCopy'] = unicode(qry(PrintShop).get(params['printShopId']))

            hdr = OrderHeader(**params)
            DBSession.add(hdr)
            qtys = []
            for item in session.get('items' , []):
                params = {
                          'header' : hdr, 'product' : item['productobj'],
                          'itemCode' : item['productobj'].itemCode,
                          'desc' : item['productobj'].desc,
                          'size' : item['productobj'].size,
                          'qty' : item['qty'] or None,
                          }
                if item.get('values', None) or None : params['optionContent'] = json.dumps(item.get('values', []))
                if item.get('optionstext', None) or None : params['optionText'] = json.dumps(item['optionstext'])

                params['layoutValue'] = json.dumps(self._setLayoutValue(item.get('values', [])))
                DBSession.add(OrderDetail(**params))
                qtys.append(item['qty'])
            DBSession.flush()
            hdr.totalQty = sum(map(int, filter(unicode.isdigit , qtys)))
        except:
            transaction.doom()
            traceback.print_exc()
            flash('Error occur on the server side!', "warn")
            return redirect('/ordering/placeorder')
        else:
            try:
                del session['items']
                session.save()
            except:
                pass
            return redirect('/ordering/afterSaveOrder?id=%s' % hdr.id)




    def _genExcel(self, hdr):
        v = getExcelVersion()
        if not v : raise ReportGenerationException()
        if v <= "2003" :  # version below 2003
            templatePath = os.path.join(config.get("public_dir"), "TEMPLATE", "FD_DETAIL_TEMPLATE.xls")
        else :  # version above 2003
            templatePath = os.path.join(config.get("public_dir"), "TEMPLATE", "FD_DETAIL_TEMPLATE.xlsx")

        current = dt.now()
        dateStr = current.strftime("%Y%m%d")
        fileDir = os.path.join(config.get("public_dir"), "excel", dateStr)
        if not os.path.exists(fileDir): os.makedirs(fileDir)

        if v <= "2003" :  # version below 2003
            tempFileName = os.path.join(fileDir, "%s_%s_%d.xls" % (request.identity["user"].user_name,
                                                               current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
            realFileName = os.path.join(fileDir, "%s_%s.xls" % (request.identity["user"].user_name, current.strftime("%Y%m%d%H%M%S")))
        else:
            tempFileName = os.path.join(fileDir, "%s_%s_%d.xlsx" % (request.identity["user"].user_name,
                                                               current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
            realFileName = os.path.join(fileDir, "%s_%s.xlsx" % (hdr.no, current.strftime("%Y%m%d%H%M%S")))

        shutil.copy(templatePath, tempFileName)

        data = { 'createTime' : hdr.createTime.strftime("%Y-%m-%d %H:%M") }
        for f in [ 'no', 'shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3',
                   'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax',
                   'shipEmail', 'shipRemark',
                   'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3',
                   'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax',
                   'billEmail', 'billRemark',
                   'customerpo', 'vendorpo', 'printShopCopy', 'shipInstructions' ]:
            data[f] = unicode(getattr(hdr, f) or '')

        data['details'] = [map(lambda v : unicode(v or ''), [d.itemCode, d.desc, d.size, d.qty,
                                                             '\n'.join(json.loads(d.optionText)) if d.optionText else '',
                                                             ]) for d in hdr.dtls]
        try:
            sdexcel = FDOrder(templatePath = tempFileName, destinationPath = realFileName)
            sdexcel.inputData(data)
            sdexcel.outputData()
            return realFileName
        except Exception, e:
            traceback.print_exc()
            raise e


    @expose()
    def getexcel(self, **kw):
        hid = kw.get('id', None)
        if not hid :
            flash("No ID provided!")
            return redirect('/index')

        hdr = DBSession.query(OrderHeader).get(hid)
        xls = self._genExcel(hdr)
        return serveFile(unicode(xls))


    @expose()
    def afterSaveOrder(self, **kw):
        _id = kw.get('id', None) or None
        if not _id:
            flash("No ID provided !", "warn")
            return redirect('/index')

        try:
            hdr = qry(OrderHeader).get(_id)
            #=======================================================================
            # generate excel
            #=======================================================================
            xls = self._genExcel(hdr)
            #=======================================================================
            # generate PDF
            #=======================================================================
            details = [(d.id, d.itemCode) for d in hdr.dtls]
            pdf = gen_pdf(hdr.no, details)
            files1 = [pdf]
            files2 = [pdf, xls, ]

            #=======================================================================
            # send email to user
            #=======================================================================
            subject = "[FD] Order(%s) is placed" % hdr.no
            content = [
                       "Dear User:",
                       "Order(%s) is placed, please check the below link to check the detail." % hdr.no,
                       "%s/ordering/detail?id=%s" % (config.get('website_url', ''), hdr.id),
                       "Thanks.", "",
                       "*" * 80,
                       "This e-mail is sent by the r-pac Family Dollar ordering system automatically.",
                       "Please don't reply this e-mail directly!",
                       "*" * 80,
                       ]
            self._toVendor(hdr, subject, content, files1)
            #=======================================================================
            # send email to print shop
            #=======================================================================
            self._toPrintshop(hdr, subject, content, files2)
            flash("Save the order successfully!", "ok")
        except:
            traceback.print_exc()
            flash("The service is not available now ,please try again later.", 'warn')
            return redirect('/ordering/index')
        else:
            return redirect('/ordering/detail?id=%s' % hdr.id)


    @expose()
    def cancelOrder(self, **kw):
        _id = kw.get("id", None) or None
        if not _id :
            flash("No ID provided!")
            return redirect('/ordering/index')

        hdr = qry(OrderHeader).get(_id)
        hdr.status = ORDER_CANCEL
        subject = "[FD] Order(%s) is cancelled" % hdr.no
        content = [
                   "Dear User:",
                   "Order(%s) is cancelled." % hdr.no,
                   "Thanks.", "",
                   "*" * 80,
                   "This e-mail is sent by the r-pac Family Dollar ordering system automatically.",
                   "Please don't reply this e-mail directly!",
                   "*" * 80,
                   ]
        #=======================================================================
        # send email to user
        #=======================================================================
        self._toVendor(hdr, subject, content)
        #=======================================================================
        # send email to print shop
        #=======================================================================
        self._toPrintshop(hdr, subject, content)
        flash("Cancel the order successfully!")
        return redirect('/ordering/index')



    @expose("json")
    def ajaxOrderInfo(self, **kw):
        hid = kw.get('id', None)
        if not hid : return {'flag' : 1 , 'msg' : 'No ID provided!'}
        try:
            data = []
            for d in qry(OrderDetail).filter(and_(OrderDetail.active == 0, OrderDetail.headerId == hid)).order_by(OrderDetail.id):
                data.append({'id' : d.id, 'code' : d.itemCode , 'qty' : d.qty})
            return {'flag' : 0, 'data' : data}
        except:
            traceback.print_exc()
            return {'flag' : 1 , 'msg' : 'Error occur on the server side!'}



    @expose('rpac.templates.ordering.manage_address')
    @paginate("result", items_per_page = 20)
    @tabFocus(tab_type = "ship")
    def manageAddress(self, **kw):
        result = DBSession.query(AddressBook).filter(and_(AddressBook.active == 0, AddressBook.createById == request.identity['user'].user_id)).order_by(desc(AddressBook.createTime))
        return {'result' : result}



    @expose('rpac.templates.ordering.edit_address')
    @tabFocus(tab_type = "ship")
    def editAddress(self, **kw):
        _id = kw.get('id', None)
        if not _id :
            flash('No id provided!' , "warn")
            return redirect('/index')

        obj = DBSession.query(AddressBook).get(_id)
        values = {'id' : obj.id}
        for f in ['shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3',
                  'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax', 'shipEmail', 'shipRemark',
                  'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3',
                  'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax', 'billEmail', 'billRemark'] :
            values[f] = unicode(getattr(obj, f) or '')
        return {'values' : values}


    @expose()
    def saveAddress(self, **kw):
        _id = kw.get('id', None)
        if not _id :
            flash('No id provided!', 'warn')
            return redirect('/ordering/manageAddress')

        fields = ['shipCompany', 'shipAttn', 'shipAddress', 'shipAddress2', 'shipAddress3',
                  'shipCity', 'shipState', 'shipZip', 'shipCountry', 'shipTel', 'shipFax', 'shipEmail', 'shipRemark',
                  'billCompany', 'billAttn', 'billAddress', 'billAddress2', 'billAddress3',
                  'billCity', 'billState', 'billZip', 'billCountry', 'billTel', 'billFax', 'billEmail', 'billRemark']

        try:
            obj = DBSession.query(AddressBook).get(_id)
            for f in fields : setattr(obj, f, kw.get(f, None) or None)
            flash('Save the record successfully!', 'ok')
        except:
            traceback.print_exc()
            flash("The service is not available now ,please try again later.", 'warn')
        return redirect('/ordering/manageAddress')


    @expose()
    def delAddress(self, **kw):
        oid = kw.get('id', None)
        if not oid :
            flash('No id provided!', 'warn')
            return redirect('/ordering/manageAddress')

        obj = DBSession.query(AddressBook).get(oid)
        if not obj :
            flash('The record does not exist!', 'warn')
            return redirect('/ordering/manageAddress')

        obj.active = 1
        flash('Update the record successfully!', 'ok')
        return redirect('/ordering/manageAddress')



    @expose('json')
    def ajaxAddress(self, **kw):
        aid = kw.get('addressID', None)
        if not aid : return {'code' : 1 , 'msg' : 'No ID provided!'}

        obj = qry(AddressBook).get(aid)
        if not obj : return {'code' : 1 , 'msg' : 'The record does not exist!'}

        result = {'code' : 0}
        for f in ["shipCompany", "shipAttn", "shipAddress", "shipAddress2", "shipAddress3", "shipCity", "shipState",
                  "shipZip", "shipCountry", "shipTel", "shipFax", "shipEmail", "shipRemark",
                  "billCompany", "billAttn", "billAddress", "billAddress2", "billAddress3", "billCity", "billState",
                  "billZip", "billCountry", "billTel", "billFax", "billEmail", "billRemark", ] :
            result[f] = unicode(getattr(obj, f) or '')
        return result



    @expose('json')
    def ajaxChangeStatus(self, **kw):
        _id, status = kw.get('id', None) or None , kw.get('status', None) or None
        if not _id or not status:
            return {'flag' : 1 , 'msg' : 'No enough parameter(s) provided!'}

        if status not in map(unicode, [ORDER_INPROCESS, ORDER_COMPLETE, ]):
            return {'flag' : 1 , 'msg' : 'No such operation!'}

        try:
            hdr = qry(OrderHeader).get(_id)

            if status == unicode(ORDER_INPROCESS):
                so = kw.get('so', None) or None
                if not so : return {'flag' : 1 , 'msg' : 'No enough parameter(s) provided!'}
                if hdr.status != ORDER_NEW:
                    return {'flag' : 1 , 'msg' : 'The record is not in NEW status!'}
                hdr.so, hdr.status = so, ORDER_INPROCESS
            elif status == unicode(ORDER_COMPLETE):
                if hdr.status != ORDER_INPROCESS:
                    return {'flag' : 1 , 'msg' : 'The record is not in process status!'}
                hdr.status, hdr.completeDate = ORDER_COMPLETE, dt.now()
                totalqty = 0
                for d in hdr.dtls:
                    key = "ship_%s" % d.id
                    if kw.get(key, None) :
                        d.shipQty = kw[key]
                        try:
                            totalqty += int(d.shipQty)
                        except:
                            pass
                hdr.shipQty = totalqty
                self._sendEmailToVendor(hdr)
                self._sendEmailToPrintshop(hdr)
        except:

            traceback.print_exc()
            return {'flag' : 1, 'msg' : 'Error occur on the sever side !'}
        return {'flag' : 0}



    def _sendEmailToVendor(self, hdr):
        subject = "[FD] Order(%s) is completed" % hdr.no
        content = [
                   "Dear User:",
                   "Order(%s) is completed, please check the below link to check the detail." % hdr.no,
                   "%s/ordering/detail?id=%s" % (config.get('website_url', ''), hdr.id),
                   "Thanks.", "",
                   "*" * 80,
                   "This e-mail is sent by the r-pac Family Dollar ordering system automatically.",
                   "Please don't reply this e-mail directly!",
                   "*" * 80,
                   ]
        self._toVendor(hdr, subject, content)


    def _sendEmailToPrintshop(self, hdr):
        subject = "[FD] Order(%s) is completed" % hdr.no
        content = [
                   "Dear User:",
                   "Order(%s) is completed, please check the below link to check the detail." % hdr.no,
                   "%s/ordering/detail?id=%s" % (config.get('website_url', ''), hdr.id),
                   "Thanks.", "",
                   "*" * 80,
                   "This e-mail is sent by the r-pac Family Dollar ordering system automatically.",
                   "Please don't reply this e-mail directly!",
                   "*" * 80,
                   ]
        self._toPrintshop(hdr, subject, content)


    def _toVendor(self, hdr , subject, content, files = []):
        defaultsendto = config.get("default_email_sendto", "").split(";")
        if hdr.createBy.email_address:  to = hdr.createBy.email_address.split(";")
        else: to = []
        sendto = defaultsendto + to
        cc = config.get("default_email_cc", "").split(";")
        if config.get("sendout_email", None) != 'F': sendEmail(DEFAULT_SENDER, sendto, subject, '\n'.join(content), cc, files)


    def _toPrintshop(self, hdr, subject, content, files = []):
        defaultsendto = config.get("default_email_sendto", "").split(";")
        if hdr.printShopId and hdr.printShop.email: to = hdr.printShop.email
        else: to = []
        sendto = defaultsendto + to
        cc = config.get("default_email_cc", "").split(";")
        if config.get("sendout_email", None) != 'F': sendEmail(DEFAULT_SENDER, sendto, subject, '\n'.join(content), cc, files)



    def _filterAndSorted(self, prefix, kw):
        return sorted(filter(lambda (k, v): k.startswith(prefix), kw.iteritems()), cmp = lambda x, y:cmp(x[0], y[0]))


    #===========================================================================
    # new function  for phase 2
    #===========================================================================
    @expose('rpac.templates.ordering.listItems')
    @tabFocus(tab_type = "main")
    def listItems(self, **kw):
        products = qry(Product).filter(and_(Product.active == 0)).order_by(Product.itemCode)
        return {'products' : products}


    def _getMaster(self, opt):
        if opt.master == 'CO' :
            objs = qry(CO).filter(and_(CO.active == 0)).order_by(CO.english)
        elif opt.master == 'Care' :
            objs = qry(Care).filter(and_(Care.active == 0 , Care.type == opt.conditions)).order_by(Care.english)
        elif opt.master == 'DateCode' :
            objs = qry(DateCode).filter(and_(DateCode.active == 0)).order_by(DateCode.val)
        elif opt.master == 'DotPantone' :
            objs = qry(DotPantone).filter(and_(DotPantone.active == 0)).order_by(DotPantone.val)
        elif opt.master == 'Category':
            objs = qry(Category).filter(and_(Category.active == 0)).order_by(Category.val)
        elif opt.master == 'Fibers':
            objs = qry(Fibers).filter(and_(Fibers.active == 0)).order_by(Fibers.english)
        else:
            objs = []
        return objs




    def _getProductInfo(self, obj):
        options = []
        product = {'id' : obj.id , 'moq' : obj.moq , 'roundup' : obj.roundup }
        for opt in obj.getOptions() :
            tmp = {
                   'name' : opt.name, 'type' : opt.type,
                   'id' : opt.id, 'multiple' : opt.multiple or '',
                   'css' :  json.loads(opt.css) if opt.css else {'SELECT' : [], 'TEXT' : []}
                   }
            if opt.type == 'TEXT':
                pass
            elif opt.type == 'SELECT' :
                tmp['values'] = [{'key' : obj.key, 'val' : obj.value} for obj in self._getMaster(opt)]
            elif opt.type == 'SELECT+TEXT':
                tmp['values'] = [{'key' : obj.key, 'val' : obj.value} for obj in self._getMaster(opt)]
            elif opt.type == 'SELECT+SELECT':
                pass
            options.append(tmp)
        return product, options


    @expose('json')
    def ajaxProductInfo(self, **kw):
        _id = kw.get('id', None) or None
        if not _id: return {'flag' : 1 , 'msg' : 'No ID provided!'}

        try:
            obj = qry(Product).get(_id)
            product, options = self._getProductInfo(obj)
            return {'flag' : 0 , 'product' : product, 'options' : options}
        except:
            traceback.print_exc()
            return {'flag' : 1, 'msg' : 'Error occur on the sever side !'}


    def _formatKW(self, kw):
        values, optionstext = [], []
        for k, v in self._filterAndSorted("option_", kw):
            val, text = v.split("|")
            values.append({ 'key' : k, 'value' : val, 'text' : text })
            if k.startswith('option_a_') :  # SELECT OR TEXT
                oid = k.split("_")[2]
                option = qry(Option).get(oid)
                if option.master in ['CO', 'Care']:
                    clz = getattr(DBModel, option.master)
                    obj = qry(clz).get(val)
                    if obj.english.upper() == 'NONE':
                        optionstext.append("%s : %s" % (option.name, ''))
                    elif option.language and 'S' not in option.language.split("|"):  # this option just need the english
                        optionstext.append("%s : %s" % (option.name, obj.english))
                    else:
                        optionstext.append("%s : [English]%s [Spanish]%s" % (option.name, obj.english, obj.spanish or ''))
                else:
                    optionstext.append("%s : %s" % (option.name, text))
            elif k.startswith('option_as_') :  # SELECT + TEXT
                oid = k.split("_")[2]
                option = qry(Option).get(oid)
                obj = qry(Fibers).get(val)
                e = obj.english if obj.english.upper() != 'NONE' else ''
                s = obj.spanish if obj.english.upper() != 'NONE' else ''

                k2 = k.replace('_as_', '_at_')
                v2 = kw.get(k2, '') or ''
                if option.language and 'S' not in option.language.split("|"):  # this option just need the english
                    optionstext.append("%s : %s - %s" % (option.name, e, v2.split('|')[0]))
                else:
                    optionstext.append("%s : [English]%s [Spanish]%s [Percentage]%s" % (option.name, e, s or '', v2.split('|')[0]))
        return values, optionstext


    @expose('json')
    def ajaxAddtoCart(self, **kw):
        _id = kw.get('id', None) or None
        if not _id : return {'flag' : 1 , 'msg' : 'No ID provided!'}

        try:
            items = session.get('items', [])
            tmp = {
                   '_k' : "%s%s" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(100, 10000)) ,
                   'id' : _id,
                   'qty' : kw.get('qty', None),
                   }
            tmp['values'], tmp['optionstext'] = self._formatKW(kw)
            items.append(tmp)
            session['items'] = items
            session.save()
            return {'flag' : 0 , 'total' : len(session['items'])}
        except:
            traceback.print_exc()
            return {'flag' : 1, 'msg':'Error occur on the sever side!'}


    @expose('json')
    def ajaxSavetoCart(self, **kw):
        _k = kw.get("_k", None)
        if not _k : return {'flag' : 1 , 'msg' : 'No ID provided!'}

        try:
            items = session.get('items', [])
            for index, item in enumerate(items):
                if item['_k'] != _k : continue
                item['qty'] = kw.get('qty', None) or None
                item['values'], item['optionstext'] = self._formatKW(kw)
                items[index] = item
                session['items'] = items
                session.save()
                return {'flag' : 0 , 'optionstext' : item['optionstext'], }
        except:
            traceback.print_exc()
            return {'flag' : 1 , 'msg' : 'Error occur on the sever side!'}
        return {'flag' : 1 , 'msg' : 'No such item!'}



    @expose('json')
    def ajaxRemoveItem(self, **kw):
        _k = kw.get("_k", None)
        if not _k : return {'flag' : 1 , 'msg' : 'No ID provided!'}

        try:
            session['items'] = filter(lambda item : item['_k'] != _k, session.get('items', []))
            session.save()
            return {'flag' : 0 }
        except:
            traceback.print_exc()
            return {'flag' : 1, 'msg':'Error occur on the sever side!'}


    @expose('json')
    def ajaxEditItem(self, **kw):
        _k = kw.get('_k', None) or None
        if not _k: return {'flag' : 1 , 'msg' : 'No ID provided!'}
        try:
            for s in session.get('items', []):
                if s['_k'] != _k : continue
                obj = qry(Product).get(s['id'])
                product, options = self._getProductInfo(obj)
                product['qty'] = s.get('qty', '')
                return {'flag' : 0 , 'product' : product, 'options' : options , 'values' : s.get('values', []) }
        except:
            traceback.print_exc()
            return {'flag' : 1, 'msg' : 'Error occur on the sever side !'}
        return {'flag' : 1 , 'msg' : 'No such item!'}



    @expose()
    def removeall(self, **kw):
        try:
            del session['items']
            session.save()
        except:
            pass
        return redirect('/ordering/listItems')



    def _setLayoutValue(self , values):
        layout = {}
        for v in values :
            gs = v['key'].split("_")
            f, oid = gs[1], gs[2]
            if f == 'at' : continue  # it's percentage ,will add in the fibers
            option = qry(Option).get(oid)

            if option.layoutKey in ['TRACKING', 'DESC', 'SKU', 'PRICE', 'NAME', 'SIZE', 'SKU', 'WPL']:
                lv = v['value']
            elif option.layoutKey in ['DOT', ]:
                d = qry(DotPantone).get(v['value'])
                lv = {'value' : v['text'] , 'css' : d.css}
            elif option.layoutKey in ['DATECODE', 'CATEGORY', ]:
                lv = v['text']
            elif option.layoutKey in ['CO', 'WASH', 'BLEACH', 'IRON', 'DRY', 'DRYCLEAN', 'SPECIALCARE']:
                if option.layoutKey == 'CO':
                    k = qry(CO).get(v['value'])
                else:
                    k = qry(Care).get(v['value'])
                if k.english.upper() == 'NONE':
                    lv = {'english' : '', 'spanish' : ''}
                else:
                    lv = {'english' : k.english, 'spanish' : k.spanish}
            elif option.layoutKey in ['FIBERS', ]:
                k = qry(Fibers).get(v['value'])
                if k.english.upper() == 'NONE':
                    lv = {'english' : '', 'spanish' : ''}
                else:
                    lv = {'english' : k.english, 'spanish' : k.spanish}

                pkey = v['key'].replace("_as_", "_at_")
                for tmp in values :
                    if tmp['key'] == pkey :
                        lv['percent'] = tmp['value']
                        break;
            if option.layoutKey not in layout:
                layout[option.layoutKey] = {'values' : [lv]}
            else:
                layout[option.layoutKey]['values'].append(lv)
        return layout



    @expose()
    def manual(self, **kw):
        _f = lambda k : kw.get(k, None) or None
        params = {
                  "customerpo" : _f("m_customerpo"), "vendorpo" : _f('m_po'), 'vendorName' : _f('m_vendorName'),
                  'so' : _f('m_so'), 'printShopId' : _f('m_location'), 'createTime' : _f('m_received'),
                  'completeDate' : _f('m_shipped'), 'status' : ORDER_MANUAL, 'source' : 'MANUAL',
                  }
        try:
            if params['printShopId'] :
                s = qry(PrintShop).get(params['printShopId'])
                params['printShopCopy'] = unicode(s)
            hdr = OrderHeader(**params)
            DBSession.add(hdr)

            itemcodes = self._filterAndSorted("m_itemcode_", kw)
            qtys = self._filterAndSorted("m_qty_", kw)
            shippedQty = []
            for (ck, cv), (qk, qv) in zip(itemcodes, qtys):
                if not cv or not qv : continue
                cv, qv = cv.strip(), qv.strip()
                if not qv.isdigit() : continue
                DBSession.add(OrderDetail(header = hdr, itemCode = cv, qty = qv, shipQty = qv))
                shippedQty.append(int(qv))
            hdr.shipQty = sum(shippedQty)
            hdr.totalQty = sum(shippedQty)
        except:
            traceback.print_exc()
            flash("Error occur on the server side!")
        else:
            flash('Save the manual order successfully!')
        return redirect('/ordering/index')
