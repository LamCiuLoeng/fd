
<!DOCTYPE html>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-Equiv="Cache-Control" Content="no-cache">
    <meta http-Equiv="Pragma" Content="no-cache">
    <meta http-Equiv="Expires" Content="0">
    <title>FD-HT-SL-36148</title>
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
            <div class="item-tag">Size Tags</div>
            <div class="item-code">FD-HT-SL-36148</div>
        </div>
        % if data and data['SIZE']['values']:
            % for i, size in enumerate(data['SIZE']['values']):

                ${pdf(size)}
            % endfor
        % endif

        <%def name="pdf(size)">
        <br>
        <div class="item-pos">FRONT</div>

        <br>


        <div id="FD-HT-SL-36148">
            <div class="small-circle"></div>

            <div class="FDHTSL36148-size-header">SIZE</div>
            <div class="FDHTSL36148-size">${size}</div>
        </div>

        <div style="page-break-after:always;"></div>

        </%def>

    </div>




    <div style="clear:both"></div>



<div id="footer"><span style="margin-right:40px">Copyright r-pac International Corp.</span></div>



</body>

</html>









