/*
 @license
 webix UI v.2.2.3
 This software is can be used only as part of webix.com site
 You are not allowed to copy this file and use in any other project
 */
webix.type(webix.ui.tree, {
	name : "FileTree",
	css : "webix_fmanager_tree",
	folder : function(t) {
		return t.$count && t.open ? "<div class='webix_icon icon fa-folder-open'></div>" : "<div class='webix_icon icon fa-folder'></div>"
	}
}), webix.type(webix.ui.dataview, {
	name : "FileView",
	css : "webix_fmanager_files",
	height : 110,
	margin : 10,
	width : 150,
	template : function(t, e) {
		var i = t.type || "file";
		i = e.icons[i] || e.icons.file;
		var s = "webix_fmanager_data_icon", n = e.templateName(t, e);
		return "<div class='webix_fmanager_file'><div class='" + s + "'>" + e.templateIcon(t, e) + "</div>" + n + "</div>"
	}
}), webix.i18n.filemanager = {
	name : "Name",
	size : "Size",
	type : "Type",
	date : "Date",
	copy : "Copy",
	cut : "Cut",
	paste : "Paste",
	upload : "Upload",
	remove : "Delete",
	create : "Create Folder",
	rename : "Rename",
	location : "Location",
	select : "Select Files",
	sizeLabels : ["B", "KB", "MB", "GB"],
	saving : "Saving...",
	errorResponse : "Error: changes were not saved!",
	replaceConfirmation : "The folder already contains files with such names. Would you like to replace existing files ?",
	createConfirmation : "The folder with such a name already exists. Would you like to replace it ?",
	renameConfirmation : "The file with such a name already exists. Would you like to replace it ?",
	yes : "Yes",
	no : "No",
	types : {
		folder : "Folder",
		doc : "Document",
		excel : "Excel",
		pdf : "PDF",
		pp : "PowerPoint",
		text : "Text File",
		video : "Video File",
		image : "Image",
		code : "Code",
		audio : "Audio",
		archive : "Archive",
		file : "File"
	}
}, webix.protoUI({
	name : "filetree"
}, webix.EditAbility, webix.ui.tree), webix.protoUI({
	name : "fileview"
}, webix.EditAbility, webix.ui.dataview), webix.protoUI({
	name : "filetable",
	$dragHTML : function(t) {
		var e = "<div class='webix_dd_drag webix_fmanager_drag' >", i = this.getColumnIndex("value");
		return e += "<div style='width:auto'>" + this.config.columns[i].template(t, this.type) + "</div>", e + "</div>"
	}
}, webix.ui.datatable), webix.protoUI({
	name : "path",
	defaults : {
		layout : "x",
		separator : ",",
		scroll : !1
	},
	$skin : function() {
		this.type.height = webix.skin.$active.buttonHeight || webix.skin.$active.inputHeight
	},
	$init : function() {
		this.$view.className += " webix_path"
	},
	value_setter : function(t) {
		return this.setValue(), t
	},
	setValue : function(t) {
		this.clearAll(), t && ("string" == typeof t && ( t = t.split(this.config.separator)), this.parse(webix.copy(t)))
	},
	getValue : function() {
		return this.serialize()
	}
}, webix.ui.list), webix.FileManagerStructure = {
	structure : {
		actions : {
			config : function() {
				var t = this.config.templateName;
				return {
					view : "contextmenu",
					width : 200,
					padding : 0,
					autofocus : !1,
					css : "webix_fmanager_actions",
					template : function(e, i) {
						var s = t(e, i);
						return "<span class='webix_icon fa-" + e.icon + "'></span>" + s
					},
					data : "actionsData"
				}
			},
			oninit : function() {
				var t = this.getMenu();
				t.$q = !1, t && (this.getMenu().attachEvent("onItemClick", webix.bind(function(e, i) {
					var s = this.getMenu().getItem(e), n = this[s.method] || this[e];
					n && this.callEvent("onbefore" + (s.method || e), [this.getActive()]) && (("upload" != e || !webix.isUndefined(XMLHttpRequest) && !webix.isUndefined((new XMLHttpRequest).upload)) && (t.Uq(!0), t.hide()), webix.delay(function() {
						n.call(this, this.getActive(), i), this.callEvent("onafter" + (s.method || e), [])
					}, this))
				}, this)), this.getMenu().attachEvent("onBeforeShow", function() {
					var t = this.getContext();
					return t && t.obj ? t.obj.callEvent("onBeforeMenuShow", [t.id]) : !0
				}))
			}
		},
		actionsData : {
			config : function() {
				return [{
					id : "copy",
					method : "markCopy",
					icon : "copy",
					value : webix.i18n.filemanager.copy
				}, {
					id : "cut",
					method : "markCut",
					icon : "cut",
					value : webix.i18n.filemanager.cut
				}, {
					id : "paste",
					method : "pasteFile",
					icon : "paste",
					value : webix.i18n.filemanager.paste
				}, {
					$template : "Separator"
				}, {
					id : "create",
					method : "createFolder",
					icon : "folder-o",
					value : webix.i18n.filemanager.create
				}, {
					id : "remove",
					method : "deleteFile",
					icon : "times",
					value : webix.i18n.filemanager.remove
				}, {
					id : "edit",
					method : "editFile",
					icon : "edit",
					value : webix.i18n.filemanager.rename
				}, {
					id : "upload",
					method : "uploadFile",
					icon : "upload",
					value : webix.i18n.filemanager.upload
				}]
			}
		},
		mainLayout : {
			type : "clean",
			rows : "mainRows"
		},
		mainRows : ["toolbar", "bodyLayout"],
		toolbar : {
			css : "webix_fmanager_toolbar",
			paddingX : 10,
			paddingY : 5,
			margin : 7,
			cols : "toolbarElements"
		},
		toolbarElements : ["menu", {
			id : "menuSpacer",
			width : 65
		}, {
			margin : 2,
			cols : ["back", "forward"]
		}, "up", "path", "search", "modes"],
		menu : {
			config : {
				view : "button",
				type : "iconButton",
				css : "webix_fmanager_back",
				icon : "bars",
				width : 37
			},
			oninit : function() {
				this.$$("menu") && (this.$$("menu").attachEvent("onItemClick", webix.bind(function() {
					this.callEvent("onBeforeMenu", []) && (this.getMenu().show(this.$$("menu").$view), this.callEvent("onAfterMenu", []))
				}, this)), this.config.readonly && (this.$$("menu").hide(), this.$$("menuSpacer") && this.$$("menuSpacer").hide()))
			}
		},
		back : {
			config : {
				view : "button",
				type : "iconButton",
				css : "webix_fmanager_back",
				icon : "angle-left",
				width : 37
			},
			oninit : function() {
				this.$$("back") && this.$$("back").attachEvent("onItemClick", webix.bind(function() {
					this.callEvent("onBeforeBack", []) && (this.goBack(), this.callEvent("onAfterBack", []))
				}, this))
			}
		},
		forward : {
			config : {
				view : "button",
				type : "iconButton",
				css : "webix_fmanager_forward",
				icon : "angle-right",
				width : 37
			},
			oninit : function() {
				this.$$("forward") && this.$$("forward").attachEvent("onItemClick", webix.bind(function() {
					this.callEvent("onBeforeForward", []) && (this.goForward(), this.callEvent("onAfterForward", []))
				}, this))
			}
		},
		up : {
			config : {
				view : "button",
				type : "iconButton",
				css : "webix_fmanager_up",
				icon : "level-up",
				disable : !0,
				width : 37
			},
			oninit : function() {
				this.$$("up") && this.$$("up").attachEvent("onItemClick", webix.bind(function() {
					this.callEvent("onBeforeLevelUp", []) && (this.levelUp(), this.callEvent("onAfterLevelUp", []))
				}, this))
			}
		},
		path : {
			config : {
				view : "path",
				borderless : !0
			},
			oninit : function() {
				this.$$("path") && (this.attachEvent("onFolderSelect", webix.bind(function(t) {
					this.$$("path").setValue(this.getPathNames(t))
				}, this)), this.$$("path").attachEvent("onItemClick", webix.bind(function(t) {
					var e = this.$$("path").getIndexById(t), i = this.$$("path").count() - e - 1;
					if (this.$searchResults && this.hideSearchResults(), i) {
						for ( t = this.getCursor(); i; )
							t = this.getParentId(t), i--;
						this.setCursor(t)
					}
					this.callEvent("onAfterPathClick", [t])
				}, this)), this.data.attachEvent("onClearAll", webix.bind(function() {
					this.clearAll()
				}, this.$$("path"))))
			}
		},
		search : {
			config : {
				view : "search",
				gravity : .3,
				css : "webix_fmanager_search"
			},
			oninit : function() {
				var t = this.$$("search");
				t && (t.attachEvent("onTimedKeyPress", webix.bind(function() {
					if (9 != this.cx) {
						var e = t.getValue();
						e ? this.callEvent("onBeforeSearch", [e]) && (this.showSearchResults(e), this.callEvent("onAfterSearch", [e])) : this.$searchResults && this.hideSearchResults()
					}
				}, this)), t.attachEvent("onKeyPress", function(t) {
					this.cx = t
				}), this.attachEvent("onAfterModeChange", function() {
					this.$searchResults && this.showSearchResults(t.getValue())
				}))
			}
		},
		bodyLayout : {
			css : "webix_fmanager_body",
			cols : "bodyCols"
		},
		bodyCols : ["tree", {
			view : "resizer",
			width : 2
		}, "modeViews"],
		tree : {
			config : {
				width : 251,
				view : "filetree",
				id : "tree",
				select : !0,
				filterMode : {
					showSubItems : !1,
					openParents : !1
				},
				type : "FileTree",
				navigation : !0,
				scroll : !0,
				editor : "text",
				editable : !0,
				editaction : !1,
				drag : !0,
				tabFocus : !0,
				onContext : {}
			},
			oninit : function() {
				var t = this.$$("tree");
				if (t) {
					t.type.icons = this.config.icons, t.sync(this, function() {
						this.filter(function(t) {
							return t.$count || "folder" == t.type
						})
					}), t.attachEvent("onAfterSelect", webix.bind(function(t) {
						this.callEvent("onFolderSelect", [t])
					}, this)), this.attachEvent("onAfterCursorChange", function(e) {
						e && (t.select(e), t.open(this.getParentId(e)))
					}), t.attachEvent("onItemClick", webix.bind(function() {
						this.$searchResults && this.hideSearchResults()
					}, this)), t.attachEvent("onItemDblClick", function(t) {
						this.isBranchOpen(t) ? this.close(t) : this.open(t)
					}), t.attachEvent("onBlur", function() {
						var t = this.getTopParentView();
						t.getMenu() && t.getMenu().isVisible() || webix.html.addCss(this.$view, "webix_blur")
					}), t.attachEvent("onFocus", webix.bind(function() {
						this.dx = t, webix.html.removeCss(t.$view, "webix_blur"), this.$$(this.config.mode).unselect()
					}, this)), this.attachEvent("onPathLevel", function(e) {
						t.open(e)
					}), this.attachEvent("onPathComplete", function(e) {
						t.showItem(e)
					}), this.config.readonly || (this.getMenu() && this.getMenu().attachTo(t), t.attachEvent("onBeforeMenuShow", function(t) {
						this.select(t), webix.UIManager.setFocus(this)
					})), t.attachEvent("onBeforeEditStop", webix.bind(function(e, i) {
						return this.callEvent("onBeforeEditStop", [i.id, e, i, t])
					}, this)), t.attachEvent("onAfterEditStop", webix.bind(function(e, i) {
						this.callEvent("onAfterEditStop", [i.id, e, i, t]) && this.renameFile(i.id, e.value)
					}, this)), t.attachEvent("onBeforeDrag", function(t, e) {
						var i = this.getTopParentView();
						return !i.config.readonly && i.callEvent("onBeforeDrag", [t, e])
					}), t.attachEvent("onBeforeDragIn", function(t, e) {
						var i = this.getTopParentView();
						return !i.config.readonly && i.callEvent("onBeforeDragIn", [t, e])
					}), t.attachEvent("onBeforeDrop", function(t, e) {
						var i = this.getTopParentView();
						return i.callEvent("onBeforeDrop", [t, e]) && t.from && (i.moveFile(t.source, t.target), i.callEvent("onAfterDrop", [t, e])), !1
					});
					var e = function() {
						t && webix.UIManager.setFocus(t)
					};
					this.attachEvent("onAfterBack", e), this.attachEvent("onAfterForward", e), this.attachEvent("onAfterLevelUp", e), this.attachEvent("onAfterPathClick", e), this.config.readonly && (t.define("drag", !1), t.define("editable", !1))
				}
			}
		},
		modeViews : {
			config : function(t) {
				var e = [];
				if (t.modes)
					for (var i = 0; i < t.modes.length; i++)
						e.push(t.modes[i]);
				return {
					animate : !1,
					cells : e
				}
			},
			oninit : function() {
				this.$$(this.config.mode) && this.$$(this.config.mode).show(), this.attachEvent("onBeforeCursorChange", function() {
					return this.$$(this.config.mode).unselect(), !0
				});
				var t = this.config.modes;
				if (t)
					for (var e = 0; e < t.length; e++)
						this.$$(t[e]) && this.$$(t[e]).filter && this.ex(t[e])
			}
		},
		modes : {
			config : function(t) {
				var e = 0, i = this.structure.modeOptions;
				if (i)
					for (var s = 0; s < i.length; s++)
						i[s].width && (e += i[s].width + (i.length ? 1 : 0));
				var n = {
					view : "segmented",
					options : "modeOptions",
					css : "webix_fmanager_modes",
					value : t.mode
				};
				return e && (n.width = e + 4), n
			},
			oninit : function() {
				this.$$("modes") && this.$$("modes").attachEvent("onBeforeTabClick", webix.bind(function(t) {
					var e = this.$$("modes").getValue();
					return this.callEvent("onBeforeModeChange", [e, t]) && this.$$(t) ? (this.config.mode = t, this.$$(t).show(), this.callEvent("onAfterModeChange", [e, t]), !0) : !1
				}, this))
			}
		},
		modeOptions : [{
			id : "files",
			width : 32,
			value : '<span class="webix_fmanager_mode_option webix_icon fa-th"></span>'
		}, {
			id : "table",
			width : 32,
			value : '<span class="webix_fmanager_mode_option webix_icon fa-list-ul"></span>'
		}],
		files : {
			config : {
				view : "fileview",
				type : "FileView",
				select : "multiselect",
				editable : !0,
				editaction : !1,
				editor : "text",
				editValue : "value",
				drag : !0,
				navigation : !0,
				tabFocus : !0,
				onContext : {}
			}
		},
		table : {
			config : {
				view : "filetable",
				css : "webix_fmanager_table",
				columns : "columns",
				editable : !0,
				editaction : !1,
				select : "multiselect",
				drag : !0,
				navigation : !0,
				resizeColumn : !0,
				tabFocus : !0,
				onContext : {}
			},
			oninit : function() {
				this.$$("table") && (this.attachEvent("onHideSearchResults", function() {
					this.$$("table").isColumnVisible("location") && this.$$("table").hideColumn("location")
				}), this.attachEvent("onShowSearchResults", function() {
					this.$$("table").isColumnVisible("location") || this.$$("table").showColumn("location")
				}), this.$$("table").attachEvent("onBeforeEditStart", function(t) {
					return this.fx ? !0 : "object" == typeof t ? !1 : (this.fx = !0, this.edit({
						row : t,
						column : "value"
					}), this.fx = !1, !1)
				}))
			}
		},
		columns : {
			config : function() {
				var t = webix.i18n.filemanager, e = this;
				return [{
					id : "value",
					header : t.name,
					fillspace : 3,
					template : function(t, e) {
						var i = e.templateName(t, e);
						return e.templateIcon(t, e) + i
					},
					sort : "string",
					editor : "text"
				}, {
					id : "date",
					header : t.date,
					fillspace : 2,
					template : function(t, e) {
						return e.templateDate(t, e)
					},
					sort : "date"
				}, {
					id : "type",
					header : t.type,
					fillspace : 1,
					sort : "string",
					template : function(t, e) {
						return e.templateType(t)
					}
				}, {
					id : "size",
					header : t.size,
					fillspace : 1,
					css : {
						"text-align" : "right"
					},
					template : function(t, e) {
						return "folder" == t.type ? "" : e.templateSize(t)
					},
					sort : "int"
				}, {
					id : "location",
					header : t.location,
					fillspace : 2,
					template : function(t) {
						for (var i = e.getPathNames(t.id), s = [], n = 0; n < i.length - 1; n++)
							s.push(i[n].value);
						return s.join("/")
					},
					sort : "string",
					hidden : !0
				}]
			}
		},
		upload : {
			config : function() {
				var t = {};
				return t = webix.isUndefined(XMLHttpRequest) || webix.isUndefined((new XMLHttpRequest).upload) ? {
					view : "uploader",
					css : "webix_upload_select_ie",
					type : "iconButton",
					icon : "check",
					label : webix.i18n.filemanager.select,
					formData : {
						action : "upload"
					}
				} : {
					view : "uploader",
					apiOnly : !0,
					formData : {
						action : "upload"
					}
				}
			},
			oninit : function() {
				var t = this.getUploader();
				if (t) {
					t.config.upload = this.config.handlers.upload;
					var e = this.config.modes;
					if (e)
						for (var i = 0; i < e.length; i++)
							this.$$(e[i]) && t.addDropZone(this.$$(e[i]).$view);
					t.attachEvent("onBeforeFileAdd", webix.bind(function(e) {
						return e.oldId = e.id, t.config.formData.target = this.gx(), this.callEvent("onBeforeFileUpload", [e])
					}, this)), t.attachEvent("onAfterFileAdd", webix.bind(function(t) {
						this.hx = null, this.add({
							id : t.id,
							value : t.name,
							type : t.type,
							size : t.size,
							date : (new Date).valueOf() / 1e3
						}, -1, this.getCursor()), this.config.uploadProgress && this.showProgress(this.config.uploadProgress), this.refreshCursor()
					}, this)), t.attachEvent("onFileUpload", webix.bind(function(t) {
						t.oldId && this.data.changeId(t.oldId, t.id), this.getItem(t.id).type = t.type, this.refreshCursor(), this.hideProgress()
					}, this)), t.attachEvent("onFileUploadError", webix.bind(function(t, e) {
						this.ix(t, e), this.hideProgress()
					}, this))
				}
			}
		}
	}
}, webix.FileManagerUpload = {
	px : function() {
		var t = webix.copy(this.structure.upload), e = this.qx(t, this.config);
		e && (webix.isUndefined(XMLHttpRequest) || webix.isUndefined((new XMLHttpRequest).upload) ? (this.Ix = webix.ui({
			view : "popup",
			padding : 0,
			width : 250,
			body : e
		}), this.rx = this.Ix.getBody(), this.attachEvent("onDestruct", function() {
			this.Ix.destructor()
		})) : (this.rx = webix.ui(e), this.attachEvent("onDestruct", function() {
			this.rx.destructor()
		})), t.oninit && t.oninit.call(this))
	},
	getUploader : function() {
		return this.rx
	},
	gx : function() {
		return this.hx || this.getCursor()
	},
	uploadFile : function(t, e) {
		this.data.branch[t] || ( t = this.getParentId(t)), this.hx = t, this.Ix ? this.Ix.show(e, {
			x : 20,
			y : 5
		}) : this.rx && this.rx.fileDialog()
	}
}, webix.protoUI({
	name : "filemanager",
	$init : function(t) {
		this.$view.className += " webix_fmanager", webix.extend(this.data, webix.TreeStore, !0), webix.extend(t, this.defaults), this.data.provideApi(this, !0), this.jx = webix.extend([], webix.PowerArray, !0), this.Pw(t), this.$ready.push(this.kx), webix.UIManager.tabControl = !0, webix.extend(t, this.zv(t))
	},
	kx : function() {
		this.lx(), this.attachEvent("onAfterLoad", function() {
			if (!this.config.disabledHistory) {
				var t = window.location.hash;
				t && 0 === t.indexOf("#!/") && this.setPath(t.replace("#!/", ""))
			}
			this.getCursor() || this.setCursor(this.Rw())
		}), this.attachEvent("onFolderSelect", function(t) {
			this.setCursor(t)
		}), this.attachEvent("onAfterCursorChange", function(t) {
			this.mx || (this.nx || this.jx.splice(1), 20 == this.jx.length && this.jx.splice(0, 1), this.jx.push(t), this.nx = this.jx.length - 1), this.mx = !1, this.config.disabledHistory || this.ox(t)
		}), this.attachEvent("onBeforeDragIn", function(t) {
			var e = t.target;
			if (e)
				for (var i = t.source, s = 0; s < i.length; s++)
					for (; e; ) {
						if (e == i[s])
							return !1;
						e = this.getParentId(e)
					}
			return !0
		}), this.px()
	},
	ox : function(t) {
		t = t || this.getCursor(), window.history && window.history.replaceState ? window.history.replaceState({
			webix : !0,
			id : this.config.id,
			value : t
		}, "", "#!/" + t) : window.location.hash = "#!/" + t
	},
	zv : function(t) {
		var e = this.structure.mainLayout, i = webix.extend({}, e.config || e);
		return this.Sw(i, t), t.on && t.on.onViewInit && t.on.onViewInit.apply(this, [t.id || "mainLayout", i]), webix.callEvent("onViewInit", [t.id || "mainLayout", i, this]), i
	},
	updateStructure : function() {
		var t = this.zv(), e = this.mc ? "rows" : "cols";
		this.define(e, t[e]), this.reconstruct()
	},
	Sw : function(t, e) {
		var i, s, n, a, r = "", o = ["rows", "cols", "elements", "cells", "columns", "options", "data"];
		for ( n = 0; n < o.length; n++)
			t[o[n]] && ( r = o[n], i = t[r]);
		if (i)
			for ("string" == typeof i && this.structure[i] && (t[r] = this.qx(webix.copy(this.structure[i]), e), i = t[r]), n = 0; n < i.length; n++) {
				if ( s = null, "string" == typeof i[n])
					if ( s = a = i[n], this.structure[a]) {
						var h = webix.extend({}, this.structure[a]);
						i[n] = this.qx(h, e), i[n].id = a, h.oninit && this.$ready.push(h.oninit)
					} else
						i[n] = {};
				this.Sw(i[n], e), s && (e.on && e.on.onViewInit && e.on.onViewInit.apply(this, [s, i[n]]), webix.callEvent("onViewInit", [s, i[n], this]))
			}
	},
	lx : function() {
		if (this.structure.actions) {
			var t = webix.copy(this.structure.actions), e = t.config || t;
			"function" == typeof e && ( e = e.call(this)), this.Sw(e, this.config), this.sx = webix.ui(e), this.attachEvent("onDestruct", function() {
				this.sx.destructor()
			}), t.oninit && this.$ready.push(t.oninit)
		}
	},
	getMenu : function() {
		return this.sx
	},
	getPath : function(t) {
		t = t || this.getCursor();
		for (var e = null, i = []; t && this.getItem(t); )
			e = this.getItem(t), i.push(t), t = this.getParentId(t);
		return i.reverse()
	},
	getPathNames : function(t) {
		t = t || this.getCursor();
		for (var e = null, i = []; t && this.getItem(t); )
			e = this.getItem(t), i.push({
				id : t,
				value : this.config.templateName(e)
			}), t = this.getParentId(t);
		return i.reverse()
	},
	setPath : function(t) {
		for (var e = t; e && this.getItem(e); )
			this.callEvent("onPathLevel", [e]), e = this.getParentId(e);
		this.setCursor(t), this.callEvent("onPathComplete", [t])
	},
	tx : function(t) {
		if (this.jx.length > 1) {
			var e = this.nx + t;
			e > -1 && e < this.jx.length && (this.mx = !0, this.setCursor(this.jx[e]), this.nx = e)
		}
		return this.getCursor()
	},
	getSearchData : function(t, e) {
		var i = [];
		return this.data.each(function(t) {
			var s = this.config.templateName(t);
			s.toLowerCase().indexOf(e.toLowerCase()) >= 0 && i.push(webix.copy(t))
		}, this, !0, t), i
	},
	showSearchResults : function(t) {
		this.callEvent("onShowSearchResults", []);
		var e = this.getSearchData(this.getCursor(), t);
		this.$searchResults = !0, this.$$(this.config.mode).filter && (this.$$(this.config.mode).clearAll(), this.$$(this.config.mode).parse(e))
	},
	hideSearchResults : function() {
		this.callEvent("onHideSearchResults", []), this.$searchResults = !1;
		var t = this.getCursor();
		this.ib = null, this.setCursor(t)
	},
	goBack : function(t) {
		return t = t ? -1 * Math.abs(t) : -1, this.tx(t)
	},
	goForward : function(t) {
		return this.tx(t || 1)
	},
	levelUp : function(t) {
		t = t || this.getCursor(), t && ( t = this.getParentId(t), this.setCursor(t))
	},
	markCopy : function(t) {
		t && (webix.isArray(t) || ( t = [t]), this.ux = t, this.vx = !0)
	},
	markCut : function(t) {
		t && (webix.isArray(t) || ( t = [t]), this.ux = t, this.vx = !1)
	},
	pasteFile : function(t) {
		webix.isArray(t) && ( t = t[0]), t && ( t = t.toString(), this.data.branch[t] && "folder" == this.getItem(t).type && this.ux && (this.vx ? this.copyFile(this.ux, t) : this.moveFile(this.ux, t)))
	},
	download : function(t) {
		var e = this.config.handlers.download;
		e && webix.send(e, {
			action : "download",
			source : t
		})
	},
	Jx : function(t, e, i) {
		var s = !1;
		return this.data.eachChild(e, webix.bind(function(e) {
			t != this.config.templateName(e) || i && e.id == i || ( s = e.id)
		}, this)), s
	},
	Kx : function(t) {
		this.data.eachSubItem(t, function(t) {
			t.value && this.changeId(t.id, this.getParentId(t.id) + "/" + t.value)
		})
	},
	Lx : function(t, e, i) {
		for (var s = i ? "copy" : "move", n = [], a = 0; a < t.length; a++) {
			var r = this.move(t[a], 0, this, {
				parent : e,
				copy : i ? !0 : !1
			});
			n.push(r)
		}
		this.refreshCursor();
		var o = this.config.handlers[s];
		o && this.xx(o, {
			action : s,
			source : t.join(","),
			temp : n.join(","),
			target : e
		}, function(t, e) {
			if (e && webix.isArray(e))
				for (var i = t.temp.split(","), s = 0; s < e.length; s++)
					e[s].id && e[s].id != i[s] && this.data.pull[i[s]] && this.data.changeId(i[s], e[s].id)
		})
	},
	copyFile : function(t, e) {
		this.moveFile(t, e, !0)
	},
	moveFile : function(t, e, i) {
		var s, n, a;
		"string" == typeof t && ( t = t.split(",")), webix.isArray(t) || ( t = [t]), this.data.branch[e] || ( e = e ? this.getParentId(e) : this.getCursor()), a = !0;
		var r = [];
		for ( s = 0; s < t.length; s++)
			if ( n = t[s].toString(), a = a && this.wx(n, e)) {
				var o = this.Jx(this.config.templateName(this.getItem(n)), e, n);
				o && r.push(o)
			}
		a ? r.length ? webix.confirm({
			width : 300,
			height : 200,
			text : webix.i18n.filemanager.replaceConfirmation,
			ok : webix.i18n.filemanager.yes,
			cancel : webix.i18n.filemanager.no,
			callback : webix.bind(function(s) {
				s && this.deleteFile(r, function() {
					this.Lx(t, e, i ? !0 : !1)
				})
			}, this)
		}) : this.Lx(t, e, i ? !0 : !1) : this.callEvent( i ? "onCopyError" : "onMoveError", [])
	},
	deleteFile : function(t, e) {
		"string" == typeof t && ( t = t.split(",")), webix.isArray(t) || ( t = [t]);
		for (var i = 0; i < t.length; i++) {
			var s = t[i];
			s == this.getCursor() && this.setCursor(this.getFirstId()), s && this.remove(s)
		}
		this.refreshCursor();
		var n = this.config.handlers.remove;
		n ? this.xx(n, {
			action : "remove",
			source : t.join(",")
		}, webix.bind(e, this)) : e && e.call(this)
	},
	Mx : function(t, e) {
		this.add(t, 0, e);
		t.source = t.value, t.target = e, this.refreshCursor();
		var i = this.config.handlers.create;
		i && (t.action = "create", this.xx(i, t, function(t, e) {
			e.id && this.data.changeId(t.id, e.id)
		}))
	},
	createFolder : function(t) {
		if ("string" == typeof t && ( t = t.split(",")), webix.isArray(t) && ( t = t[0]), t) {
			t = "" + t;
			var e = this.getItem(t);
			this.data.branch[t] || "folder" == e.type || ( t = this.getParentId(t));
			var i = this.config.templateCreate(e), s = this.Jx(this.config.templateName(i), t);
			t = "" + t, s ? webix.confirm({
				width : 300,
				height : 200,
				text : webix.i18n.filemanager.createConfirmation,
				ok : webix.i18n.filemanager.yes,
				cancel : webix.i18n.filemanager.no,
				callback : webix.bind(function(e) {
					e && this.deleteFile(s, function() {
						this.Mx(i, t)
					})
				}, this)
			}) : this.Mx(i, t)
		}
	},
	editFile : function(t) {
		webix.isArray(t) && ( t = t[0]), this.getActiveView() && this.getActiveView().edit && this.getActiveView().edit(t)
	},
	Nx : function(t, e, i) {
		var s = this.getItem(t);
		i = i || "value", s[i] = e, this.refreshCursor(), this.callEvent("onFolderSelect", [this.getCursor()]);
		var n = this.config.handlers.rename;
		if (n) {
			var a = {
				source : t,
				action : "rename",
				target : e
			};
			this.xx(n, a, function(t, e) {
				e.id && this.data.changeId(t.source, e.id)
			})
		}
	},
	renameFile : function(t, e, i) {
		var s = this.Jx(e, this.getParentId(t), t);
		s ? webix.confirm({
			width : 300,
			height : 200,
			text : webix.i18n.filemanager.renameConfirmation,
			ok : webix.i18n.filemanager.yes,
			cancel : webix.i18n.filemanager.no,
			callback : webix.bind(function(n) {
				n ? this.deleteFile(s, function() {
					this.Nx(t, e, i)
				}) : this.refreshCursor()
			}, this)
		}) : this.Nx(t, e, i)
	},
	wx : function(t, e) {
		for (; e; ) {
			if (e == t || !this.data.branch[e])
				return !1;
			e = this.getParentId(e)
		}
		return !0
	},
	Ox : function(t) {
		this.Px = new Date, this.Qx || (this.Qx = webix.html.create("DIV", {
			"class" : "webix_fmanager_save_message"
		}, ""), this.x.style.position = "relative", webix.html.insertBefore(this.Qx, this.x)), this.Qx.innerHTML = t ? webix.i18n.filemanager.errorResponse : webix.i18n.filemanager.saving
	},
	Rx : function() {
		this.Qx && (webix.html.remove(this.Qx), this.Qx = null)
	},
	xx : function(t, e, i) {
		this.Ox(), webix.ajax().post(t, webix.copy(e), {
			success : webix.bind(function(t, s) {
				var n = this.data.driver.toObject(t, s);
				this.callEvent("onSuccessResponse", [e, n]), this.Rx(), i && i.call(this, e, n)
			}, this),
			error : webix.bind(function(t) {
				this.callEvent("onErrorResponse", [e, t]) && this.ix(e, t)
			}, this)
		})
	},
	getActiveView : function() {
		return this.dx || this.$$("tree") || null
	},
	getActive : function() {
		var t = this.$$(this.config.mode).getSelectedId(!0), e = [];
		if (webix.isArray(t))
			for (var i = 0; i < t.length; i++)
				e.push(t[i].toString());
		else
			e = t.toString();
		return e.length ? e : this.getCursor()
	},
	yx : function(t) {
		var t = t.toString(), e = this.getItem(t);
		this.data.branch[t] || "folder" == e.type ? this.callEvent("onBeforeLevelDown", [t]) && (this.setCursor(t), this.callEvent("onAfterLevelDown", [t])) : this.callEvent("onBeforeRun", [t]) && (this.download(t), this.callEvent("onAfterRun", [t]))
	},
	Bt : function(t, e, i) {
		var s = webix.UIManager.addHotKey(t, e, i);
		(i || this).attachEvent("onDestruct", function() {
			webix.UIManager.removeHotKey(s, e, i)
		})
	},
	ix : function() {
		var t = this.data.url;
		if (t) {
			var e = this.data.driver;
			this.Ox(!0);
			var i = this;
			webix.ajax().get(t, {
				success : function(s, n) {
					var a = e.toObject(s, n);
					a && ( a = e.getDetails(e.getRecords(a)), i.clearAll(), i.parse(a), i.data.url = t)
				},
				error : function() {
				}
			})
		}
	},
	ex : function(t) {
		var e = this.$$(t);
		this.data.attachEvent("onIdChange", function(t, i) {
			e.data.pull[t] && e.data.changeId(t, i)
		}), this.$$(t).data.qf = webix.bind(function(t) {
			var e = this.getItem(t.id);
			e && e.$count && (t.type = "folder")
		}, this), this.$$(t).type.icons = this.config.icons, this.$$(t).type.templateIcon = this.config.templateIcon, this.$$(t).type.templateName = this.config.templateName, this.$$(t).type.templateSize = this.config.templateSize, this.$$(t).type.templateDate = this.config.templateDate, this.$$(t).type.templateType = this.config.templateType, this.$$(t).attachEvent("onItemDblClick", webix.bind(this.yx, this)), this.data.attachEvent("onClearAll", webix.bind(function() {
			this.clearAll()
		}, this.$$(t))), this.$$(t).bind(this, "$data", webix.bind(function(e, i) {
			if (!e)
				return this.$$(t).clearAll();
			if (!this.$searchResults) {
				var s = [].concat(webix.copy(i.data.getBranch(e.id))).concat(e.files || []);
				this.$$(t).data.importData(s, !0)
			}
		}, this)), this.$$(t).attachEvent("onFocus", function() {
			webix.delay(function() {
				if (!this.getSelectedId()) {
					var t = this.getFirstId();
					t && this.select(t)
				}
				this.getTopParentView().dx = this, webix.html.removeCss(this.$view, "webix_blur")
			}, this, [], 100)
		}), this.$$(t).attachEvent("onBlur", function() {
			var t = this.getTopParentView();
			t.getMenu() && t.getMenu().isVisible() || webix.html.addCss(this.$view, "webix_blur")
		}), this.getMenu() && !this.config.readonly && (this.getMenu().attachTo(this.$$(t)), this.$$(t).attachEvent("onBeforeMenuShow", function(t) {
			for (var e = this.getSelectedId(!0), i = !1, s = 0; s < e.length && !i; s++)
				e[s].toString() == t.toString() && ( i = !0);
			return i || this.select(t.toString()), webix.UIManager.setFocus(this), !0
		})), this.$$(t).attachEvent("onBeforeEditStop", function(t, e) {
			return this.getTopParentView().callEvent("onBeforeEditStop", [e.id || e.row, t, e, this])
		}), this.$$(t).attachEvent("onAfterEditStop", function(t, e) {
			var i = this.getTopParentView();
			i.callEvent("onAfterEditStop", [e.id || e.row, t, e, this]) && i.renameFile(e.id || e.row, t.value)
		}), this.$$(t).attachEvent("onBeforeDrop", function(t) {
			var e = this.getTopParentView();
			return e.callEvent("onBeforeDrop", [t]) && t.from && e.moveFile(t.source, t.target), !1
		}), this.$$(t).attachEvent("onBeforeDrag", function(t, e) {
			var i = this.getTopParentView();
			return !i.config.readonly && i.callEvent("onBeforeDrag", [t, e])
		}), this.$$(t).attachEvent("onBeforeDragIn", function(t, e) {
			var i = this.getTopParentView();
			return !i.config.readonly && i.callEvent("onBeforeDragIn", [t, e])
		}), this.Bt("enter", webix.bind(function(t) {
			for (var e = t.getSelectedId(!0), i = 0; i < e.length; i++)
				this.yx(e[i]);
			if (webix.UIManager.setFocus(t), e = t.getSelectedId(!0), !e.length) {
				var s = t.getFirstId();
				s && t.select(s)
			}
		}, this), this.$$(t)), this.config.readonly && (this.$$(t).define("drag", !1), this.$$(t).define("editable", !1))
	},
	Rw : function() {
		var t = this.config.defaultSelection;
		return t ? t.call(this) : this.getFirstChildId(0)
	},
	qx : function(t, e) {
		var i = t.config || t;
		return "function" == typeof i ? i.call(this, e) : i
	},
	Pw : function(t) {
		var e, i, s = t.structure;
		if (s)
			for (i in s)
			if (s.hasOwnProperty(i)) {
				var e = webix.copy(s[i]);
				this.structure[i] && this.structure[i].config ? this.structure[i].config = e.config || e : this.structure[i] = e.config || e
			}
	},
	defaults : {
		modes : ["files", "table"],
		mode : "table",
		handlers : {},
		structure : {},
		templateName : webix.template("#value#"),
		templateSize : function(t) {
			for (var e = t.size, i = webix.i18n.filemanager.sizeLabels, s = 0; e / 1024 > 1; )
				e /= 1024, s++;
			var n = parseInt(e, 10) == e, a = webix.Number.numToStr({
				decimalDelimiter : webix.i18n.decimalDelimiter,
				groupDelimiter : webix.i18n.groupDelimiter,
				decimalSize : n ? 0 : webix.i18n.groupSize
			});
			return a(e) + "" + i[s]
		},
		templateType : function(t) {
			var e = webix.i18n.filemanager.types;
			return e && e[t.type] ? e[t.type] : t.type
		},
		templateDate : function(t) {
			var e = t.date;
			return "object" != typeof e && ( e = new Date(1e3 * parseInt(t.date, 10))), webix.i18n.fullDateFormatStr(e)
		},
		templateCreate : function() {
			return {
				value : "newFolder",
				type : "folder",
				date : new Date
			}
		},
		templateIcon : function(t, e) {
			return "<span class='webix_icon webix_fmanager_icon fa-" + (e.icons[t.type] || e.icons.file) + "'></span>"
		},
		uploadProgress : {
			type : "top",
			delay : 3e3,
			hide : !0
		},
		idChange : !0,
		icons : {
			folder : "folder",
			doc : "file-word-o",
			excel : "file-excel-o",
			pdf : "file-pdf-o",
			pp : "file-powerpoint-o",
			text : "file-text-o",
			video : "file-video-o",
			image : "file-image-o",
			code : "file-code-o",
			audio : "file-audio-o",
			archive : "file-archive-o",
			file : "file-o"
		}
	}
}, webix.FileManagerUpload, webix.FileManagerStructure, webix.ProgressBar, webix.IdSpace, webix.ui.layout, webix.TreeDataMove, webix.TreeDataLoader, webix.DataLoader, webix.EventSystem, webix.Settings);
