#import sqlite3
#import os-sys
from pywebio.platform.flask import webio_view
from flask import Flask
import pywebio
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *


app = Flask(__name__)

if __name__ == '__main__':
    
    popup("hello")

