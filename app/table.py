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
    
    def delete_all_table(tab_widget):
        count = tab_widget.count()
        for i in range(count - 1, -1, -1):
            current_widget = tab_widget.widget(i)
            tab_widget.removeTab(i)
            current_widget.deleteLater()

    def add_table_tab(self, df, tab_widget, tab_name="All logs"):
        """Добавляет вкладку с таблицей"""
        header_name = df.columns
        rows, columns = df.shape
        df_list = df.values.tolist()

        # Создаем фрейм с таблицей
        self.table_frame = TableFrame(self)
        self.table_frame.set_table_size(rows, columns, header_name)
        self.table_frame.draw_table(df_list)

        # Добавляем вкладку
        tab_widget.addTab(self.table_frame, tab_name)

    def set_table_size(self, rows: int, columns: int, headers):
        import pandas as pd
        """Задает размеры таблицы и опционально устанавливает заголовки столбцов."""
        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        if headers is not None and len(headers) > 0:  # Проверка на наличие заголовков
            if isinstance(headers, pd.Index):  # Если это pandas.Index, преобразуем в список
                headers = headers.tolist()
                #print(headers)
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
