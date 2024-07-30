import matplotlib
import numpy as np
from flask import *
import matplotlib.pyplot as plt
import os

matplotlib.use('Agg')

text = None
grafs = {}
app = Flask(__name__)

graf_num = 1
g_colors = ["#47cfed", "#fcb708", "#12c745"]

def create_graf():
    plt.clf()
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.grid()

    g_colors[0] = request.form["tbut1_color"]
    global grafs
    for i in range(len(grafs)):
        x_y = from_text_to_graf_arr(grafs[i + 1], -10, 10)
        plt.plot(x_y[0], x_y[1], color=g_colors[i])
    try:
        os.remove("static/graf_picture.png")
        plt.savefig("static/graf_picture")
    except:
        plt.savefig("static/graf_picture")


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', text=text)

    # @app.route("/t", methods=["POST"])
    # def show_text():
    #     global text, grafs
    #     text = request.form["tbut"]
    # x_lst, y_lst = [i for i in range(-100, 100)], []
    # for i in range(-100, 100):
    #     t = text.replace("x", f"({str(i)})")
    #     y = eval(t)
    #     y_lst.append(y)
    #
    #
    # # print(x_lst, y_lst)
    # create_graf(x_lst, y_lst)
    # return render_template('base.html', text=text)


def from_text_to_graf_arr(text, border_neg, border_pos):
    b_n, b_p = border_neg, border_pos
    x_lst, y_lst = [i for i in range(b_n, b_p)], []
    for i in range(b_n, b_p):
        t = text.replace("x", f"({str(i)})")
        y = eval(t)
        y_lst.append(y)
    # print(x_lst, y_lst)
    return x_lst, y_lst


@app.route("/cr_graf1", methods=["POST"])
def create_graf_1():
    global grafs
    grafs[1] = request.form["tbut1"]
    print(grafs)
    # for i in range(len(grafs)):
    # x_l, y_l = from_text_to_graf_arr(grafs[1], -100, 100)
    create_graf()
    try:
        return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], g_num=graf_num, col1=g_colors[0])
    except:
        return render_template('base.html', gr_1=grafs[1], g_num=graf_num, col1=g_colors[0])


@app.route("/cr_graf2", methods=["POST"])
def create_graf_2():
    global grafs
    grafs[2] = request.form["tbut2"]
    print(grafs)
    create_graf()
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], g_num=graf_num, col1=g_colors[0])


@app.route("/cr_graf3", methods=["POST"])
def create_graf_3():
    global grafs
    grafs[3] = request.form["tbut3"]
    print(grafs)
    create_graf()
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], g_num=graf_num, col1=g_colors[0])


@app.route("/PLUS_2", methods=["POST"])
def plus_2():
    global graf_num
    if graf_num == 1:
        graf_num += 1
    return render_template('base.html', gr_1=grafs[1], g_num=graf_num, col1=g_colors[0])


@app.route("/PLUS_3", methods=["POST"])
def plus_3():
    global graf_num
    if graf_num == 2:
        graf_num += 1
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], g_num=graf_num, col1=g_colors[0])


@app.route("/MINUS_2", methods=["POST"])
def minus_2():
    global graf_num
    if graf_num == 2:
        graf_num -= 1
    return render_template('base.html', gr_1=grafs[1], g_num=graf_num, col1=g_colors[0])


@app.route("/MINUS_3", methods=["POST"])
def minus_3():
    global graf_num
    if graf_num == 3:
        graf_num -= 1
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], g_num=graf_num, col1=g_colors[0])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
