import xlrd, xlsxwriter

def to_input_svkm(file_sumber, nama_file_output):
    file = xlrd.open_workbook(file_sumber)
    data = file.sheet_by_index(0)

    workbook = xlsxwriter.Workbook(nama_file_output)
    worksheet = workbook.add_worksheet()
    
    temp = {}

    for n in range(data.nrows):
        x = data.cell_value(rowx=n,colx=2).replace(" ","")
        temp[data.cell_value(rowx=n,colx=1)] = x
    
    for key in temp:
        worksheet.write(int(key)-1,0,key)
        worksheet.write(int(key)-1,1,temp.get(key))
    workbook.close()

def hitung_keyword(nama_file):
    item = xlrd.open_workbook(nama_file)
    X = item.sheet_by_index(0)
    temp = []
    for n in range(X.nrows):
        for keyword in X.cell_value(rowx=n,colx=1).split(","):
            if keyword in temp:
                pass
            else:
                temp.append(keyword)
    return len(temp)

# normalisasi_keyword("datamerge_input_CB (tanpa spasi).xlsx")
print(hitung_keyword("data_deskripsi_buku.xlsx"))
to_input_svkm("data_item_train1_cb.xlsx","data_deskripsi_buku.xlsx")