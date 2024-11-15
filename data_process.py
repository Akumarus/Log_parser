import pandas as pd

class DataProcess:
    def process_table(self, df, json):
        processed_df = self.process_byte_data(df, json)
        #processed_df  = pd.DataFrame(processed_rows.to_list())
        return processed_df

    def process_byte_data(self, df, json_data):
        # Словарь для хранения обработанных данных по каждому ID
        processed_tables = {}
        df = df.dropna()
        for _, row in df.iterrows():
            #if pd.isna(row["ID"]):
            #     continue

            id = int(row["ID"])

            # Проверяем, есть ли данные для текущего ID в JSON
            if str(id) in json_data:
                processed_data = {}
                for field in json_data[str(id)]["data"]:
                    byte_index = field["byte"]
                    var_name = field["variable"]
                    var_format = field["format"]
                    coefficient = field.get("coefficient", 1) or 1
                    offset = field.get("offset", 0) or 0

                    #print(f"byte_index:  {byte_index}" )
                    #print(f"var_name:    {var_name}" )
                    #print(f"var_format:  {var_format}" )
                    #print(f"coefficient: {coefficient}" )
                    #print(f"offset:      {offset}\n" )

                    if var_format == "Uint16" and isinstance(byte_index, str):
                        byte_i = list(map(int, byte_index.split('-')))
                        value = int(row.iloc[byte_i[0]]) * 256 + int(row.iloc[byte_i[1]])
                        value = value * coefficient + offset
                        #print(f"byte_i[0]:  {row[byte_i[0]]}")
                        #print(f"byte_i[1]:  {row[byte_i[1]]}")
                        #print(f"value:      {value}\n")

                    elif var_format == "Uint8":
                        value = int(row.iloc[byte_index])
                        value = value * coefficient + offset
                        #print(f"byte_index: {byte_index}\n")
                        #print(f"value:      {value}\n")
                    elif var_format == "Time":
                        value = row.iloc[byte_index]
                    else:
                        value = None

                    processed_data[var_name] = value

                # Добавляем обработанные данные в таблицу для текущего ID
                if id not in processed_tables:
                    processed_tables[id] = []
                processed_tables[id].append(processed_data)

        for id in processed_tables:
            processed_tables[id] = pd.DataFrame(processed_tables[id])

        return processed_tables