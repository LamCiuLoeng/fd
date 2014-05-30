
<%
    from rpac.util.layout_pdf import null_string_sizes
    from rpac.util.layout_pdf import format_fibers
    from rpac.util.layout_pdf import format_cares
    from rpac.util.layout_pdf import format_coo
    from rpac.util.layout_pdf import format_list
%>
<!DOCTYPE html>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-Equiv="Cache-Control" Content="no-cache">
    <meta http-Equiv="Pragma" Content="no-cache">
    <meta http-Equiv="Expires" Content="0">
    <title>FD-HT-SL-36146</title>
    <link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon" />
    <link rel="stylesheet" type="text/css" href="/css/screen.css" media="all"/>
    <link rel="stylesheet" type="text/css" href="/css/all.css" media="all"/>
    <link rel="stylesheet" type="text/css" href="/css/custom/pdf.css" media="all"/>

<style type="text/css">

</style>


</head>

<body>


    <div id="label-layout">

        <div>
            <div class="warning">Warning: This pdf is for the demo only!!!</div>
            <div class="item-tag">Heat Seal</div>
            <div class="item-code">FD-HT-SL-36146</div>
        </div>

        % if data:
            % for i, size in enumerate(null_string_sizes(data)):
                ${pdf(size, format_fibers(data), format_cares(data), format_coo(data))}
            % endfor
        % endif


        <!-- <div class="item-pos">FRONT</div> -->

        <%def name="pdf(size, fibers, cares, coo)">
        <br>
        <div id="FD-HT-SL-36146">
            <div>
                <img src="/images/pdf/FD-HT-SL-36146.jpg" alt="FD-HT-SL-36146">
            </div>

            <div class="FDHTSL36146-size">${size}</div>
            <div class="FDHTSL36146-box2">
                <div>${format_list(fibers['en'], 'upper', ' / ')}</div>
                <div>${format_list(cares['en'], 'upper', '. ')}</div>
                <!-- <div>00% COTTON / 00% POLYESTER</div> -->
                <!-- <div>EXCLUSIVE OF DECORATION</div> -->
                <!-- <div>INCLUDE CARE INSTRUCTIONS HERE</div> -->
                <!-- <div>CARE INSTRUCTIONS AS NEEDED</div> -->
                <div>${format_list(coo['en'], 'upper', '')}</div>
                <div>RN# 57623</div>
            </div>

        </div>

        <div style="page-break-after:always;"></div>

        </%def>

    </div>




    <div style="clear:both"></div>



<div id="footer"><span style="margin-right:40px">Copyright r-pac International Corp.</span></div>



</body>

</html>









