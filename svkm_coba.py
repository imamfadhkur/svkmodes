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
                for m in range(len(self.X.get(1))):     # untuk melooping tiap fitur yang ada
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
                min_dm_dens = centers[jumlah_cluster]        # variabel min_dm digunakan untuk menginisiaisasi nilai Dm yang terendah dari centroid yang mana terhadap semua object
                if len(centers) > 1:            # if disini digunakan untuk memfilter jika panjang center lebih dari 1 maka masuk bagian if disini yang digunakan untuk mencari nilai Dm terendah dari tiap centroid terhadap semua item
                    Xm = []                     # variabel Xm bertype list yang digunakan untuk menyimpan data centroid
                    Dm_dens = []                # variabel Dm bertype list yang digunakan untuk menyimpan nilai Dm dari centroid terhadap object yang mana nilai Dm yang terendah
                    for xmi in centers:         # perulangan sebanyak centroid yang ada, karena digunakan untuk mencari nilai Dm terendah dari tiap centroid terhadap object manapun
                        Xm.append(xmi)          # menyimpan centroid pada variabel Xm
                        x = list(self.calc_and_save_dm(xmi).values())   # variabel x menyimpan data berbentuk list dari nilai yang dikembalikan oleh fungsi calc_and_save_dm
                        x.sort()                            # variabel x yang tadinya menyimpan data list Dm kemudian nilai nya di sort secara ascending, untuk mengetahui nilai terkecil yang terletak paling awal
                        Dm_dens.append(x[1])                     # dari variabel x yang telah di sort, kemudian diambil nilai kedua paling awal, diambil yang kedua karena yaitu Dm yang pertama adalah antara dua object yang sama, sehingga nilai nya akan 0, dan jika hal itu terus diulangi maka tiap iterasi untuk menentukan nilai Dm terendah akan terdapat pada index awal terus
                    min_dm_dens = Xm[Dm_dens.index(min(Dm_dens))]     # Xm menyimpan centroid dengan data urutan sesuai index, Dm menyimpan nilai terendah dari tiap Xm dengan urutan sesuai index, sehingga Xm dengan index a memiliki nilai Dm pada variabel Dm dengan index a juga
                Dm_dens = self.calc_and_save_dm(min_dm_dens)          # mengambil kembali nilai Dm dari centroid yang memiliki Dm terkecil tadi
                Dm_dens = list(Dm_dens.values())                 # mengambil hanya value nya saja, lalu diubah menjadi type data list agar dapat di proses untuk mencari object yang memiliki nilai Dm maksimal yang lalu dari Dm maksimal itu akan dijadikan sebagai centroid baru
                sort_dm = Dm_dens.copy()     # copy nilai dm ke sort_dm,
                sort_dm.sort()               # mengurutkan nilai dari sort_dm, agar dapat dengan mudah mencari nilai maksimal lainnya ketika nilai paling maksimal sudah menjadi center

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
                            loop = False                                 # looping pun disudahi
                else:                                                    # jika nilai Dm yang terbesar indexnya tidak terdapat pada centers
                    centers.append(Dm_dens.index(max(Dm_dens))+1)             # maka index tersebut akan dicatat sebagai centers selanjutnya
                    self.calc_and_save_dm(Dm_dens.index(max(Dm_dens))+1)
        return centers                                              # mengembalikan nilai berupa himpunan centers yang berisi objek yang berlaku sebagai centroid (output)
        # BATAS PROSES MENCARI CLUSTER KEDUA DAN SETERUSNYA

    # METODE YANG DIGUNAKAN UNTUK MENCARI UPDATE CLUSTER CENTER BARU
    def hafsm(self,X):                                  # parameter inputan X merupakan himpunan cluster dan membernya, misal X = [[1, 2, 3, 4], [5, 7, 8], [6, 9]], X[0][0] merupakan member cluster pertama
        set_valued_modes_Q = {}
        for m in range(len(self.X.get(1))):             # looping sebanyak fitur yang ada
            for cluster in X:                           # untuk me looping tiap cluster 
                print("\n")
                # proses menambahkan keyword pada variabel vj
                vj = {}                                 # untuk menyimpan keyword sebagai key nya, dan nilai frekuensi dari keyword sebagai value nya
                Q = []
                for obj in cluster:                     # untuk me looping tiap object yang ada pada cluster
                    for keyword in self.X.get(obj)[m]:  # untuk me looping tiap keyword yang ada pada object, agar tiap keyword tersebut dapat dimasukkan kedalam variabel vj
                        if keyword not in vj:           # melakukan pengecekan jika keyword tidak ada di variabel vj, maka di tambahkan, karena keyword dalam variabel vj tidak boleh duplikat
                            vj[keyword] = 0             # menambahkan keyword pada variabel vj
                # proses menghitung probability-based frequency (f)
                for key in vj:              # me-looping setiap keyword yang ada pada variabel vj
                    temp = 0                # variabel semenara untuk menyimpan nilai frekuensi 
                    for obj in cluster:     # looping tiap object yang ada pada cluster, yang tujuannya digunakan untuk menghitung frekuensi probabilitas yang dihitungnya adalah antara keyword vj nya, dan dengan keywords dari object
                        if key in self.X.get(obj)[m]:           # untuk melakukan pengecekan jika keyword termasuk subset dari object, maka operasinya adalah len keyword dibagi len keywords nya object
                            temp += 1/len(self.X.get(obj)[m])   # langkah terakhir dalam mencari frekuensi probabilitas
                    vj[key] = temp/len(cluster)                 # memasukkan nilai frekuensi probabilitas kedalam dict yang key nya adalah keyword
                x = dict(sorted(vj.items(), key=lambda item: item[1], reverse=True))    # proses mengurutkan vj berdasarkan values nya
                vj_sort = list(x.keys())          # mengambil key nya saja yang mana telah diurutkan by value
                # proses menghitung r
                r = 0
                for obj in cluster:                             # me-looping semua object yang ada pada cluster
                    r += len(self.X.get(obj)[m])/len(cluster)   # menghitung nilai r, yaitu dengan menghitung penjumlahan dari banyaknya keyword yang ada pada suatu object dibagi banyaknya object
                r = round(r)                    # me-round nilai r, dimana round yaitu membulatkan ke bawah apabila dibawah 0.5, dan dibulatkan keatas apabila nilai lebih dari atau sama dengan 0.5
                print("r:",r)
                print("vj:",vj)
                print("vj sort:",vj_sort)
                kwsv = [k for k,v in vj.items() if v == x.get(vj_sort[r-1])]
                print("keys with same value by r:",kwsv)
                if r == 0:                      # untuk memfilter apabila terdapat nilai r yang tidak diharapkan
                    print("cluster:",cluster)   # untuk mencetak di cluster mana dan apa membernya
                    print("error r = 0")
                    exit()
                elif r == 1:
                    Q.append(vj_sort[0])        # untuk menambahkan nilai Q
                    print("masuk langkah 5")
                elif r > 1 and x.get(vj_sort[r-1]) > x.get(vj_sort[r]):   # nilai r dikurangi satu karena dalam program ini membacanya berdasarkan index, sedangkan dalam contoh perhitungan manual nilai r di baca berdasarkan urutan, bukan secara index
                    Q.append(vj_sort[r-1])
                    print("masuk langkah 6")
                
                # awal proses langkah 7
                elif r > 1 and x.get(vj_sort[0]) >= x.get(vj_sort[1]) >= x.get(vj_sort[r-2]) > x.get(vj_sort[r-1]) == x.get(vj_sort[r]) > x.get(vj_sort[r+1]) >= x.get(vj_sort[len(vj_sort)-1]) : # langkah 7 pada algoritma HAFSM
                    print("masuk langkah 7")
                    Q.append(vj_sort[0])
                    Qrj = 0
                    for rj in range(r-2):               # min 2 karena 1 dihitung berdasarkan index sedangkan r nya tidak menghitung berdasarkan index, dan 1 nya karena dari rumus dikurangi 1
                        Qrj += vj.get(vj_sort[rj])      # untuk menghitung nilai frekuensi semua object sebelum r 
                    Qrj1 = Qrj                          # meng-copy nilai frekuensi semua object sebelum r
                    Qrj += vj.get(vj_sort[rj+1])        # meng-update nilai Qrj yang ke r
                    Qrj1 += vj.get(vj_sort[rj+2])       # meng-update nilai Qrj yang ke r+1
                    if Qrj > Qrj1:                      # jika jumlah semua frekuensi ke r lebih besar dari jumlah semua frekuensi ke r+1
                        Q.append(vj_sort[rj+1])         # maka, yang dijadikan nilai Q selanjutnya adalah keyword ke r
                    else:                               # jika jumlah semua frekuensi ke r lebih kecil atau sama dengan jumlah semua frekuensi ke r+1
                        Q.append(vj.get(vj_sort[rj+2])) # maka, yang dijadikan nilai Q selanjutnya adalah keyword ke r+1
                # batas proses langkah 7
                
                # proses masuk langkah 8
                else:
                    print("masuk langkah 8")
                    print("vj",vj)
                    print("keys with same value by r:",kwsv)
                    print("r =",r,". ->",vj_sort[r-1])
                    print("p':",vj_sort.index(vj_sort[r-1])-1)
                    print("r-p'-1:",r-(vj_sort.index(vj_sort[r-1])-1)-1)
                    exit()
                # batas proses langkah 8
                print("Q: ",Q)

    # METODE CLUSTERING SV-K-MODES NYA
    def clustering(self,centers,max_iter):              # membutuhkan centers untuk proses didalamnya
        matriksW = np.zeros((len(centers),len(self.X))) # membentuk matriks numpy yang berukuran sama dengan matriks W (simbol-simbol atau notasi yang digunakan mempunyai rujukan, yaitu dari skripsi imam)
        temp = {}                                       # ex: {0: [1, 2, 3, 4], 1: [5, 7, 8], 2: [6, 9]} --> variabel sementara yang digunakan untuk menyimpan member cluster, key nya merupakan cluster, value nya merupakan object
        for i in range(len(self.X)):                    # looping sebanyak objek
            pembanding = 0                              # variabel yang digunakan untuk menyimpan info bahwa suatu object dia berada pada cluster mana gitu
            for Xm in range(len(centers)-1):            # loop dikurangi 1 karena didalam loop membandingkan object saat ini dengan object selanjutnya, jika tidak dikurangi 1 maka disaat membandingkan dengan "object selanjutnya" akan error out of range
                if self.semua_dm.get((centers[Xm+1],i+1)) < self.semua_dm.get((centers[pembanding],i+1)):   # membandingkan nilai dm dari object sekarang (pembanding, yang menyimpan info dia pada cluster mana) dengan object selanjutnya (center Xm+1)
                    pembanding = Xm+1           # ini akan terjadi manabila object center xm+1 nilai dm nya lebih kecil dari center pembanding, maka center pembanding di update nilai nya menjadi center xm+1, karena untuk mencari suatu object dia terletak jaraknya paling dekat yang mana kedalam cluster nya
            matriksW[pembanding][i] = 1         # proses mengisi element matriks menjadi 1, karena telah dicari object tersebut berada pada cluster berapa (pada variabel pembanding)
            # proses pembuatan member cluster yaitu dengan sistem list dalam list, adapun list utama sebagai value dari dictionary, didalamnya terdapat list yang mana list tersebut merupakan cluster, anggota list tersebut merupakan object.
            if temp.get(pembanding) == None:    # jika variabel temp dengan key "pembanding" masih belum ada isinya,
                temp[pembanding] = [i+1]        # maka variabel temp dengan key "pembanding" akan diisi sebuah data yang dibentuk type data list
            else:                               # jika variabel temp dengan key "pembanding" sudah ada isinya, sudah ada value nya, 
                temp[pembanding].append(i+1)    # maka value yang berbentuk list tersebut akan ditambahkan sebuah object
        # proses mengisikan variabel utama center_and_member, yang berisi centers sebagai key, valuenya temp sebagai value pada center_and_member
        keys = list(temp.keys())                # mengambil key dari variabel temp
        self.centers_and_member[tuple(centers)] = list([temp[i] for i in keys])     # proses pengisian center_and_member, key nya adalah centers dan value nya adalah semua value yang ada pada variabel temp
        # proses awal membuat matriks Q yang mana elemen nya adalah nilai dm dari masing-masing centroid kepada setiap object
        matriksQ = []                               # variabel yang digunakan untuk menyimpan matriks Q, variabel ini akan bertype 2 dimensi
        for jml_cluster in range(len(centers)):     # looping sebanyak jumlah cluster nya
            temp = []                               # variabel sementara untuk menyimpan nilai dm dari tiap object terhadap satu centroid
            for item in range(len(self.X)):         # looping sebanyak object yang ada
                temp.append(self.semua_dm.get((centers[jml_cluster],item+1)))       # proses pemanggilan nilai dm dari variabel utama (self.semua_dm) untuk ditambahkan kedalam variabel temp
            matriksQ.append(temp)                   # menambahkan data dm semua object terhadap satu centroid kedalam variabel matriks Q
        matriksQ = matriksW*(np.array(matriksQ))    # setelah selesai proses pembuatan matriks Q nya, langsung mengalikan tiap element matriks Q dengan matriks W
        F_aksen = np.sum(matriksQ)                  # pada baris ini melakukan penjumlahan pada tiap cell dari matriks
        # print(self.X)
        # print(self.centers_and_member)
        # exit()

        # PROSES UNTUK ITERASI KEDUA DAN SETERUSNYA
        if max_iter > 1:                        # pemfilteran pertama untuk looping, jika looping nya lebih dari satu kali maka akan di looping dengan melakukan proses yang ada dibawah nya
            for iter in range(max_iter-1):      # looping sebanyak jumlah iterasi, dikurangi 1 karena iterasi pertama telah dilakukan di sebelum proses ini
                print("iterasi ke-",iter)       # untuk keterangan iterasi ke berapa
                values = list(self.centers_and_member.values())     # mengambil values nya saja
                self.hafsm(values[len(values)-1])                   # memanggil method hafsm untuk mencari update centroid berdasarkan tiap cluster


        # KETIKA SUDAH SELESAI PADA ITERASI TERAKHIR, MAKA DATA TERAKHIR PADA PROPERTI CENTER_AND_MEMBER ADALAH HASIL CLUSTERING YANG SUDAH KONVERGEN
        keys = self.centers_and_member.keys()
        values = self.centers_and_member.values()
        # print(keys,":",values)
        # for data in self.centers_and_member:
        #     for centroid in range(len(self.centers_and_member.keys())):
        #         print("list",self.centers_and_member.keys())
        #         print(self.centers_and_member.get(data)[centroid])

        ab = list(values)
        # return "SV-K-Modes:",ab[len(ab)-1]
        # return self.centers_and_member
        return "SV-K-Modes:",F_aksen,max_iter

    def run(self,max_iter):                                  # main metode untuk mengeksekusi antar metode
        initial_cluster_center = self.gicca()       # variabel fiturs merupakan list berbentuk 3 dimensi, dengan isi yaitu fitur. k merupakan variabel untuk menampung jumlah cluster
        clustering_svkmodes = self.clustering(initial_cluster_center,max_iter)
        return clustering_svkmodes

nama_file = "write_datav2-langkah8.xlsx"               # bentuk data file excel yg berisi 2 kolom, kolom = A id buku, kolom B = daftar keyword yang dipisahkan dengan tanda koma. toy data ukuran 9*2
jumlah_cluster = 3                          # variabel untuk menampung jumlah cluster 
data = SVKModes(nama_file,jumlah_cluster)   # inisialisasi awal dengan membawa informasi nama file, dan jumlah cluster
max_iter = 2
print(data.run(max_iter))                           # menampilkan hasil dari perhitungan