<%inherit file="rpac.templates.master"/>

<%
  from repoze.what.predicates import not_anonymous, in_group, has_permission
%>

<%def name="extTitle()">r-pac - Production</%def>

<div class="main-div">
	<div id="main-content">
        %if has_permission("PRODUCTION"):
    	    <div class="block">
    	    	<a href="/logic/production"><img src="/images/fd.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/logic/production">Family Dollar</a></p>
    	    	<div class="block-content">Items in Production</div>
    	    </div>
        %endif
	</div>
</div>