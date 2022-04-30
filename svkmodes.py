# initial cluster method
def gicca(X,k):
    return True

# update cluster center method
def hafsm():
    return True

# clustering method
def svkmodes(X,k):
    return True

# main method
def run(X,k):
    # menentukan insial cluster center
    gicca(X,k)

# item = []
# jumlah_cluster = 3
# run(item, jumlah_cluster)

new_empty_dict = {}

new_empty_dict[1] = [[26, 34],["liva", "Elijah", "Georg"],["ekonomi", "moneter"]]
# nw_list = ['Oliva', 'Elijah', 'George']
# nw_list2 = ['ekonomi', 'moneter']
# new_empty_dict["Student_id"].append(nw_list)
# new_empty_dict["Student_id"].append(nw_list2)
new_empty_dict[2] = 22
new_empty_dict["3"] = [["liva", "Elijah", "Georg"],["ekonomi", "moneter"]]
# print(new_empty_dict)
# types2 = [type(k) for k in new_empty_dict.values()]
# print(types2)
for item in new_empty_dict.get(1):
    print(item)