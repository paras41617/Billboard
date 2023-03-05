var socket = new WebSocket("wss://www.blockonomics.co/payment/"+ address);
socket.onmessage = function(event){
  response = JSON.parse(event.data);
    if (parseInt(response.status) > parseInt(status_))
    setTimeout(function(){window.location.reload() }, 1000); 
}

window.onbeforeunload = function() {
  // close the WebSocket connection
  socket.close();
  // or force close the connection
  socket.terminate();
};