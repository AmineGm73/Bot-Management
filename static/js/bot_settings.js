const socket = io({autoConnect: true});

window.onload = () => {
    socket.emit("connect");
}