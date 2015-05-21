/*!
 * WebIM for Flask @VERSION
 * http://nextalk.im
 *
 * Copyright (c) 2013 NexTalk.IM
 *
 * Released under the MIT, BSD, and GPL Licenses.
 */
(function(webim) {
	var path = _IMC.path;
	webim.extend(webim.setting.defaults.data, _IMC.setting);
    var cookie_key = "_webim_cookie_";
	if( _IMC.is_visitor ) { cookie_key = "_webim_v_cookie_"; }
    if( _IMC.user != "" ) { cookie_key = cookie_key + _IMC.user.id; }
    webim.status.defaults.key = cookie_key;
	//configure api routes
	webim.route( {
		online: path + "/webim/online",
		offline: path + "/webim/offline",
		deactivate: path + "/webim/refresh",
		message: path + "/webim/message",
		presence: path + "/webim/presence",
		status: path + "/webim/status",
		setting: path + "/webim/setting",
		history: path + "/webim/history",
		clear: path + "/webim/history/clear",
		download: path + "/webim/history/download",
		buddies: path + "/webim/buddies",
        //room actions
		invite: path + "/webim/room/invite",
		join: path + "/webim/room/join",
		leave: path + "/webim/room/leave",
		block: path + "/webim/room/block",
		unblock: path + "/webim/room/unblock",
		members: path + "/webim/room/members",
        //notifications
		notifications: path + "/webim/notifications",
        //upload files
		upload: path + "/webim/upload"
	} );

	//configure emotion icons
	webim.ui.emot.init({"dir": path + "/static/webim/images/emot/default"});

	//configure sound mp3
	var soundUrls = {
		lib: path + "/static/webim/assets/sound.swf",
		msg: path + "/static/webim/assets/sound/msg.mp3"
	};

	//configure ui
	var ui = new webim.ui(document.body, {
		imOptions: {
			jsonp: _IMC.jsonp
		},
		soundUrls: soundUrls,
		//layout: "layout.popup",
        layoutOptions: {
            unscalable: _IMC.is_visitor,
            //detachable: true, //true
	    maximizable: true
        },
		buddyChatOptions: {
            downloadHistory: !_IMC.is_visitor,
			//simple: _IMC.is_visitor,
			upload: _IMC.upload && !_IMC.is_visitor
		},
		roomChatOptions: {
            downloadHistory: !_IMC.is_visitor,
			upload: _IMC.upload
		}
	}), im = ui.im;
    //全局化
    window.webimUI = ui;

	if( _IMC.user ) im.setUser( _IMC.user );
	if( _IMC.menu ) ui.addApp("menu", { "data": _IMC.menu } );
	if( _IMC.enable_shortcut ) ui.layout.addShortcut( _IMC.menu );

	//configure buddy list
	ui.addApp("buddy", {
		showUnavailable: _IMC.show_unavailable,
		is_login: _IMC['is_login'],
		disable_login: true,
		collapse: false,
		//disable_user: _IMC.is_visitor,
        //simple: _IMC.is_visitor,
		loginOptions: _IMC['login_options']
	});
    if(!_IMC.is_visitor) {
        if( _IMC.enable_room )ui.addApp("room", { discussion: (_IMC.discussion && !_IMC.is_visitor) });
        if(_IMC.enable_noti )ui.addApp("notification");
    }
    if(_IMC.enable_chatbtn) {
        ui.addApp("chatbtn", {
            elmentId: null,
            chatbox: true,
            classRe: /webim-chatbtn/,
            hrefRe: [/chatbox\/(\d+)$/i]
        });
        //ui.addApp("chatbtn");
    }
    //if(_IMC.enable_chatlink) ui.addApp("chatbtn");
    ui.addApp("setting", {"data": webim.setting.defaults.data, "copyright": true});
    //render
	ui.render();
	//online
	_IMC['is_login'] && im.autoOnline() && im.online();
})(webim);
