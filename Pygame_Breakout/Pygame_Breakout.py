import tkinter as tk
import random

# ค่าต่าง ๆ ของเกม
WIDTH, HEIGHT = 500, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 80, 10
BALL_SIZE = 15
BRICK_ROWS, BRICK_COLUMNS = 5, 8
BRICK_WIDTH = WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 20
BALL_SPEED = 3

class BreakoutGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Atari Breakout")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        
        self.paddle = self.canvas.create_rectangle(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT - 40,
                                                   WIDTH//2 + PADDLE_WIDTH//2, HEIGHT - 30, fill="white")
        
        self.ball = self.canvas.create_oval(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2,
                                            WIDTH//2 + BALL_SIZE//2, HEIGHT//2 + BALL_SIZE//2, fill="red")
        
        self.bricks = []
        self.create_bricks()
        
        self.ball_dx = BALL_SPEED * random.choice([-1, 1])
        self.ball_dy = -BALL_SPEED
        
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("r", self.restart_game)
        self.running = True
        self.update()
    
    def create_bricks(self):
        colors = ["blue", "green", "yellow", "orange", "red"]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                x1, y1 = col * BRICK_WIDTH, row * BRICK_HEIGHT
                x2, y2 = x1 + BRICK_WIDTH, y1 + BRICK_HEIGHT
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row], outline="white")
                self.bricks.append(brick)
    
    def move_left(self, event):
        if self.canvas.coords(self.paddle)[0] > 0:
            self.canvas.move(self.paddle, -20, 0)
    
    def move_right(self, event):
        if self.canvas.coords(self.paddle)[2] < WIDTH:
            self.canvas.move(self.paddle, 20, 0)
    
    def update(self):
        if not self.running:
            return
        
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)
        
        if x1 <= 0 or x2 >= WIDTH:
            self.ball_dx *= -1
        if y1 <= 0:
            self.ball_dy *= -1
        
        paddle_coords = self.canvas.coords(self.paddle)
        if y2 >= paddle_coords[1] and paddle_coords[0] <= x1 <= paddle_coords[2]:
            self.ball_dy *= -1
        
        for brick in self.bricks:
            bx1, by1, bx2, by2 = self.canvas.coords(brick)
            if bx1 < x2 and bx2 > x1 and by1 < y2 and by2 > y1:
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_dy *= -1
                break
        
        if y2 >= HEIGHT:
            self.running = False
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over", fill="red", font=("Arial", 24, "bold"))
            self.canvas.create_text(WIDTH//2, HEIGHT//2 + 30, text="Press 'R' to Restart", fill="white", font=("Arial", 16, "bold"))
        elif not self.bricks:
            self.running = False
            self.canvas.create_text(WIDTH//2, HEIGHT//2, text="You Win!", fill="green", font=("Arial", 24, "bold"))
            self.canvas.create_text(WIDTH//2, HEIGHT//2 + 30, text="Press 'R' to Restart", fill="white", font=("Arial", 16, "bold"))
        else:
            self.root.after(16, self.update)
    
    def restart_game(self, event):
        self.canvas.delete("all")
        self.paddle = self.canvas.create_rectangle(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT - 40,
                                                   WIDTH//2 + PADDLE_WIDTH//2, HEIGHT - 30, fill="white")
        self.ball = self.canvas.create_oval(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2,
                                            WIDTH//2 + BALL_SIZE//2, HEIGHT//2 + BALL_SIZE//2, fill="red")
        self.bricks = []
        self.create_bricks()
        self.ball_dx = BALL_SPEED * random.choice([-1, 1])
        self.ball_dy = -BALL_SPEED
        self.running = True
        self.update()

root = tk.Tk()
BreakoutGame(root)
root.mainloop()
