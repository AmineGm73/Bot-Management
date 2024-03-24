const socket = io({autoConnect: true});
var scrolled = false;

// Function to update PrismJS and its dependencies
function update() {
    Prism.plugins.autoloader.languages_path = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.25.0/components/';
    Prism.plugins.autoloader.use_minified = true;
    Prism.highlightAll(); // Reapply Prism.js highlighting after updating log data
}

// Socket.io event listener
socket.on('log_update', function(data) {
    // Code to be executed when 'log_update' event is received
    let botName = window.location.href.split('/').pop();
    document.getElementById("logs").innerHTML = data[botName];
    update();
    if (scrolled) {
        return;
    }
    var container = document.querySelector(".container"); // Replace ".container" with your actual container class or ID
    container.scrollTop = container.scrollHeight;
    scrolled = true;
});

window.onload = () => {
    console.log("Loaded!!");
    scrolled = false;
}
