import os
import json
import pandas as pd
from tkinter import filedialog

csv_data = pd.read_csv("canbus.csv", sep=";", header=None, names=["Время", "ID"] + [f"Байт_{i}" for i in range(8)])

class DataLoader:
    def load_file(self):
        df = None
        file_path = filedialog.askopenfilename(filetypes=[(".CSV", ".csv")])
        if file_path:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path, sep=";", header=None, names=["Время", "ID"] + [f"Байт_{i}" for i in range(8)])

                # Удаляет все строки с NaN
                df = df.dropna()  
                for col in df.select_dtypes(include=['float64']):
                    df[col] = df[col].apply(lambda x: int(x) if isinstance(x, float) and not pd.isna(x) and x.is_integer() else x)       
        
        return df
    
    def load_json(self):
        with open("log.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def save_file(self, tables):
        script_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(script_path, "saved_tables")
        os.makedirs(folder_path, exist_ok=True)

        for unique_id, id_table in tables.items():
            # Сохраняем каждую таблицу в отдельный CSV-файл
            print("id: ", unique_id)
            print("id_table: ", id_table)
            id_table = id_table.astype(str)
            file_path = os.path.join(folder_path, f"table_id_{unique_id}.csv")
            id_table.to_csv(file_path, encoding='utf-8-sig', index=False, sep=';')
            #id_table.to_excel(file_path, index=False, engine='openpyxl')
            print(f"Сохранена таблица для ID {unique_id} в файл: {file_path}")

