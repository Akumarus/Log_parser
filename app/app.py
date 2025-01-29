from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QTabWidget, QMessageBox, QProgressDialog
from PyQt5.QtGui import QIcon

from csv_handler import CsvHandler
from json_handler import JsonHandler
from button import ButtonFrame
from table import TableFrame
from plot import PlotFrame

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игорь лох")
        self.showMaximized()
        #self.setGeometry(100, 100, 800, 800)

        # Устанавливаем иконку для заголовка окна
        self.setWindowIcon(QIcon("icon.png"))

        # Основной компоновщик
        self.main_layout = QVBoxLayout(self)

        # Фрейм для кнопок
        self.button_frame = ButtonFrame(self)

        # Создаем QTabWidget для вкладок
        self.tab_widget = QTabWidget(self)
        self.plot_widget = QWidget(self)
        self.plot = PlotFrame(self.plot_widget)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.tab_widget)
        self.horizontal_layout.addWidget(self.plot_widget)
        self.horizontal_layout.setStretch(0, 1)  # Растяжение для tab_widget
        self.horizontal_layout.setStretch(1, 1)  # Растяжение для plot_widget

        self.main_layout.addLayout(self.button_frame)
        self.main_layout.addLayout(self.horizontal_layout)
        self.setLayout(self.main_layout)

        # Путь до csv-файла и json-конфига
        self.file_path = None
        self.conf_path = None

    def show_progress(self, title, message, max_value):
        progress = QProgressDialog(message, "Отмена", 0, max_value, self)
        progress.setWindowTitle(title)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        return progress

    def load_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        progress = self.show_progress("Загрузка файла", "Загрузка CSV-файла..", 100)

        data = CsvHandler.load_csv(self.file_path)
        progress.setValue(50)
        if data is not None:
            print("CSV-файл успешно загружен")
            table_frame = TableFrame(self)
            table_frame.add_table_tab(df=data, tab_widget=self.tab_widget)
            progress.setValue(100)
        else:
            print("CSV-файл не был загружен, указанный путь не существует.")
            QMessageBox.warning(self, "Предупреждение", "Укажите путь к файлу")
            progress.setValue(0)
        
        progress.close()

    def split_file(self):
        progress = self.show_progress("Разделение файла", "Обработака данных", 100)
        TableFrame.delete_all_table(self.tab_widget)

        conf = JsonHandler.load_json()
        progress.setValue(10)

        #data = CsvHandler.load_csv(self.file_path)
        data = CsvHandler.load_csv("tables/17.01.2025.csv")
        progress.setValue(30)

        if data is not None:
            self.plot.del_parameter_button()

            print("CSV-файл успешно загружен")
            self.tables = JsonHandler.log_splite(conf, data)
            progress.setValue(50)

            total_tables = len(self.tables)
            for i, (id, df) in enumerate(self.tables.items()):
                if str(id) in conf:
                    tab_name = conf[str(id)]["name"]
                table_frame = TableFrame(self)
                table_frame.add_table_tab(df=df, tab_widget=self.tab_widget, tab_name=tab_name)
                
                header_name = df.columns
                for name in header_name:
                    if name != "ID" and name != "Время": #and name != "Счетчик количества сообщений":
                        self.plot.add_parameter_button(name, df[name].tolist())
                
                progress.setValue(50 + int((i + 1) / total_tables * 50))
                if progress.wasCanceled():
                    break

            progress.setValue(100)
        else:
            print("CSV-файл не был загружен, указанный путь не существует.")
            QMessageBox.warning(self, "Предупреждение", "Укажите путь к файлу.")
            progress.setValue(0)

    def save_table(self):
        progress = self.show_progress("Сохранение файла", "Сохранение таблиц...", 100)
        CsvHandler.save_csv(self.tables)
        progress.setValue(100)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()