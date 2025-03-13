// ==UserScript==
// @name         uuid
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  try to take over the world!
// @author       You
// @match        http*://*/*
// @grant        GM_setClipboard
// @run-at       context-menu
// ==/UserScript==

(function () {
    'use strict';

    function guid() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0,
                v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    GM_setClipboard(guid())


    // Your code here...
})();