from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import time
#from PyQt5.QtCore import QSortFilterProxyModel

#import pandas
import pandas as pd
# Импортируем нашу форму.
from qtable import Ui_MainWindow # Наше окно
from help import Ui_help_ui # Наше ресурс
from procedures import *
import sys

import xlwings as xw
import numpy as np
# import xlrd





#наш класс главного окна
class mywindow(QtWidgets.QMainWindow):

    switch_window = QtCore.pyqtSignal()
    path_file_1 = ""
    list_of_keys = [] #Левая колонка 1
    list_of_keys_flags = [] #Правая колонка 1, Выбраные ключи

    table_1 = []
    table_out_1 = []

    def __init__(self):
        # self.list_of_keys = [] #Левая колонка 1
        # self.list_of_keys_flags = [] #Правая колонка 1, Выбраные ключи
        #
        # self.table_1 = []
        # self.table_out_1 = []


        #something default
        super(mywindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.Window) #
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint) # Кпока закрыть
        self.ui = Ui_MainWindow()# инициализация
        self.ui.setupUi(self)# инициализация
        #button to open files
        self.ui.button_open_file.clicked.connect(self.startToListen)#Нажатие кнопки открыть файл
        self.ui.help_button.clicked.connect(self.help)#Нажатие кнопки help

        #События колонки 1-2
        self.ui.pushButton_add.clicked.connect(lambda: self.Add_key())
        self.ui.list_keys.doubleClicked.connect(lambda: self.Add_key())
        # действие по нажатию кнопки удалить
        self.ui.pushButton_delete.clicked.connect(lambda: self.Delete_key())
        self.ui.list_selected_keys.doubleClicked.connect(lambda: self.Delete_key())

        #result

        self.ui.result_button.clicked.connect(lambda: self.progress())



    def startToListen(self):#Нажатие кнопки открыть файл

        self.ui.list_keys.clear()
        self.ui.list_selected_keys.clear()

        # манипуляции с открытием файла
        file, _  = QtWidgets.QFileDialog.getOpenFileName(self,
                        'Open File',
                        './',
                        'Excel files (*.xm*;*.xl*);;All files (*)')

        self.path_file_1 = file

        if not file:
            #если файл не был открыт, то очищаем лейбл и 2 наших листа от информации
            self.ui.label_file_name.setText('Выберите файл')
            self.ui.list_keys.clear()#Зачищаем поля
            self.ui.list_selected_keys.clear()#Зачищаем поля
            self.list_of_keys = []
            self.list_of_keys_flags = []
            return
            #huynua

        # если файл был открыт
        # меняем строку label на название файла
        self.ui.label_file_name.setText("file name " + str(file))
        # создаем датафрейм через pandas
        #print(file)


        #Помозгуй че сделать с расширениями
        self.table_1 = pd.read_excel(file)
        # df = dict_list(self.table_1)
        self.list_of_keys = self.table_1.columns
        self.list_of_keys_flags = []

        # заполняем строки данными из Датафрейма
        for i in range(len(self.list_of_keys)):
            self.ui.list_keys.insertItem(i,self.list_of_keys[i])
            self.list_of_keys_flags.append(False)



        return
    def Add_key(self):

        # print(list_of_keys)
        # print("!")
        # print(list_of_keys_flags)
        print("LOX")

        # получить индекс (0, n) текущей (выделенной) строки
        value = self.ui.list_keys.currentRow()
        # получить количество строк в листе
        value2 = self.ui.list_selected_keys.count()
        # сравниваем по флагу, выбран ли уже элемент или он доступен к выбору


        if (value < 0):
            return
        if self.list_of_keys_flags[value] == False:
            self.ui.list_selected_keys.insertItem(value2, self.list_of_keys[value])
            self.list_of_keys_flags[value] = True



    def Delete_key(self):
        value = self.ui.list_selected_keys.currentRow()
        value2 = self.ui.list_selected_keys.count()
        # если в поле ХВыбранные ключиХ какое-то поле выделено то
        if (value < 0):
            return

        if self.ui.list_selected_keys.currentItem() != None:
            # доступ к текстовому значению строки в листе
            text = self.ui.list_selected_keys.currentItem().text()
            # выставляем флаги в Фолсе, чтобы повторно можно было выбрать поле
            for i in range(len(self.list_of_keys)):
                if text == self.list_of_keys[i]:
                    self.list_of_keys_flags[i] = False
                    break
            self.ui.list_selected_keys.takeItem(value)

    def progress(self): #Нажатие кнопки результаты
        #Проверка на заполненость данных
        if(len(self.list_of_keys) == 0  or len(self.list_of_keys_flags) == 0):
            return
        flag = False

        i = 0
        keys = []
        for el in self.list_of_keys_flags:
            if (el):
                keys.append(self.list_of_keys[i])
            i = i + 1
            flag = flag or el

        if(not flag):
            return

        print(self.ui.comboBox.currentIndex())
        print(keys)
        #выбор действия
        if(self.ui.comboBox.currentIndex() == 0):
            df = dict_list(self.table_1, True)# add "id"
            df = sort_list(df,keys)
            df = group_list(df,keys)# add "Подгруппa" , "Колличество"

            print("!1")
            df = sort_list(df,["id"],False)
            print("!2")
            pd.DataFrame(df).to_excel('lololo.xlsx')
            #
            #
            #
            # print("!1")
            # print(df[0])
            # df = sort_list(df,["id"])
            # print(df)
            # df = list_dict(df)
            # print("!3")
            #
            # #Вывод в таблицу
            #
            # wb = xw.Book(self.path_file_1)
            # len_colunm = len(self.list_of_keys)
            # print("!4")
            #
            # wb.sheets[0].cells(len_colunm + 1,1).value = ["Подгруппа","Колличество"]
            # wb.sheets[0].cells(len_colunm + 1,2).value = [df["Подгруппа"],df["Колличество"]]

            # wb.sheets[0].cells(len(self.list_of_keys) + 1,1).value = ["1"]
            print("OK")


        # self.table_out_1 = dict_list(self.table_1,True)



        # print("выбранный файл = {}".format(file))
        # print("!")
        # print("выбранный параметр комбобокс = {}".format(list_of_keys_flags))
        # print("выбранный параметр комбобокс = {}".format(self.ui.comboBox.currentText()))
        # print("красная активна {}".format(self.ui.checkBox_red.isChecked()))
        # print("зеленая активна {}".format(self.ui.checkBox_green.isChecked()))
        # print("синяя активна {}".format(self.ui.checkBox_blue.isChecked()))
        # print("желтая активна {}".format(self.ui.checkBox_yellow.isChecked()))
        # print("вариант обработки 1 {}".format(self.ui.radioButton.isChecked()))
        # print("вариант обработки 2 {}".format(self.ui.radioButton_2.isChecked()))
        # print("вариант обработки 3 {}".format(self.ui.radioButton_3.isChecked()))
        #
        #
        # function()
        #
        #
        #
        #
        # for i in range(101): # движение прогресс бара
        #     self.ui.progressBar.setValue(i)
        #     time.sleep(0.05)
        # if i == 100:
        #     self.ui.print_complited.setText('COMPLITED!!!')

    def help(self):
        print('help')
        self.switch_window.emit()

class help_window(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        # something default
        super(help_window, self).__init__()
        #self.setWindowFlags(QtCore.Qt.Window)
        #self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.ui = Ui_help_ui()
        self.ui.setupUi(self)
        self.ui.close_btn.clicked.connect(self.close)

    # def close(self):
    #     self.switch_window.emit()


# эта штука отвечает за переключение между окнами, запускает их и вообще Зая
class Controller:

    def __init__(self):
        pass

    def show_main_page(self): # Проказывает главное окно
        self.main_page = mywindow()
        self.main_page.switch_window.connect(self.show_help_page)
        self.main_page.show()


    def show_help_page(self):# Проказывает  help
        self.help_page = help_window()
        # self.help_page.switch_window.connect(self.show_main_page_after_help)

        self.help_page.show()

    # def show_main_page_after_help(self):
    #     self.main_page = mywindow()
    #     self.help_page = help_window()
    #     self.help_page.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main_page()
    sys.exit(app.exec_())

main()