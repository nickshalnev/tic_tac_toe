const socket = io();

let player = prompt("Enter your player symbol (X/O):").toUpperCase();
while (player !== 'X' && player !== 'O') {
    player = prompt("Invalid input. Enter your player symbol (X/O):").toUpperCase();
}
let room = prompt("Enter room name:");
socket.emit('join', { room: room, player: player });

socket.on('join_error', (data) => {
    alert(data.message);
    player = prompt("Enter a different player symbol (X/O):").toUpperCase();
    while (player !== 'X' && player !== 'O') {
        player = prompt("Invalid input. Enter your player symbol (X/O):").toUpperCase();
    }
    socket.emit('join', { room: room, player: player });
});

socket.on('game_state', (data) => {
    updateBoard(data.board);
    if (data.turn) {
        document.getElementById('game-board').dataset.turn = data.turn;
        document.getElementById('turn-indicator').innerText = `Turn: ${data.turn}`;
    }
});

socket.on('game_over', (data) => {
    alert(`Game Over! Winner: ${data.winner}`);
    resetBoard();
});

socket.on('invalid_move', (data) => {
    alert(data.message);
});

function updateBoard(board) {
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            document.getElementById(`cell-${row}-${col}`).innerText = board[row][col];
        }
    }
}

function resetBoard() {
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            document.getElementById(`cell-${row}-${col}`).innerText = '';
        }
    }
    document.getElementById('turn-indicator').innerText = '';
}

document.getElementById('game-board').addEventListener('click', (event) => {
    if (event.target.tagName === 'TD') {
        let cell = event.target.id.split('-');
        let row = parseInt(cell[1]);
        let col = parseInt(cell[2]);
        let turn = document.getElementById('game-board').dataset.turn;
        if (turn === player) {
            socket.emit('make_move', { room: room, row: row, col: col, player: player });
        } else {
            alert("It's not your turn!");
        }
    }
});
