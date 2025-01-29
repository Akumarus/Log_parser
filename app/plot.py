from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotFrame(QWidget):
    def __init__(self, widget):
        super().__init__()

        # Кнопка для включения сетки
        self.button = QPushButton("Включить сетку")
        self.button.clicked.connect(self.switch_grid)

        # Создаем график
        self.figure = plt.Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)

        # Layout для кнопок
        self.button_layout = QVBoxLayout()
        self.button_layout.setSpacing(5)  # Отступ между кнопками
        self.button_layout.addStretch()  # Растяжение, чтобы кнопки были сверху

        # Контейнер для кнопок
        self.button_container = QWidget()
        self.button_container.setLayout(self.button_layout)

        # Создаем QScrollArea для кнопок
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Разрешаем изменение размера содержимого
        self.scroll_area.setWidget(self.button_container)  # Устанавливаем контейнер в QScrollArea

        # Layout для графика
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.button)
        plot_layout.addWidget(self.canvas)

        # Основной layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.scroll_area)  # Добавляем QScrollArea с кнопками
        main_layout.addLayout(plot_layout)  # Добавляем график
        widget.setLayout(main_layout)

        # Переменные для хранения данных и состояния
        self.grid_enabled = False
        self.active_parameter = {}  # Словарь для отслеживания активных параметров
        self.param_data = {}  # Словарь для хранения данных по параметрам
        self.lines = {}  # Словарь для хранения линий графиков
    
    def del_parameter_button(self):
        self.param_data.clear()
        self.active_parameter.clear()
        

        while self.button_layout.count() > 1:
          item = self.button_layout.takeAt(0)  # Берем первый элемент
          widget = item.widget()
          if widget:
            widget.deleteLater()  # Удаляем виджет (кнопку)

    def add_parameter_button(self, param_name, data=None):
        button = QPushButton(param_name)
        button.setCheckable(True)  # Делаем кнопку переключаемой
        button.clicked.connect(lambda: self.toggle_parameter(param_name))  # Связываем кнопку с функцией

        self.button_layout.insertWidget(self.button_layout.count() - 1, button)

        self.param_data[param_name] = data  # Сохраняем данные по ключу param_name
        self.active_parameter[param_name] = False  # Изначально параметр неактивен

    def toggle_parameter(self, param_name):
        """
        Переключение состояния параметра (активен/неактивен).
        :param param_name: Имя параметра.
        """
        if param_name in self.active_parameter:
            self.active_parameter[param_name] = not self.active_parameter[param_name]

            if self.active_parameter[param_name]:
                line, = self.axes.plot(self.param_data[param_name], label=param_name)
                self.lines[param_name] = line 
            else:
                if param_name in self.lines:
                    self.lines[param_name].remove()
                    del self.lines[param_name]

            if self.axes.get_legend():
                self.axes.get_legend().remove()
            if self.lines:
                self.axes.legend()

            self.axes.relim()
            self.axes.autoscale()
            self.canvas.draw()
        else:
            print(f"Параметр '{param_name}' не найден.")

    def switch_grid(self):
        """Включение/отключение сетки на графике."""
        self.grid_enabled = not self.grid_enabled
        self.axes.grid(self.grid_enabled)
        self.canvas.draw()
        if self.grid_enabled:
            print("Сетка включена")
            self.button.setText("Выключить сетку")
        else:
            print("Сетка выключена")
            self.button.setText("Включить сетку")

    def plot_example(self, x, y):
        """Пример построения графика с временной осью."""
        x = pd.to_datetime(x, format="%H:%M:%S")
        self.axes.plot(x, y, label="Пример")
        self.axes.set_title("Пример графика")
        self.axes.legend()

        # Уменьшаем количество меток на оси X
        self.axes.xaxis.set_major_locator(MaxNLocator(nbins=10))  # Не более 10 меток на оси X
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))  # Формат ЧЧ:ММ:СС
        self.figure.autofmt_xdate()

        self.canvas.draw()