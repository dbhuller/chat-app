document.addEventListener('DOMContentLoaded', () => {
    var socket = io();

    let room = 'General';
    joinRoom("General")

    // Display incoming messages from users
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span')
        const br = document.createElement('br');

        // if data contians username, display username, timestamp and message (not system message)
        if (data.username) {
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        // else display system message for user leaving/joining room
        } else {
            printSysMsg(data.msg);
        }
        
    });


    // Send message text
    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector('#user_message').value, 'username': username, 'room': room });
        // Clear input area 
        document.querySelector('#user_message').value = "";
        // Autofocus on textbox --> doesnt seem to work
        document.querySelector('#user_message').focus();
    };

    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in the ${room} room.`;
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });

    // Leave room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

    // Join room
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
        // Clear room message area
        document.querySelector('#display-message-section').innerHTML = '';
    }

    // Print system messages
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }
})