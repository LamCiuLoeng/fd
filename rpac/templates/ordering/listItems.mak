<%inherit file="rpac.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>
<%
from tg import session
from repoze.what.predicates import in_group
%>

<%def name="extTitle()">r-pac - Service Bureau Ordering</%def>

<%def name="extCSS()">
<link rel="stylesheet" type="text/css" href="/css/nyroModal.css" media="screen,print"/>
<style type="text/css">
	td {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 12px;
        line-height: normal;
    }
	
	.option {
        border: #aaa solid 1px;
        width: 250px;
        background-color: #FFe;
    }

	
	#warning {
		font:italic small-caps bold 16px/1.2em Arial;
	}
	
	.error {
	   background-color: #FFEEEE !important;
	   border: 1px solid #FF6600 !important;
	}
	        
    .num,.float{
        text-align : right;
    }
    
    .label{
       background-color: #4e7596;
        border-bottom: #FFF solid 1px;
        padding-right: 10px;
        font-family: Tahoma, Geneva, sans-serif;
        color: #fff;
        font-size: 12px;
        font-weight: bold;
        text-decoration: none;
    }
    
    .template {
        display : none;
    }
</style>
</%def>

<%def name="extJavaScript()">
<script type="text/javascript" src="/js/jquery.nyroModal.custom.min.js" language="javascript"></script>
<script type="text/javascript" src="/js/numeric.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/listItems.js" language="javascript"></script>
<script type="text/javascript" src="/js/custom/item_common.js" language="javascript"></script>
<script language="JavaScript" type="text/javascript">
//<![CDATA[
        $(document).ready(function(){
            $(".num").numeric();
            $('.nyroModal').nyroModal();
            
            $( "#option-div" ).dialog({
                  modal: true,
                  autoOpen: false,
                  width: 800,
                  height: 400 ,
                  buttons: {
                    "Submit" : function() { 
                        addtocart();
                    },
                    "Cancel" : function() { $( this ).dialog( "close" ); }
                  }
             });
                
        });
        
        function checkout(){
            window.location.href = '/ordering/placeorder';
        }
        
        function PreviewImage(imageUrl, index) {
            $("#nyroModal" + index).html("<img src=\"" + imageUrl + "\" />");
        }
        

//]]>
</script>
</%def>

<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
  	<td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
  	<td width="64" valign="top" align="left"><a href="/index"><img src="/images/images/menu_return_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_confirm_g.jpg"/></a></td>
  	<td width="64" valign="top" align="left"><a href="#" onclick="toCancel()"><img src="/images/images/menu_cancel_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Main&nbsp;&nbsp;&gt;&nbsp;&nbsp;Service Bureau Ordering</div>

<div style="width:1000px;padding:10px">
    
    <p style="text-align:right; padding:0px 0px 0px 0px">
        <input type="button" onclick="checkout()" class="btn checkoutbtn" value="Shopping Cart [${len(session.get('items',[]))}],Checkout">
    </p> 
    
    <table cellspacing="0" cellpadding="0" border="0" class="gridTable" style="background:white">
    <thead>
        <tr style="text-align: center;">                     
            <th style="width:150px;height:30px;">Item Code</th>
            <th style="width:350px">Description</th>
            <th style="width:150px">Image</th>
            <th style="width:200px">Size</th>
            <th style="width:100px">Action</th>
        </tr>
    </thead>
    <tbody>
        %for index,p in  enumerate(products):
            %if index % 2 == 0:
                <tr class="even">
            %else:
                <tr class="odd">
            %endif
                <td style="border-left:1px solid #ccc;">${p.itemCode}</td>
                <td style="padding:5px;">${p.desc}</td>
                <td style="padding:5px;">
                    <a href='/images/products/${p.itemCode.replace("#","")}.jpg' class="nyroModal" title="${p.itemCode}">
                    <img width="100" src="/images/products/${p.itemCode.replace("#","")}.jpg"/>
                    </a>
                </td>      
                <td>${p.size}</td>
                <td><input type="button" class="btn" value="Add to Cart" onclick="showoptions(${p.id})"/></td>
            </tr>
        %endfor
    </tbody>
    </table>
    
    <p style="text-align:right; padding:0px 0px 0px 0px">
        <input type="button" onclick="checkout()" class="btn checkoutbtn" value="Shopping Cart [${len(session.get('items',[]))}],Checkout">
    </p> 
</div>

<div style="clear:both"></div>


<div id="option-div" title="Select Item's Option">
    <input type="hidden" id="current_item" value=""/>
    <table class="" cellpadding="3" cellspacing="3" border="1" id="option-tb" style="width:700px">
        
    </table>
</div>
