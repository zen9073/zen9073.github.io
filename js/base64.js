// ==UserScript==
// @name         base64
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  try to take over the world!
// @author       You
// @match        http*://*/*
// @require      https://libs.baidu.com/jquery/1.9.1/jquery.min.js
// @grant        GM_addStyle
// @grant        GM_setClipboard
// @run-at       context-menu
// ==/UserScript==


(function () {
    "use strict";

    GM_setClipboard(getEncode64(selectText()))

    function getEncode64(str) {
        return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
            function toSolidBytes(match, p1) {
                return String.fromCharCode('0x' + p1);
            }));

    }

    function selectText() {
        if (document.Selection) {
            //ie浏览器
            return document.selection.createRange().text;
        } else {
            //标准浏览器
            return window.getSelection().toString();
        }
    }


})();
