import pandas as pd
import json

with open("log.json", "r", encoding="utf-8") as f:
    json_structure = json.load(f)

csv_data = pd.read_csv("canbus.csv", sep=";", header=None, names=["Время", "ID"] + [f"Байт_{i}" for i in range(8)])

#class DataProcess:
#    def process_table(self, df, json):
#        processed_rows = df.apply(lambda row: self.process_byte_data(row, json), axis=1)
#        processed_df  = pd.DataFrame(processed_rows.to_list())
#        return processed_df
    
def process_byte_data(df, json_data):
    # Словарь для хранения обработанных данных по каждому ID
    processed_tables = {}

    for _, row in df.iterrows():
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
                elif var_format == "Uint8":
                    value = int(row.iloc[byte_index])
                    value = value * coefficient + offset
                elif var_format == "Time":
                    value = row.iloc[byte_index]
                else:
                    value = None
                    
#        processed_data = {}
#        json_keys = json_data.keys()
#        for key in json_keys:
#            for field in json_data[key]["data"]:
#                byte_index = field["byte"]
#                var_name = field["variable"]
#                var_format = field["format"]
#                coefficient = field.get("coefficient", 1) or 1
#                offset = field.get("offset", 0) or 0
#
#                #if var_name == "ID":
#                #    continue
#                print(f"byte_index:  {byte_index}" )
#                print(f"var_name:    {var_name}" )
#                print(f"var_format:  {var_format}" )
#                print(f"coefficient: {coefficient}" )
#                print(f"offset:      {offset}\n" )
#
#                if var_format == "Uint16" and isinstance(byte_index, str):
#                    # Обработка двухбайтового значения, если byte_index это строка диапазона, например "0-1"
#                    byte_i = list(map(int, byte_index.split('-')))
#                    value = int(row.iloc[byte_i[0]]) * 256 + int(row.iloc[byte_i[1]])
#                    value = value * coefficient + offset
#                    #print(f"byte_i[0]:  {row[byte_i[0]]}")
#                    #print(f"byte_i[1]:  {row[byte_i[1]]}")
#                    #print(f"value:      {value}\n")
#                elif var_format == "Uint8":
#                    value = int(row.iloc[byte_index])
#                    value = value * coefficient + offset
#                    #print(f"byte_i:     {row[byte_index]}")
#                    #print(f"value:      {value}\n")
#                elif var_format == "Time":
#                    value = row.iloc[byte_index]
#                else:
#                    value = None
#
#                processed_data[var_name] = value
#
#        return processed_data
    


csv_data = csv_data.dropna()
processed_rows = process_byte_data(csv_data, json_structure)
#processed_df = pd.DataFrame(processed_rows.to_list())
print(processed_rows)
#
#print(processed_df)
#print(csv_data)