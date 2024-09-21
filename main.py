import matplotlib
import numpy as np
import sympy
from flask import *
from sympy import *
from sympy.calculus.util import function_range, continuous_domain
import matplotlib.pyplot as plt
import os

matplotlib.use('Agg')

vis_1_1 = "hidden"
vis_2_1 = "hidden"
vis_3_1 = "hidden"

vis = "hidden"

grafs = {1: "", 2: "", 3: ""}
grafs_border = [(-5, 5), (-5, 5), (-5, 5)]
app = Flask(__name__)


def create_graf():
    plt.clf()
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.grid()
    global grafs
    for i in range(len(grafs)):
        if grafs[i + 1] != "":
            func = grafs[i + 1]
            x = np.linspace(-10, 10, 100)
            y = eval(func)
            plt.plot(x, y)
            # border = grafs_border[i]
            # x_y = from_text_to_graf_arr(grafs[i + 1], border[0], border[1])
            # plt.plot(x_y[0], x_y[1])
    try:
        os.remove("static/graf_picture.png")
        plt.savefig("static/graf_picture")
    except:
        plt.savefig("static/graf_picture")


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis=vis)


# def from_text_to_graf_arr(text, border_neg, border_pos):
#     b_n, b_p = border_neg, border_pos
#     x_lst, y_lst = [i for i in range(b_n, b_p)], []
#     for i in range(b_n, b_p):
#         t = text.replace("x", f"({str(i)})")
#         try:
#             y = eval(t)
#         except ZeroDivisionError:
#             pass
#         y_lst.append(y)
#     return x_lst, y_lst


@app.route('/cr_graf1', methods=["post", "get"])
def cr_gr1():
    a = request.form["tbut1"]
    grafs[1] = a
    create_graf()
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis=vis)


@app.route('/cr_graf2', methods=["post", "get"])
def cr_gr2():
    b = request.form["tbut2"]
    grafs[2] = b
    create_graf()
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis=vis)


@app.route('/cr_graf3', methods=["post", "get"])
def cr_gr3():
    c = request.form["tbut3"]
    grafs[3] = c
    create_graf()
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis=vis)


# @app.route("/settings__1", methods=["post", "get"])
# def sett__1():
#     global vis_1, vis_1_1, grafs_border
#     vis_1 = "hidden"
#     if vis_1_1 == "hidden":
#         vis_1_1 = "visibility"
#     else:
#         vis_1_1 = "hidden"
#         # print(request.form["border_1"], grafs_border)
#         grafs_border[0] = (-int(request.form["border_1"]), int(request.form["border_1"]))
#         # print(request.form["border_1"], grafs_border)
#     return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis=vis)


# @app.route("/settings__2", methods=["post", "get"])
# def sett__2():
#     global vis_2, vis_2_1, grafs_border
#     vis_2 = "hidden"
#     if vis_2_1 == "hidden":
#         vis_2_1 = "visibility"
#     else:
#         vis_2_1 = "hidden"
#         # print(request.form["border_1"], grafs_border)
#         grafs_border[1] = (-int(request.form["border_2"]), int(request.form["border_2"]))
#         # print(request.form["border_1"], grafs_border)
#     return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis_1=vis_1, vis_2=vis_2,
#                            vis_3=vis_3,
#                            info_1=info_1, info_2=info_2, info_3=info_3, vis_1_1=vis_1_1, vis_2_1=vis_2_1,
#                            vis_3_1=vis_3_1, val_1=grafs_border[0][1], val_2=grafs_border[1][1],
#                            val_3=grafs_border[2][1])
#
#
# @app.route("/settings__3", methods=["post", "get"])
# def sett__3():
#     global vis_3, vis_3_1, grafs_border
#     vis_3 = "hidden"
#     if vis_3_1 == "hidden":
#         vis_3_1 = "visibility"
#     else:
#         vis_3_1 = "hidden"
#         # print(request.form["border_1"], grafs_border)
#         grafs_border[2] = (-int(request.form["border_3"]), int(request.form["border_3"]))
#         # print(request.form["border_1"], grafs_border)
#     return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis_1=vis_1, vis_2=vis_2,
#                            vis_3=vis_3,
#                            info_1=info_1, info_2=info_2, info_3=info_3, vis_1_1=vis_1_1, vis_2_1=vis_2_1,
#                            vis_3_1=vis_3_1, val_1=grafs_border[0][1], val_2=grafs_border[1][1],
#                            val_3=grafs_border[2][1])


# функция для всей инфы
@app.route("/info", methods=["post", "get"])
def info_():
    info = ""
    f1 = grafs[1]
    f2 = grafs[2]
    f3 = grafs[3]
    info += f"Точка пересечения(1 - 2): {points_per(f1, f2)}\n"
    info += f"Точка пересечения(1 - 3): {points_per(f1, f3)}\n"
    info += f"Точка пересечения(2 - 3): {points_per(f2, f3)}\n"
    info += "\n"

    info += f"Область определения функции 1: {domain_x(f1)}\n"
    info += f"Область определения функции 2: {domain_x(f2)}\n"
    info += f"Область определения функции 3: {domain_x(f3)}\n"
    info += "\n"

    info += f"Область значений функции 1: {domain_y(f1)}\n"
    info += f"Область значений функции 2: {domain_y(f2)}\n"
    info += f"Область значений функции 3: {domain_y(f3)}\n"
    info += "\n"

    info += f"Производная функции 1: {derivative(f1)}\n"
    info += f"Производная функции 2: {derivative(f2)}\n"
    info += f"Производная функции 3: {derivative(f3)}\n"
    info += "\n"

    info += f"первообразная функции 1: {antiderivative(f1)}\n"
    info += f"первообразная функции 2: {antiderivative(f2)}\n"
    info += f"первообразная функции 3: {antiderivative(f3)}\n"
    print(info)
    return render_template('base.html', gr_1=grafs[1], gr_2=grafs[2], gr_3=grafs[3], vis=vis)


def points_per(f, f_):
    try:
        x, y = symbols('x y')
        f = f
        f_ = f_
        func = eval(f)
        func_ = eval(f_)
        equation = Eq(func, func_)
        intersection_x = solve(equation, x)[0]  # Находим x
        intersection_y = func.subs(x, intersection_x)
    except:
        return None, None
    return intersection_x, intersection_y


def domain_x(f):
    try:
        x = sympy.symbols('x')
        func = eval(f)
        domain = continuous_domain(func, x, S.Reals)
    except:
        return None
    return domain


def domain_y(f):
    try:
        x = sympy.symbols('x')
        func = eval(f)
        domain = function_range(func, x, S.Reals)
    except:
        return None
    return domain


def derivative(f):
    try:
        x = sympy.symbols('x')
        func = eval(f)
        f_prime = sympy.diff(f, x)
    except:
        return None
    return f_prime


def antiderivative(f):
    try:
        x = symbols("x")
        func = eval(f)
        antiderivative = integrate(func, x)
    except:
        return None
    return antiderivative


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
