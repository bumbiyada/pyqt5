import pandas as pd
import numpy as np
import xlrd
import time


def function():
        print('procedure')

def function2(x):
    print(x)

def dict_list(df, add = False):
    # print("!")
    keys = list(df.keys())
    lenth = len(df[keys[0]])
    write_list = []

    item_format = {}

    for key in keys:
        item_format.update({key: ""})

    if(add):
        item_format.update({"id": ""})

    item = item_format
    for i in range(lenth):
        # if(i%1000 == 0):
        #     print('Загрузка : ' + str(int(i/lenth*100))+" %               ",  end='\r')


        for key in keys:
            item[key] = df[key][i]

        if(add):
            item["id"] = i

        write_list.append(dict(item))


    # print('Загрузка : ' + "100 %               ",  end='\r')


    return write_list

def list_dict(list):
    keys = list[0].keys()
    lenth = len(list)
    write_dict = {}
    for key in keys:
        write_dict.update({key: []})

    print(lenth)

    for i in range(lenth):
        # if(i%1000 == 0 ):
        #     print('Загрузка : ' + str(int(i/lenth*100))+" %               ",  end='\r')
        print(i)

        for key in keys:
            print(i)
            print(key)
            print(list[i][key])
            print("_____________")
            write_dict[key].append(list[i][key])

    # print('Загрузка : ' +"100 %               ",  end='\r')

    return write_dict


#Сортировка по одному из стб (и приведение типов)
def sort_list(list, stb, casting  = True):
    #Приведение типов
    if(casting):
        for i in range(len(list)):
            for j in stb:
                list[i][j] = str(list[i][j])

    #Сортировка по первому нужному стб
    from operator import itemgetter
    list.sort(key=itemgetter(stb[0]))

    # print("GG")
    #Сортировка по остальным стб
    for i in range(1,len(stb)):
        i2 = 0
        while(i2 < len(list)):
            i3 = i2
            while(i3 < len(list) and list[i3][stb[i - 1]] == list[i2][stb[i - 1]]):
                i4 = i - 2
                flag = False
                while(i4>=0):
                    if(list[i3][stb[i4]] != list[i2][stb[i4]]):
                        flag = True
                        break
                    i4 = i4-1
                if(flag):
                    break
                i3 = i3 + 1

            list[i2:i3] = sorted(list[i2:i3], key=itemgetter(stb[i]))
            i2=i3

    # print("GG2")
    return list

#Группировка и подсчет уникальных ключей (в уже отсортированном двумерном массиве)
def group_list(list, stb):
    for i in range(len(list)):
        list[i].update({"Подгруппа": ""})
        list[i].update({"Колличество": ""})

    i = 0
    n = len(list)
    group = 1
    while(i < n):

        flag = True
        i2 = i + 1
        count = 1
        # print(stb)
        while(i2 < n and flag):
            for key in stb:
                if(list[i][key] != list[i2][key]):
                    flag = False
                    break
            if(not flag):
                break
            count = count + 1
            i2 = i2 + 1

        i2 = i2 - 1

        while (i <= i2):

            list[i]["Подгруппа"] = group
            list[i]["Колличество"] = count
            i = i + 1

        group = group + 1
        # print(i," ",n)
        # i = i + 1

    return list


