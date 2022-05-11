import xlrd
wb=xlrd.open_workbook("toyFQ.xlsx")
sh=wb.sheet_by_index(0)
print("Jumlah baris =",sh.nrows)
dataFQ=[]

print (int(sh.cell_value(rowx=0, colx=0)), " ",int(sh.cell_value(rowx=0, colx=1)))
jml_user=5
jml_buku=19

##membangun matriks awal

#perulangan baris matriks (user)
for i in range(jml_user):
    temp=[]
    #perulangan kolom matriks (buku)
    for j in range (jml_buku):
        temp.append(0)
    dataFQ.append(temp)
print("data awal")
print(dataFQ)

#input data matriks
for x in range(sh.nrows-1):
    for u in range(jml_user+1):
        if (sh.cell_value(rowx=x, colx=0)==u):
            for b in range(jml_buku+1):
                if (sh.cell_value(rowx=x, colx=1)==b):
                    val=dataFQ[u-1][b-1]
                    val=val+1
                    dataFQ[u-1][b-1]=val
print("data akhir")
print(dataFQ)
