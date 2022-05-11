# importing library
import xlrd
import re
import xlsxwriter

# preprocessing method
def preprocessing(X):
    tanda_baca = "!\"#$%&'()*+-./:<=>?@[\]^_`{|}~"
    workbook = xlsxwriter.Workbook('write_data.xlsx')
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
    preprocessing(X)

data_file = "datatoybuku.xlsx"
data = run(data_file)