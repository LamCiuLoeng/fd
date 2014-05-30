
<!DOCTYPE html>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-Equiv="Cache-Control" Content="no-cache">
    <meta http-Equiv="Pragma" Content="no-cache">
    <meta http-Equiv="Expires" Content="0">
    <title>FD-PD-SL-36143</title>
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
            <div class="item-tag">Tracking Number Label</div>
            <div class="item-code">FD-PD-SL-36143</div>
        </div>

        % if data and data['TRACKING']['values']:
            % for i, v in enumerate(data['TRACKING']['values']):

                ${pdf(v)}
            % endfor
        % endif

        <!-- <div class="item-pos">FRONT</div> -->
        <%def name="pdf(tracking)">
        <br>


        <div id="FD-PD-SL-36143">
            <div class="FDPDSL36143-box1"></div>

            <div class="FDPDSL36143-box2">
                <div class="FDPDSL36143-fixed">MIDWOOD BRANDSLLC</div>
                <!-- <div>BRANDSLLC</div> -->
                <div class="FDPDSL36143-fixed">${tracking}</div>
                <!-- <div>0412</div> -->
            </div>
        </div>

        <div style="page-break-after:always;"></div>

        </%def>

    </div>




    <div style="clear:both"></div>



<div id="footer"><span style="margin-right:40px">Copyright r-pac International Corp.</span></div>



</body>

</html>









