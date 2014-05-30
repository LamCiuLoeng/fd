$(document).ready(function(){
    $( ".datePicker" ).datepicker({"dateFormat":"yy/mm/dd"});
    $(".num").numeric();
    
    $(".cboxClass").click(function(){
       isCompleteOK();            
    });

    $( "#so-div" ).dialog({
        modal: true,
        autoOpen: false,
        width: 400,
        height: 200 ,
        buttons: {
        "Submit" : function() { 
            var so = $("#so").val();
            if(!so){
                alert("Please input the SO number!");
                return;
            }else{
                var params = {
                    id : $(".cboxClass:checked").val(),
                    status : 1,                            
                    so : so,
                    t : $.now()
                };
                $.getJSON('/ordering/ajaxChangeStatus',params,function(r){
                    if(r.flag != 0){
                        alert(r.msg);
                    }else{
                        alert('Update the record successfully!');
                        window.location.reload(true);
                    }
                });
            }
    
        },
        "Cancel" : function() { $( this ).dialog( "close" ); }
        }
    });
    
    
    $( "#ship-div" ).dialog({
        modal: true,
        autoOpen: false,
        width: 600,
        height: 400 ,
        buttons: {
        "Submit" : function() { 
            var params = {
                id : $(".cboxClass:checked").val(),
                status : 2,
                t : $.now()
            };
            
            var allQtyOK = true;
            $(".shipinput").each(function(){
                var tmp = $(this);
                if(!tmp.val()){ allQtyOK = false; }
                else{ params[tmp.attr("name")] = tmp.val(); }
            });
            if(!allQtyOK){
                alert('Please input all the ship qty!');
                return;
            }
            
            $.getJSON('/ordering/ajaxChangeStatus',params,function(r){
                if(r.flag != 0){
                    alert(r.msg);
                }else{
                    alert('Update the record successfully!');
                    window.location.reload(true);
                }
            });
    
        },
        "Cancel" : function() { $( this ).dialog( "close" ); }
        }
    });
    
    
    
    $( "#manual-div" ).dialog({
        modal: true,
        autoOpen: false,
        width: 800,
        height: 500 ,
        buttons: {
        "Submit" : function() { 
        	submitManual();
        },
        "Cancel" : function() { $( this ).dialog( "close" ); }
        }
    });
    
});

function isCompleteOK(){
   var one = false;               
   $(".cboxClass").each(function(){
       var t = $(this);
       if(t.attr("status") == "1" && t.is(":checked")){
           one = true;
       }
   });
   if(one){
       $("#completebtn").addClass("btn").removeClass("btndisable");
   }else{
       $("#completebtn").addClass("btndisable").removeClass("btn");
   }
}

function toSearch(){
   $(".ordersearchform").attr("action","/ordering/index");
   $(".ordersearchform").submit();
}

function toExport(){
   $(".ordersearchform").attr("action","/ordering/export");
   $(".ordersearchform").submit();
}


function selectAll(obj){
    if($(obj).is( ":checked" )){
        $(".cboxClass").prop("checked",true);
    }else{
        $(".cboxClass").prop("checked",false);
    }
    isCompleteOK();
}

function toAssign(){
    var cb = $(".cboxClass:checked");
    if(cb.length != 1){
        alert("Please select one and only one record to assign so!");
        return;        
    }else if(cb.attr("status") != 0){
        alert("The record is not in New status!");
        return;
    }else{
        $( "#so-div" ).dialog( "open" );
    }
}

function toComplete(){
    var cb = $(".cboxClass:checked");
    if(cb.length != 1){
        alert("Please select one and only one record to edit status!");
        return;        
    }else if(cb.attr("status") != 1){
        alert("The record is not in process status!");
        return;
    }else{
        var params = {
            id : cb.val(),                       
            t : $.now()
        };
        $.getJSON("/ordering/ajaxOrderInfo",params,function(r){
            if(r.flag != 0 ){
                alert(r.msg);
                return;
            }else{
                var html = '';
                for(var i=0;i<r.data.length;i++){
                    var tmp = r.data[i];
                    html += '<tr><td style="border-left:1px solid #ccc;">'+tmp.code+'</td><td>'+tmp.qty+'</td><td><input type="text" class="shipinput num" name="ship_'+tmp.id+'" value=""/></td></tr>';
                }
                $("#shipbody").html(html);
                $(".num","#ship-div").numeric();
                $( "#ship-div" ).dialog( "open" );
            }
        });
    }     
}


function enterManual(){
	$( "#manual-div" ).dialog( "open" );
}



var item_index = 11;
function addItem(obj){
    var t = $(obj);
    var tb = $(t.parents('table')[0]);
    var template = $(".template",tb);
    var tpl = template.clone().removeClass("template");
    
    $("select,input[type='text']",tpl).each(function(){
        var k = $(this);
        var n = k.attr('name');
        k.attr('name',n.replace("_x","_"+item_index));
    });
    
    item_index ++ ;
    //tb.append(tpl);
    template.before(tpl);
}

function delItem(obj){
    var k = $(obj);
    $(k.parents("tr")[0]).remove();
}


function submitManual(){
	var msg = [];
	
	if(!$("#m_customerpo").val()){ msg.push("Please input the customer PO !"); }
	if(!$("#m_po").val()){ msg.push("Please input the vendor PO !"); }
	if(!$("#m_vendorName").val()){ msg.push("Please input the vendor name !"); }
	if(!$("#m_so").val()){ msg.push("Please input the r-pac SO !"); }
	if(!$("#m_location").val()){ msg.push("Please input the production location !"); }
	if(!$("#m_received").val()){ msg.push("Please input the 'PO received on' !"); }
	if(!$("#m_shipped").val()){ msg.push("Please input the 'PO shipped on' !"); }
	
	var allitemOK = true;
	var oneitem = false;
	$("input[name^='m_itemcode_']").each(function(){
		var i = $(this);
		var tr = $(i.parents("tr")[0]);
		var q = $("input[name^='m_qty_']",tr);
		
		if( i.val() && q.val() ){ oneitem = true; }
		else if( i.val() || q.val() ){ allitemOK = false; }
	});
	
	if(!oneitem){ msg.push("Please input at least one item and qty !"); }
	if(!allitemOK){ msg.push("Please input the item and qty correctly !"); }
	if(msg.length>0){
		alert(msg.join("\n"));
	}else{
		$("#manual-form").submit();
	}
}