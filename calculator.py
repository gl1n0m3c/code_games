# MY CALCULATOR
# PART WITH FUNCTIOUS
def ClearBoard():
    global CanInsert
    calc.delete(0, 'end')
    CanInsert = False

def AddOnEntry(value):
    global MaxElements
    global NowElements
    global CanInsert
    if NowElements > MaxElements:
        ClearBoard()
        calc.insert(0, 'Превышено количество элементов!')
        return 
    if value.isdigit():
        CanInsert = True
    if CanInsert:
        calc.insert('end', value)
        if value.isdigit():
            NowElements += 1
        else:
            NowElements += 3
    if value == ' * ' or value == ' / ' or value == ' + ' or value == ' - ':
        if CanInsert == False and len(calc.get()) != 0:
            calc.delete(len(calc.get()) - 3, 'end')
            calc.insert('end', value)
        CanInsert = False

def GiveResault():  # поступает строка
    global NeetToClear
    global CanInsert
    value = calc.get()
    array = value.split()
    if array[-1].isdigit():
        while len(array) != 1:
            flag = False
            for i in range(len(array)):
                if array[i] == '*':
                    array[i - 1] = int(array[i - 1]) * int(array[i + 1])
                    array.pop(i)
                    array.pop(i)
                    flag = True
                    break
                elif array[i] == '/':
                    if int(array[i + 1]) == 0:
                        ClearBoard()
                        calc.insert(0, 'Делить на 0 нельзя!')
                        return
                    array[i - 1] = int(array[i - 1]) / int(array[i + 1])
                    array.pop(i)
                    array.pop(i)
                    flag = True
                    break
            if flag == False:
                for i in range(len(array)):
                    if array[i] == '+':
                        array[i - 1] = int(array[i - 1]) + int(array[i + 1])
                        array.pop(i)
                        array.pop(i)
                        break
                    elif array[i] == '-':
                        array[i - 1] = int(array[i - 1]) - int(array[i + 1])
                        array.pop(i)
                        array.pop(i)
                        break
    else:
        ClearBoard()
        calc.insert(0, 'Преобразования невозможны, вы не дописали число!')
        return

    ClearBoard()
    if len(str(array[0])) > 2 and  str(array[0])[-2:] == '.0':
        calc.insert(0, str(array[0])[:-2])
    else:
        calc.insert(0, array[0])
        CanInsert = True

# PART WITH tkinter

import tkinter as tk

NeetToClear = CanInsert = False
MaxElements = 40
NowElements = 0

win = tk.Tk()
win.geometry('480x520+200+100')
win.title('Калькулятор')
win['bg'] = '#A3887B'

calc = tk.Entry(win, bd=5, font=('Arial', 20))
calc.grid(row=0, column=0, sticky='nswe', columnspan=4, ipadx=5, ipady=5)
tk.Button(win, font=('Arial', 18), text='1', bd=5, command=lambda: AddOnEntry('1')).grid(row=1, column=0, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='2', bd=5, command=lambda: AddOnEntry('2')).grid(row=1, column=1, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='3', bd=5, command=lambda: AddOnEntry('3')).grid(row=1, column=2, sticky='nswe', padx=5, pady=5)
tk.Button(win, fg='red', font=('Arial', 18), text='+', bd=5, command=lambda: AddOnEntry(' + ')).grid(row=1, column=3, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='4', bd=5, command=lambda: AddOnEntry('4')).grid(row=2, column=0, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='5', bd=5, command=lambda: AddOnEntry('5')).grid(row=2, column=1, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='6', bd=5, command=lambda: AddOnEntry('6')).grid(row=2, column=2, sticky='nswe', padx=5, pady=5)
tk.Button(win, fg='red', font=('Arial', 18), text='-', bd=5, command=lambda: AddOnEntry(' - ')).grid(row=2, column=3, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='7', bd=5, command=lambda: AddOnEntry('7')).grid(row=3, column=0, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='8', bd=5, command=lambda: AddOnEntry('8')).grid(row=3, column=1, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='9', bd=5, command=lambda: AddOnEntry('9')).grid(row=3, column=2, sticky='nswe', padx=5, pady=5)
tk.Button(win, fg='red', font=('Arial', 18), text='/', bd=5, command=lambda: AddOnEntry(' / ')).grid(row=3, column=3, sticky='nswe', padx=5, pady=5)
tk.Button(win, font=('Arial', 18), text='0', bd=5, command=lambda: AddOnEntry('0')).grid(row=4, column=0, sticky='nswe', padx=5, pady=5)
tk.Button(win, fg='red', font=('Arial', 18), text='C', bd=5, command=ClearBoard).grid(row=4, column=1, sticky='nswe', padx=5, pady=5)
tk.Button(win, fg='red', font=('Arial', 18), text='=', bd=5, command=GiveResault).grid(row=4, column=2, sticky='nswe', padx=5, pady=5)  # отдельная функция
tk.Button(win, fg='red', font=('Arial', 18), text='*', bd=5, command=lambda: AddOnEntry(' * ')).grid(row=4, column=3, sticky='nswe', padx=5, pady=5)

win.grid_rowconfigure(0, minsize=104)
for i in range(4):
    win.grid_columnconfigure(i, minsize=120)
    win.grid_rowconfigure(i + 1, minsize=104)



win.mainloop()