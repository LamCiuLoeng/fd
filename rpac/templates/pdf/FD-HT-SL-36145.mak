<%
    from rpac.util.layout_pdf import (null_string_sizes,
        format_coo, format_cares, format_fibers,
        format_list, format_list2, format_price)
%>

<!DOCTYPE html>

<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-Equiv="Cache-Control" Content="no-cache">
    <meta http-Equiv="Pragma" Content="no-cache">
    <meta http-Equiv="Expires" Content="0">
    <title>FD-HT-SL-36145</title>
    <link href="/images/favicon.ico" type="images/x-icon" rel="shortcut icon" />
    <link rel="stylesheet" type="text/css" href="/css/screen.css" media="all"/>
    <link rel="stylesheet" type="text/css" href="/css/all.css" media="all"/>
    <link rel="stylesheet" type="text/css" href="/css/custom/pdf.css" media="all"/>

<style type="text/css">
    .FD-HT-SL-36145-circle {
        background-color: #76bd1d;
    }
</style>


</head>

<body>


    <div id="label-layout">

        <div>
            <div class="warning">Warning: This pdf is for the demo only!!!</div>
            <div class="item-tag">Accessories Hang Tags</div>
            <div class="item-code">FD-HT-SL-36145</div>
        <!-- <br> -->
        <!-- <div class="item-code">English / Spanish</div> -->
        </div>


        <!-- <div class="item-pos">FRONT</div> -->

        % if data:
            % for i, size in enumerate(null_string_sizes(data)):
                ${pdf(size, format_coo(data), data['NAME']['values'], format_cares(data), format_fibers(data, True), data['SKU']['values'], data['PRICE']['values'], data['TRACKING']['values'])}
            % endfor
        % endif

        <%def name="pdf(size, coo, item_name, cares, fibers, sku, price, tracking)">
        <br>
        <div id="FD-HT-SL-36145">
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
                            <div class="FD-HT-SL-36145-front">
                                <div class="FD-HT-SL-36145-box1">
                                    <div>SIZE: ${size}</div>
                                    <div class="FD-HT-SL-36145-coo1">${format_list(coo['en'], 'upper', '')}</div>
                                </div>

                            </div>
                        </td>
                        <td>
                            <div class="FD-HT-SL-36145-back">
                                <div class="FD-HT-SL-36145-box2">
                                    <div class="FD-HT-SL-36145-item-name">${format_list(format_list2(item_name))}</div>
                                    <div class="FD-HT-SL-36145-price">
                                        <div class="FD-HT-SL-36145-price-circle">
                                            <div class="FD-HT-SL-36145-price-v">
                                                <span class="FD-HT-SL-36145-price-s">$</span><span class="FD-HT-SL-36145-price-vv">${price[0] if price else ''}</span>
                                            </div>
                                        </div>

                                    </div>
                                </div>

                                <div style="clear:both"></div>

                                <div class="FD-HT-SL-36145-box4">
                                    <div class="FD-HT-SL-36145-100logo">
                                        <img width="138" src="/images/pdf/HL-MBG-Red.jpg">
                                    </div>

                                    <div class="FD-HT-SL-36145-100text">
                                        <div class="FD-HT-SL-36145-100text-h">Not 100% satisfied?</div>
                                        <div class="FD-HT-SL-36145-100text-v">Return item within 30 days to any Family Dollar store for a refund (with receipt) or exchange.</div>
                                    </div>
                                </div>

                                <div style="clear:both"></div>

                                <div class="FD-HT-SL-36145-box6">

                                    <div class="FD-HT-SL-36145-box8">
                                        <!-- care -->
                                        <div class="FD-HT-SL-3614-cares">
                                        ${format_list(format_list2(cares['en']), None, '. ')}
                                        </div>

                                        <!-- ff -->
                                        <div class="FD-HT-SL-3614-ff">
                                             % for cc in fibers['en']:
                                            <div>${cc}</div>
                                            <!-- <div>00% Content</div> -->
                                            % endfor
                                        </div>

                                        <!-- RN -->
                                        <div class="FD-HT-SL-36145-RN">RN#57623</div>

                                        <div class="FD-HT-SL-36145-dis">
                                            <div>DISTRIBUTED BY:</div>
                                            <div>MIDWOOD BRANDS, LLC 10611 MONROE RD. MATTHEWS, NC 28105 USA</div>
                                        </div>

                                        <!-- coo -->
                                        <div class="FD-HT-SL-36145-coo22">${format_list(coo['en'], 'upper', '')}</div>

                                    </div>

                                    <div class="FD-HT-SL-36145-box10">

                                        <div class="FD-HT-SL-36145-llc">
                                            <div>MIDWOOD BRANDS LLC</div>
                                            <div>${format_list(tracking)}</div>
                                        </div>


                                        <div class="FD-HT-SL-36145-sbc">
                                        <!-- sku, v00 -->
                                            <div class="FD-HT-SL-36145-skuv">
                                                <div class="FD-HT-SL-36145-sku">SKU ${format_list(sku)}</div>
                                                <div class="FD-HT-SL-36145-v0">V-0000</div>
                                            </div>

                                            <!-- barcode -->
                                            <div class="FD-HT-SL-36145-barcode"><img src="/images/pdf/FD-HT-SL-36145-barcode.jpg"></div>
                                        </div>


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









