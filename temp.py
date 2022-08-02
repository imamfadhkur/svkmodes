# importing library
from ast import While
from traceback import print_tb
import xlrd, re, numpy as np, string, xlsxwriter, xlwt, sys

b = {
    (1,2,3): [[3,3,1,3,4,52,2],[8,9,6,4],[3,6,8]],
    (1,7,4): [[3,2,1,45,4,52,2],[8,9,6],[3,7,8]]
}
a = list(b.keys())
a = a[len(a)-1]
c = list(b.values())
c = c[len(c)-1]
d = [9,2,1,3]
print("len:",len(d))
for i in range(len(d)):
    print(i)
    