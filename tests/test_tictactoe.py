import unittest
import logging
from flask import Flask
from flask_testing import TestCase
from app import create_app, socketio
from flask_socketio import SocketIOTestClient

logger = logging.getLogger(__name__)

class TestTicTacToe(TestCase):

    def create_app(self):
        logger.info("Creating Flask test application...")
        app = create_app()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'secret!'
        return app

    def setUp(self):
        logger.info("Setting up test case...")
        self.client = socketio.test_client(self.app)

    def tearDown(self):
        logger.info("Tearing down test case...")
        self.client.disconnect()

    def test_join_game(self):
        logger.info("Testing joining game...")
        self.client.emit('join', {'room': 'test_room', 'player': 'X'})
        received = self.client.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['name'], 'game_state')
        game_state = received[0]['args'][0]
        self.assertEqual(game_state['turn'], 'X')

    def test_join_game_symbol_taken(self):
        logger.info("Testing joining game with symbol already taken...")
        self.client.emit('join', {'room': 'test_room', 'player': 'X'})
        self.client.emit('join', {'room': 'test_room', 'player': 'X'})
        received = self.client.get_received()
        self.assertEqual(len(received), 2)
        self.assertEqual(received[1]['name'], 'join_error')
        join_error = received[1]['args'][0]
        self.assertEqual(join_error['message'], 'This symbol is already taken. Choose another one.')

    def test_make_move(self):
        logger.info("Testing making a move...")
        self.client.emit('join', {'room': 'test_room', 'player': 'X'})
        self.client.emit('join', {'room': 'test_room', 'player': 'O'})
        self.client.emit('make_move', {'room': 'test_room', 'row': 0, 'col': 0, 'player': 'X'})
        received = self.client.get_received()
        self.assertEqual(len(received), 3)
        self.assertEqual(received[2]['name'], 'game_state')
        game_state = received[2]['args'][0]
        self.assertEqual(game_state['board'][0][0], 'X')
        self.assertEqual(game_state['turn'], 'O')

    def test_win_condition(self):
        logger.info("Testing win condition...")
        self.client.emit('join', {'room': 'test_room', 'player': 'X'})
        self.client.emit('join', {'room': 'test_room', 'player': 'O'})
        moves = [(0, 0, 'X'), (1, 0, 'O'), (0, 1, 'X'), (1, 1, 'O'), (0, 2, 'X')]
        for row, col, player in moves:
            self.client.emit('make_move', {'room': 'test_room', 'row': row, 'col': col, 'player': player})

        received = self.client.get_received()
        self.assertEqual(len(received), 6)
        self.assertEqual(received[-1]['name'], 'game_over')
        game_over = received[-1]['args'][0]
        self.assertEqual(game_over['winner'], 'X')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()
