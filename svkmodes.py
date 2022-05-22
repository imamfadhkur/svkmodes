# importing library
from traceback import print_tb
import xlrd
import re
import string
import xlsxwriter
import xlwt
import sys
# sys.exit()

# initial cluster method
def gicca(X,k): # X = data buku beserta keyword, k = jumlah cluster
    centers = [] # variabel yang digunakan untuk menyimpan center
    dens = [] # variabel yang digunakan untuk menyimpan informasi density dari setiap buku
    # awal code untuk mencari cluster center pertama
    for i in range(X.nrows): # untuk data real akan di loop sebanyak 3585 kali
        dens_fitur = 0
        for m in range((X.ncols)-1): # loop 1 kali
            for n in range(X.nrows): # loop 3585 kali
                irisan_vajxi = 0
                # print(X.cell_value(rowx=i,colx=(m+1)),"|",X.cell_value(rowx=n,colx=(m+1)))
                for vajxi in X.cell_value(rowx=i,colx=(m+1)).split(","): # melooping tiap keyword pada satu cell
                    if vajxi in X.cell_value(rowx=n,colx=(m+1)).split(","):
                        irisan_vajxi += 1
                dens_fitur += irisan_vajxi/(len(X.cell_value(rowx=i,colx=(m+1)).split(","))+len(X.cell_value(rowx=n,colx=(m+1)).split(","))-irisan_vajxi)
        dens.append(dens_fitur/(X.nrows+1)) # setiap nilai dens_fitur dibagi banyaknya objek
    centers.append(dens.index(max(dens)))
    # batas code batas mencari cluster center pertama
    
    # awal code mencari cluster center kedua
    dm = []
    for i in range(X.nrows): # loop sebanyak bukunya (3585)
        dmd = 0
        irisan_vasxi = 0
        for m in range((X.ncols)-1): # 
            for vasxi in X.cell_value(rowx=centers[0],colx=(m+1)).split(","): # untuk melooping tiap keyword dari center
                if vasxi in X.cell_value(rowx=i,colx=(m+1)).split(","):
                    irisan_vasxi += 1
            dmd += 1-(irisan_vasxi/(len(X.cell_value(rowx=centers[0],colx=(m+1)).split(","))+len(X.cell_value(rowx=i,colx=(m+1)).split(","))-irisan_vasxi))
        dm.append(dmd*dens[i])
    centers.append(dm.index(max(dm)))
    # batas code mencari cluster center kedua

    # awal code mencari cluster center ketiga dst.
    if k > 2:
        for jumlah_cluster in range(k-2):            
            minxm = len(centers)-1
            dm = []
            for i in range(X.nrows):
                dmd = 0
                irisan_vasxi = 0
                for m in range((X.ncols)-1):
                    for vasxi in X.cell_value(rowx=minxm,colx=(m+1)).split(","):
                        if vasxi in X.cell_value(rowx=i,colx=(m+1)).split(","):
                            irisan_vasxi += 1
                    dmd += 1-(irisan_vasxi/(len(X.cell_value(rowx=minxm,colx=(m+1)).split(","))+len(X.cell_value(rowx=i,colx=(m+1)).split(","))-irisan_vasxi))
                dm.append(dmd*dens[i])
            print(dm.index(max(dm)))
            
            # if dm.index(max(dm)) in centers:
            #     print("ada di centers")
            #     nilai_terbesar = 0
            #     for nilai_dm in range(len(dm)-1):
            #         if dm[nilai_dm] > dm[nilai_dm+1]:
            #             nilai_terbesar = dm[nilai_dm]
            #         else:
            #             nilai_terbesar = dm[nilai_dm+1]
            # else:
            #     centers.append(dm.index(max(dm)))
            # exit()
            # centers.append(dm.index(max(dm)))
    # batas code mencari cluster center ketiga dst.

    return centers

# update cluster center method
def hafsm():
    return True

# clustering method
def svkmodes(X,k):
    return True

# main method
def run(item,k):
    item = xlrd.open_workbook(item)
    X = item.sheet_by_index(0)
    # menentukan insial cluster center
    initial_cluster_center = gicca(X,k)
    return initial_cluster_center

data_file = "write_data.xlsx" # bentuk data file excel yg berisi 2 kolom, kolom = A id buku, kolom B = daftar keyword yang dipisahkan dengan tanda koma. toy data ukuran 9*2

jumlah_cluster = 4
data = run(data_file, jumlah_cluster)
print(data)