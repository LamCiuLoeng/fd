<%
    from rpac.util.layout_pdf import format_list, format_price
%>
<!DOCTYPE html>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-Equiv="Cache-Control" Content="no-cache">
    <meta http-Equiv="Pragma" Content="no-cache">
    <meta http-Equiv="Expires" Content="0">
    <title>FD-HT-SL-36144</title>
    <link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon" />
    <link rel="stylesheet" type="text/css" href="/css/screen.css" media="screen,print"/>
    <link rel="stylesheet" type="text/css" href="/css/all.css" media="screen,print"/>
    <link rel="stylesheet" type="text/css" href="/css/custom/pdf.css" media="screen,print"/>

<style type="text/css">
    .FD-HT-SL-36144-circle {
        /*background-color: #76bd1d;*/
        background-color: ${data['DOT']['values'][0]['css']};
    }
</style>


</head>

<body>


    <div id="label-layout">

        <div>
            <div class="warning">Warning: This pdf is for the demo only!!!</div>
            <div class="item-tag">Apparel Hang Tags</div>
            <div class="item-code">FD-HT-SL-36144</div>
        <!-- <br> -->
        <!-- <div class="item-code">English / Spanish</div> -->
        </div>
        <br>

        <!-- <div class="item-pos">FRONT</div> -->


        % if data:
        <div id="FD-HT-SL-36144">
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
                            <div class="FD-HT-SL-36144-front">
                                <div class="FD-HT-SL-36144-box1">
                                    <img src="/images/pdf/FD-HT-SL-36144.jpg">
                                </div>

                            </div>
                        </td>
                        <td>
                            <div class="FD-HT-SL-36144-back">
                                <div class="FD-HT-SL-36144-box2">
                                    <div class="FD-HT-SL-36144-category">${format_list(data['CATEGORY']['values'])}</div>
                                    <div><img src="/images/pdf/FD-HT-SL-36144_0.jpg"></div>
                                    <div class="FD-HT-SL-36144-item-desc">${format_list(data['DESC']['values'])}</div>

                                    <div class="FD-HT-SL-36144-circle"></div>

                                    <div class="FD-HT-SL-36144-date-code">${format_list(data['DATECODE']['values'])}</div>

                                    <div><img src="/images/pdf/FD-HT-SL-36144_sku.jpg"></div>

                                    <div class="FD-HT-SL-36144-sku">SKU ${format_list(data['SKU']['values'])}</div>

                                    <div class="FD-HT-SL-36144-dis">
                                        <div>DISTRIBUTED BY:</div>
                                        <div>MIDWOOD BRANDS, LLC</div>
                                        <div>10611 MONROE RD.</div>
                                        <div>MATTHEWS, NC 28105 USA</div>
                                    </div>
                                    <div>MIDWOODBRANDSLLC${format_list(data['TRACKING']['values'])}</div>


                                </div>

                                <div class="FD-HT-SL-36144-price">${format_price(data)}</div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>

        </div>
        % endif

    </div>




    <div style="clear:both"></div>



<div id="footer"><span style="margin-right:40px">Copyright r-pac International Corp.</span></div>



</body>

</html>









