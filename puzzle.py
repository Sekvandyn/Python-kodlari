# puzzle oyunu ile yüklediğiniz fotoğraf istediğiniz sayıda parçaya bölünüp karıştırılır ve parçalar tekrar doğru yere gelip kontrol et tuşuna basıldığında sana sonucu gösyterir

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import time


DIFFICULTY_LEVELS = {
    "Kolay (2x2)": 2,
    "Orta (3x3)": 3,
    "Zor (4x4)": 4,
    "Çok Zor (5x5)": 5
}

class PuzzlePiece(tk.Label):
    def __init__(self, master, app, image, correct_pos, grid_pos, **kwargs):
        super().__init__(master, image=image, **kwargs)
        self.app = app
        self.image = image
        self.correct_pos = correct_pos
        self.grid_pos = grid_pos
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_click(self, event):
        self.lift()
        self.app.dragged_piece = self

    def on_release(self, event):
        target = self.app.get_piece_at(event.x_root, event.y_root)
        if target and target != self:
            self.grid_pos, target.grid_pos = target.grid_pos, self.grid_pos
            self.app.update_piece_positions()
            self.app.increment_moves()

class PuzzleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Puzzle Oyunu")
        self.geometry("360x500")
        self.pieces = []
        self.dragged_piece = None
        self.start_time = None
        self.move_count = 0
        self.puzzle_size = None

        
        self.info_label = tk.Label(self, text="Süre: 00:00 | Hamle: 0", font=("Arial", 12))
        self.info_label.pack(pady=5)

        
        self.load_button = tk.Button(self, text="Görsel Yükle", command=self.load_image)
        self.load_button.pack(pady=10)

       
        self.frame = tk.Frame(self, width=300, height=300, bg="lightgray")
        self.frame.pack()

        self.check_button = None
        self.difficulty_menu = None
        self.start_button = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Resimler", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return

        self.image_path = file_path
        self.load_button.destroy()

        # Zorluk seçimi
        self.difficulty_var = tk.StringVar(value="Orta (3x3)")
        self.difficulty_menu = tk.OptionMenu(self, self.difficulty_var, *DIFFICULTY_LEVELS.keys())
        self.difficulty_menu.pack(pady=10)

        # Başla butonu
        self.start_button = tk.Button(self, text="Başla", command=self.start_game)
        self.start_button.pack(pady=5)

    def start_game(self):
        difficulty = self.difficulty_var.get()
        self.puzzle_size = DIFFICULTY_LEVELS[difficulty]

        img = Image.open(self.image_path).resize((300, 300))

       
        self.difficulty_menu.destroy()
        self.start_button.destroy()

        self.create_puzzle(img)

    
        self.check_button = tk.Button(self, text="Kontrol Et", command=self.check_solution)
        self.check_button.pack(pady=10)

      
        self.start_time = time.time()
        self.update_timer()

    def create_puzzle(self, img):
        piece_w = img.width // self.puzzle_size
        piece_h = img.height // self.puzzle_size

        positions = [(i, j) for i in range(self.puzzle_size) for j in range(self.puzzle_size)]
        random_positions = positions[:]
        random.shuffle(random_positions)

        for i, j in positions:
            box = (j * piece_w, i * piece_h, (j + 1) * piece_w, (i + 1) * piece_h)
            piece_img = img.crop(box)
            tk_img = ImageTk.PhotoImage(piece_img)

            piece = PuzzlePiece(self.frame, self, tk_img, correct_pos=(i, j), grid_pos=random_positions.pop())
            self.pieces.append(piece)

        self.update_piece_positions()

    def update_piece_positions(self):
        piece_w = 300 // self.puzzle_size
        piece_h = 300 // self.puzzle_size
        for piece in self.pieces:
            row, col = piece.grid_pos
            piece.place(x=col * piece_w, y=row * piece_h, width=piece_w, height=piece_h)

    def get_piece_at(self, x_root, y_root):
        for piece in self.pieces:
            x1 = piece.winfo_rootx()
            y1 = piece.winfo_rooty()
            x2 = x1 + piece.winfo_width()
            y2 = y1 + piece.winfo_height()
            if x1 <= x_root <= x2 and y1 <= y_root <= y2:
                return piece
        return None

    def increment_moves(self):
        self.move_count += 1
        self.update_info_label()

    def update_timer(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.update_info_label(minutes, seconds)
        self.after(1000, self.update_timer)

    def update_info_label(self, minutes=None, seconds=None):
        if minutes is None or seconds is None:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
        self.info_label.config(text=f"Süre: {minutes:02d}:{seconds:02d} | Hamle: {self.move_count}")

    def check_solution(self):
        incorrect = 0
        for piece in self.pieces:
            if piece.grid_pos != piece.correct_pos:
                incorrect += 1

        if incorrect == 0:
            messagebox.showinfo("Tebrikler", f"Kazandınız!\n{self.info_label.cget('text')}")
        else:
            messagebox.showwarning("Hatalı", f"Bazı parçaların yeri hatalı ({incorrect} parça).")

if __name__ == "__main__":
    app = PuzzleApp()
    app.mainloop()

