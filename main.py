# Importing required modules 
import os
import random
import telebot

# Creating a bot instance with the token
BOT_TOKEN = '00000#dsifa1335kfks5063283djsfja583743'
bot = telebot.TeleBot(BOT_TOKEN)
# Creating a 2D array for the board
board = [['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-']]

# Defining the players and their marks
players = ['X', 'O']
turn = random.choice(players) # Randomly choosing the first player

# Defining a function to check if the board is full
def is_full(board):
    for row in board:
        for cell in row:
            if cell == '-':
                return False
    return True

# Defining a function to check if a player has won
def has_won(board, mark):
    # Checking rows
    for row in board:
        if row.count(mark) == 3:
            return True
    # Checking columns
    for i in range(3):
        col = [row[i] for row in board]
        if col.count(mark) == 3:
            return True
    # Checking diagonals
    diag1 = [board[i][i] for i in range(3)]
    diag2 = [board[i][2-i] for i in range(3)]
    if diag1.count(mark) == 3 or diag2.count(mark) == 3:
        return True
    # No win condition met
    return False

# Defining a function to display the board
def display_board(board, chat_id):
    # Using emojis to represent the board and the marks
    symbols = {'-': '⬜️', 'X': '❌', 'O': '⭕️'}
    # Creating a string with the board
    board_str = ''
    for row in board:
        for cell in row:
            board_str += symbols[cell]
        board_str += '\n'
    # Sending the board to the chat
    bot.send_message(chat_id, board_str)

# Defining a function to handle user input
def handle_input(message):
    global turn, board
    chat_id = message.chat.id # Getting the chat id
    user_id = message.from_user.id # Getting the user id
    user_input = message.text # Getting the user input
    
    # Validating the user input
    if user_input.isdigit(): # Checking if it is a number
        user_input = int(user_input)
        if 1 <= user_input <= 9: # Checking if it is in range
            row = (user_input - 1) // 3 # Calculating the row index
            col = (user_input - 1) % 3 # Calculating the column index
            if board[row][col] == '-': # Checking if the position is empty
                # Updating the board with the user input
                board[row][col] = turn 
                # Displaying the updated board
                display_board(board, chat_id)
                # Checking if the game is over
                if has_won(board, turn): # Checking if the player has won
                    bot.send_message(chat_id, f'Player {turn} has won! 🎉')
                    reset_game() # Resetting the game
                elif is_full(board): # Checking if the board is full
                    bot.send_message(chat_id, 'The game is a tie! 😐')
                    reset_game() # Resetting the game
                else: # The game is not over
                    # Switching the turn to the other player
                    turn = 'O' if turn == 'X' else 'X'
                    bot.send_message(chat_id, f"It's {turn}'s turn.")
            else: # The position is not empty
                bot.send_message(chat_id, 'That position is already taken. Please choose another one.')
        else: # The input is not in range
            bot.send_message(chat_id, 'Please enter a number between 1 and 9.')
    else: # The input is not a number
        bot.send_message(chat_id, 'Please enter a valid number.')

# Defining a function to reset the game
def reset_game():
    global board, turn
    # Clearing the board
    board = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]
    # Randomly choosing the first player
    turn = random.choice(players)

# Setting up the command handler for /start
@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id # Getting the chat id
    bot.send_message(chat_id, 'Welcome to Tic-Tac-Toe!') # Sending a welcome message
    bot.send_message(chat_id, f'Player X is {turn}.') # Sending the first player's mark
    display_board(board, chat_id) # Displaying the initial board
    bot.send_message(chat_id, f"It's {turn}'s turn. Please enter a number between 1 and 9 to make a move.") # Prompting the user to enter a number

# Setting up the message handler for user input
@bot.message_handler(func=lambda msg: True)
def get_input(message):
    handle_input(message) # Calling the handle_input function

# Running the bot
bot.polling()
