import tkinter as tk
import random

# กำหนดค่าต่าง ๆ
WIDTH, HEIGHT = 400, 500
BIRD_SIZE = 20
PIPE_WIDTH = 60
PIPE_GAP = 180
PIPE_HEIGHT_RANGE = (100, 300)
GRAVITY = 2
FLAP_STRENGTH = -15
PIPE_SPEED = 5

class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()
        
        self.init_game()
        
        self.root.bind("<space>", self.flap)
        self.root.bind("r", self.restart_game)
        
    def init_game(self):
        """ รีเซ็ตค่าเริ่มต้นของเกม """
        self.canvas.delete("all")  # ลบทุกอย่างบนจอ
        self.bird = self.canvas.create_oval(50, HEIGHT//2, 50 + BIRD_SIZE, HEIGHT//2 + BIRD_SIZE, fill="yellow")
        self.pipes = []
        self.bird_velocity = 0
        self.game_over = False
        self.score = 0
        self.score_text = self.canvas.create_text(WIDTH//2, 30, text=f"Score: {self.score}", fill="black", font=("Arial", 16, "bold"))

        # เริ่มสร้างท่อใหม่
        self.pipe_after_id = self.root.after(2000, self.create_pipe)
        self.update()
        
    def create_pipe(self):
        if self.game_over:
            return
        gap_y = random.randint(PIPE_HEIGHT_RANGE[0], HEIGHT - PIPE_GAP - PIPE_HEIGHT_RANGE[0])
        top_pipe = self.canvas.create_rectangle(WIDTH, 0, WIDTH + PIPE_WIDTH, gap_y, fill="green")
        bottom_pipe = self.canvas.create_rectangle(WIDTH, gap_y + PIPE_GAP, WIDTH + PIPE_WIDTH, HEIGHT, fill="green")
        self.pipes.append((top_pipe, bottom_pipe, False))  # False = ยังไม่ได้เพิ่มคะแนน
        self.pipe_after_id = self.root.after(2000, self.create_pipe)  # สร้างท่อใหม่ทุก 2 วินาที
        
    def flap(self, event):
        if not self.game_over:
            self.bird_velocity = FLAP_STRENGTH
    
    def update(self):
        if self.game_over:
            return
        
        # อัปเดตความเร็วของนก (แรงโน้มถ่วง)
        self.bird_velocity += GRAVITY
        self.canvas.move(self.bird, 0, self.bird_velocity)
        
        # ตรวจสอบการชนกับพื้นหรือเพดาน
        x1, y1, x2, y2 = self.canvas.coords(self.bird)
        if y1 <= 0 or y2 >= HEIGHT:
            self.end_game()
            return
        
        # อัปเดตตำแหน่งของท่อ
        for i, (top_pipe, bottom_pipe, passed) in enumerate(self.pipes):
            self.canvas.move(top_pipe, -PIPE_SPEED, 0)
            self.canvas.move(bottom_pipe, -PIPE_SPEED, 0)
            
            px1, py1, px2, py2 = self.canvas.coords(top_pipe)
            bx1, by1, bx2, by2 = self.canvas.coords(bottom_pipe)
            
            # ตรวจสอบการชนกับท่อ
            if (x2 > px1 and x1 < px2 and (y1 < py2 or y2 > by1)):
                self.end_game()
                return
            
            # เพิ่มคะแนนเมื่อผ่านท่อไปได้
            if not passed and x1 > px2:
                self.pipes[i] = (top_pipe, bottom_pipe, True)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        
        self.root.after(50, self.update)
        
    def end_game(self):
        self.game_over = True
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over", fill="red", font=("Arial", 24, "bold"))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 30, text="Press 'R' to Restart", fill="red", font=("Arial", 16, "bold"))
    
    def restart_game(self, event=None):
        """ รีสตาร์ทเกมโดยเคลียร์ท่อเก่าและเริ่มใหม่ """
        self.root.after_cancel(self.pipe_after_id)  # ยกเลิกการสร้างท่อเก่าที่ค้างอยู่
        self.init_game()

root = tk.Tk()
FlappyBirdGame(root)
root.mainloop()
