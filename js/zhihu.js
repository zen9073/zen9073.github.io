// ==UserScript==
// @name         知乎免登录
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  知乎免登录脚本
// @author       You
// @match        https://*.zhihu.com/*
// @grant        none
// ==/UserScript==

(function () {
    // 若要开启实验性功能，请将下方 experimentalFunction = false 改成 experimentalFunction = true
    const experimentalFunction = false

    "use strict";
    if (document.location.href.indexOf("/signin?") > -1) {
        window.location.href = "//zhihu.com/explore";
    }


    function htmlObservation(mutationList, observer) {
        for (let mutation of mutationList) {
            if ('attributes' === mutation.type && 'style' === mutation.attributeName) {
                if (document.documentElement.style.overflow !== 'auto') {
                    document.documentElement.style.overflow = 'auto'
                }
            }
        }
    }

    function bodyObservation(mutationList, observer) {
        if (document.getElementsByClassName('signFlowModal')[0]) {
            const model = document.getElementsByClassName('Modal-wrapper')[0]
            if (model) {
                model.parentNode.removeChild(model)
            }
        } else {
            if (experimentalFunction && document.getElementsByClassName('Modal-backdrop')[0]) {
                const backdrop = document.getElementsByClassName('Modal-backdrop')[0]
                if (!backdrop.getAttribute('clickedevent')) {
                    backdrop.onclick = function (e) {
                        const closebutton = backdrop.parentNode.getElementsByClassName('Modal-closeButton')[0]
                        if (closebutton) {
                            closebutton.click()
                        }
                    }
                    backdrop.setAttribute('clickedevent', true)
                }
            }
        }
    }

    document.documentElement.style.overflow = 'auto'
    const htmlObserverConfig = { attributes: true }
    const htmlObserver = new MutationObserver(htmlObservation)
    htmlObserver.observe(document.documentElement, htmlObserverConfig)

    const bodyObserverConfig = { childList: true, subtree: true }
    const bodyObserver = new MutationObserver(bodyObservation)
    bodyObserver.observe(document.body, bodyObserverConfig)


})();
