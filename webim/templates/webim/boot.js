var _IMC = {
	version: 'v5.4.2',
    product: 'django',
	path: '',
	is_login: '1',
    is_visitor: false,
	login_options: "",
	user: '',
	setting: {},
	menu: "",
	enable_chatlink: true,
	enable_shortcut: true,
	enable_menu: '',
	discussion: true,
	enable_room: true,
	enable_noti: true,
	theme: 'base',
	local: 'zh-CN',
	upload: false,
	show_unavailable: true,
	jsonp: '',
	min: ''
};

_IMC.script = window.webim ? '' : ('<link href="' + _IMC.path + '/static/webim/webim' + _IMC.min + '.css?' + _IMC.version + '" media="all" type="text/css" rel="stylesheet"/><link href="' + _IMC.path + '/static/webim/themes/' + _IMC.theme + '/jquery.ui.theme.css?' + _IMC.version + '" media="all" type="text/css" rel="stylesheet"/><script src="' + _IMC.path + '/static/webim/webim' + _IMC.min + '.js?' + _IMC.version + '" type="text/javascript"></script><script src="' + _IMC.path + '/static/webim/i18n/webim-' + _IMC.local + '.js?' + _IMC.version + '" type="text/javascript"></script>');
_IMC.script += '<script src="' + _IMC.path + '/static/webim/webim.' + _IMC.product + '.js?' + _IMC.version + '" type="text/javascript"></script>';

document.write( _IMC.script );

