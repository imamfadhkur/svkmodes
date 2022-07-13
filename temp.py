# importing library
from ast import While
from traceback import print_tb
import xlrd, re, numpy as np, string, xlsxwriter, xlwt, sys

a = ['corel draw']
b = ['corel draw', 'ekonomi', 'sasa']
check = all(item in b for item in a)
# if check == True:
#     print("ya")
a.extend(b)
print(a)