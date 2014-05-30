# -*- coding: utf-8 -*-
'''
Created on 2014-3-5
@author: CL.lam
'''
from sqlalchemy.sql.expression import and_
from rpac.widgets.components import RPACForm, RPACText, RPACCalendarPicker, \
    RPACSelect, RPACHidden


__all__ = ['master_search_form1', 'master_search_form2', ]


class MasterSearchForm1( RPACForm ):
    fields = [
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACText( "val", label_text = "Value" ),
              RPACHidden( 't' ),
              ]

master_search_form1 = MasterSearchForm1()



class MasterSearchForm2( RPACForm ):
    fields = [
              RPACText( "english", label_text = "English Term" ),
              RPACText( "spanish", label_text = "Spanish Term" ),
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACHidden( 't' ),
              ]

master_search_form2 = MasterSearchForm2()



class MasterSearchForm3( RPACForm ):
    fields = [
              RPACText( "english", label_text = "English Term" ),
              RPACText( "spanish", label_text = "Spanish Term" ),
              RPACCalendarPicker( "create_time_from", label_text = "Create Date(from)" ),
              RPACCalendarPicker( "create_time_to", label_text = "Create Date(to)" ),
              RPACSelect( "type", label_text = "Type", options = [( "", "" ), ( 'WASH', "Wash" ), ( 'BLEACH', "Bleach" ),
                                                                     ( 'DRY', "Dry" ), ( 'IRON', "Iron" ),
                                                                     ( 'DRYCLEAN', "Dry Clean" ), ( 'SPECIALCARE', "Special Care" ),
                                                                     ] ),
              RPACHidden( 't' ),
              ]

master_search_form3 = MasterSearchForm3()

