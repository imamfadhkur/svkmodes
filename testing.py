import xlrd
import numpy as np
# np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
import sys
# sys.exit()

item = xlrd.open_workbook("write_data.xlsx")
X = item.sheet_by_index(0)
data = np.array([[]])
nparray = np.array([])
for m in range(X.ncols-1):
      for n in range(X.nrows):
            pass
            # print(X.cell_value(rowx=n,colx=(m+1)).split(","))
            # data = np.append(data,X.cell_value(rowx=n,colx=(m+1)).split(","),axis=0)
      # data.append(nparray)
# print(data)
# print("=================")
# print(nparray[0][0])
# exit()
# step_n = 10
# fitur = []
# steps = np.array([])
# print(steps)
fiturs = []
for m in range(X.ncols-1):
      fitur = []
      for n in range(X.nrows):
            # step = np.array(X.cell_value(rowx=n,colx=(m+1)).split(","),dtype=object)
            fitur.append(X.cell_value(rowx=n,colx=(m+1)).split(","))
            # print(step,step1)
            # print(len(np.intersect1d(step, step1)))
            # steps = np.append(steps, step, axis=0)
            # print(steps)
            # exit()
            # data = np.append(data,[X.cell_value(rowx=n,colx=(m+1))],axis=0)
      fiturs.append(fitur)
print(fiturs[0][1],fiturs[0][2])
print(len(np.intersect1d(fiturs[0][1], fiturs[0][2]))) # intersect1d (untuk mencari IRISAN DARI DUA LIST)
# for n in range(step_n-1):
#     step = np.array([[3,4]])
#     steps = np.append(steps, step, axis=0)
# steps = np.delete(steps,1,0)
# print(steps)

arr1 = np.array([
  ["ekonomi","moneter"],
  ["ekonomi","mikro"],
  ["ekonomi"],
  ["coreldraw"],
  ["kepemimpinan","manusia"]],dtype=object)
arr2 = np.array(["ekonomi","mikro"],dtype=object)
newarr = np.intersect1d(arr2, arr1[1])
# data = [arr1,arr2]
# print(arr1)
# print(len(newarr))
# print(arr1)