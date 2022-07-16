# importing library
from ast import While
from traceback import print_tb
import xlrd, re, numpy as np, string, xlsxwriter, xlwt, sys

a = []
b = [[1,2,3],[34,34,52,2],[2314,4,32]]
for i in b:
    a.append(tuple(i))
a = tuple(a)
print(a)