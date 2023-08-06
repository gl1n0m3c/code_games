# MY TicTacToe
# main class
class TicTacToe():
    def __init__(self, now_player):
        self.now_player = now_player
    
    def make_turn(self, position):
        pass



# tkinter part
import tkinter as tk

positions = [[None]*3]*3
buttons = []
win = tk.Tk()
win.geometry('300x330+200+100')
win.title('Крестики нолики')
TTT = tk.Entry(win, state='disabled')
TTT.grid(row=0, column=0, sticky='nswe', columnspan=3)
win.grid_rowconfigure(0, minsize=30)  # entry
for i in range(1, 4):
    win.grid_rowconfigure(i, minsize=100)
    win.grid_columnconfigure(i - 1, minsize=100)
    for j in range(3):
        tk.Button(win).grid(row=i, column=j, sticky='nswe')



win.mainloop()