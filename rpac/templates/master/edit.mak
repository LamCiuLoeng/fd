<%inherit file="rpac.templates.master"/>
<%namespace name="tw" module="tw.core.mako_util"/>

<%def name="extTitle()">r-pac - Master</%def>

<%def name="extCSS()">
<link rel="stylesheet" href="/css/custom/access.css" type="text/css" />
</%def>

<%def name="extJavaScript()">
	<script language="JavaScript" type="text/javascript">
    //<![CDATA[
        function toSave(){
            %if t in ['DotPantone','Category','DateCode',]:
                if(!$("#form1_value").val()){
                   alert("Please input the ${label} value!");
                   return false;
                }else{
                   $("form").submit();
                }
            %elif t in ['Fibers','CO',]:
                if(!$("#form2_english").val()){
                   alert("Please input the English!");
                   return false;
                }else{
                    $("form").submit();
                }
            %elif t in ['Care']:
                if(!$("#form3_english").val()){
                   alert("Please input the English!");
                   return false;
                }else{
                    $("form").submit();
                }            
            %endif
        }

    //]]>
   </script>
</%def>


<div id="function-menu">
    <table width="100%" cellspacing="0" cellpadding="0" border="0">
  <tbody><tr>
    <td width="36" valign="top" align="left"><img src="/images/images/menu_start.jpg"/></td>
    <td width="176" valign="top" align="left"><a href="/access/index"><img src="/images/images/menu_master_g.jpg"/></a></td>
    <td width="176" valign="top" align="left"><a href="#" onclick="toSave()"><img src="/images/images/menu_save_g.jpg"/></a></td>
    <td width="23" valign="top" align="left"><img height="21" width="23" src="/images/images/menu_last.jpg"/></td>
    <td valign="top" style="background:url(/images/images/menu_end.jpg) repeat-x;width:100%"></td>
  </tr>
</tbody></table>
</div>

<div class="nav-tree">Master&nbsp;&nbsp;&gt;&nbsp;&nbsp;${label}&nbsp;&nbsp;&gt;&nbsp;&nbsp;Edit</div>

<div style="margin: 10px 0px; overflow: hidden;">
  <div style="float: left;">
    %if t in ['DotPantone','Category','DateCode',]:
        <div>
          <form name="userForm" class="tableform" method="post" action="/master/save_edit">
          	<input type="hidden" name="t" value="${t}"/>
          	<input type="hidden" name="id" value="${obj.id}"/>
            <div class="case-list-one">
              <div class="case-list">
                <ul>
                  <li class="label">
                    <label for="form1_value" class="fieldlabel">${label} Value</label>
                  </li>
                  <li>
                    <input type="text" id="form1_value" name="value" class="textfield" style="width: 250px;" value="${obj.val}"/>
                  </li>
                </ul>            
              </div>
            </div>
            <div style="clear: both;"><br/>
            </div>
          </form>
        </div>
    %elif t in ['Fibers','CO',]:
        <div>
          <form name="groupForm" class="tableform" method="post" action="/master/save_edit">
          	<input type="hidden" name="t" value="${t}"/>
          	<input type="hidden" name="id" value="${obj.id}"/>
            <div class="case-list-one">
              <div class="case-list">
                <ul>
                  <li class="label">
                    <label for="form2_english" class="fieldlabel">English Term</label>
                  </li>
                  <li>
                    <input type="text" id="form2_english" name="english" class="textfield" style="width: 250px;" value="${obj.english}"/>
                  </li>
                </ul>
              </div>
            </div>
            <div class="case-list-one">
              <div class="case-list">
                <ul>
                  <li class="label">
                    <label for="form2_spanish" class="fieldlabel">Spanish Term</label>
                  </li>
                  <li>
                    <input type="text" id="form2_spanish" name="spanish" class="textfield" style="width: 250px;" value="${obj.spanish}"/>
                  </li>
                </ul>
              </div>
            </div>
            <div style="clear: both;"><br/></div>
          </form> 
        </div>
    %elif t in ['Care',]:
        <div>
          <form name="groupForm" class="tableform" method="post" action="/master/save_edit">
            <input type="hidden" name="t" value="${t}"/>
            <input type="hidden" name="id" value="${obj.id}"/>
            <div class="case-list-one">
              <div class="case-list">
                <ul>
                  <li class="label">
                    <label for="form3_english" class="fieldlabel">English Term</label>
                  </li>
                  <li>
                    <input type="text" id="form3_english" name="english" class="textfield" style="width: 250px;" value="${obj.english}"/>
                  </li>
                </ul>
                <ul>
                  <li class="label">
                    <label for="form3_type" class="fieldlabel">Type</label>
                  </li>
                  <li>
                    <select id="form3_type" name="type" style="width: 250px;">
                        %for k,v in [( 'WASH', "Wash" ), ( 'BLEACH', "Bleach" ),( 'DRY', "Dry" ), ( 'IRON', "Iron" ),( 'DRYCLEAN', "Dry Clean" ), ( 'SPECIALCARE', "Special Care" )]:
                            <option value="${k}" ${tw.attrs([('selected',k == obj.type)])}>${v}</option>
                        %endfor
                    </select>
                  </li>
                </ul>
              </div>
            </div>
            <div class="case-list-one">
              <div class="case-list">
                <ul>
                  <li class="label">
                    <label for="form3_spanish" class="fieldlabel">Spanish Term</label>
                  </li>
                  <li>
                    <input type="text" id="form3_spanish" name="spanish" class="textfield" style="width: 250px;" value="${obj.spanish}"/>
                  </li>
                </ul>
              </div>
            </div>
            <div style="clear: both;"><br/></div>
          </form> 
        </div>
    %endif
  </div>
</div>