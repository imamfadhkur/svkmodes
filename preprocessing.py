# importing library
import xlrd
import re
import xlsxwriter

# preprocessing method
def preprocessing(X):
    tanda_baca = "!\"#$%&'()*+-./:<=>?@[\]^_`{|}~"
    workbook = xlsxwriter.Workbook('data_input_CB.xlsx')
    worksheet = workbook.add_worksheet()
    for m in range((X.ncols)):
        for n in range(X.nrows):
            if m > 0:
                dataafter_satuan = X.cell_value(rowx=n,colx=(m)).lower()
                dataafter_satuan = re.sub(r"\d+", "", dataafter_satuan)
                dataafter_satuan = dataafter_satuan.translate(str.maketrans(";",",",tanda_baca))
                dataafter_satuan = re.sub('\s+','',dataafter_satuan)
            else:
                dataafter_satuan = X.cell_value(rowx=n,colx=(m))
            worksheet.write(n,m,dataafter_satuan)
    workbook.close()
    

# main method
def run(item):
    item = xlrd.open_workbook(item)
    X = item.sheet_by_index(0)
    max_val = 0
    for n in range(X.nrows):
        if X.cell_value(rowx=n,colx=0) > max_val:
            max_val = X.cell_value(rowx=n,colx=0)
    if X.nrows > max_val:
        # print("terdapat data duplikat")
        workbook = xlsxwriter.Workbook('data_input_CB(tanpa duplikasi data).xlsx')
        worksheet = workbook.add_worksheet()
    else:
        print("tidak terdapat data duplikat")
    # preprocessing(X)

data_file = "data_index-untuk_CB.xlsx"
data = run(data_file)