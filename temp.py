# importing library
from ast import While
from traceback import print_tb
import xlrd, re, numpy as np, string, xlsxwriter, xlwt, sys

a = [[2,1,5,2]]
b = [[6,6,437,7]]

np.save("temp/temp.npy",a)
x = np.load("temp/temp.npy")
print(x)
