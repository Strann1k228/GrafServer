import matplotlib
import numpy as np
from flask import *
from sympy import *
import matplotlib.pyplot as plt
import os

matplotlib.use('Agg')

vis_1 = "hidden"

info_1 = ""

grafs = {1: "", 2: "", 3: ""}
app = Flask(__name__)


def create_graf():
    plt.clf()
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.grid()
    global grafs
    for i in range(len(grafs)):
        if grafs[i + 1] != "":
            x_y = from_text_to_graf_arr(grafs[i + 1], -10, 10)
            plt.plot(x_y[0], x_y[1])
    try:
        os.remove("static/graf_picture.png")
        plt.savefig("static/graf_picture")
    except:
        plt.savefig("static/graf_picture")


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', vis_1=vis_1)


def from_text_to_graf_arr(text, border_neg, border_pos):
    b_n, b_p = border_neg, border_pos
    x_lst, y_lst = [i for i in range(b_n, b_p)], []
    for i in range(b_n, b_p):
        t = text.replace("x", f"({str(i)})")
        y = eval(t)
        y_lst.append(y)
    # print(x_lst, y_lst)
    return x_lst, y_lst


@app.route('/cr_graf1', methods=["post", "get"])
def cr_gr1():
    a = request.form["tbut1"]
    grafs[1] = a
    create_graf()
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis_1=vis_1)


@app.route('/cr_graf2', methods=["post", "get"])
def cr_gr2():
    b = request.form["tbut2"]
    grafs[2] = b
    create_graf()
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis_1=vis_1)


@app.route('/cr_graf3', methods=["post", "get"])
def cr_gr3():
    c = request.form["tbut3"]
    grafs[3] = c
    create_graf()
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis_1=vis_1)


@app.route("/info_1", methods=["post", "get"])
def info_1():
    global vis_1, info_1
    if vis_1 == "hidden":
        vis_1 = "visibility"
    else:
        vis_1 = "hidden"
    print(grafs)
    poi_1_2 = []
    poi_1_3 = []
    try:
        for i in range(len(find_poi_x(grafs[1], grafs[2]))):
            poi_1_2.append((find_poi_x(grafs[1], grafs[2])[i], find_poi_y(find_poi_x(grafs[1], grafs[2]), grafs[1])[i]))
    except:
        pass
    try:
        for ii in range(len(find_poi_x(grafs[1], grafs[3]))):
            poi_1_3.append((find_poi_x(grafs[1], grafs[3])[ii], find_poi_y(find_poi_x(grafs[1], grafs[3]), grafs[1])[ii]))
    except:
        pass
    print(poi_1_2)
    print(poi_1_3)
    info_1 = 'y1 ∩ y2 = '
    for j in range(len(poi_1_2)):
        info_1 = info_1 + str(poi_1_2[j])
        if j + 1 <= len(poi_1_2) - 1:
            info_1 = info_1 + ";  "
    info_1 = info_1 + "\n" + 'y1 ∩ y3 = '

    for jj in range(len(poi_1_3)):
        info_1 = info_1 + str(poi_1_3[jj])
        if jj + 1 <= len(poi_1_3) - 1:
            info_1 = info_1 + ";  "
    print(info_1)
    info_1 = info_1.replace('\n', '<br>')
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis_1=vis_1, info_1=info_1)


def find_poi_x(eq1, eq2):
    if eq1 != '' and eq2 != '':
        x = symbols("x")
        equation = sympify("Eq(" + str(eq1) + "," + str(eq2) + ")")
        solution = solve(equation, x)
        return solution
    return None


def find_poi_y(points, eq1):
    y_points = []
    for i in range(len(points)):
        x, y = symbols('x y')
        x_eq = eq1.replace("x", f"({points[i]})")
        equation = sympify("Eq(" + str(y) + "," + x_eq + ")")
        solution = solve(equation, y)
        y_points.append(*solution)
    return y_points


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
