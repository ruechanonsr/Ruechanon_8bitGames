import tkinter as tk

def check_winner():
    for row in board:
        if row[0]["text"] == row[1]["text"] == row[2]["text"] != "":
            highlight_winner(row)
            update_status(f"{row[0]['text']} Wins!")
            return True
    
    for col in range(3):
        if board[0][col]["text"] == board[1][col]["text"] == board[2][col]["text"] != "":
            highlight_winner([board[i][col] for i in range(3)])
            update_status(f"{board[0][col]['text']} Wins!")
            return True
    
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] != "":
        highlight_winner([board[0][0], board[1][1], board[2][2]])
        update_status(f"{board[0][0]['text']} Wins!")
        return True
    
    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] != "":
        highlight_winner([board[0][2], board[1][1], board[2][0]])
        update_status(f"{board[0][2]['text']} Wins!")
        return True
    
    if all(board[r][c]["text"] != "" for r in range(3) for c in range(3)):
        update_status("It's a draw!")
        return True
    
    return False

def highlight_winner(buttons):
    for btn in buttons:
        btn.config(bg="#90EE90")  # Light green background for winning buttons

def on_click(row, col):
    global current_player, game_over
    if board[row][col]["text"] == "" and not game_over:
        board[row][col]["text"] = current_player
        board[row][col].config(fg="#1E90FF" if current_player == "X" else "#FF4500")
        if check_winner():
            game_over = True
            return
        current_player = "O" if current_player == "X" else "X"
        update_status(f"{current_player}'s turn")

def reset_game():
    global current_player, game_over
    current_player = "X"
    game_over = False
    for row in board:
        for btn in row:
            btn.config(text="", bg="#E6E6FA", fg="black")
    update_status("X's turn")

def update_status(text):
    status_label.config(text=text)

root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("620x660")
root.configure(bg="#D3D3D3")

current_player = "X"
game_over = False
board = [[None, None, None] for _ in range(3)]

for r in range(3):
    for c in range(3):
        board[r][c] = tk.Button(root, text="", font=("Arial", 36, "bold"), width=6, height=2, bg="#E6E6FA",
                                command=lambda r=r, c=c: on_click(r, c))
        board[r][c].grid(row=r, column=c, padx=8, pady=8)

status_label = tk.Label(root, text="X's turn", font=("Arial", 20, "bold"), bg="#D3D3D3")
status_label.grid(row=3, column=0, columnspan=3, pady=10)

restart_button = tk.Button(root, text="Restart", font=("Arial", 20, "bold"), command=reset_game, bg="#FFB6C1", fg="black", padx=10, pady=5)
restart_button.grid(row=4, column=0, columnspan=3, pady=15)

root.mainloop()
