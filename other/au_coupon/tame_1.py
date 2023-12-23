"""
"""
import poplib
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from my_module import my_function, mail_receiving_pop3
import random
import chromedriver_binary
import time
import openpyxl
import win32com
import xl
import re
import subprocess
import chardet
from my_module import trashmail_mass_production
from selenium.webdriver.common.alert import Alert
from pykakasi import kakasi
from ctypes import windll
import pyautogui
import time
import threading
import sys
import signal
import pyautogui

EXCEL = r'C:\Users\YUTANAO\Dropbox\予定表.xlsx'
subprocess.Popen(['<strong>start</strong>', EXCEL], shell=True)