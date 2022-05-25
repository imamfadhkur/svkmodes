# importing library
from ast import While
from traceback import print_tb
import xlrd, re, numpy as np, string, xlsxwriter, xlwt, sys

# initial cluster method
def gicca(X,k): # X = data buku beserta keyword, k = jumlah cluster
    centers = [] # variabel yang digunakan untuk menyimpan center
    dens = [] # variabel yang digunakan untuk menyimpan informasi density dari setiap buku
    # awal code untuk mencari cluster center pertama
    for i in range(len(X[0])): # untuk looping data 
        dens_fitur = 0      # membuat variabel kosongan untuk menampung nilai density tiap fitur
        for m in range(len(X)): # loop 1 kali
            for n in range(len(X[0])): # loop 3585 kali
                irisan_vajxi = np.intersect1d(X[m][i], X[m][n])     # mencari irisan dari fitur pada objek ke-i dengan fitur pada objek ke-n
                gabungan_vajxi = np.union1d(X[m][i], X[m][n])   # mencari gabungan dari fitur pada objek ke-i dengan fitur pada objek ke-n
                dens_fitur += len(irisan_vajxi)/len(gabungan_vajxi)     # untuk mencari density yaitu dengan cara membagi irisan dengan union
        dens.append(dens_fitur/(len(X[0]))) # setiap nilai dens_fitur dibagi banyaknya objek
    centers.append(dens.index(max(dens)))   # menambahkan elemen center pertama
    # batas code batas mencari cluster center pertama
    
    # awal code mencari cluster center kedua dan selanjutnya
    if k > 1:
        for jumlah_cluster in range(k-1):   # k dikurangi 2 karena: 1. nilai k pertama telah dicari yaitu pada cluster center pertama, 2. karena looping for memulai loop dari angka 0, maka harus dikurangi 1 lagi karena nilai k tidak mengawali sebagai index
            print("K:",jumlah_cluster)
            dm = []     # membuat variabel kosongan untuk nilai dm
            for i in range(len(X[0])): # loop sebanyak bukunya (3585)
                dmd = 0     # membuat variabel kosongan untuk menyimpan nilai dm dari tiap fitur
                for m in range(len(X)): # untuk melooping tiap fitur yang ada
                    irisan_vasxi = np.intersect1d(X[m][i], X[m][centers[jumlah_cluster]])     # mencari irisan dari fitur pada objek ke-i dengan center
                    gabungan_vasxi = np.union1d(X[m][i], X[m][centers[jumlah_cluster]])      # mencari gabungan dari fitur pada objek ke-i dengan center
                    dmd += 1-(len(irisan_vasxi)/len(gabungan_vasxi))    # penggabungan semua nilai dm dari semua fitur
                dm.append(dmd*dens[i])      # menyimpan nilai dm pada variabel dm
            
            sort_dm = dm.copy()     # proses copy isi dm ke sort_dm,
            sort_dm.sort()  # mengurutkan isi dari dm, agar dapat dengan mudah mencari nilai maksimalnya ketika nilai maksimal sudah mencari center

            # PROSES MENCARI NILAI DM TERBESAR DENGAN TIDAK MENGULANGI OBJEK YANG TELAH MENJADI CENTER
            if dm.index(max(dm)) in centers:    # melakukan pengecekan, apakah nilai maksimal dari dm yang tidak diurutkan indeksnya sudah tercatat pada centers.
                loop = True     # variabel tambahan untuk melakukan perulangan
                n = 0   # variabel yang digunakan untuk mencari nilai index terakhir ke depan, dst hingga menemukan nilai maksimal dari objek yang tidak ada pada centers
                while loop == True:   # perulangan yang mengecek hingga menemukan nilai dm terbesar pada objek yang tidak terdapat pada centers
                    n += 1      # dengan increasing, maka di setiap perulangan akan menambahkan nilai n yang digunakan untuk menjadi kunci letak dm yaitu yang menggunakan index
                    temp = sort_dm[len(sort_dm)-n]   # variabel temp menyimpan value dari dm yang terbesar
                    if dm.index(temp) in centers:   # jika value dari dm terbesar index nya telah terdapat pada centers, maka objek tersebut telah tercatat sebagai centers, jika tidak maka belum
                        pass
                    else:   # else - jika nilai dm yang terbesar indexnya tidak terdapat pada centers,
                        centers.append(dm.index(temp))  # maka index tersebut akan dicatat sebagai centers - append().
                        loop = False    # looping pun selesai
            else:   # jika nilai di yang terbesar indexnya tidak terdapat pada centers.
                centers.append(dm.index(max(dm)))  # maka index tersebut akan dicatat sebagai centers selanjutnya.
            print(dm)
    return centers
    # batas code mencari cluster center kedua dan selanjutnya

