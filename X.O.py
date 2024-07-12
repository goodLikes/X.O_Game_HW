import tkinter as tk
from tkinter import messagebox
import random

def drawBoard(board):
    for i in range(1, 10):
        buttons[i].config(text=board[i], state="normal" if board[i] == ' ' else "disabled")

def choosePlayerLetter():
    global playerLetter, computerLetter
    playerLetter = player_var.get()
    computerLetter = 'O' if playerLetter == 'X' else 'X'

def whoGoesFirst():
    return 'computer' if random.randint(0, 1) == 0 else 'player'

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le) or
            (bo[7] == le and bo[5] == le and bo[3] == le) or
            (bo[9] == le and bo[5] == le and bo[1] == le))

def getBoardCopy(board):
    return board[:]

def isSpaceFree(board, move):
    return board[move] == ' '

def chooseRandomMoveFromList(board, movesList):
    possibleMoves = [move for move in movesList if isSpaceFree(board, move)]
    return random.choice(possibleMoves) if possibleMoves else None

def getComputerMove(board, computerLetter):
    if difficulty_var.get() == 'Легкий':
        return chooseRandomMoveFromList(board, [i for i in range(1, 10) if isSpaceFree(board, i)])
    elif difficulty_var.get() == 'Средний':
        playerLetter = 'O' if computerLetter == 'X' else 'X'
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, computerLetter, i)
                if isWinner(copy, computerLetter):
                    return i
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, playerLetter, i)
                if isWinner(copy, playerLetter):
                    return i
        return chooseRandomMoveFromList(board, [i for i in range(1, 10) if isSpaceFree(board, i)])
    else:
        playerLetter = 'O' if computerLetter == 'X' else 'X'
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, computerLetter, i)
                if isWinner(copy, computerLetter):
                    return i
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, playerLetter, i)
                if isWinner(copy, playerLetter):
                    return i
        move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
        if move is not None:
            return move
        if isSpaceFree(board, 5):
            return 5
        return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    return all(not isSpaceFree(board, i) for i in range(1, 10))

def playerMove(i):
    global turn, theBoard, gameIsPlaying, player_wins, computer_wins, ties
    if gameIsPlaying and turn == 'player':
        makeMove(theBoard, playerLetter, i)
        drawBoard(theBoard)
        if isWinner(theBoard, playerLetter):
            messagebox.showinfo("Крестики-нолики", "Поздравляем! Вы выиграли!")
            player_wins += 1
            updateScore()
            gameIsPlaying = False
        elif isBoardFull(theBoard):
            messagebox.showinfo("Крестики-нолики", "Ничья!")
            ties += 1
            updateScore()
            gameIsPlaying = False
        else:
            turn = 'computer'
            computerMove()

def computerMove():
    global turn, theBoard, gameIsPlaying, player_wins, computer_wins, ties
    if gameIsPlaying and turn == 'computer':
        move = getComputerMove(theBoard, computerLetter)
        makeMove(theBoard, computerLetter, move)
        drawBoard(theBoard)
        if isWinner(theBoard, computerLetter):
            messagebox.showinfo("Крестики-нолики", "Компьютер выиграл! Вы проиграли.")
            computer_wins += 1
            updateScore()
            gameIsPlaying = False
        elif isBoardFull(theBoard):
            messagebox.showinfo("Крестики-нолики", "Ничья!")
            ties += 1
            updateScore()
            gameIsPlaying = False
        else:
            turn = 'player'

def updateScore():
    score_label.config(text=f"Игрок: {player_wins}  Компьютер: {computer_wins}  Ничья: {ties}")

def resetGame():
    global theBoard, turn, gameIsPlaying
    theBoard = [' '] * 10
    choosePlayerLetter()
    turn = whoGoesFirst()
    drawBoard(theBoard)
    if turn == 'computer':
        computerMove()
    gameIsPlaying = True

app = tk.Tk()
app.title("Крестики-нолики")

player_var = tk.StringVar(value='X')
difficulty_var = tk.StringVar(value='Легкий')
player_wins = 0
computer_wins = 0
ties = 0
gameIsPlaying = False  # Объявляем глобальную переменную здесь

tk.Label(app, text="Выберите букву:").grid(row=0, column=0)
tk.Radiobutton(app, text="X", variable=player_var, value='X').grid(row=0, column=1)
tk.Radiobutton(app, text="O", variable=player_var, value='O').grid(row=0, column=2)

tk.Label(app, text="Сложность:").grid(row=1, column=0)
tk.Radiobutton(app, text="Легкий", variable=difficulty_var, value='Легкий').grid(row=1, column=1)
tk.Radiobutton(app, text="Средний", variable=difficulty_var, value='Средний').grid(row=1, column=2)
tk.Radiobutton(app, text="Тяжелый", variable=difficulty_var, value='Тяжелый').grid(row=1, column=3)

buttons = [None] * 10
for i in range(1, 10):
    buttons[i] = tk.Button(app, text=' ', font=('normal', 20), width=5, height=2, command=lambda i=i: playerMove(i))
    buttons[i].grid(row=(i-1)//3 + 2, column=(i-1)%3)

score_label = tk.Label(app, text="Игрок: 0  Компьютер: 0  Ничья: 0")
score_label.grid(row=5, column=0, columnspan=4)

tk.Button(app, text='Сброс', command=resetGame).grid(row=6, column=0, columnspan=4)

resetGame()
app.mainloop()
