
var page = require('webpage').create();
var system = require('system');

// console.log(system.args[0]);

// var address = 'http://127.0.0.1:7060/pdflayout/index';
// var output = 'D:/fd.pdf';

var address = system.args[1];
var output = system.args[2];

// console.log(system.args);

page.paperSize = { format: 'A4', orientation: 'portrait', margin: '1cm' };
// page.zoomFactor =
// page.paperSize = {
//         format: 'A4',
//         orientation: 'landscape'};

// page.viewportSize = { width: 800, height: 700 };
// page.paperSize = { format: 'Letter', orientation: 'portrait', margin: '1cm' };

// Orientation ：orientation属性用来设置文档打印格式是“Portrait”还是“Landscape”。
// Landscape为横式打印，Portrait为纵向打印
// Format：设置打印格式，一般设置为A4

// change the paper size to letter, add some borders
// add a footer callback showing page numbers
// page.paperSize = {
//   format: "Letter",
//   orientation: "portrait",
//   margin: {left:"2.5cm", right:"2.5cm", top:"1cm", bottom:"1cm"},
//   footer: {
//     height: "0.9cm",
//     contents: phantom.callback(function(pageNum, numPages) {
//       return "<div style='text-align:center;'><small>" + pageNum +
//         " / " + numPages + "</small></div>";
//     })
//   }
// };

// Note: manual page breaks can be added with:
// <div style="page-break-before:always;"></div>
// or
// <div style="page-break-after:always;"></div>

// page.open('http://127.0.0.1:7060/pdflayout/index', function() {
//   page.render('D:/fd.pdf');
//   phantom.exit();
// });


page.open(address, function (status) {
    if (status !== 'success') {
        console.log('Unable to load the address!');
        phantom.exit();
    } else {
        window.setTimeout(function () {
            page.render(output);
            phantom.exit();
        }, 200);
    }
});
