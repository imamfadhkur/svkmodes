from dis import dis
import numpy as np
from random import random
import xlrd, re

dm = {}
cluster = ["ekonomi,moneter","ekonomi,mikro"]
key2 = ["ekonomi,moneter","ekonomi,mikro"]
for i in range(len(cluster)):
    for j in range(len(key2)):
          key = cluster[i]+";"+key2[j]
          dm[key] = [[2,3,44,2,1,22,4],[2,3,23,4],["saya,saja,selingkuh"]]
x = dm.get('ekonomi,moneter;ekonomi,moneter')
# print(x)
item = xlrd.open_workbook("write_data.xlsx")    # membuka file external
data = item.sheet_by_index(0) 
X = {}                        # membuat properti container untuk menyimpan fitur
for n in range(data.nrows):              # perulangan untuk sebanyak fitur, dikurangi 1 karena dibaca perkolom sedangkan kolom pertama bukan fitur
    fitur = []                          # variabel sementara untuk menyimpan masing-masing fitur
    for m in range(data.ncols-1):            # perulangan sebanyak bukunya
        fitur.append(data.cell_value(rowx=n,colx=(m+1)).split(","))
    X[data.cell_value(rowx=n,colx=0)] = fitur    # memecah isi fitur dan menjadikannya sebagai list dengan pemisah yaitu tanda koma
# print(len(X.get(1)))
def getList(dict):
    list = []
    x = {}
    for key in dict.keys():
        # print(key)
        pass
    # y = 1,"[ekonomi,coreldraw]"
    # x[y] = [["ekonomi"]]
    # print(dict.get(1))
    return [ v for k,v in dict.items() if 3 in k]
    # if dict.get(4) != None:
    #     print("ada")
    # else:
    #     print("tidak ada")
          
    # return list
      
# Driver program
dict = {1.0:'Geeks', 2:'for', 3:'geeks'}
x = {
    (3.0, 1.0): 0.31, 
    (3.0, 2.0): 0.32, 
    (3.0, 3.0): 0.33, 
    (3.0, 4.0): 0.34, 
    (1.0, 1.0): 0.11, 
    (1.0, 2.0): 0.12, 
    (1.0, 3.0): 0.13, 
    (1.0, 4.0): 0.14
    }
d = max(x, key=x.get)
# print(type(d))
a = 0.10416666666666667
b = 0.1388888888888889
if a > b:
    print("iya")
exit()
satu = 1.0
du = 4.0
y = (satu,du)
x = ((satu,"",du))
# print(y)
# print(x)
ages = {
    'Matt': 30,
    'Katie': 29,
    'Nik': 31,
    'Jack': 43,
    'Alison': 32,
    'Kevin': 38
}
max_value = max(ages)
imax_value = max(ages.values())
amax_value = max(ages, key=ages.get)
# print(amax_value)
# print(np.intersect1d(X.get(1)[0],X.get(2)[0]))
# for item in range(X.nrows):
#     print(item)



# CARA MENGAKSES KEY BY VALUE DAN ATAU SEBALIKNYA
my_dict ={"j,a,v,a":100, "python":112, "c":11}

key_list = list(my_dict.keys())
val_list = list(my_dict.values())

position = val_list.index(100)
for key in key_list:
    pass
    # print(my_dict[key])
# print(key_list)
# print(val_list)
# print(key_list[position].split(","))


# KEY DICTIONARY MENGGUNAKAN ANGKA DAN TEKS, INT OR FLOAT DAN STRING
my_dict ={(3.0, 'ekonomi, corel draw'): 0.10185185185185185, (3.0, 2.0): 0.10185185185185185, (3.0, 3.0): 0.0, (3.0, 4.0): 0.1111111111111111, (3.0, 5.0): 0.1388888888888889, (3.0, 6.0): 0.14814814814814814, (3.0, 7.0): 0.1388888888888889, (3.0, 8.0): 0.16666666666666666, (3.0, 9.0): 0.14814814814814814}
key_list = list(my_dict.keys())
val_list = list(my_dict.values())
for key in key_list:
    print(type(key[1]))


# CARA TERBAIK UNTUK MENGGUNAKAN REPLACE
a = '[ekonomi, corel draw]'
b = a.replace('[','').replace(']','')

print(type(a))
print(a)
print(type(b))
print(b)
print(b.split(","))