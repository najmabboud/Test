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

if __name__ == '__main__':
    
    popup("hello")

