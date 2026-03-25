import tkinter as tk
import random

WIDTH = 800
HEIGHT = 400
BAR_WIDTH = 30
DELAY = 100  # миллисекунды

class SortVisualizer:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.arr = [random.randint(10, 100) for _ in range(20)]
        self.rects = []

        self.draw_bars()

        self.i = 0
        self.j = 0
        self.min_idx = 0

        self.root.after(500, self.selection_step)

    def draw_bars(self, highlight={}):
        self.canvas.delete("all")

        for i, val in enumerate(self.arr):
            x0 = i * BAR_WIDTH
            x1 = x0 + BAR_WIDTH - 2

            # обычные столбцы (снизу вверх)
            y0 = HEIGHT - val * 3
            y1 = HEIGHT

            color = "blue"

            if i in highlight:
                color = highlight[i]

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

            # подпись числа
            self.canvas.create_text(x0 + 10, y0 - 10, text=str(val), fill="white")

    def selection_step(self):
        n = len(self.arr)

        if self.i >= n:
            return

        if self.j == 0:
            self.min_idx = self.i
            self.j = self.i + 1

        if self.j < n:
            highlight = {
                self.i: "orange",
                self.j: "orange",
                self.min_idx: "red"
            }

            self.draw_bars(highlight)

            if self.arr[self.j] < self.arr[self.min_idx]:
                self.min_idx = self.j

            self.j += 1
        else:
            # swap
            self.arr[self.i], self.arr[self.min_idx] = self.arr[self.min_idx], self.arr[self.i]
            self.i += 1
            self.j = 0

        self.root.after(DELAY, self.selection_step)


# запуск
root = tk.Tk()
root.title("Selection Sort Visualization")

app = SortVisualizer(root)

root.mainloop()