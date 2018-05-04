# _*_ encoding:utf-8 _*_

import matplotlib.pyplot as plt
import matplotlib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

xy_dict = {}
hex_re = re.compile(r'^-?0[xX]([0-9a-fA-F])+$')
float_re = re.compile(r'^-?[0-9]+(.[0-9]+)?$')

def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2 - 40)
    root.maxsize(width=width, height=height)
    root.minsize(width=width, height=height)
    root.geometry(size)

'''
a=(Σxy-ΣxΣy/N)/(Σx^2-(Σx)^2/N)
b=y(平均)-a*x(平均)
'''
def getAB(data_dict={}):
    #print(data_dict)
    N = len(data_dict)
    if N < 2:
        return 0, 0
    Ex2sum = 0.0
    Exysum = 0.0
    Exsum = 0.0
    Eysum = 0.0
    a = 0.0
    b = 0.0
    for x,y in data_dict.items():
        Ex2sum += x*x
        Exsum += x
        Exysum += x*y
        Eysum += y
    a = (Exysum - Exsum*Eysum/N)/(Ex2sum-Exsum*Exsum/N)
    a = round(a, 5)
    b = Eysum/N - a*(Exsum/N)
    return a,b

'''
 获取最小二乘法计算的直线上的两个点
'''
def get_any_line_points(a=0, b=0, minX=0, maxX=1):
    return {x:a*x+b for x in [minX, maxX]}
 	

def disp(data_dict):
    listX = list(data_dict.keys())
    listY = list(data_dict.values())

    fig = plt.Figure(figsize=(7, 6), dpi=100)
    plt1 = fig.add_subplot(1, 1, 1)
    plt1.plot(listX, listY, 'ok')  # o->点图；k->黑色点
    if(len(data_dict) > 1):
        a, b = getAB(data_dict)
        #print('a={0}, b={1}'.format(a, b))
        maxX = max(data_dict.keys())
        minX = min(data_dict.keys())
        line_dict = get_any_line_points(a, b, minX, maxX)
        listLX = list(line_dict.keys())
        listLY = list(line_dict.values())
        plt1.plot(listLX, listLY, 'b')  # b->黑色线
        if(b < 0):
        	str_line.set('C/V = {0} * AD - {1}'.format(a, -b))
        else:
        	str_line.set('C/V = {0} * AD + {1}'.format(a, b))
    else:
        str_line.set("")
    plt1.set_title("LeastSquares")
    plt1.set_xlabel("AD")
    plt1.set_ylabel("C/V")


    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=7)
    canvas.show()


def on_btn_add():
    strx = editX.get()
    stry = editY.get()
    if hex_re.search(strx) != None:
    	x = int(strx, 16)
    elif float_re.search(strx) != None:
    	x = float(strx)
    else:
    	return
    if hex_re.search(stry) != None:
    	y = int(stry, 16)
    elif float_re.search(stry) != None:
    	y = float(stry)
    else:
    	return
    xy_dict[x] = y
    disp(xy_dict)

def clear_data():
    xy_dict.clear()
    disp(xy_dict)
def on_btn_delete():
    strx = editX.get()
    if hex_re.search(strx) != None:
        x = int(strx, 16)
    elif float_re.search(strx) != None:
        x = float(strx)
    else:
        return
    if x in xy_dict.keys():
        xy_dict.pop(x)
        disp(xy_dict)

if __name__ == '__main__':
    #matplotlib.use('TkAgg')
    root = tk.Tk()
    root.title("least squares line tool")
    center_window(root, 700, 680)
    tk.Label(root, text='AD:', background='red').grid(row=1,column=0)
    editX = tk.Entry(root)
    editX.grid(row=1,column=1, sticky=tk.W)
    tk.Label(root, text='I:', background='red').grid(row=1,column=2)
    editY = tk.Entry(root)
    editY.grid(row=1,column=3, sticky=tk.W)
    tk.Button(root, text='Add', command=on_btn_add).grid(row=1, column=4)
    tk.Button(root, text='delete', command=on_btn_delete).grid(row=1, column=5)
    tk.Button(root, text='Clear', command=clear_data).grid(row=1, column=6)
    tk.Label(root, text="Line：", background='red').grid(row=2, column=0, columnspan=1)
    str_line = tk.StringVar()
    edit_line = tk.Entry(root, width=80, textvariable=str_line, background='#623456')
    edit_line.grid(row=2, column=1, columnspan=5)
    edit_line['state'] = 'readonly'
    disp(xy_dict)
    root.mainloop()


