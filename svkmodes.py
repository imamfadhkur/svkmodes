# importing library
from ast import While
from traceback import print_tb
import xlrd, re, numpy as np, string, xlsxwriter, xlwt, sys

class SVKModes:
    def __init__(self,nama_file,k):             # saat pertama kali class dipanggil maka file akan langsung di proses
        self.k = k                              # inisialisasi properti k (jumlah clustering)
        self.semua_dm = {}                      # digunakan untuk menyimpan nilai dm dari tiap cluster ke tiap objek
        self.centers_and_member = {}            # properti yang digunakan untuk menyimpan semua informasi centroid dan member nya pada tiap iterasi
        self.dens = {}                          # properti yang digunakan untuk menyimpan informasi density dari setiap buku
        self.X = {}                             # properti yang digunakan untuk menyimpan informasi data object dan keywordnya, berisi key yaitu object nya, dan value nya yaitu keyword nya
        
        item = xlrd.open_workbook(nama_file)    # membuka file di directory saat ini 
        data = item.sheet_by_index(0)           # membaca file berdasarkan sheet pertama
        
        # PROSES MEMINDAHKAN DATA KEYWORD KEDALAM SEBUAH VARIABEL UNTUK PROSES SELANJUTNYA
        for n in range(data.nrows):             # perulangan sebanyak baris pada excel dengan tujuan untuk memfilter data
            fitur = []                          # variabel sementara untuk menyimpan informasi satu fitur
            for m in range(data.ncols-1):       # perulangan sebanyak fitur yang ada
                fitur.append(data.cell_value(rowx=n,colx=(m+1)).split(", "))    # memecah isi fitur dan menjadikannya sebagai list dengan pemisah yaitu tanda koma
            self.X[data.cell_value(rowx=n,colx=0)] = fitur                      # setelah satu fitur pada satu objek telah selesai te-record, maka disimpan pada variabel utama
        
        # AWAL PROSES UNTUK MENCARI DENSITY
        for i in self.X.keys():                     # perulangan sebanyak key yang ada, dengan nilai i yaitu tiap key
            dens_fitur = 0                          # membuat variabel kosongan untuk menampung nilai density tiap fitur
            for m in range(len(self.X.get(1))):     # looping sebanyak fitur yang ada
                for n in self.X.keys():             # looping semua objek yang ada (key merupakan object pada properti X)
                    irisan_vajxi = np.intersect1d(self.X.get(i)[m], self.X.get(n)[m])     # mencari irisan dari fitur pada objek ke-i dengan fitur pada objek ke-n
                    gabungan_vajxi = np.union1d(self.X.get(i)[m], self.X.get(n)[m])       # mencari gabungan dari fitur pada objek ke-i dengan fitur pada objek ke-n
                    dens_fitur += len(irisan_vajxi)/len(gabungan_vajxi)                   # untuk mencari density yaitu dengan cara membagi irisan dengan union
            self.dens[i] = dens_fitur/(len(self.X))                              # nilai density dari tiap fitur dibagi banyaknya objek
        # AKHIR PROSES UNTUK MENCARI DENSITY
        
    def calc_and_save_dm(self,Xm):                      # fungsi yang digunakan untuk menghitung dan menyimpan dm
        Dm_dens = {}                                    # membuat variabel kosongan untuk menyimpan nilai Dm yang dikali dengan dens dari cluster tertentu kepada semua item. perlu di ketahui bahwa untuk mencari centroid yang diperlukan ialah dm*dens, dm != dm*dens
        if type(Xm) != list:                            # untuk mengecek apakah Xm (centroid) bukan list, karena jika berbentuk list yaitu berarti centroid nya bukan lah object yang ada, melainkan object baru yang hanya berisi keyword
            for i in self.X.keys():                     # loop sebanyak objeknya
                dmd = 0                                 # membuat variabel kosongan untuk menyimpan nilai dm dari masing-masing fitur (dissimiliarity measure)
                for m in range(len(self.X.get(1))):       # untuk melooping tiap fitur yang ada
                    irisan_vasxi = np.intersect1d(self.X.get(Xm)[m], self.X.get(i)[m])      # mencari irisan antara centroid dengan fitur pada objek ke-i
                    gabungan_vasxi = np.union1d(self.X.get(Xm)[m], self.X.get(i)[m])        # mencari gabungan antara centroid dengan fitur pada objek ke-i
                    dmd += 1-(len(irisan_vasxi)/len(gabungan_vasxi))                        # penggabungan semua nilai dissimiliarity measure dari semua fitur
                Dm_dens[Xm,i] = dmd*self.dens.get(i)                                        # menyimpan nilai dissimiliarity measire pada variabel Dm
                self.semua_dm[Xm,i] = dmd                                                   # menyimpan informasi Dm ke properti penampung utama, yaitu semua_dm yang digunakan untuk menyimpan semua dm dari tiap centroid ke tiap object. perlu di ketahui bahwa untuk mencari centroid yang diperlukan ialah dm*dens, dm != dm*dens
        else:                                           # jika centroid adalah object baru, yang hanya berisi keyword, maka masuk bagian else sini
            for i in self.X.keys():                     # loop sebanyak object
                dmd = 0                                 # membuat variabel kosongan untuk menyimpan nilai dissimiliarity measure dari tiap fitur dari salah satu object ke tiap fitur dari tiap object
                for m in range(len(self.X.get(1))):     # untuk melooping tiap fitur yang ada
                    irisan_vasxi = np.intersect1d(Xm, self.X.get(i)[m])    # mencari irisan antara centroid dengan fitur pada objek ke-i
                    gabungan_vasxi = np.union1d(Xm, self.X.get(i)[m])      # mencari gabungan antara centroid dengan fitur pada objek ke-i
                    dmd += 1-(len(irisan_vasxi)/len(gabungan_vasxi))       # penggabungan semua nilai dissimiliarity measure dari semua fitur
                Dm_dens[Xm,i] = dmd*self.dens.get(i)                       # menyimpan nilai dissimiliarity measure pada variabel Dm
                self.semua_dm[Xm,i] = dmd                                  # menyimpan informasi Dm ke properti penampung utama, yaitu semua_dm yang digunakan untuk menyimpan semua dm dari tiap centroid ke tiap object
        return Dm_dens                                                     # mengembalikan nilai Dm, tujuan dari fungsi ini yaitu digunakan untuk mengembalikan nilai berupa dictionary yang berisi key nya yaitu centroid dan semua object, dan value nya yaitu berisi hasil perhitungan (nilai Dm dari tiap centroid terhadap object)
    
    # METODE UNTUK MENCARI INITIAL CLUSTER CENTER
    def gicca(self):                                            # fungsi ini tidak membutuhkan parameter, karena data yang dibutuhkan telah ada pada properties class
        centers = []                                            # variabel yang digunakan untuk menyimpan data center pada satu iterasi
        centers.append(int(max(self.dens, key=self.dens.get)))  # menambahkan elemen center pertama yang diperoleh dari nilai density terbesar pada properti dens

        # AWAL PROSES UNTUK MENCARI PUSAT CLUSTER KEDUA DAN SETERUSNYA
        if self.k > 1:                                  # looping untuk mencari cluster yang dibutuhkan sebanyak k, k dikurangi 1 karena centroid pertama telah didapatkan dari nilai density
            for jumlah_cluster in range(self.k-1):      # k dikurangi 1 karena nilai k pertama telah dicari yaitu pada cluster center pertama yang didapatkan dari nilai density
                min_dm = centers[jumlah_cluster]        # variabel min_dm digunakan untuk menginisiaisasi nilai Dm yang terendah dari centroid yang mana terhadap semua object
                if len(centers) > 1:            # if disini digunakan untuk memfilter jika panjang center lebih dari 1 maka masuk bagian if disini yang digunakan untuk mencari nilai Dm terendah dari tiap centroid terhadap semua item
                    Xm = []                     # variabel Xm bertype list yang digunakan untuk menyimpan data centroid
                    Dm_dens = []                # variabel Dm bertype list yang digunakan untuk menyimpan nilai Dm dari centroid terhadap object yang mana nilai Dm yang terendah
                    for xmi in centers:         # perulangan sebanyak centroid yang ada, karena digunakan untuk mencari nilai Dm terendah dari tiap centroid terhadap object manapun
                        Xm.append(xmi)          # menyimpan centroid pada variabel Xm
                        x = list(self.calc_and_save_dm(xmi).values())   # variabel x menyimpan data berbentuk list dari nilai yang dikembalikan oleh fungsi calc_and_save_dm
                        x.sort()                            # variabel x yang tadinya menyimpan data list Dm kemudian nilai nya di sort secara ascending, untuk mengetahui nilai terkecil yang terletak paling awal
                        Dm_dens.append(x[1])                     # dari variabel x yang telah di sort, kemudian diambil nilai kedua paling awal, diambil yang kedua karena yaitu Dm yang pertama adalah antara dua object yang sama, sehingga nilai nya akan 0, dan jika hal itu terus diulangi maka tiap iterasi untuk menentukan nilai Dm terendah akan terdapat pada index awal terus
                    min_dm = Xm[Dm_dens.index(min(Dm_dens))]          # Xm menyimpan centroid dengan data urutan sesuai index, Dm menyimpan nilai terendah dari tiap Xm dengan urutan sesuai index, sehingga Xm dengan index a memiliki nilai Dm pada variabel Dm dengan index a juga
                Dm_dens = self.calc_and_save_dm(min_dm)          # mengambil kembali nilai Dm dari centroid yang memiliki Dm terkecil tadi
                Dm_dens = list(Dm_dens.values())                      # mengambil hanya value nya saja, lalu diubah menjadi type data list agar dapat di proses untuk mencari object yang memiliki nilai Dm maksimal yang lalu dari Dm maksimal itu akan dijadikan sebagai centroid baru
                sort_dm = Dm_dens.copy()     # copy nilai dm ke sort_dm,
                sort_dm.sort()          # mengurutkan nilai dari sort_dm, agar dapat dengan mudah mencari nilai maksimal lainnya ketika nilai paling maksimal sudah menjadi center

                # PROSES MENCARI NILAI DM TERBESAR YANG BUKAN OBJEK PADA CENTER
                # yang terdapat + 1 pada proses ini karena yang dibaca adalah berdasarkan index, sedangkan pada center yang disimpan adalah value nya, bukan index nya
                if Dm_dens.index(max(Dm_dens))+1 in centers:  # melakukan pengecekan, apakah nilai maksimal dari Dm yang tidak diurutkan indeksnya sudah tercatat pada centers.
                    loop = True                     # variabel tambahan untuk melakukan perulangan
                    n = 0                           # variabel yang digunakan untuk mencari nilai index terakhir satu persatu ke depan, hingga menemukan nilai maksimal dari objek yang tidak ada pada centers
                    while loop == True:             # perulangan yang mengecek hingga menemukan nilai dm terbesar pada objek yang tidak terdapat pada centers
                        n += 1                      # dengan increasing, maka di setiap perulangan akan menambahkan nilai n yang digunakan sebagai posisi index pada variabel sort_dm
                        temp = sort_dm[len(sort_dm)-n]          # variabel temp menyimpan value dari Dm yang terbesar, adapun index nya yaitu membaca banyaknya nilai yang ada pada sort_dm dan dikurangi n sehingga bisa terurut mulai dari terakhir ke awal karena nilai maksimal terdapat pada akhir list
                        if Dm_dens.index(temp)+1 in centers:    # jika value dari dm terbesar index nya telah terdapat pada centers, maka objek tersebut telah tercatat sebagai centers, maka proses pencarian centroid baru dilanjutkan dengan memilih object lain
                            pass
                        else:                                            # else - jika nilai dm yang terbesar tidak terdapat pada centers
                            centers.append(Dm_dens.index(temp)+1)        # maka index tersebut akan dicatat sebagai centers - append()
                            self.calc_and_save_dm(Dm_dens.index(temp)+1) # memanggil fungsi calc_and_save_dm untuk menyimpan informasi Dm dari centroid terakhir
                            loop = False                            # looping pun disudahi
                else:                                               # jika nilai Dm yang terbesar indexnya tidak terdapat pada centers
                    centers.append(Dm_dens.index(max(Dm_dens))+1)             # maka index tersebut akan dicatat sebagai centers selanjutnya
                    self.calc_and_save_dm(Dm_dens.index(max(Dm_dens))+1)
        return centers                                              # mengembalikan nilai berupa himpunan centers yang berisi objek yang berlaku sebagai centroid (output)
        # BATAS PROSES MENCARI CLUSTER KEDUA DAN SETERUSNYA

    # METODE YANG DIGUNAKAN UNTUK MENCARI UPDATE CLUSTER CENTER BARU
    def hafsm(self):
        return True

    # METODE CLUSTERING SV-K-MODES NYA
    def clustering(self,centers,max_iter):             # membutuhkan centers untuk proses didalamnya
        matriksW = np.zeros((len(centers),len(self.X))) # membentuk matriks numpy yang berukuran sama dengan matriks W (simbol-simbol atau notasi yang digunakan mempunyai rujukan, yaitu dari skripsi imam)
        for i in range(len(self.X)):            # looping sebanyak objek
            pembanding = 0
            for Xm in range(len(centers)-1):
                if self.semua_dm.get((centers[Xm+1],i+1)) < self.semua_dm.get((centers[pembanding],i+1)):
                    pembanding = Xm+1
            matriksW[pembanding][i] = 1
        self.centers_and_member[tuple(centers)] = matriksW

        # KETIKA SUDAH SELESAI PADA ITERASI TERAKHIR, MAKA DATA TERAKHIR PADA PROPERTI CENTER_AND_MEMBER ADALAH HASIL CLUSTERING YANG SUDAH KONVERGEN
        key_list = list(self.centers_and_member.keys())
        member_center = {}
        for centroid in range(len(self.centers_and_member.get((key_list[len(key_list)-1])))):
            temp = []
            for item in range(len(self.centers_and_member.get((key_list[len(key_list)-1]))[centroid])):
                if self.centers_and_member.get((key_list[len(key_list)-1]))[centroid][item] == 1:
                    temp.append(item+1)
            member_center[centroid+1] = temp
        return member_center

    def run(self,max_iter):                                  # main metode untuk mengeksekusi antar metode
        initial_cluster_center = self.gicca()       # variabel fiturs merupakan list berbentuk 3 dimensi, dengan isi yaitu fitur. k merupakan variabel untuk menampung jumlah cluster
        clustering_svkmodes = self.clustering(initial_cluster_center,max_iter)
        return clustering_svkmodes

nama_file = "write_data.xlsx"               # bentuk data file excel yg berisi 2 kolom, kolom = A id buku, kolom B = daftar keyword yang dipisahkan dengan tanda koma. toy data ukuran 9*2
jumlah_cluster = 3                          # variabel untuk menampung jumlah cluster 
data = SVKModes(nama_file,jumlah_cluster)   # inisialisasi awal dengan membawa informasi nama file, dan jumlah cluster
print(data.run(10))                           # menampilkan hasil dari perhitungan