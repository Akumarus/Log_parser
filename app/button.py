from PyQt5.QtWidgets import QHBoxLayout, QPushButton

class ButtonFrame(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        # Создаем кнопки
        self.button1 = QPushButton("Открыть CSV")
        self.button2 = QPushButton("Разделить ID")
        self.button3 = QPushButton("Сохраненить таблицы")

        self.button1.clicked.connect(parent.load_file)
        self.button2.clicked.connect(parent.split_file)
        self.button3.clicked.connect(parent.save_table)

        # Добавляем кнопки в компоновщик
        self.addWidget(self.button1)
        self.addWidget(self.button2)
        self.addWidget(self.button3)
        
        