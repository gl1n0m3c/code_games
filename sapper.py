import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror


colors = ('#2A1FFF', '#006d5b', '#E0DD28', '#8713F2', '#DEA1A0', '#E1724C', '#E0D24C', '#E10043')

class MyButton(tk.Button):
    
    def __init__(self, master, row, column, number=0, *args, **kwargs):
        super().__init__(master, width=3, font='Calibri 20 bold', *args, **kwargs)
        self.number   = number
        self.row      = row
        self.column   = column
        self.is_mine  = False
        self.bombs    = 0

    def __repr__(self):
        return f'Button {self.number} ({self.row} {self.column})'


class Minesweeper():

    ROWS = 5
    COLUMNS = 7
    MINES = 5
    IS_GAMEOVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []

    def rows_colimns(self):
        for i in range(1, Minesweeper.ROWS + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for j in range(1, Minesweeper.COLUMNS + 1):
            tk.Grid.columnconfigure(self.window, j, weight=1)

    def make_buttons(self):
        count = 0
        for i in range(Minesweeper.ROWS + 2):
            array = []
            for j in range(Minesweeper.COLUMNS + 2):
                if i != 0 and i != Minesweeper.ROWS + 1 and j != 0 and j != Minesweeper.COLUMNS + 1:
                    count += 1
                    btn = MyButton(self.window, i, j, count)
                    btn.bind('<Button-3>', self.right_click)
                    btn['command'] = lambda button=btn: self.click(button)
                    btn.grid(row=i, column=j, sticky='news')
                else:
                    btn = MyButton(self.window, i, j)
                array.append(btn)
            self.buttons.append(array)
    
    def right_click(self, event):
        if Minesweeper.IS_GAMEOVER:
            return None
        curr_btn = event.widget
        if curr_btn['state'] == 'normal':
            curr_btn['state'] = 'disabled'
            curr_btn['text']  = '🚩'
            curr_btn['disabledforeground'] = 'red'
        elif curr_btn['text']  == '🚩':
            curr_btn['text']  = ''
            curr_btn['state'] = 'normal'

    def count_bombs(self):
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine == False:    
                    count = 0
                    for p in [-1, 0, 1]:
                        for q in [-1, 0, 1]:
                            neighbour = self.buttons[btn.row + p][btn.column + q]
                            if neighbour.is_mine:
                                count += 1
                    btn.bombs = count

    def create_indexes_of_bombs(self, n):
        a = list(range(1, Minesweeper.ROWS * Minesweeper.COLUMNS + 1))
        a.remove(n)
        shuffle(a)
        return a[:Minesweeper.MINES]

    def click(self, clicked_button: MyButton):
        
        if Minesweeper.IS_GAMEOVER:
            return None

        if Minesweeper.IS_FIRST_CLICK:
            self.make_bombs(clicked_button.number)
            self.count_bombs()
            self.show_buttons()  # удалить функцию
            Minesweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text='*', bg='red', fg='black')
            Minesweeper.IS_GAMEOVER = True
            showinfo('Game over', 'Вы проиграли!')
            for i in range(1, Minesweeper.ROWS + 1):
                for j in range(1, Minesweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            if 1 <= clicked_button.bombs <= 8:  # изменить на кол-во бомб
                clicked_button.config(text=clicked_button.bombs, disabledforeground=colors[clicked_button.bombs - 1], state='disabled')
            elif clicked_button.bombs == 0:
                self.open_neighbours(clicked_button)

    def make_bombs(self, n):
        array = self.create_indexes_of_bombs(n)
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                if self.buttons[i][j].number in array:
                    self.buttons[i][j].is_mine = True

    def show_buttons(self):
        for i in range(1, Minesweeper.ROWS + 1):
            for j in range(1, Minesweeper.COLUMNS + 1):
                if self.buttons[i][j].is_mine:
                    print('B', end=' ')
                else:
                    print(self.buttons[i][j].bombs, end=' ')
            print()
        print()

    def open_neighbours(self, btn: MyButton):  # дописать диагональ
        check_queue = [(btn.row, btn.column)]
        checked_buttons = set()
        while True:
            checking_btn = self.buttons[check_queue[0][0]][check_queue[0][1]]
            if checking_btn.is_mine == False and checking_btn.bombs == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if not dx == dy == 0:
                            if check_queue[0][0] + dx < 1 or check_queue[0][0] + dx > Minesweeper.ROWS or check_queue[0][1] + dy < 1 or check_queue[0][1] + dy > Minesweeper.COLUMNS or ((check_queue[0][0] + dx, check_queue[0][1] + dy) in checked_buttons):
                                continue
                            else:
                                neighbour = self.buttons[check_queue[0][0] + dx][check_queue[0][1] + dy]
                                if neighbour.is_mine == False:
                                    check_queue += [(neighbour.row, neighbour.column)]
            elif checking_btn.is_mine == False:
                checking_btn.config(text=checking_btn.bombs, disabledforeground=colors[checking_btn.bombs - 1])

            checking_btn['state'] = 'disabled'
            checking_btn['relief'] = 'sunken'
            checked_buttons.add(check_queue[0])
            check_queue.pop(0)
            if not check_queue:
                break
    
    def reload(self):
        while self.window.winfo_children():
            self.window.winfo_children()[0].destroy()
        Minesweeper.IS_FIRST_CLICK = True
        Minesweeper.IS_GAMEOVER = False
        self.__init__()
        self.make_buttons()
        self.make_menu()

    def create_settings_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.title('Настройки')

        tk.Label(win_settings, text='Количкство рядов').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        row_entry.insert(0, Minesweeper.ROWS)

        tk.Label(win_settings, text='Количкство столбцов').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        column_entry.insert(0, Minesweeper.COLUMNS)

        tk.Label(win_settings, text='Количкство мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        mines_entry.insert(0, Minesweeper.MINES)

        tk.Button(win_settings, text='Применить', 
                  command=lambda: self.change_settings(row_entry, column_entry, mines_entry)).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except:
            showerror('Ошибка', 'Вы ввели неправильное значение')
            return None
        Minesweeper.ROWS    = int(row.get())
        Minesweeper.COLUMNS = int(column.get())
        Minesweeper.MINES   = int(mines.get())
        self.reload()

    def make_menu(self):
        menubar = tk.Menu(self.window)
        self.window['menu'] = menubar

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_settings_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings_menu)

    def start(self):
        self.window  = tk.Tk()
        self.make_buttons()
        self.rows_colimns()
        self.make_menu()
        self.window.mainloop()



game = Minesweeper()
game.start()