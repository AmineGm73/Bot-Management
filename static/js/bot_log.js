const socket = io({autoConnect: true});

// Function to update PrismJS and its dependencies
function update() {
    // Clone the first script tag
    var codeToolBarElement = document.querySelector(".code-toolbar")
    var originalScriptTag = document.querySelector('script');
    var clonedScriptTag = originalScriptTag.cloneNode(true);
    // Extract the src attribute
    var scriptSrc = clonedScriptTag.getAttribute('src');

    // Modify the src attribute to load PrismJS
    clonedScriptTag.setAttribute('src', '/static/js/prism.js');

    let logElement = codeToolBarElement.querySelector("language-log");
    var newLogElement = logElement.cloneNode(true);
    logElement.parentNode.replaceChild(newLogElement, logElement);

    // Replace the original script tag with the modified cloned script tag
    originalScriptTag.parentNode.replaceChild(clonedScriptTag, originalScriptTag);
}

  // Socket.io event listener
socket.on('log_update', function(data) {
    // Code to be executed when 'log_update' event is received
    let botName = window.location.href.split('/').pop();
    document.querySelector(".language-log").innerHTML = data[botName];
    update();
});
window.onload = () => {
    console.log("Loaded!!");
}
