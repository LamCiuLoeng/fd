function showoptions(id){
    $("#current_item").val(id);
    var params = {
        id : id,
        t : $.now()
    };
    $.getJSON('/ordering/ajaxProductInfo',params,function(r){
       if(r.flag!=0){
           alert(r.msg);
           return ;
       }else{
           //parese the product option begin
           var required = '<sup class="star">*</sup>';
           var html = '<tr><td style="width:200px">'+required+'Qty</td><td><input type="text" class="option num required"  id="item_qty" name="qty" moq="'+r.product.moq+'" roundup="'+r.product.roundup+'" onchange="adjustqty(this)"/></td></tr>';
           for(var i=0;i<r.options.length;i++){
               var option = r.options[i];
               html += '<tr><td valign="top">';              
               if(option.css.SELECT.indexOf('required') > -1 || option.css.TEXT.indexOf('required') > -1){
                   html += required + option.name+'</td><td>';
               }else{ html += option.name+'</td><td>'; }
               if(option.type == 'TEXT'){ // ONLY TEXT
                   var css = option.css.TEXT.join(" ");        
                   if(option.multiple == 'Y'){  //multiple 
                       html += '<div><input type="text" class="option '+css+'" name="option_a_'+option.id+'_10" value=""/>';
                       html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                       html += '<div class="template"><input type="text" class="option '+css+'" name="option_a_'+option.id+'_x" value=""/>';
                       html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                   }else{
                       html += '<input type="text" class="option '+css+'" name="option_a_'+option.id+'" value=""/>';
                   }
                   
               }else if(option.type == 'SELECT'){ // ONLY SELECT
                   var optionhtml = outputOptions(option.values,null);
                   var css = option.css.SELECT.join(" ");
                   if(option.multiple == 'Y'){  //multiple
                       html += '<div><select name="option_a_'+option.id+'" class="option '+css+'">' + optionhtml + '</select>';
                       html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                       html += '<div class="template"><select name="option_a_' + option.id + '_x" class="option '+css+'">' + optionhtml + '</select>';
                       html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                   }else{
                       html += '<select name="option_a_'+option.id+'" class="option '+css+'">'+optionhtml+'</select>';
                   }
               }else if(option.type == 'SELECT+TEXT'){ // SELECT + TEXT
                   var optionhtml = outputOptions(option.values,null);
                   var selectcss = option.css.SELECT.join(" ");
                   var textcss = option.css.TEXT.join(" ");
                   if(option.multiple == 'Y'){  //multiple
                       html += '<div><select name="option_as_'+option.id+'" class="option '+selectcss+'">' + optionhtml + '</select>';
                       html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'" style="width:80px"/>';
                       html += '&nbsp;<input type="button" class="btn" value="Add" onclick="addrow(this)"/></div>';
                       html += '<div class="template"><select name="option_as_' + option.id + '_x" class="option '+selectcss+'">' + optionhtml + '</select>';
                       html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'_x" style="width:80px"/>';
                       html += '&nbsp;<input type="button" class="btn" value="Del" onclick="delrow(this)"/></div>';
                   }else{
                       html += '<select name="option_as_'+option.id+'" class="option '+selectcss+'">'+optionhtml+'</select>';
                       html += '&nbsp;<input type="text" class="option '+textcss+'" name="option_at_'+option.id+'" style="width:80px"/>';
                   }
               }
               html += '</td></tr>' ;
           }//FOR
                                                    
           $("#option-tb").html(html);
           $(".num,.float","#option-tb").numeric();
           //parese the product option end
           var height = 400; 
           if(r.options.length < 3){
               height = 300;
           }else if(r.options.length < 5){
               height = 400;
           }else if(r.options.length < 9){
               height = 500;
           }else{
               height = 600;
           }
           $( "#option-div" ).dialog({height : height});
           $( "#option-div" ).dialog( "open" );           
       }
    });
}
    


    
function outputOptions(list,val){
    html = '';
    for(var i=0;i<list.length;i++){
        var t = list[i];
        if(t.key+'' == val + ''){
            html += '<option value="'+t.key+'" selected="selected">'+t.val+'</option>';
        }else{
            html += '<option value="'+t.key+'">'+t.val+'</option>';
        }
    }
    return html;
}



function addtocart(){
    var msg = checkInput();
    if(msg.length > 0){
        alert(msg.join('\n'));
        return;
    }
    var params = {
        id : $("#current_item").val(),
        qty : $("#item_qty").val(),
        t : $.now()
    };
    
    $(".template").remove();
    $("[name^='option_']").each(function(){
        var t = $(this);
        
        if(t.prop('tagName') == 'INPUT'){
            params[t.attr('name')] = [t.val(),t.val()].join("|");
        }else if(t.prop('tagName') == 'SELECT'){
            params[t.attr('name')] = [t.val(),$(":selected",t).text()].join("|");
        }        
    });
    
    $.getJSON('/ordering/ajaxAddtoCart',params,function(r){
        if(r.flag !=0){
            alert(r.msg);
        }else{
            //window.location.reload(true);
            alert('Add the item to shopping cart successfully!');
            $(".checkoutbtn").val("Shopping Cart [" + r.total + "],Checkout");
            $( "#option-div" ).dialog( "close" );  
        }
    });
}
