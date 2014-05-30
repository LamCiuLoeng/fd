# -*- coding: utf-8 -*-
'''
Created on 2014-3-5
@author: CL.lam
'''

from tg import flash, redirect, expose
from tg.decorators import paginate
from repoze.what import authorize
from sqlalchemy.sql.expression import and_, desc


from rpac.lib.base import BaseController
from rpac.util.common import tabFocus
from rpac.model import qry, Care, Fibers, CO, DotPantone, Category, DateCode, PrintShop, DBSession
from rpac.widgets.master import master_search_form1, master_search_form2, \
    master_search_form3

__all__ = ['MasterController', ]


class MasterController( BaseController ):
    allow_only = authorize.not_anonymous()

    @expose( 'rpac.templates.master.index' )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "master" )
    def index( self , **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        dbclz = vs['dbclz']
        search_form = vs['search_form']
        label = vs['label']
        ws = []
        if search_form == master_search_form1:
            if kw.get( "val", False ) : ws.append( dbclz.val.op( "ilike" )( "%%%s%%" % kw["val"] ) )
        elif search_form == master_search_form2 or search_form == master_search_form3:
            if kw.get( "english", False ) : ws.append( dbclz.english.op( "ilike" )( "%%%s%%" % kw["english"] ) )
            if kw.get( "spanish", False ) : ws.append( dbclz.spanish.op( "ilike" )( "%%%s%%" % kw["spanish"] ) )
            if search_form == master_search_form3:
                if kw.get( "type", False ) : ws.append( dbclz.type == kw['type'] )
        if kw.get( "create_time_from", False ) : ws.append( dbclz.createTime >= kw["create_time_from"] )
        if kw.get( "create_time_to", False ) : ws.append( dbclz.createTime <= kw["create_time_from"] )
        ws.append( dbclz.active == 0 )

        result = qry( dbclz ).filter( and_( *ws ) ).order_by( desc( dbclz.createTime ) ).all()
        return { "result" : result , "values" : kw, "widget" : search_form, 'label' : label}


    @expose( 'rpac.templates.master.add' )
    @tabFocus( tab_type = "master" )
    def add( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        return {'t' : t , 'label' : vs['label']}


    @expose()
    def save_new( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        dbclz = vs['dbclz']
        if t in ['DotPantone', 'Category', 'DateCode', ]:
            val = kw.get( 'value', None ) or None
            if not val:
                flash( "The value could not be blank!", "warn" )
                return redirect( '/master/add?t=%s' % t )
            DBSession.add( dbclz( val = val ) )
            flash( 'Save the new recored successfully!', "ok" )
        elif t in ['Fibers', 'CO', ]:
            e, s = kw.get( 'english', None ) or None, kw.get( 'spanish', None ) or None
            if not e :
                flash( 'The English value could not be blank!', "warn" )
                return redirect( 'master/add?t=%s' % t )
            DBSession.add( dbclz( english = e, spanish = s ) )
            flash( 'Save the new recored successfully!', "ok" )
        elif t in ['Care', ]:
            e, s, tt = kw.get( 'english', None ) or None, kw.get( 'spanish', None ) or None, kw.get( 'type', None ) or None
            if not e :
                flash( 'The English value could not be blank!', "warn" )
                return redirect( 'master/add?t=%s' % t )
            DBSession.add( dbclz( english = e, spanish = s, type = tt ) )
            flash( 'Save the new recored successfully!', "ok" )
        return redirect( '/master/index?t=%s' % t )


    @expose( 'rpac.templates.master.edit' )
    @tabFocus( tab_type = "master" )
    def edit( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        _id = kw.get( 'id', None )
        dbclz = vs['dbclz']
        obj = qry( dbclz ).get( _id )
        return {'t' : t, 'obj' : obj , 'label' : vs['label']}


    @expose()
    def save_edit( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        _id = kw.get( 'id', None )
        dbclz = vs['dbclz']
        obj = qry( dbclz ).get( _id )

        if t in ['DotPantone', 'Category', 'DateCode', ]:
            val = kw.get( 'value', None ) or None
            if not val:
                flash( "The value could not be blank!", "warn" )
                return redirect( '/master/edit?id=%s&t=%s' % ( obj.id, t ) )
            obj.val = val

        elif t in ['Fibers', 'CO', ]:
            e, s = kw.get( 'english', None ) or None, kw.get( 'spanish', None ) or None
            if not e :
                flash( 'The English value could not be blank!', "warn" )
                return redirect( 'master/edit?t=%s' % t )
            obj.english , obj.spanish = e, s
        elif t in ['Care', ]:
            e, s, tt = kw.get( 'english', None ) or None, kw.get( 'spanish', None ) or None, kw.get( 'type', None ) or None
            if not e :
                flash( 'The English value could not be blank!', "warn" )
                return redirect( 'master/edit?t=%s' % t )
            obj.english , obj.spanish , obj.type = e, s, tt
        flash( 'Update the record successfully!', "ok" )
        return redirect( '/master/index?t=%s' % t )


    @expose()
    def delete( self, **kw ):
        t = kw.get( 't', None )
        vs = self._check( t )
        _id = kw.get( 'id', None )
        dbclz = vs['dbclz']
        obj = qry( dbclz ).get( _id )
        obj.active = 1
        flash( 'Delete the record successfully!', 'ok' )
        return redirect( '/master/index?t=%s' % t )


    def _check( self, t ):
        if t not in ['Care', 'Fibers', 'CO', 'DotPantone', 'Category', 'DateCode', 'PrintShop']:
            flash( "No such acton!", "warn" )
            return redirect( '/index' )

        if t == 'Care':
            dbclz, search_form, label = Care, master_search_form3, 'Care Instruction'
        elif t == 'Fibers':
            dbclz, search_form, label = Fibers, master_search_form2, 'Fibers Content'
        elif t == 'CO':
            dbclz, search_form, label = CO, master_search_form2, 'Country Of Origin'
        elif t == 'DotPantone':
            dbclz, search_form, label = DotPantone, master_search_form1, 'DOT Pantone#'
        elif t == 'Category':
            dbclz, search_form, label = Category, master_search_form1, 'Category'
        elif t == 'DateCode':
            dbclz, search_form, label = DateCode, master_search_form1, 'Date Code'
        elif t == 'PrintShop':
            dbclz, search_form, label = PrintShop, master_search_form1, 'Print Shop'

        return {'dbclz' : dbclz, 'search_form' : search_form, 'label' : label }


