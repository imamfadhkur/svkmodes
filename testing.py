# importing library
import xlrd
import re
import string
import xlsxwriter
import xlwt
import sys
# sys.exit()

# initial cluster method
def gicca(X,k):
    centers = []
    dens = []
    # awal code untuk mencari cluster center pertama
    for i in range(X.nrows):
        dens_fitur = 0
        for m in range((X.ncols)-1):
            for n in range(X.nrows):
                irisan_vajxi = 0
                for vajxi in X.cell_value(rowx=i,colx=(m+1)).split(", "):
                    if vajxi in X.cell_value(rowx=n,colx=(m+1)).split(", "):
                        irisan_vajxi += 1
                dens_fitur += irisan_vajxi/(len(X.cell_value(rowx=i,colx=(m+1)).split(", "))+len(X.cell_value(rowx=n,colx=(m+1)).split(", "))-irisan_vajxi)
        dens.append(dens_fitur/9)
    centers.append(dens.index(max(dens)))
    # batas code batas mencari cluster center pertama
    
    # awal code mencari cluster center kedua
    dm = []
    for i in range(X.nrows):
        dmd = 0
        irisan_vasxi = 0
        for m in range((X.ncols)-1):
            for vasxi in X.cell_value(rowx=centers[0],colx=(m+1)).split(", "):
                if vasxi in X.cell_value(rowx=i,colx=(m+1)).split(", "):
                    irisan_vasxi += 1
            dmd += 1-(irisan_vasxi/(len(X.cell_value(rowx=centers[0],colx=(m+1)).split(", "))+len(X.cell_value(rowx=i,colx=(m+1)).split(", "))-irisan_vasxi))
        dm.append(dmd*dens[i])
    centers.append(dm.index(max(dm)))
    # batas code mencari cluster center kedua

    return dens

# update cluster center method
def hafsm():
    return True

# clustering method
def svkmodes(X,k):
    return True

# preprocessing method
def preprocessing(X):
    databefore = []
    dataafter = []
    tanda_baca = ""
    for ww in string.punctuation:
        if ww == "," or ww == ";":
            pass
        else:
            tanda_baca += ww
    # print(tanda_baca)
    workbook = xlsxwriter.Workbook('write_data.xlsx')
    worksheet = workbook.add_worksheet()
    for m in range((X.ncols)):
        for n in range(X.nrows):
            # print(X.cell_value(rowx=n,colx=(m)),"|",X.cell_value(rowx=n,colx=(m+1)).lower())
            # databefore.append(X.cell_value(rowx=n,colx=(m+1)))
            # dataafter.append(X.cell_value(rowx=n,colx=(m+1)).lower())
            if m > 0:
                dataafter_satuan = X.cell_value(rowx=n,colx=(m)).lower()
                # print(dataafter_satuan)
                # print("===================")
                dataafter_satuan = re.sub(r"\d+", "", dataafter_satuan)
                dataafter_satuan = dataafter_satuan.translate(str.maketrans(";",",",tanda_baca))
                dataafter_satuan = re.sub('\s+','',dataafter_satuan)
            else:
                dataafter_satuan = X.cell_value(rowx=n,colx=(m))
            
            worksheet.write(n,m,dataafter_satuan)

            # print(dataafter_satuan)
            # print("")
    workbook.close()
    # print(databefore)
    # dataafter = re.sub(r"\d+", "", dataafter)
    # print(dataafter)
    

# main method
def run(item,k):
    item = xlrd.open_workbook(item)
    X = item.sheet_by_index(0)
    preprocessing(X)
    # menentukan insial cluster center
    # initial_cluster_center = gicca(X,k)
    # return initial_cluster_center

data_file = "datatoybuku.xlsx"

jumlah_cluster = 3
data = run(data_file, jumlah_cluster)
# print(data)