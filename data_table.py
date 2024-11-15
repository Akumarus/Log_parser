import pandas as pd
import tkinter as tk
from tkinter import ttk

class DataTable:
    def __init__(self, perent):
        self.notebook = ttk.Notebook(perent)
        self.notebook.pack(expand=True, fill="both")

        self.tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_frame, text=f"Таблица {len(self.notebook.tabs()) + 1}")

        # Создание таблицы
        self.columns = ["Время", "ID", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7"]
        self.table = ttk.Treeview(self.tab_frame, columns=self.columns, show="headings")
        self.table.pack(side="left", fill="both", expand=True)

        # Настройка заголовков таблицы
        for col in self.columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=50)

        # Создание полосы прокрутки
        scrollbar = tk.Scrollbar(self.tab_frame, command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.config(yscrollcommand=scrollbar.set)

    def display_data(self, df):
        # Очистка таблицы и добавление новых данных
        for row in self.table.get_children():
            self.table.delete(row)
        for _, row in df.iterrows():
            self.table.insert("", "end", values=list(row))

    def display_sort_id(self, processed_df):
        for id, df in processed_df.items():
            # Создаем вкладку для каждого уникального ID
            id_frame = ttk.Frame(self.notebook)
            self.notebook.add(id_frame, text=f"ID{id}")

            # Заменяем пробелы в названиях столбцов
            columns = [col.replace(" ", "_") for col in df.columns]

            # Создаем виджет Treeview для отображения данных
            table = ttk.Treeview(id_frame, columns=columns, show="headings")
            table.pack(side="left", fill="both", expand=True)

            # Настройка заголовков таблицы
            for col in columns:
                table.heading(col, text=col)
                table.column(col, anchor="center",)

            # Создание полосы прокрутки
            scrollbar = tk.Scrollbar(id_frame, command=table.yview)
            scrollbar.pack(side="right", fill="y")
            table.config(yscrollcommand=scrollbar.set)

            # Заполнение таблицы данными
            for _, row in df.iterrows():
                table.insert("", "end", values=row.tolist())
 