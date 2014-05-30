if(!Array.indexOf) 
{ 
    Array.prototype.indexOf = function(obj) 
    {                
        for(var i=0; i<this.length; i++) 
        { 
            if(this[i]==obj){ return i; } 
        } 
        return -1; 
    };
}

if(!String.trim){
    String.prototype.trim=function(){return this.replace(/(^\s*)|(\s*$)/g,"");};
}
    


function adjustqty(obj){
    var t = $(obj);
    var v = t.val().trim();
    var moq = parseInt(t.attr('moq'));
    var roundup = parseInt(t.attr('roundup'));
    
    if(!isNaN(moq)){
        v = v > moq ? v : moq;
    }
    if(!isNaN(roundup)){
        var n = v % roundup == 0 ? 0 : 1; 
        v = roundup * (parseInt(v / roundup ) + n);
    }
    t.val(v);
}

var timestamp = $.now();
var index = 11;

function addrow(obj){
    var t = $(obj);
    var td = $(t.parents("td")[0]);
    var template = $(".template",td);
    var clone = template.clone().removeClass("template");
    index ++;
    $("input[type='text'],select",clone).each(function(){
        var k = $(this);
        var n = k.attr("name");
        k.attr("name",n.replace("_x","_"+timestamp+index));
    });
    template.before(clone);
}

function delrow(obj){
    var t = $(obj);
    $(t.parents("div")[0]).remove();
}


function checkInput(){
    var msg = [];
    var numreg = /^\d+$/;
    var floatreg = /^\d+(.\d+)?$/;
    
    $(".error").removeClass("error");
    
    var allrequired = true;
    $(".required").not("[name$='_x']").each(function(){
        var t = $(this);
        if(!t.val()){ 
            allrequired = false;
            t.addClass("error"); 
        }
    });
    if(!allrequired){ msg.push("Please input the required field(s)"); }
        
    var allnum = true;
    $(".num").not("[name$='_x']").each(function(){
        var t = $(this);
        if(t.val() && !numreg.test(t.val()) ){ 
            allnum = false; 
            t.addClass("error");
        }
    });
    if(!allnum){ msg.push("Please correct the number field(s)"); }
    
    var allfloat = true;
    $(".float").not("[name$='_x']").each(function(){
        var t = $(this);
        if(t.val() && !floatreg.test(t.val()) ){ 
            allfloat = false; 
            t.addClass("error");
        }
    });
    if(!allfloat){ msg.push("Please correct the float field(s)"); }
    
    
    var allsku = true;
    $(".sku").not("[name$='_x']").each(function(){
        var t = $(this);
        var v = t.val();
        if(v && v.length != 7 && numreg.test(v)){ 
            allsku = false;
            t.addClass("error");
        }
    });
    
    if(!allsku){ msg.push("Please correct the SKU field(s), must be 7 chars and digital"); }
    
    var allsum = {};
    var sumok = true;
    $(".percent").not("[name$='_x']").each(function(){
        var t = $(this);    
        var _id = t.attr("name").split("_")[2];
        var v = parseFloat(t.val());
        if(!isNaN(v)){ 
            if(isNaN(allsum[_id])){ allsum[_id] = 0; }
            allsum[_id] += v; 
        }        
    });
    
    for(k in allsum){
        if(allsum[k] != 100){ sumok = false; }
    }
    if(!sumok){ msg.push("Please input the correct fiber percentage, total should be 100%"); }
    return msg;
}