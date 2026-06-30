mytup1 = ("fruits","banana","orange","mango")
mytup2 = ("Ahmad","hassan","Bilal","ali")
mylist = list(mytup1)
del mylist[0:2]
mytup1 = mylist.copy()
print(mylist)

del mytup2[1:3]
print(mytup2)
# mytup1
print(mytup1)