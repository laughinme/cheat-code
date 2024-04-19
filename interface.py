a = 'ale'
print(a[:2])

print('1'.isnumeric())

import tkinter as tk

class MazeEditor:
    def __init__(self, master, rows=10, cols=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.cell_size = 40
        self.canvas = tk.Canvas(master, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        self.cells = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()
        self.canvas.bind('<Button-1>', self.cell_clicked)  # ЛКМ

    def draw_grid(self):
        for y in range(self.rows):
            for x in range(self.cols):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.cells[y][x] = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', tags='cell')


    def cell_clicked(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        cell = self.cells[row][col]
        current_outline = self.canvas.itemcget(cell, 'outline')

        if current_outline == 'black':
            self.canvas.itemconfig(cell, outline='red', width=2)  # Изменяем границу на более толстую и красную
        else:
            self.canvas.itemconfig(cell, outline='black', width=1)  # Возвращаем обычное состояние


    def run(self):
        self.master.mainloop()

root = tk.Tk()
editor = MazeEditor(root)
editor.run()