# update cluster center method
def hafsm():
    return True

# clustering method
def svkmodes(X,centers):
    himp_cluster = []

    # proses mencari dm antara center dengan object
    for jumlah_cluster in centers:   # k dikurangi 2 karena: 1. nilai k pertama telah dicari yaitu pada cluster center pertama, 2. karena looping for memulai loop dari angka 0, maka harus dikurangi 1 lagi karena nilai k tidak mengawali sebagai index
        dm = []     # membuat variabel kosongan untuk nilai dm
        for i in range(len(X[0])): # loop sebanyak bukunya (3585)
            dmd = 0     # membuat variabel kosongan untuk menyimpan nilai dm dari tiap fitur
            for m in range(len(X)): # untuk melooping tiap fitur yang ada
                irisan_vasxi = np.intersect1d(X[m][i], X[m][centers[jumlah_cluster]])     # mencari irisan dari fitur pada objek ke-i dengan center
                gabungan_vasxi = np.union1d(X[m][i], X[m][centers[jumlah_cluster]])      # mencari gabungan dari fitur pada objek ke-i dengan center
                dmd += 1-(len(irisan_vasxi)/len(gabungan_vasxi))    # penggabungan semua nilai dm dari semua fitur
            dm.append(dmd*dens[i])      # menyimpan nilai dm pada variabel dm
    return centers

# main method
def run(item,k):
    # PROSES MEMINDAHKAN DATA KEYWORD KEDALAM SEBUAH VARIABEL UNTUK PROSES SELANJUTNYA
    item = xlrd.open_workbook(item)     # membuka file external
    X = item.sheet_by_index(0)      # membaca file berdasarkan sheet pertama
    fiturs = []     # membuat variabel container untuk semua fitur
    for m in range(X.ncols-1):      # perulangan untuk sebanyak fitur, dikurangi 1 karena dibaca perkolom sedangkan kolom pertama bukan fitur
        fitur = []      # variabel sementara untuk menyimpan masing-masing fitur
        for n in range(X.nrows):        # perulangan sebanyak bukunya
                fitur.append(X.cell_value(rowx=n,colx=(m+1)).split(","))    # menyimpan fitur pada variabel sementara
        fiturs.append(fitur)      # setelah salah satu fitur pada satu objek telah selesai te-record, maka disimpan pada variabel container (variabel untuk semua fitur)
    
    # PROSES CLUSTERING
    initial_cluster_center = gicca(fiturs,k)    # variabel fiturs merupakan list berbentuk 3 dimensi, dengan isi yaitu fitur. k merupakan variabel untuk menampung jumlah cluster
    clustering_svkmodes = svkmodes(fiturs,initial_cluster_center)
    return clustering_svkmodes

data_file = "write_data.xlsx"      # bentuk data file excel yg berisi 2 kolom, kolom = A id buku, kolom B = daftar keyword yang dipisahkan dengan tanda koma. toy data ukuran 9*2
jumlah_cluster = 3      # variabel untuk menampung jumlah cluster 
data = run(data_file, jumlah_cluster)   # memanggil metode run dengan membawa nama file dan jumlah cluster, lalu disimpan pada variabel data
print(data)     # menampilkan apa hasil dari perhitungan