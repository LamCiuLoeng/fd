<%inherit file="rpac.templates.master"/>

<%
  from repoze.what.predicates import not_anonymous, in_group, has_permission
%>

<%def name="extTitle()">r-pac - Master</%def>

<div class="main-div">
	<div id="main-content">
	       <!--
            <div class="block">
                <a href=""><img src="/images/fd.jpg" width="55" height="55" alt="" /></a>
                <p><a href="">Product</a></p>
            </div>        
            -->
    	    <div class="block">
    	    	<a href="/master/index?t=Category"><img src="/images/cat.jpg" width="55" height="55" alt="" /></a>
    	    	<p><a href="/master/index?t=Category">Category</a></p>
    	    </div>
        
            <div class="block">
                <a href="/master/index?t=DotPantone"><img src="/images/dot.jpg" width="55" height="55" alt="" /></a>
                <p><a href="/master/index?t=DotPantone">DOT Pantone#</a></p>
            </div>
            
            <div class="block">
                <a href="/master/index?t=DateCode"><img src="/images/date.jpg" width="55" height="55" alt="" /></a>
                <p><a href="/master/index?t=DateCode">Date Code</a></p>
            </div>
            
            <div class="block">
                <a href="/master/index?t=Fibers"><img src="/images/fibers.jpg" width="55" height="55" alt="" /></a>
                <p><a href="/master/index?t=Fibers">Fiber Content</a></p>
            </div>
            
            <div class="block">
                <a href="/master/index?t=Care"><img src="/images/care.jpg" width="55" height="55" alt="" /></a>
                <p><a href="/master/index?t=Care">Care instructions</a></p>
            </div>
            
            <div class="block">
                <a href="/master/index?t=CO"><img src="/images/co.jpg" width="55" height="55" alt="" /></a>
                <p><a href="/master/index?t=CO">Country Of Origin</a></p>
            </div>
	</div>
</div>