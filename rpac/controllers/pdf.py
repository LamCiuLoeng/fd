# -*- coding: utf-8 -*-

import os
import json

# turbogears imports
from tg import expose, redirect, validate, flash, session, request, config
from tg.decorators import *

# third party imports
from repoze.what import authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission
from sqlalchemy.sql.expression import and_

# project specific imports
from rpac.lib.base import BaseController
from rpac.model import *

from rpac.util.common import *
from rpac.util.layout_pdf import gen_pdf


__all__ = ['PdfController', 'PdfLayoutController']


class PdfController( BaseController ):
    # Uncomment this line if your controller requires an authenticated user
#    allow_only = authorize.in_group( 'Admin' )
    allow_only = authorize.not_anonymous()


    @expose()
    def index(self, **kw):
        header = None
        # details = None
        hid = kw.get('id', None)
        if hid:
            header = qry( OrderHeader ).filter( and_( OrderHeader.active == 0 , OrderHeader.id == hid ) ).first()
        if header and header.dtls:
            details = [(d.id, d.itemCode) for d in header.dtls]
            # print details
            pdf_zip_file = gen_pdf(header.no, details)
            return serveFile(unicode(pdf_zip_file))


class PdfLayoutController( BaseController ):
    # Uncomment this line if your controller requires an authenticated user
#    allow_only = authorize.in_group( 'Admin' )


    @expose('rpac.templates.pdf.index')
    def index(self, **kw):
        detail = None
        data = None
        detail_id = kw.get('id', None)
        if detail_id:
            detail = qry( OrderDetail ).filter( and_( OrderDetail.active == 0 , OrderDetail.id == detail_id ) ).first()

        if detail:
            item_code = detail.itemCode
            template_dir = config.get('pdf_template_dir')
            pdf_template = os.path.join(template_dir, '%s.mak' % item_code)
            # print item_code, pdf_template
            if os.path.exists(pdf_template):
                # print os.path.exists(pdf_template)
                data = detail.layoutValue
                data = json.loads(data) if data else None
                override_template(self.index, 'mako:rpac.templates.pdf.%s' % item_code)

        # print data
        return dict(data=data)
