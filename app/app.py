from email import header
from genericpath import exists
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QTabWidget, QMessageBox
from PyQt5.QtGui import QIcon

from csv_handler import CsvHandler
from json_handler import JsonHandler
from button import ButtonFrame
from table import TableFrame
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Full Screen Example")
        self.setGeometry(100, 100, 800, 800)

        # Устанавливаем иконку для заголовка окна
        self.setWindowIcon(QIcon("icon.png"))

        # Основной компоновщик
        self.layout = QVBoxLayout(self)

        # Фрейм для кнопок
        self.button_frame = ButtonFrame(self)
        self.layout.addLayout(self.button_frame)

        # Создаем QTabWidget для вкладок
        self.tab_widget = QTabWidget(self)
        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)

        # Путь до csv-файла и json-конфига
        self.file_path = None
        self.conf_path = None

    def delete_all_table(self):
        count = self.tab_widget.count()
        for i in range(count - 1, -1, -1):
            tab_name = self.tab_widget.tabText(i)
            current_widget = self.tab_widget.widget(i)
            self.tab_widget.removeTab(i)
            current_widget.deleteLater()

    def load_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        df = CsvHandler.load_csv(self.file_path)

        if df is not None:
            print("CSV-файл успешно загружен")
            tab_name = "All logs"
            #header_name = df.columns
            self.add_table_tab(df, tab_name=tab_name)
        else:
            print("CSV-файл не был загружен, указанный путь не существует.")

    def split_file(self):
        self.delete_all_table()
        conf = JsonHandler.load_json()
        data = CsvHandler.load_csv(self.file_path)

        if data is not None:
            print("CSV-файл успешно загружен")
            self.tables = JsonHandler.log_splite(conf, data)
            for id, df in self.tables.items():
                if str(id) in conf:
                    tab_name = conf[str(id)]["name"]
                self.add_table_tab(df, tab_name=tab_name)
        else:
            print("CSV-файл не был загружен, указанный путь не существует.")
            QMessageBox.warning(self, "Предупреждение", "Укажите путь к файлу.")

    def save_table(self):
        CsvHandler.save_csv(self.tables)

    def add_table_tab(self, df, tab_name):
        """Добавляет вкладку с таблицей"""
        header_name = df.columns
        print(header_name)
        rows, columns = df.shape
        df_list = df.values.tolist()

        # Создаем фрейм с таблицей
        self.table_frame = TableFrame(self)
        self.table_frame.set_table_size(rows, columns, header_name)
        self.table_frame.draw_table(df_list)

        # Добавляем вкладку
        self.tab_widget.addTab(self.table_frame, tab_name)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()