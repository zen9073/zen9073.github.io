// ==UserScript==
// @name         QR
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  二维码生成
// @author       You
// @match        http*://*/*
// @grant        none
// @run-at       context-menu
// ==/UserScript==


(function () {
    'use strict';
    // Your code here...

    let text = window.getSelection().toString();
    let qr_url = "https://chart.googleapis.com/chart?chs=500x500&cht=qr&choe=UTF-8&chl=" + encodeURIComponent(text)
    window.open(qr_url, 'target', '');
})();
