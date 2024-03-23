const socket = io({autoConnect: true});


function getProps() {
    let propsList = document.getElementById('props').getElementsByTagName('li');
    let propsDict = {};

    for (let i = 0; i < propsList.length; i++) {
        let prop = propsList[i];
        let propKey = prop.id;
        let input = prop.querySelector('input');
        let propValue = input.value;
        propsDict[propKey] = propValue.trim();
    }
    
    return propsDict;
}

function formatSecondsIntoTime(seconds) {
    if (seconds < 60) {
        return `${seconds}s`;
    } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}min ${remainingSeconds}s`;
    } else if (seconds < 86400) {
        const hours = Math.floor(seconds / 3600);
        const remainingMinutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${remainingMinutes}min`;
    } else {
        const days = Math.floor(seconds / 86400);
        const remainingHours = Math.floor((seconds % 86400) / 3600);
        return `${days}day ${remainingHours}h`;
    }
}

function redirectToMainRoute() {
    window.location.href = "/";
}

window.onload = () => {
    socket.emit("connect");
}

socket.on('runtime_update', function(data) {
    // Get the runtime value from the data
    let botName = window.location.href.split('/').pop();
    var runtime = data[botName];
    
    // Find the <h4> element with the class "runtime-txt"
    var runtimeElement = document.querySelector('.runtime-txt');
    
    // Change the value of the <h4> element
    if (runtimeElement) {
        runtimeElement.textContent = `Running for : ${formatSecondsIntoTime(runtime)}`;
    }
});

function sendData() {
    data = getProps();
    let botName = window.location.href.split('/').pop();
    data["bot_name"] = botName;
    socket.emit("saveData", data);

    alert("Bot Saved Successfuly!!!")
    redirectToMainRoute();
}