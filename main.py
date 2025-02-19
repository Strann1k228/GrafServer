import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sympy
from flask import Flask, render_template, request, send_file
from sympy import symbols, Eq, solve, S, diff, simplify, oo, integrate, N
from sympy.calculus.util import function_range, continuous_domain

grafs = {1: "", 2: "", 3: ""}
matplotlib.use('Agg')
app = Flask(__name__)
info = ""
vis = "hidden"
image_path = 'static/user_plot.png'


@app.route('/', methods=['GET', 'POST'])
def index():
    global grafs, image_path
    if request.method == 'POST':
        grafs[1] = f1 = request.form.get('func_1').strip()
        grafs[2] = f2 = request.form.get('func_2').strip()
        grafs[3] = f3 = request.form.get('func_3').strip()
        plt.axhline(0, color='black', linewidth=0.8)
        plt.axvline(0, color='black', linewidth=0.8)
        plt.xlim(-50, 50)  # Границы по оси X
        plt.ylim(-50, 50)  # Границы по оси Y
        plt.grid()
        print(grafs)
        for i in range(len(grafs)):
            if grafs[i + 1] != "":
                func = grafs[i + 1].replace("X", "x")
                x = np.linspace(-50, 50, 500)
                y = eval(func)
                plt.plot(x, y)
        plt.savefig(image_path)
        plt.close()
        return render_template('base.html', image_path=image_path, t1=f1, t2=f2, t3=f3)
    else:
        plt.axhline(0, color='black', linewidth=0.8)
        plt.axvline(0, color='black', linewidth=0.8)
        plt.xlim(-50, 50)  # Границы по оси X
        plt.ylim(-50, 50)  # Границы по оси Y
        plt.grid()
        plt.savefig(image_path)
        plt.close()
        return render_template('base.html', image_path=image_path)


@app.route('/download')
def download():
    return send_file('static/user_plot.png', as_attachment=True)


# функция для всей инфы
@app.route("/info", methods=["post", "get"])
def info_():
    global info, vis
    info = ""
    f1 = grafs[1]
    f2 = grafs[2]
    f3 = grafs[3]
    info += f"Функция 1: {f1}<br>"
    info += f"Функция 2: {f2}<br>"
    info += f"Функция 3: {f3}<br>"
    info += "<br>"

    info += f"Точка пересечения(1 - 2): {points_per(f1, f2)}<br>"
    info += f"Точка пересечения(1 - 3): {points_per(f1, f3)}<br>"
    info += f"Точка пересечения(2 - 3): {points_per(f2, f3)}<br>"
    info += "<br>"

    info += f"Область определения функции 1: {domain_x(f1)}<br>"
    info += f"Область определения функции 2: {domain_x(f2)}<br>"
    info += f"Область определения функции 3: {domain_x(f3)}<br>"
    info += "<br>"

    info += f"Область значений функции 1: {domain_y(f1)}<br>"
    info += f"Область значений функции 2: {domain_y(f2)}<br>"
    info += f"Область значений функции 3: {domain_y(f3)}<br>"
    info += "<br>"

    info += f"Производная функции 1: {derivative_f(f1)}<br>"
    info += f"Производная функции 2: {derivative_f(f2)}<br>"
    info += f"Производная функции 3: {derivative_f(f3)}<br>"
    info += "<br>"

    info += f"Первообразная функции 1: {antiderivative_f(f1)}<br>"
    info += f"Первообразная функции 2: {antiderivative_f(f2)}<br>"
    info += f"Первообразная функции 3: {antiderivative_f(f3)}<br>"
    info += "<br>"

    info += f"Промежутки возрастания функции 1: {inc_and_dec_intervals(f1)[0] if inc_and_dec_intervals(f1)[0] is not None else None}<br>"
    info += f"Промежутки убывания функции 1: {inc_and_dec_intervals(f1)[1] if inc_and_dec_intervals(f1)[1] is not None else None}<br>"
    info += "<br>"

    info += f"Промежутки возрастания функции 2: {inc_and_dec_intervals(f2)[0] if inc_and_dec_intervals(f2)[0] is not None else None}<br>"
    info += f"Промежутки убывания функции 2: {inc_and_dec_intervals(f2)[1] if inc_and_dec_intervals(f2)[1] is not None else None}<br>"
    info += "<br>"

    info += f"Промежутки возрастания функции 3: {inc_and_dec_intervals(f3)[0] if inc_and_dec_intervals(f3)[0] is not None else None}<br>"
    info += f"Промежутки убывания функции 3: {inc_and_dec_intervals(f3)[1] if inc_and_dec_intervals(f3)[1] is not None else None}<br>"
    info += "<br>"

    info += f"Функция 1 {odd_or_parity(f1)}<br>"
    info += f"Функция 2 {odd_or_parity(f2)}<br>"
    info += f"Функция 3 {odd_or_parity(f3)}<br>"
    if vis == "hidden":
        vis = "visibility"
    else:
        vis = "hidden"
    return render_template('base.html', vis=vis, info=info, image_path=image_path, t1=f1, t2=f2, t3=f3)


def points_per(f, f_):
    try:
        x, y = symbols('x y')
        func = eval(f)
        func_ = eval(f_)
        equation = Eq(func, func_)
        intersection_x = solve(equation, x)[0]  # Находим x
        intersection_y = func.subs(x, intersection_x)

    except:
        return None, None
    return N(intersection_x, accuracy), N(intersection_y, accuracy)


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


def derivative_f(f):
    try:
        x = sympy.symbols('x')
        func = eval(f)
        f_prime = sympy.diff(func, x)
    except:
        return None
    return f_prime


def antiderivative_f(f):
    try:
        x = symbols("x")
        func = eval(f)
        antiderivative = integrate(func, x)
    except:
        return None
    return antiderivative


def inc_and_dec_intervals(f):
    try:
        x = symbols('x')
        func = eval(f)
        f_prime = diff(func, x)
        critical_points = solve(f_prime, x)
        intervals = [(-oo, critical_points[0])] + [(critical_points[i], critical_points[i + 1]) for i in
                                                   range(len(critical_points) - 1)] + [(critical_points[-1], oo)]
        increasing_intervals = []
        decreasing_intervals = []
        for interval in intervals:
            test_point = (interval[0] + interval[1]) / 2
            sign = f_prime.subs(x, test_point)
            if sign > 0:
                increasing_intervals.append(interval)
            elif sign < 0:
                decreasing_intervals.append(interval)
    except:
        return [None, None]
    return increasing_intervals, decreasing_intervals


def odd_or_parity(f):
    try:
        x = symbols('x')
        func = eval(f)
        f_neg_x = func.subs(x, -x)
        if simplify(f_neg_x - func) == 0:
            return "чётная"
        elif simplify(f_neg_x + func) == 0:
            return "нечётная"
        return "общего вида"
    except:
        return None


if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=False)

