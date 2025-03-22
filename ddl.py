import json
import pandas as pd
import duckdb


DB_FILE = 'my.db'

def create_tables():#функция создания таблиц
    try:
        # читаем содержимое файла 'queries/tables.sql', т.е. SQL-запросы для создания таблиц
        with open('queries/tables.sql') as f:
            tables_query = f.read()
        
         # Подключаемся к базе данных и выполняем SQL-запрос,т.е.создаём схему и таблицы
        with duckdb.connect(DB_FILE) as duck:
            duck.execute(tables_query)
        
        print("Tables created successfully")
    except Exception as e:
        print(e)#логирование ошибки, если что-то пошло не так
        #(это процесс записи информации о работе программы, который помогает отслеживать ошибки, 
        # анализировать выполнение кода и понимать, что происходит "под капотом)


def read_xl(sheet_name, columns_dict):
    #читаем лист из файла excel, указанного в качестве источника (patients.xlsx), присваиваем имя листу тоже самое, что и у листа в источнике
    temp_df = pd.read_excel(
        'source/patients.xlsx',
        sheet_name=sheet_name,
        usecols=columns_dict.keys()# выбираем только столбцы, выбранные из словаря
    ).rename(columns=columns_dict)#переименовываем столбцы, ориентируясь на названия в словаре
    return temp_df#возвращает датафрейм с выбранными столбцами


with open('tables.json') as f:#открываем json -файл
    tables_dict = json.load(f) #читаем содержимое json-файла и конвертируем содержимое в словарь Python


def insert_to_db(temp_df, tbl_name):#функция вставки данных из таблицы
    with duckdb.connect(DB_FILE) as duck:#открываем доступ к DuckDB
        duck.register('temp_table', temp_df)# регистрируем temp_df как временную таблицу в DuckDB
        duck.execute(f"""
            insert into{tbl_name}
            select * from temp_table
        """)# Вставляем данные из зарегистрированной таблицы в целевую таблицу

def create_views():#читаем вьюшку из файла views.sql и запускает ее в DuckDB
    with open('queries/views.sql') as f:
        views = f.read()#читаем вьюшку

    with duckdb.connect(DB_FILE) as duck:
        duck.execute(views)
        duck.commit()#подключаемся к DuckDB  и выполняем sql - запрос, указанный во вьюшке

    print("Views were successfully created")


def xl_etl(sheet_name, columns_dict, tbl_name):#выполняем ETL-процесс (Extract - экстракция, Transform - изменение, Load - загрузка) из листа Excel в DuckDB
    print(f"inserting data to {tbl_name}...")
    temp_df = read_xl(sheet_name, columns_dict)#читаем из листа Excel
    insert_to_db(temp_df, tbl_name)#вставляем данные в таблицу из листа Excel в DuckDB
    


def create_n_insert():    
    try:
        print('try entrypoint')
        with duckdb.connect(DB_FILE) as duck:
            duck.execute("select 1 from patients").fetchone()   # Пытаемся подключиться к DuckDB и проверяем существует ли таблица "patients"
    except:
        print('except entrypoint')
        create_tables()  # если таблица "patients" не существует, то создаём её
        for k, v in tables_dict.items():# загружаем данные из листов Excel в таблицы
            xl_etl(k, v["columns"], v["table_name"])
        print('data inserted successfully')

        create_views()#создаём вьюшки


create_n_insert()#вызываем функцию по созданию таблиц, если они не существуют и их заполняем из источника, SQL-вьюшек
