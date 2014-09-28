var form = document.getElementById("chat_form");
var text_input = document.getElementById("chat_input_text");
var chat_list = document.getElementById("chat_list");
var chatSocket

var create_socket = function create_socket(){
    if (chatSocket){chatSocket.close()}
    var websocket_url = "ws://" + window.location.hostname +
        ":" + window.location.port + "/chat/websocket";
    chatSocket = new WebSocket(websocket_url);
    chatSocket.onopen = function (event) {
        console.log("WebSocket creado");
        form.addEventListener("submit", function(event){
            event.preventDefault();
            var msg  = {
                type:"message",
                text: text_input.value,
            };
            if(text_input.value)
            {chatSocket.send(JSON.stringify(msg));}
            text_input.value = "";
            return false;
        }, false);
    }

    chatSocket.onmessage = function(event){
        console.log("Mensaje Recibido!");
        var data = JSON.parse(event.data);
        console.log(data);
        var first_child = chat_list.firstChild;
        switch(data.type){
        case "message":
            item = document.createElement("li");
            item.innerHTML = data.rendered_text;
            if(first_child)
            {chat_list.insertBefore(item, first_child);}
            else
            {chat_list.appendChild(item);}
            break;
        }
    }

    chatSocket.onerror = function(event){
        console.log("WebSocket Error");
        setTimeout(create_socket, 3000);
    }
}

console.log("Js ejecutado");
create_socket();
