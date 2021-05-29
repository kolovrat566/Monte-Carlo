import kivy
import matplotlib.pyplot as plt
import numpy as np
import random
from sympy import *

kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication,
    implicit_multiplication_application)

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout


class Container(BoxLayout):

    def cont(self):

        self.another_num = 1
        being = int(self.ids.being.text)
        ending = int(self.ids.ending.text)
        density = int(self.ids.density.text)
        quantity = int(self.ids.quantity.text)
        formula_str = self.ids.form.text

        trf = (
                standard_transformations +
                (implicit_multiplication_application,))

        x, y, z, t = symbols('x y z t')
        formula = parse_expr(formula_str, transformations=trf)          #парсинг функции formula_str
        x1 = np.linspace(being, ending, density * (ending - being))
        y1 = [formula.subs(x, i) for i in x1]
        min_y = np.amin(y1)
        max_y = np.amax(y1)

        def nuule(x1, y1):
            k = 0
            a = []
            b = []
            for i in range(len(y1) - 1):
                if (y1[i] < 0 and y1[i + 1] > 0) or y1[i] > 0 and y1[i + 1] < 0:
                    k += 1
                    a.append(x1[i])
                    if y1[i] < 0:
                        b.append(-1)
                    else:
                        b.append(1)
            if k >= 1:
                b.append(b[k - 1] * (-1))
            else:
                b.append(1)
            return a, b

        def rand(a, b, maxy,quantity):

            nuz_toch = 0
            for i in range(quantity):

                x11 = random.uniform(a, b)
                y11 = random.uniform(0, maxy)
                if maxy > 0:
                    if y11 <= formula.subs(x, x11):
                        nuz_toch += 1

                koof = nuz_toch / quantity
                if maxy < 0:
                    if y11 >= formula.subs(x, x11):
                        nuz_toch += 1
                koof = nuz_toch / quantity

            if a == b:
                koof = 0

            return (koof)

        # вывод нулей функции и знаков перехода

        nol, nol_znak = nuule(x1, y1)
        nol.insert(0, being)
        nol.append(ending)
        res = 0
        for i in range(len(nol) - 1):
            g = nol[i]
            diapozon = []
            k = 0
            while g < nol[i + 1]:
                diapozon.append(y1[k])
                k += 1
                g = x1[k]
            if nol_znak[i] == 1:
                maxy = max(diapozon)
            else:
                maxy = min(diapozon)

            koof = rand(nol[i], nol[i + 1], maxy, quantity)     # maxy
            res += (nol[i + 1] - nol[i]) * maxy * koof          # *nol_znak[i]

        fig = plt.figure()
        fig.patch.set_facecolor(color = (.5, .5, .5, .5))
        ax=plt.title("График функции")                          # заголовок
        ax=plt.xlabel("x")                                      # ось абсцисс
        ax = plt.grid(color=(0.1, 0.3, 0.3))                    # включение отображение сетки
        ax = plt.axes()
        ax.set_facecolor(color = (.5, .5, .5, .5))
        ax=plt.plot(x1, y1, linewidth = 2.5, color = (0.2, 0.4, 0.2))  # построение графика

        for i in range(len(self.ids.destination.children)):
            self.ids.destination.remove_widget(self.ids.destination.children[-1])

        self.ids.destination.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        self.ids.answer.text = 'Ответ: ' + str(res)
        self.ids.min.text = 'Минимальный У: ' + str(min_y)
        self.ids.max.text = 'Максимальный У: ' + str(max_y)


class TestApp(App):
    def build(self):

        Window.clearcolor = (.5, .5, .5, .5)                    # установка цвета нового фона
        return Container()

if __name__ == '__main__':
    TestApp().run()
