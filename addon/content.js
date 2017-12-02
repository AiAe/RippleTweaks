$(document).ready(function () {
        var url = window.location.href;
        var user_id = url.split('/')[4].split('?')[0];
        var mode = url.split('=')[1];

        var dark = false;
        var c = document.cookie.split(" ");
        for (var i = 0; i < c.length; i++)
            if (c[i].startsWith("cflags"))
                dark = c[i].split("=")[1].startsWith("1");

        var modes = [
            {mode: 0, visible: mode === '0'},
            {mode: 1, visible: mode === '1'},
            {mode: 2, visible: mode === '2'},
            {mode: 3, visible: mode === '3'}
        ];

        for(var m of modes)
            $(`<div class='ui raised segment twemoji' id='userpage-content' data-mode='${m.mode}' ${!m.visible ? 'hidden':'visible'}><iframe frameBorder='0' scrolling='no' width='100%' height='400px' src='https://rippletweaks.aiae.ovh/${user_id}/${m.mode}/${dark}/'></iframe></div>`).insertAfter( "#mode-menu" );
    });