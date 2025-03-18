import tkinter as tk
import random

# กำหนดค่าต่าง ๆ
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 20
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BG_COLOR = "lightgreen"
TEXT_COLOR = "red"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()
        
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.spawn_food()
        self.direction = "Right"
        self.game_over = False
        self.text_id = None  # ใช้เก็บข้อความ Game Over
        
        self.root.bind("<KeyPress>", self.change_direction)
        self.root.bind("r", self.restart_game)
        self.update()
    
    def spawn_food(self):
        while True:
            x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            if (x, y) not in self.snake:
                return x, y
    
    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if event.keysym != opposites[self.direction]:
                self.direction = event.keysym
    
    def move(self):
        if self.game_over:
            return
        
        x, y = self.snake[0]
        if self.direction == "Up":
            y -= GRID_SIZE
        elif self.direction == "Down":
            y += GRID_SIZE
        elif self.direction == "Left":
            x -= GRID_SIZE
        elif self.direction == "Right":
            x += GRID_SIZE
        
        new_head = (x, y)
        
        if new_head in self.snake or x < 0 or y < 0 or x >= WIDTH or y >= HEIGHT:
            self.game_over = True
            self.display_game_over()
            return
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.food = self.spawn_food()
        else:
            self.snake.pop()
    
    def update(self):
        self.canvas.delete("all")
        
        if not self.game_over:
            self.move()
            
            for x, y in self.snake:
                self.canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=SNAKE_COLOR, outline="black")
            
            fx, fy = self.food
            self.canvas.create_oval(fx, fy, fx + GRID_SIZE, fy + GRID_SIZE, fill=FOOD_COLOR, outline="black")
            
            self.root.after(100, self.update)
        else:
            self.display_game_over()
    
    def display_game_over(self):
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over", fill=TEXT_COLOR, font=("Arial", 24, "bold"))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 30, text="Press 'R' to Restart", fill=TEXT_COLOR, font=("Arial", 16, "bold"))
    
    def restart_game(self, event=None):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.food = self.spawn_food()
        self.direction = "Right"
        self.game_over = False
        self.update()

root = tk.Tk()
SnakeGame(root)
root.mainloop()
