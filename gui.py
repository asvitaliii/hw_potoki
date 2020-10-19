from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from random import randint
from threading import Thread


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__win = uic.loadUi('gui.ui')
        self.__file_name = ''
        self.__data = []

    def __set_slots(self):
        self.__win.read_file.clicked.connect(self.read_file)
        self.__win.new_list.clicked.connect(self.new_list)
        self.__win.sort_list.clicked.connect(self.sort)

    def show(self):
        self.__set_slots()
        self.__win.show()

    def read_file(self):
        self.__file_name = self.__win.file_name.text()
        if self.__file_name == '':
            QMessageBox.information(self, 'Ошибка!', 'Введите имя файла!')
            return None
        with open(self.__file_name, 'r', encoding='utf-8') as data:
            self.__data = data.read().split('\n')
        self.__win.input_list.setText(f'Исходный список: {self.__data}')
        self.__win.input_list.adjustSize()

    def new_list(self):
        self.__file_name = self.__win.file_name.text()
        if self.__file_name == '':
            QMessageBox.information(self, 'Ошибка!', 'Введите имя файла!')
            return None
        self.__data = []
        for i in range(15):
            self.__data.append(str(randint(-100, 100)))
        self.write_data('\n'.join(self.__data), self.__file_name)
        self.__win.input_list.setText(f'Исходный список: {self.__data}')
        self.__win.input_list.adjustSize()

    def sort(self):
        flow_pos = Sort(self.__data, True)
        flow_neg = Sort(self.__data, False)
        flow_pos.daemon = True
        flow_neg.daemon = True
        flow_pos.start()
        flow_neg.start()
        res_pos = flow_pos.get_res()
        res_neg = flow_neg.get_res()
        self.write_data('\n'.join(res_pos), f'{self.__file_name}.pos')
        self.__win.positive_numbers.setText(f'Положительные числа: {res_pos}')
        self.__win.positive_numbers.adjustSize()
        self.write_data('\n'.join(res_neg), f'{self.__file_name}.neg')
        self.__win.negative_numbers.setText(f'Отрицательные числа: {res_neg}')
        self.__win.negative_numbers.adjustSize()

    def write_data(self, data, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(data)


class Sort(Thread):
    def __init__(self, data: list, positive: bool):
        super().__init__()
        self.__data = data
        self.__pos = positive
        self.__res = []

    def run(self):
        num_lst = [int(i) for i in self.__data]
        res = []
        if self.__pos:
            for i in num_lst:
                if i >= 0:
                    res.append(i)
        else:
            for i in num_lst:
                if i < 0:
                    res.append(i)
        res.sort()
        self.__res = [str(i) for i in res]

    def get_res(self):
        return self.__res
