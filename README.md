#  Создание окружения conda с Python 3.12
1. Откройте терминал или командную строку.
2. Выполните следующую команду для создания нового окружения  conda с Python 3.12:
```sh
conda create --name myenv python=3.12
```
3. Активируйте созданное окружение :
```sh
conda activate myenv
```
4. Установите зависимости из requirements.txt:
```sh
pip install -r requirements.txt
```
5. Запустить Python-скрипт
```sh
python app/app.py
