from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QHeaderView


class TableFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создаем компоновщик для таблицы
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Настройка растягивания таблицы
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Устанавливаем жирный шрифт для заголовков столбцов
        font = QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)
    
    def delete_table(self):
        """Удаляет текущую таблицу (вкладку)"""
        current_index = self.tab_widget.currentIndex()
        if current_index != -1:
            widget_to_remove = self.tab_widget.widget(current_index)
            self.tab_widget.removeTab(current_index)
            widget_to_remove.deleteLater()
            print("Таблица удалена.")


    def adjust_column_widths(self, headers):
        """Настраивает ширину столбцов на основе длины текста в заголовках"""
        font = self.table.horizontalHeader().font()  # Получаем шрифт заголовка
        font_metrics = QFontMetrics(font)

        for col, header in enumerate(headers):
            text_width = font_metrics.width(header)  # Рассчитываем ширину текста
            self.table.setColumnWidth(col, text_width + 20)  # Добавляем запас (20 пикселей)
            print(text_width)

    def set_table_size(self, rows: int, columns: int, headers):
        import pandas as pd
        """Задает размеры таблицы и опционально устанавливает заголовки столбцов."""
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        if headers is not None and len(headers) > 0:  # Проверка на наличие заголовков
            if isinstance(headers, pd.Index):  # Если это pandas.Index, преобразуем в список
                headers = headers.tolist()
                print(headers)
        self.table.setHorizontalHeaderLabels(headers)

        # Подстройка ширины столбцов по тексту заголовков
        font_metrics = QFontMetrics(self.table.horizontalHeader().font())
        for col in range(self.table.columnCount()):
            header_text = self.table.horizontalHeaderItem(col).text()
            header_width = font_metrics.horizontalAdvance(header_text) + 20  # 20 px — добавляем немного отступа
            self.table.setColumnWidth(col, header_width)

        # Настройка подгонки ширины столбцов
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Растянуть столбцы на всю ширину

    def draw_table(self, data: list):
        """Заполняет таблицу данными"""
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)

                # Выравниваем значения по центру
                item.setTextAlignment(Qt.AlignCenter)
