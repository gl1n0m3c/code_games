import tkinter

window = tkinter.Tk()  # window становится объектом класса (старт работы)

ROW = 5
COLOMNS = 7

buttoms = []
for i in range(ROW):
    temp = []
    for j in range(COLOMNS):
        btn = tkinter.Button(window)
        temp.append(btn)
    buttoms.append(temp)

window.mainloop()  # вызов метода mainloop (создание окошка)

