# Tic-Tac-Toe

## Overview

It's a Tic-Tac-Toe game that allows two players to play against each other over the web.
Tech stack: Python with Flask for the backend, Flask-SocketIO for real-time communication, and a simple
HTML/JavaScript frontend.

## Structure

- **Backend**: Flask and Flask-SocketIO handle real-time communication and game logic.
- **Frontend**: HTML, CSS, and JavaScript handle the user interface.

## Game Flow

1. Joining the Game: Players join the game by specifying a room and their symbol ('X' or 'O').
2. Making Moves: Players take turns to make moves. The server checks the validity of each move and updates the game
   state accordingly.
3. Checking for Win Condition: After each move, the server checks if the move results in a win or a draw.
4. Real-time Updates: The game state is updated in real-time using Socket.IO, allowing both players to see the latest
   game state immediately.

### Checking for Win Condition

The win condition is checked by verifying if any row, column, or diagonal of the board contains the same symbol ('X'
or 'O'). If a player achieves this condition, they are declared the winner.

## How to Run

### Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO

### Server Side

### Creating virtual environment

To crete a virtual env, run:

```bash
python3 -m venv venv
```

and activate it with command:

```bash
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Installing Dependencies

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Server

To start the server, run:

```bash
python run.py
```

### Accessing the Game

Open a web browser and navigate to http://127.0.0.1:15239/ to start the game.

## Testing the Game

### Running Unit Tests

To run the unit tests, execute:

```bash
python -m unittest discover -s tests
```

