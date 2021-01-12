if ('WebSocket' in window) {
    var protocol = window.location.protocol === 'http:' ? 'ws://' : 'wss://';
    var address = protocol + window.location.host + '/ws';
    var socket = new WebSocket(address);
    socket.onmessage = function (msg) {
        if (msg.data == 'reload') {
            window.location.reload();
            console.log("Reload message relayed.")
        }
    };
    if (sessionStorage && !sessionStorage.getItem('WutchInitialized')) {
        console.log('Wutch is enabled.');
        sessionStorage.setItem('WutchInitialized', true);
    }
}
else {
    console.log('This browser does not support WebSocket technology required for live reloading. Falling back to HTTP fetch requests.');
}