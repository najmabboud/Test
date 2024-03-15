#import sqlite3
#import os
import pysqlite3
from pywebio.platform.flask import webio_view
from flask import Flask
import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *


app = Flask(__name__)

def create_database():
    

    # الاتصال بقاعدة البيانات أو إنشاؤها إذا لم تكن موجودة
    conn = sqlite3.connect('users.db')

    # إنشاء جدول "user" إذا لم يكن موجودًا
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT,
                       email TEXT,
                       password TEXT)''')
    conn.commit()

    # إغلاق الاتصال بقاعدة البيانات
    conn.close()
    popup("yes")


app.add_url_rule('/','main',webio_view(create_database)),





if __name__ == '__main__':
    app.run(port=1234)
    
    popup("hello")

