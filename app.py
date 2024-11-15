import tkinter as tk
from data_loader import DataLoader
from data_table import DataTable
from data_process import DataProcess

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Парсер таблицы")

        # Получаем размер экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width - 10}x{screen_height -10}")

        # Фрейм для кнопки
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side="top", fill="x")

        # Фреймы
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(side="left", fill="both", expand=True)

        self.data_loader = DataLoader()
        self.data_process = DataProcess()
        self.data_table = DataTable(self.table_frame)

        # Кнопки
        self.load_button = tk.Button(self.button_frame, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(side="left")

        self.parse_button = tk.Button(self.button_frame, text="Разделить ID", command=self.sort_table)
        self.parse_button.pack(side="left")

        self.save_button = tk.Button(self.button_frame, text="Сохранить", command=self.save_table)
        self.save_button.pack(side="left")

    def load_file(self):
        self.df = self.data_loader.load_file()
        if self.df is not None:
            self.data_table.display_data(self.df)

    def sort_table(self):
        json_config = self.data_loader.load_json()
        self.processed_df = self.data_process.process_table(self.df, json_config)
        self.data_table.display_sort_id(self.processed_df)

    def save_table(self):
        self.data_loader.save_file(self.processed_df)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()