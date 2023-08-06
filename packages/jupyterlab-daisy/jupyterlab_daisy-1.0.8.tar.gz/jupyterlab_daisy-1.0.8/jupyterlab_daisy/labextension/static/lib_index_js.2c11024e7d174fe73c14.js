"use strict";
(self["webpackChunkjupyterlab_daisy"] = self["webpackChunkjupyterlab_daisy"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-daisy', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");






// TODO: Should probably split sidebar logic/layout from button class
class ButtonExtension {
    constructor(app, tracker) {
        this.sidebar = undefined;
        this.editor = undefined;
        this.daisy_address = "";
        this.app = app;
        this.tracker = tracker;
    }
    // Closes the sidebar and replaces the selected text
    // TODO: If the user modifies the selection, the sidebar should also close
    closeAndReplace(ev, sidebar) {
        var _a, _b;
        sidebar === null || sidebar === void 0 ? void 0 : sidebar.close();
        let chosen = (_a = ev.target.textContent) !== null && _a !== void 0 ? _a : '';
        (_b = this.editor) === null || _b === void 0 ? void 0 : _b.replaceSelection(`${chosen}`);
    }
    setDaisyAddress(daisy_address) {
        this.daisy_address = daisy_address;
    }
    populateListRelated(source_asset_name, target_asset_names, list) {
        while (list.firstChild != null) {
            list.removeChild(list.firstChild);
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)(`get-related?source_asset_id=${source_asset_name}&target_asset_ids=${target_asset_names.join(',')}`)
            .then(json => {
            json['RelatedTables'].forEach((entry) => {
                const bla = document.createElement('li');
                const button = document.createElement('button');
                button.className = 'my-button';
                button.textContent = '+';
                const text = document.createElement('p');
                const splitLinks = entry.links.map(l => l.split('/'));
                const itemName = `${splitLinks[0][0]}/${splitLinks[0][splitLinks[0].length - 1]} -> ${splitLinks[splitLinks.length - 1][0]}/${splitLinks[splitLinks.length - 1][splitLinks[splitLinks.length - 1].length - 1]}`;
                bla.setAttribute('title', `${itemName}. Click '+' for details...`);
                text.textContent = itemName;
                text.className = 'my-list-item-text';
                const tableContainer = document.createElement('div');
                const table = document.createElement('table');
                table.setAttribute('style', 'width: 100%;');
                tableContainer.className =
                    'my-column-table-div-collapsed';
                tableContainer.setAttribute('style', 'height: 0px');
                tableContainer.appendChild(table);
                const itemDiv = document.createElement('div');
                itemDiv.className = 'my-list-item-div';
                itemDiv.appendChild(button);
                itemDiv.appendChild(text);
                bla.appendChild(itemDiv);
                bla.appendChild(tableContainer);
                bla.className = 'my-list-item';
                const tableHeader = document.createElement('tr');
                tableHeader.innerHTML = `
                    <th>Connected via</th>
                    `;
                table.appendChild(tableHeader);
                splitLinks.forEach(link => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${link[0]}/${link[link.length - 1]}</td>
                      `;
                    table.appendChild(tr);
                });
                button.onclick = () => {
                    if (tableContainer.className === 'my-column-table-div') {
                        tableContainer.className =
                            'my-column-table-div-collapsed';
                        button.className = 'my-button';
                        button.textContent = '+';
                        tableContainer.setAttribute('style', 'height: 0px');
                    }
                    else {
                        tableContainer.className = 'my-column-table-div';
                        button.className = 'my-button-toggled';
                        button.textContent = '-';
                        tableContainer.setAttribute('style', `height: ${table.clientHeight}px`);
                    }
                };
                text.onclick = ev => this.closeAndReplace(ev, this.sidebar);
                list.appendChild(bla);
            });
        })
            .catch(reason => { console.error('AEUHHH????', reason); });
    }
    populateList(asset_name, list) {
        while (list.firstChild != null) {
            list.removeChild(list.firstChild);
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)(`get-joinable?asset_id=${asset_name}`)
            .then(json => {
            json['JoinableTables'].forEach((entry) => {
                const bla = document.createElement('li');
                bla.setAttribute('title', `Matched ${entry.matches.length} columns, click '+' for details...`);
                const button = document.createElement('button');
                button.className = 'my-button';
                button.textContent = '+';
                const text = document.createElement('p');
                text.textContent = entry.table_path.split('/')[0];
                text.className = 'my-list-item-text';
                const tableContainer = document.createElement('div');
                const table = document.createElement('table');
                table.setAttribute('style', 'width: 100%;');
                tableContainer.className =
                    'my-column-table-div-collapsed';
                tableContainer.setAttribute('style', 'height: 0px');
                tableContainer.appendChild(table);
                const itemDiv = document.createElement('div');
                itemDiv.className = 'my-list-item-div';
                itemDiv.appendChild(button);
                itemDiv.appendChild(text);
                bla.appendChild(itemDiv);
                bla.appendChild(tableContainer);
                bla.className = 'my-list-item';
                const tableHeader = document.createElement('tr');
                tableHeader.innerHTML = `
                    <th>Column Name</th>
                    <th align="right">COMA Score</th>
                    `;
                table.appendChild(tableHeader);
                entry.matches.forEach(match => {
                    const tr = document.createElement('tr');
                    const split = match['PK']['from_id'].split('/');
                    tr.setAttribute('title', match['PK']['from_id']);
                    tr.innerHTML = `
                        <td>${split[0]}/${split[split.length - 1]}</td>
                        <td class='alnright'>${parseFloat(match['RELATED']['coma']).toFixed(3)}</td>
                      `;
                    table.appendChild(tr);
                });
                button.onclick = () => {
                    if (tableContainer.className === 'my-column-table-div') {
                        tableContainer.className =
                            'my-column-table-div-collapsed';
                        button.className = 'my-button';
                        button.textContent = '+';
                        tableContainer.setAttribute('style', 'height: 0px');
                    }
                    else {
                        tableContainer.className = 'my-column-table-div';
                        button.className = 'my-button-toggled';
                        button.textContent = '-';
                        tableContainer.setAttribute('style', `height: ${table.clientHeight}px`);
                    }
                };
                text.onclick = ev => this.closeAndReplace(ev, this.sidebar);
                list.appendChild(bla);
            });
        })
            .catch(reason => { console.error('AEUHHH????', reason); });
    }
    createNew(panel, context) {
        const mybutton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.paletteIcon,
            tooltip: "Augment Data",
            onClick: () => {
                var _a, _b, _c, _d, _e;
                (_a = this.sidebar) === null || _a === void 0 ? void 0 : _a.close();
                const activeCell = this.tracker.activeCell;
                if (activeCell !== null) {
                    this.editor = activeCell.editor;
                    let value = this.editor.getRange(this.editor.getCursor('start'), this.editor.getCursor('end'));
                    this.sidebar = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Panel();
                    this.sidebar.addClass('my-panel');
                    this.sidebar.id = 'daisy-jupyterlab';
                    this.sidebar.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.paletteIcon;
                    this.app.shell.add(this.sidebar, 'right', { rank: 50000 });
                    this.app.shell.activateById(this.sidebar.id);
                    const header = document.createElement('h1');
                    header.textContent = 'Related Datasets';
                    const runButton = document.createElement('button');
                    runButton.textContent = 'Execute Query';
                    runButton.className = 'my-query-button';
                    const inp = document.createElement('input');
                    inp.type = "text";
                    inp.name = "name";
                    inp.id = "source";
                    inp.value = value;
                    inp.className = 'my-highlighted-item';
                    inp.placeholder = "Source Table Name";
                    const sep = document.createElement('hr');
                    sep.className = 'solid';
                    const additionalFields = document.createElement('div');
                    additionalFields.id = "targets";
                    const form = document.createElement('form');
                    form.appendChild(inp);
                    form.appendChild(sep);
                    form.appendChild(additionalFields);
                    form.appendChild(runButton);
                    const checkbox = document.createElement('input');
                    checkbox.type = "checkbox";
                    checkbox.id = "related";
                    checkbox.name = "related";
                    const checkboxLabel = document.createElement('label');
                    checkboxLabel.htmlFor = "related";
                    checkboxLabel.textContent = "Connect to existing assets";
                    const checkboxSpan = document.createElement('span');
                    checkboxSpan.appendChild(checkbox);
                    checkboxSpan.appendChild(checkboxLabel);
                    const addField = function (node) {
                        var _a;
                        const extraInp = document.createElement('input');
                        extraInp.type = "text";
                        extraInp.name = `target-${additionalFields.childElementCount}`;
                        extraInp.value = "";
                        extraInp.className = 'my-highlighted-item';
                        const delButton = document.createElement('button');
                        delButton.className = 'my-button';
                        delButton.textContent = '-';
                        delButton.type = "button";
                        const fieldSpan = document.createElement('span');
                        fieldSpan.className = "my-input-span";
                        fieldSpan.appendChild(extraInp);
                        fieldSpan.appendChild(delButton);
                        delButton.onclick = (event) => {
                            fieldSpan.remove();
                            for (let i = 0; i < additionalFields.childElementCount; i++) {
                                additionalFields.children[i].children[0].placeholder = `Table Name ${i}`;
                            }
                        };
                        additionalFields.insertBefore(fieldSpan, (_a = node === null || node === void 0 ? void 0 : node.nextSibling) !== null && _a !== void 0 ? _a : null);
                        for (let i = 0; i < additionalFields.childElementCount; i++) {
                            additionalFields.children[i].children[0].placeholder = `Table Name ${i}`;
                        }
                    };
                    checkbox.addEventListener('change', (event) => {
                        if (event.currentTarget.checked) {
                            addField(null);
                            const addButton = document.createElement('button');
                            addButton.className = 'my-query-button';
                            addButton.textContent = 'Add Item';
                            addButton.type = "button";
                            addButton.onclick = () => { addField(additionalFields.lastChild); };
                            addButton.id = "addButton";
                            form.insertBefore(addButton, runButton);
                        }
                        else {
                            while (additionalFields.firstChild != null) {
                                additionalFields.removeChild(additionalFields.firstChild);
                            }
                            document.getElementById('addButton').remove();
                        }
                    });
                    const list = document.createElement('ul');
                    list.className = 'my-list';
                    const temp = this;
                    form.onsubmit = function (event) {
                        event.preventDefault();
                        event.stopPropagation();
                        if (!checkbox.checked) {
                            temp.populateList(inp.value, list);
                        }
                        else {
                            const targets = [];
                            for (const child of additionalFields.children) {
                                const target = child.children[0].value;
                                targets.push(target);
                            }
                            temp.populateListRelated(inp.value, targets, list);
                        }
                    };
                    (_b = this.sidebar) === null || _b === void 0 ? void 0 : _b.node.appendChild(header);
                    (_c = this.sidebar) === null || _c === void 0 ? void 0 : _c.node.appendChild(checkboxSpan);
                    (_d = this.sidebar) === null || _d === void 0 ? void 0 : _d.node.appendChild(form);
                    (_e = this.sidebar) === null || _e === void 0 ? void 0 : _e.node.appendChild(list);
                    this.populateList(value, list);
                }
            }
        });
        // Add the toolbar button to the notebook toolbar
        panel.toolbar.insertItem(10, 'mybutton', mybutton);
        return mybutton;
    }
}
/**
 * Initialization data for the jupyterlab_daisy extension.
 */
const plugin = {
    id: 'jupyterlab_daisy:plugin',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: (app, settingRegistry, palette, tracker) => {
        console.log('JupyterLab extension jupyterlab_daisy is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('jupyterlab_daisy settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for jupyterlab_daisy.', reason);
            });
        }
        const button = new ButtonExtension(app, tracker);
        app.docRegistry.addWidgetExtension('Notebook', button);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.2c11024e7d174fe73c14.js.map