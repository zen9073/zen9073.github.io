// ==UserScript==
// @name         CSDN 免登录
// @namespace    http://tampermonkey.net/
// @version      0.19
// @description  CSDN 免登录脚本
// @author       You
// @match        https://blog.csdn.net/*
// @require      https://libs.baidu.com/jquery/1.9.1/jquery.min.js
// @grant        GM_addStyle
// @grant        GM_setClipboard
// ==/UserScript==

(function () {
    "use strict";

    //去除登录框
    GM_addStyle(".passport-login-mark,#passportbox{display:none!important;}");

    //免登录复制
    $(".hljs-button").attr("data-title", "免登录复制");
    $(".hljs-button").click(function () {
        GM_setClipboard(this.parentNode.innerText);
        $(".hljs-button").attr("data-title", "复制成功");
        setTimeout(function () {
            $(".hljs-button").attr("data-title", "免登录复制");
        }, 1000);
    });

    // 自动阅读更多
    $(".hide-preCode-bt").click()
 
    // 运行复制文本
    $('code').css({ 'user-select': 'unset' })
    $('#content_views pre').css({ 'user-select': 'unset' })

    //去掉版权信息
    document.addEventListener("copy", function (e) {
        console.log('copy');
        var data = e.clipboardData;
        var text = data.getData('text');
        var pos = text.indexOf('————————————————');
        if (pos !== -1) {
            text = text.substring(0, pos - 2);
            data.setData('text', text);
        }
    });

})();
