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
    <title>FD-PD-SL-36147C</title>
    <link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon" />
    <link rel="stylesheet" type="text/css" href="/css/screen.css" media="screen,print"/>
    <link rel="stylesheet" type="text/css" href="/css/all.css" media="screen,print"/>
    <link rel="stylesheet" type="text/css" href="/css/custom/pdf.css" media="screen,print"/>

<style type="text/css">

</style>


</head>

<body>


    <div id="label-layout">

        <div>
            <div class="warning">Warning: This pdf is for the demo only!!!</div>
            <div class="item-tag">Sew-in Care Label</div>
            <div class="item-code">FD-PD-SL-36147C</div>
        <br>
        <div class="item-code">English / Spanish</div>
        </div>
        <!-- <br> -->

        <!-- <div class="item-pos">FRONT</div> -->

        % if data:
            % for i, size in enumerate(null_string_sizes(data)):
                ${pdf(size, data)}
            % endfor
        % endif

        <%def name="pdf(size, data)">
        <br>

        <div id="FD-PD-SL-36147C">
            <table class="layout-table">
                <thead>
                    <tr>
                        <td><div class="item-pos">FRONT</div></td>
                        <td><div class="item-pos">BACK</div></td>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <td>
                            <div class="FD-PD-SL-36147C-front">
                                <div class="FD-PD-SL-36147C-box1"></div>

                                <img src="/images/pdf/FD-PD-SL-36147C.jpg">

                                <div class="FD-PD-SL-36147C-box3">
                                    <div class="FD-PD-SL-36147C-size-header">SIZE/TALLA:</div>
                                    <div class="FD-PD-SL-36147C-size">${size}</div>

                                    <div class="FD-PD-SL-36147C-box5">
                                        % for ct in format_fibers(data)['en']:
                                        <div>${ct.upper()}</div>
                                        <!-- <div>00% POLYESTER</div> -->
                                        % endfor

                                        <div>${format_list(format_coo(data)['en'], 'upper', '')}</div>

                                        <div class="FD-PD-SL-36147C-for-care">SEE REVERSE FOR CARE</div>

                                        <!-- Spanish -->

                                       % for ct in format_fibers(data)['sp']:
                                        <div>${ct.upper()}</div>
                                        <!-- <div>00% POLYESTER</div> -->
                                        % endfor

                                        <div>${format_list(format_coo(data)['sp'], 'upper', '')}</div>

                                        <div class="FD-PD-SL-36147C-for-care">VE EL REVERSO PARA EL CUIDADO</div>
                                    </div>
                                </div>


                            </div>
                        </td>
                        <td>
                            <div class="FD-PD-SL-36147C-back">
                                <div class="FD-PD-SL-36147C-box2">
                                    <br>
                                    <div class="FD-PD-SL-36147C-care">
                                     <!--    MACHINE WASH COLD WITH LIKE COLOS.
                                        GENTLE CYCLE DO NOT BLEACH. TUMBLE DRY LOW.
                                        COOL IRON IF NEEDED. -->
                                        ${format_list(format_cares(data)['en'], 'upper', '. ')}
                                    </div>

                                    <div class="FD-PD-SL-36147C-care">
                                       <!--  MACHINE WASH COLD WITH LIKE COLOS.
                                        GENTLE CYCLE DO NOT BLEACH. TUMBLE DRY LOW.
                                        COOL IRON IF NEEDED. -->
                                        ${format_list(format_cares(data)['sp'], 'upper', '. ')}
                                    </div>

                                    <div class="FD-PD-SL-36147C-RN">
                                        <div>RN#57623</div>
                                        <div>SKU ${format_list(data['SKU']['values'])}</div>
                                        <div>WPL#${format_list(data['WPL']['values'])}</div>
                                    </div>
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>
        <div style="page-break-after:always;"></div>

        </%def>

    </div>




    <div style="clear:both"></div>



<div id="footer"><span style="margin-right:40px">Copyright r-pac International Corp.</span></div>



</body>

</html>









