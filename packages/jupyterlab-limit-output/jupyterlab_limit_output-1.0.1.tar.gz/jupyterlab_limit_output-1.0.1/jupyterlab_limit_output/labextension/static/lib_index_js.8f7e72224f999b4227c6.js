"use strict";
(self["webpackChunkjupyterlab_limit_output"] = self["webpackChunkjupyterlab_limit_output"] || []).push([["lib_index_js"],{

/***/ "./lib/formatters.js":
/*!***************************!*\
  !*** ./lib/formatters.js ***!
  \***************************/
/***/ ((__unused_webpack_module, exports) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.limitByLines = exports.limitByCharacters = void 0;
const NEW_LINE = '\n';
const SPACER = '\n\n\n';
/**
 * Return a string with at most head starting characters and tail ending (plus a warning)
 */
const limitByCharacters = (text, head, tail) => {
    const maxChars = head + tail;
    if (text.length > maxChars) {
        const headstr = text.substring(0, head);
        const tailstr = text.substring(text.length - tail);
        let msg = '';
        if (head) {
            msg = ` first ${head}`;
        }
        if (tail) {
            msg += `${head ? ' and' : ''} last ${tail}`;
        }
        return `${headstr}${head ? SPACER : ''}WARNING: Output limited. Showing${msg} characters.${tail ? SPACER : ''}${tailstr}`;
    }
    return text;
};
exports.limitByCharacters = limitByCharacters;
/**
 * Find the nth index of the newline character
 */
function _nthNewLineIndex(text, n) {
    let idx = 0;
    while (n-- > 0 && idx++ < text.length) {
        idx = text.indexOf(NEW_LINE, idx);
        // Not found before we ran out of n
        if (idx < 0) {
            return null;
        }
    }
    return idx;
}
/**
 * Find the nth newline from the end of the string (excluding a possible final new line)
 */
function _nthNewLineFromLastIndex(text, n) {
    let idx = text.length - 1; // Ignore a possible final trailing \n
    while (n-- > 0 && idx-- >= 0) {
        idx = text.lastIndexOf(NEW_LINE, idx);
        // Not found before we ran out of n
        if (idx < 0) {
            return null;
        }
    }
    return idx;
}
/**
 * Return a string with at most head starting lines and tail ending (plus a warning)
 */
const limitByLines = (text, head, tail) => {
    const headEndPos = head > 0 ? _nthNewLineIndex(text, head) : -1;
    if (headEndPos === null) {
        return text;
    }
    const tailStartPos = tail > 0 ? _nthNewLineFromLastIndex(text, tail) : text.length;
    if (tailStartPos === null) {
        return text;
    }
    if (tailStartPos <= headEndPos) {
        return text;
    }
    const headstr = text.substring(0, headEndPos);
    const tailstr = text.substring(tailStartPos);
    let msg = '';
    if (head) {
        msg = ` first ${head}`;
    }
    if (tail) {
        msg += `${head ? ' and' : ''} last ${tail}`;
    }
    return `${headstr}${head ? SPACER : ''}WARNING: Output limited. Showing${msg} lines.${tail ? SPACER : ''}${tailstr}`;
};
exports.limitByLines = limitByLines;


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
const rendermime_1 = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
const settingregistry_1 = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
const renders_1 = __webpack_require__(/*! ./renders */ "./lib/renders.js");
const PLUGIN_NAME = 'jupyterlab-limit-output';
const extension = {
    id: `${PLUGIN_NAME}:rendertext`,
    rendererFactory: renders_1.rendererFactory,
    // This number is NOT random. It's just lower (more preferred) than https://github.com/jupyterlab/jupyterlab/blob/0cbfcbe8c09d2c1fbfd1912f4d36c12479893946/packages/rendermime/src/factories.ts#L68
    // Setting the rank too low makes the text version of renders too preferred (e.g. show text instead of the widget render)
    rank: 119,
    dataType: 'string',
};
const RenderExtension = {
    id: `${PLUGIN_NAME}:renders`,
    autoStart: true,
    requires: [rendermime_1.IRenderMimeRegistry, settingregistry_1.ISettingRegistry],
    activate: function (app, rendermime, settingRegistry) {
        // eslint-disable-next-line no-console
        console.log('JupyterLab extension jupyterlab-limit-output is activated!');
        rendermime.addFactory(extension.rendererFactory, extension.rank);
        function updateSettings(settings) {
            const head = settings.get('head').composite;
            const tail = settings.get('tail').composite;
            const enabled = settings.get('enabled').composite;
            const method = settings.get('method')
                .composite;
            renders_1.updateLimitOutputSettings({ head, tail, method, enabled });
        }
        settingRegistry.load(`${PLUGIN_NAME}:settings`).then((settings) => {
            updateSettings(settings);
            settings.changed.connect(updateSettings);
        }, (err) => {
            console.error(`Could not load settings, so did not activate ${PLUGIN_NAME}: ${err}`);
        });
    },
};
exports["default"] = RenderExtension;


/***/ }),

/***/ "./lib/renders.js":
/*!************************!*\
  !*** ./lib/renders.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.rendererFactory = exports.MyRenderedText = exports.updateLimitOutputSettings = void 0;
const rendermime_1 = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
const formatters_1 = __webpack_require__(/*! ./formatters */ "./lib/formatters.js");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const WARN_BEFORE_EXPANDING_SOURCE_LENGTH_CH = 100000;
const WARN_BEFORE_EXPANDING_SOURCE_LENGTH_LINES = 1000;
let limitSettings = {
    head: 50,
    tail: 50,
    method: 'lines',
    enabled: true,
};
const updateLimitOutputSettings = (settings) => {
    limitSettings = settings;
    if (limitSettings.head < 0) {
        limitSettings.head = 0;
    }
    if (limitSettings.tail < 0) {
        limitSettings.tail = 0;
    }
    if (limitSettings.tail === 0 && limitSettings.head === 0) {
        limitSettings.enabled = false;
    }
    if (limitSettings.method !== 'lines' &&
        limitSettings.method !== 'characters') {
        limitSettings.method = 'lines';
    }
};
exports.updateLimitOutputSettings = updateLimitOutputSettings;
const limitOutputRenderText = async (options, _head = 0, _tail = 0, _cleanupButtonFn = null) => {
    if (limitSettings.enabled) {
        // We have to clone so that we can both keep track of number of head/tail
        // shown as well as keep the original options unchanged
        const clonedOptions = Object.assign(Object.assign({}, options), { head: _head || limitSettings.head, tail: _tail || limitSettings.tail });
        if (limitSettings.method === 'characters') {
            clonedOptions.source = formatters_1.limitByCharacters(options.source, clonedOptions.head, clonedOptions.tail);
        }
        else {
            clonedOptions.source = formatters_1.limitByLines(options.source, clonedOptions.head, clonedOptions.tail);
        }
        // Add a div so we can easily remove output
        const div = document.createElement('div');
        options.host.append(div);
        clonedOptions.host = div;
        // Wait for text to render so that we can add our buttons after it
        const ret = await rendermime_1.renderText(clonedOptions);
        // If we need to, add buttons for expanding output
        if (_cleanupButtonFn === null &&
            clonedOptions.source.length !== options.source.length) {
            const expandLines = Math.max(limitSettings.tail, limitSettings.head);
            const span = document.createElement('span');
            [
                // label, expand head, expand tail, warn on click
                [
                    `↑ Show ${expandLines} ${limitSettings.method}`,
                    expandLines,
                    0,
                    false,
                ],
                [`Show all ${limitSettings.method}`, Infinity, Infinity, true],
                [
                    `↓ Show ${expandLines} ${limitSettings.method}`,
                    0,
                    expandLines,
                    false,
                ],
            ].map((b) => {
                const [label, expandUp, expandDown, warnOnClick] = b;
                const button = document.createElement('button');
                button.innerText = label;
                button.className = 'bp3-button jp-Button limit-output-button';
                const cleanup = () => span.remove();
                button.onclick = async () => {
                    if (warnOnClick) {
                        let warningLabel;
                        if (limitSettings.method === 'lines') {
                            let count = 0;
                            for (let i = 0; i < options.source.length; ++i) {
                                if (options.source[i] === '\n') {
                                    count++;
                                }
                            }
                            if (count > WARN_BEFORE_EXPANDING_SOURCE_LENGTH_LINES) {
                                warningLabel = `${count.toLocaleString()} lines`;
                            }
                        }
                        else {
                            if (options.source.length > WARN_BEFORE_EXPANDING_SOURCE_LENGTH_CH) {
                                warningLabel = `${options.source.length.toLocaleString()} characters`;
                            }
                        }
                        if (warningLabel) {
                            const result = await apputils_1.showDialog({
                                title: 'Show all',
                                body: `Do you really want to show all ${warningLabel}?`,
                            });
                            if (!result.button.accept) {
                                return;
                            }
                        }
                    }
                    // This binds the first clonedOptions call
                    // i.e. future calls will updated clonedOptions but this onclick won't change
                    clonedOptions.head += expandUp;
                    clonedOptions.tail += expandDown;
                    await limitOutputRenderText(Object.assign(Object.assign({}, options), { host: clonedOptions.host }), clonedOptions.head, clonedOptions.tail, cleanup);
                    // Not the best design, but we know the prev element added is the renderText one
                    // so we remove it before we redisplay
                    clonedOptions.host.childNodes.forEach((n) => n.remove());
                };
                span.appendChild(button);
            });
            options.host.append(span);
            // We are fully expanded!
        }
        else if (clonedOptions.source.length === options.source.length &&
            _cleanupButtonFn) {
            _cleanupButtonFn();
        }
        return ret;
    }
    return rendermime_1.renderText(options);
};
class MyRenderedText extends rendermime_1.RenderedText {
    /**
     * Render a mime model.
     *
     * @param model - The mime model to render.
     *
     * @returns A promise which resolves when rendering is complete.
     */
    render(model) {
        return limitOutputRenderText({
            host: this.node,
            sanitizer: this.sanitizer,
            source: String(model.data[this.mimeType]),
            translator: this.translator,
        });
    }
    /**
     * Dispose the contents of node to contain potential memory leak.
     *
     * **Notes**: when user attempts to clean the output using context menu
     * they invoke `JupyterFrontEnd.evtContextMenu` which caches the event
     * to enable commands and extensions to access it later; this leads to
     * a memory leak as the event holds the target node reference.
     */
    dispose() {
        // TODO: remove ts-ignore during JupyterLab 4.0/TypeScript 5.0 migration
        // @ts-ignore
        this.node.replaceChildren();
        super.dispose();
    }
}
exports.MyRenderedText = MyRenderedText;
exports.rendererFactory = {
    safe: true,
    mimeTypes: [
        'text/plain',
        'application/vnd.jupyter.stdout',
        'application/vnd.jupyter.stderr',
    ],
    createRenderer: (options) => new MyRenderedText(options),
};


/***/ })

}]);
//# sourceMappingURL=lib_index_js.8f7e72224f999b4227c6.js.map