import tkinter as tk
from random import shuffle

colors = ('#2A1FFF', '#006d5b', '#E0DD28', '#8713F2', '#DEA1A0', '#E1724C', '#E0D24C', '#E10043')

class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0

    def __repr__(self):
        return f'MyButton {self.x}, {self.y}, {self.is_mine}'


class Minesweeper():

    window = tk.Tk()
    window.title('Minesweeper')
    ROWS = 5
    COLUMNS = 6
    MINES = 10

    def __init__(self):
        self.buttons = []
        count = 0
        for i in range(Minesweeper.ROWS + 2):
            array = []
            for j in range(Minesweeper.COLUMNS + 2):
                if i != 0 and i != Minesweeper.ROWS + 1 and j != 0 and j != Minesweeper.COLUMNS + 1:
                    count += 1 
                    btn = MyButton(Minesweeper.window, i, j, width=4, height=2, number=count, font='Arial 12 bold')
                    btn.config(command=lambda button=btn: self.click(button))
                    btn.grid(row=i, column=j)
                else:
                    btn = MyButton(Minesweeper.window, i, j, width=4, height=2, font=('Arial 12 bold'))
                array.append(btn) 
            self.buttons.append(array)
        
    def get_mines_places(self):
        a = list(range(1, Minesweeper.COLUMNS * Minesweeper.ROWS + 1))
        shuffle(a)
        return a[:Minesweeper.MINES]
    
    def insert_mines(self):
        index_of_mines = self.get_mines_places()
        print(index_of_mines)
        for row_btn in self.buttons:
            for btn in row_btn:
                if btn.number in index_of_mines:
                    btn.is_mine = True

    def start(self):
        self.insert_mines()
        self.count_mines_in_buttons()
        Minesweeper.window.resizable(False, False)
        Minesweeper.window.mainloop()
    
    def click(self, clicked_button: MyButton):
        print(clicked_button)
        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
        else:
            if 1 <= clicked_button.count_bomb <= 8:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=colors[clicked_button.count_bomb - 1])
        clicked_button.config(state='disabled', relief=tk.SUNKEN)
    
    def count_mines_in_buttons(self):
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                    btn.count_bomb = count_bomb



game = Minesweeper()
game.start()