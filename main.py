import matplotlib
from flask import *

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

text = None
app = Flask(__name__)

graf_num = 1

def create_graf(x_l, y_l):
    plt.clf()
    plt.axhline(0, color='black', linewidth=0.2)
    plt.axvline(0, color='black', linewidth=0.2)
    plt.plot(x_l, y_l)
    try:
        os.remove("static/graf_picture.png")
        plt.savefig("static/graf_picture")
    except:
        plt.savefig("static/graf_picture")


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', text=graf_num)


@app.route("/t", methods=["POST"])
def show_text():
    global text
    text = request.form["name"]
    x_lst, y_lst = [i for i in range(-10, 10)], []
    for i in range(-10, 10):
        t = text.replace("x", f"({str(i)})")
        print(t)
        y = eval(t)
        y_lst.append(y)
    print(x_lst, y_lst)
    create_graf(x_lst, y_lst)
    return render_template('base.html', text=graf_num)


@app.route("/PLUS", methods=["POST"])
def plus_graf():
    global graf_num
    if graf_num <= 2:
        graf_num += 1
    return render_template('base.html', text=graf_num, g_num=graf_num)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
