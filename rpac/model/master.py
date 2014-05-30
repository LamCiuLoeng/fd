# -*- coding: utf-8 -*-
'''
Created on 2014-3-3
@author: CL.lam
'''
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import synonym, backref, relation
from sqlalchemy.sql.expression import and_

from rpac.model import DeclarativeBase, qry
from interface import SysMixin


__all__ = [
           'ProductMixin',
           'Care', 'Fibers', 'CO', 'DotPantone', 'Category', 'DateCode',
           'PrintShop', 'Product', 'Option' ]


class ProductMixin( object ):
    itemCode = Column( "item_code", Text )
    desc = Column( Text )
    size = Column( Text )


class OptionMixin( object ):

    @property
    def key( self ): return self.id

    @property
    def value( self ): raise NotImplementedError()


class Care( DeclarativeBase , SysMixin, OptionMixin ):
    __tablename__ = 'master_care'

    id = Column( Integer, primary_key = True )
    type = Column( Text )
    english = Column( Text )
    spanish = Column( Text )

    @property
    def value( self ): return self.english

    def showType( self ):
        return {
                'WASH' : "Wash", 'BLEACH' : "Bleach", 'DRY' : "Dry",
                'IRON' : "Iron", 'DRYCLEAN' : "Dry Clean", 'SPECIALCARE' : "Special Care"
                }.get( self.type, '' )


class Fibers( DeclarativeBase , SysMixin, OptionMixin ):
    __tablename__ = 'master_fibers'

    id = Column( Integer, primary_key = True )
    english = Column( Text )
    spanish = Column( Text )

    @property
    def value( self ): return self.english


class CO( DeclarativeBase , SysMixin, OptionMixin ):
    __tablename__ = 'master_co'

    id = Column( Integer, primary_key = True )
    english = Column( Text )
    spanish = Column( Text )

    @property
    def value( self ): return self.english


class DotPantone( DeclarativeBase , SysMixin, OptionMixin ):
    __tablename__ = 'master_dot_pantone'

    id = Column( Integer, primary_key = True )
    val = Column( Text )
    css = Column( Text )

    @property
    def value( self ): return self.val


class Category( DeclarativeBase , SysMixin, OptionMixin ):
    __tablename__ = 'master_category'

    id = Column( Integer, primary_key = True )
    val = Column( Text )

    @property
    def value( self ): return self.val


class DateCode( DeclarativeBase , SysMixin, OptionMixin ):
    __tablename__ = 'master_date_code'

    id = Column( Integer, primary_key = True )
    val = Column( Text )

    @property
    def value( self ): return self.val


class PrintShop( DeclarativeBase , SysMixin ):
    __tablename__ = 'master_print_shop'

    id = Column( Integer, primary_key = True )
    name = Column( Text )
    _email = Column( "email", Text )


    def __unicode__( self ): return self.name
    def __str__( self ): return self.name


    def _getEmail( self ):
        if not self._email : return []
        return self._email.split( ";" )

    def _setEmail( self, s ): self._email = s

    @declared_attr
    def email( self ): return synonym( '_email', descriptor = property( self._getEmail, self._setEmail ) )




class Product( DeclarativeBase , SysMixin, ProductMixin ):
    __tablename__ = 'master_product'

    id = Column( Integer, primary_key = True )
    moq = Column( Integer, default = None )
    roundup = Column( Integer, default = None )

    def __unicode__( self ): return self.itemCode
    def __str__( self ): return self.itemCode

    def getOptions( self ):
        return qry( Option ).filter( and_( Option.active == 0, Option.productId == self.id ) ).order_by( Option.order )




class Option( DeclarativeBase , SysMixin ):
    __tablename__ = 'master_option'

    id = Column( Integer, primary_key = True )
    productId = Column( "product_id", Integer, ForeignKey( 'master_product.id' ) )
    product = relation( Product )

    name = Column( Text )
    type = Column( Text )
    multiple = Column( Text )    #Y is multiple
    css = Column( Text )    #json value for css {'SELECT' : ['required','sku','num'],'TEXT' : ['required','sku','num']}
    master = Column( Text, default = None )
    conditions = Column( Text, default = None )
    order = Column( Integer )
    layoutKey = Column( "layout_key", Text )
    language = Column( Text )
