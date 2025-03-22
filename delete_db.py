import os

db_file = "my.db"

if os.path.exists(db_file):
    os.remove(db_file)
    print("База данных удалена ✅")
else:
    print("Файл my.db не найден ❌")

