import json
import pandas as pd

class JsonHandler:
    
    @staticmethod
    def load_json():
        with open("log.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def log_splite(json, df : pd.DataFrame):
        processed_tables = {}
        for _, row in df.iterrows():
            id = int(row["ID"])
            
            # Проверяем есть ли данные для текущего ID в JSON
            if str(id) in json:
                processed_data = {}
                for var in json[str(id)]["data"]:
                    var_index  = var["byte"]
                    var_name   = var["variable"]
                    var_format = var["format"]
                    var_coeff  = var.get("coefficient", 1) or 1
                    var_offset = var.get("offset", 0) or 0

                    if var_name == "Резерв":
                        continue

                    if var_format == "Uint16" and isinstance(var_index, str):
                        index = list(map(int, var_index.split('-')))
                        value = int(row.iloc[index[0]]) * 256 + int(row.iloc[index[1]])
                        value = value * var_coeff + var_offset

                    elif var_format == "Uint8":
                        index = var_index
                        value = int(row.iloc[index])
                        value = value * var_coeff + var_offset

                    elif var_format == "Time":
                        index = var_index
                        value = row.iloc[index]

                    else:
                        value = None

                    processed_data[var_name] = value

                if id not in processed_tables:
                    processed_tables[id] = []
                processed_tables[id].append(processed_data)

        for id in processed_tables:
            processed_tables[id] = pd.DataFrame(processed_tables[id])

        return processed_tables