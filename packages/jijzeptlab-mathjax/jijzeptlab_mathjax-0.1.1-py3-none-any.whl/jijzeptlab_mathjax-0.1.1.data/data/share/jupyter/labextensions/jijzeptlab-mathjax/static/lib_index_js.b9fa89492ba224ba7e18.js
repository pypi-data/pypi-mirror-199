"use strict";
(self["webpackChunkjijzeptlab_mathjax"] = self["webpackChunkjijzeptlab_mathjax"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MathJax3Typesetter": () => (/* binding */ MathJax3Typesetter),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var mathjax_full_js_mathjax__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! mathjax-full/js/mathjax */ "./node_modules/mathjax-full/js/mathjax.js");
/* harmony import */ var mathjax_full_js_input_tex__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! mathjax-full/js/input/tex */ "./node_modules/mathjax-full/js/input/tex.js");
/* harmony import */ var mathjax_full_js_input_tex__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(mathjax_full_js_input_tex__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var mathjax_full_js_output_chtml__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! mathjax-full/js/output/chtml */ "./node_modules/mathjax-full/js/output/chtml.js");
/* harmony import */ var mathjax_full_js_output_chtml__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(mathjax_full_js_output_chtml__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var mathjax_full_js_output_chtml_fonts_tex__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! mathjax-full/js/output/chtml/fonts/tex */ "./node_modules/mathjax-full/js/output/chtml/fonts/tex.js");
/* harmony import */ var mathjax_full_js_output_chtml_fonts_tex__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(mathjax_full_js_output_chtml_fonts_tex__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var mathjax_full_js_input_tex_AllPackages__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! mathjax-full/js/input/tex/AllPackages */ "./node_modules/mathjax-full/js/input/tex/AllPackages.js");
/* harmony import */ var mathjax_full_js_ui_safe_SafeHandler__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! mathjax-full/js/ui/safe/SafeHandler */ "./node_modules/mathjax-full/js/ui/safe/SafeHandler.js");
/* harmony import */ var mathjax_full_js_ui_safe_SafeHandler__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(mathjax_full_js_ui_safe_SafeHandler__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var mathjax_full_js_handlers_html_HTMLHandler__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! mathjax-full/js/handlers/html/HTMLHandler */ "./node_modules/mathjax-full/js/handlers/html/HTMLHandler.js");
/* harmony import */ var mathjax_full_js_handlers_html_HTMLHandler__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(mathjax_full_js_handlers_html_HTMLHandler__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var mathjax_full_js_adaptors_browserAdaptor__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! mathjax-full/js/adaptors/browserAdaptor */ "./node_modules/mathjax-full/js/adaptors/browserAdaptor.js");
/* harmony import */ var mathjax_full_js_input_tex_require_RequireConfiguration__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! mathjax-full/js/input/tex/require/RequireConfiguration */ "./node_modules/mathjax-full/js/input/tex/require/RequireConfiguration.js");
/* harmony import */ var mathjax_full_js_input_tex_require_RequireConfiguration__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(mathjax_full_js_input_tex_require_RequireConfiguration__WEBPACK_IMPORTED_MODULE_9__);

// MathJax core

// TeX input

// HTML output







mathjax_full_js_mathjax__WEBPACK_IMPORTED_MODULE_1__.mathjax.handlers.register((0,mathjax_full_js_ui_safe_SafeHandler__WEBPACK_IMPORTED_MODULE_6__.SafeHandler)(new mathjax_full_js_handlers_html_HTMLHandler__WEBPACK_IMPORTED_MODULE_7__.HTMLHandler((0,mathjax_full_js_adaptors_browserAdaptor__WEBPACK_IMPORTED_MODULE_8__.browserAdaptor)())));
class emptyFont extends mathjax_full_js_output_chtml_fonts_tex__WEBPACK_IMPORTED_MODULE_4__.TeXFont {
}
emptyFont.defaultFonts = {};
class MathJax3Typesetter {
    constructor(app) {
        const chtml = new mathjax_full_js_output_chtml__WEBPACK_IMPORTED_MODULE_3__.CHTML({
            font: new emptyFont()
        });
        const tex = new mathjax_full_js_input_tex__WEBPACK_IMPORTED_MODULE_2__.TeX({
            packages: mathjax_full_js_input_tex_AllPackages__WEBPACK_IMPORTED_MODULE_5__.AllPackages.concat('require'),
            inlineMath: [
                ['$', '$'],
                ['\\(', '\\)']
            ],
            displayMath: [
                ['$$', '$$'],
                ['\\[', '\\]']
            ],
            processEscapes: true,
            processEnvironments: true,
            maxBuffer: 5000000000 * 1024
        });
        this._mathDocument = mathjax_full_js_mathjax__WEBPACK_IMPORTED_MODULE_1__.mathjax.document(window.document, {
            InputJax: tex,
            OutputJax: chtml
        });
        console.log(tex);
        const mjclipboard = 'mathjax:clipboard';
        const mjscale = 'mathjax:scale';
        app.commands.addCommand(mjclipboard, {
            execute: (args) => {
                const md = this._mathDocument;
                const oJax = md.outputJax;
                navigator.clipboard.writeText(oJax.math.math);
            },
            label: 'MathJax Copy Latex'
        });
        app.commands.addCommand(mjscale, {
            execute: (args) => {
                const scale = args['scale'] || 1.0;
                const md = this._mathDocument;
                md.outputJax.options.scale = scale;
                md.rerender();
            },
            label: (args) => 'Mathjax Scale ' + (args['scale'] ? `x${args['scale']}` : 'Reset')
        });
    }
    /**
     * Typeset the math in a node.
     */
    typeset(node) {
        this._mathDocument.options.elements = [node];
        this._mathDocument.clear().render();
        delete this._mathDocument.options.elements;
    }
}
/**
 * Initialization data for the jijzeptlab-mathjax extension.
 */
const plugin = {
    id: 'jijzeptlab-mathjax:plugin',
    autoStart: true,
    // optional: [ISettingRegistry],
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__.ILatexTypesetter,
    activate: (app, settingRegistry) => new MathJax3Typesetter(app)
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b9fa89492ba224ba7e18.js.map