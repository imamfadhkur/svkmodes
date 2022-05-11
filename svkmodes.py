# importing library
import xlrd
import sys
# sys.exit()

# initial cluster method
def gicca(X,k):
    centers = []
    dens = []
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

data_file = "datatoybuku.xlsx"

jumlah_cluster = 3
data = run(data_file, jumlah_cluster)
print(data)