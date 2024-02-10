import os
import sqlite3

# الحصول على مسار وحدة التخزين الداخلية
internal_storage = os.path.expanduser("~")

# اسم المجلد
folder_name = "my_database_folder"

# الحصول على مسار المجلد
folder_path = os.path.join(internal_storage, folder_name)

# إنشاء المجلد إذا لم يكن موجودًا بالفعل
os.makedirs(folder_path, exist_ok=True)

# المسار الكامل لملف قاعدة البيانات
database_path = os.path.join(folder_path, "my_database.db")

# إنشاء اتصال بقاعدة البيانات
conn = sqlite3.connect(database_path)

# إنشاء جدول في قاعدة البيانات
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS employees (id INT, name TEXT, age INT)")

# إضافة بيانات افتراضية
cursor.execute("INSERT INTO employees VALUES (1, 'John Doe', 30)")
cursor.execute("INSERT INTO employees VALUES (2, 'Jane Smith', 25)")

# حفظ التغييرات وإغلاق اتصال قاعدة البيانات
conn.commit()
conn.close()

print("تم إنشاء قاعدة البيانات بنجاح في المجلد:", folder_path)
print("مسار قاعدة البيانات:", database_path)
