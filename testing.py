# importing library
import xlrd
import sys
# sys.exit()

# initial cluster method
def gicca(X,k):
    centers = []
    # jika terdapat fitur lebih dari satu
    # if X.ncols > 2:
    #     centers.append("X1")
    # else:
    #     centers.append("X2")
    # for m in range(X.ncols):
        # print("m: ",m)
        # for n in range(X.nrows):
            # print("n: ",n)
            # X.cell_value(rowx=0,colx=0)
    dens = []
    for i in range(X.nrows):
        dens_fitur = 0
        for m in range((X.ncols)-1):
            for n in range(X.nrows):
                irisan_vajxi = 0
                # print("X",i)
                # print("n",n)
                # print(X.cell_value(rowx=i,colx=(m+1)).split(", "), " | ",X.cell_value(rowx=n,colx=(m+1)).split(", "))
                # set1 = set(X.cell_value(rowx=i,colx=(m+1)))
                # set2 = set(X.cell_value(rowx=n,colx=(m+1)))
                # print(set1.intersection(set2))
                for vajxi in X.cell_value(rowx=i,colx=(m+1)).split(", "):
                    if vajxi in X.cell_value(rowx=n,colx=(m+1)).split(", "):
                        irisan_vajxi += 1
                # print("irisan",irisan_vajxi)
                # print("gabungan",len(X.cell_value(rowx=i,colx=(m+1)).split(", "))+len(X.cell_value(rowx=n,colx=(m+1)).split(", "))-irisan_vajxi)
                dens_fitur += irisan_vajxi/(len(X.cell_value(rowx=i,colx=(m+1)).split(", "))+len(X.cell_value(rowx=n,colx=(m+1)).split(", "))-irisan_vajxi)
        dens.append(dens_fitur/9)
    print("dens X: ",dens)
    centers.append(dens.index(max(dens)))
    print("centers 1: ",centers)
    # return centers

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
    # return initial_cluster_center

data_file = "datatoybuku.xlsx"

jumlah_cluster = 3
data = run(data_file, jumlah_cluster)
# print(data)