import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QTableWidget,
                             QWidget, QHBoxLayout, QVBoxLayout, QCalendarWidget, QTimeEdit, QListWidget, QTabWidget,
                             QFileDialog, QMessageBox)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QDateTime, QDate
from templates.cal import Cal
from templates.db_add import Db_Add
from templates.main_wd import MainWd
from templates.my_flowers import My_Flowers
from templates.new_reg import New_Reg
from templates.old_reg import Old_Reg
from templates.photo_add import Photo_Add
from templates.reg_main import Reg_Main
from PyQt6.QtCore import QEvent


class OldReg(QMainWindow, Old_Reg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Вход в аккаунт")
        self.pushButton.clicked.connect(self.return_reg)

        self.textEdit.installEventFilter(self)
        self.textEdit_2.installEventFilter(self)

        self.default_texts = {
            self.textEdit: "Введите имя пользователя:",
            self.textEdit_2: "Введите пароль:",
        }
        self.pushButton_2.clicked.connect(self.return_reg)
        self.pushButton.clicked.connect(self.log_in)

    def return_reg(self):
        self.addform = MainReg()
        self.addform.show()
        self.close()

    def log_in(self):
        username = self.textEdit.toPlainText().strip()
        password = self.textEdit_2.toPlainText().strip()

        if (not username or username == self.default_texts[self.textEdit] or
                not password or password == self.default_texts[self.textEdit_2]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля ввода!")
            return

        conn = sqlite3.connect("bd's/Main.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, login, hashed_password) VALUES (?, ?, ?)",
                (username, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Ошибка", "Пользователь с таким логином уже существует!")
            conn.close()
            return
        finally:
            conn.close()

        self.addform = MainWindow()
        self.addform.show()
        self.close()

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.FocusIn:
            if watched in self.default_texts:
                current_text = watched.toPlainText().strip()
                trigger = self.default_texts[watched]
                if current_text.startswith(trigger) or current_text == trigger:
                    watched.clear()
        return super().eventFilter(watched, event)


class NewReg(QMainWindow, New_Reg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Регистрация нового аккаунта")

        self.textEdit.installEventFilter(self)
        self.textEdit_2.installEventFilter(self)
        self.textEdit_3.installEventFilter(self)

        self.default_texts = {
            self.textEdit: "Введите имя пользователя:",
            self.textEdit_2: "Введите логин:",
            self.textEdit_3: "Введите пароль:"
        }
        self.pushButton_2.clicked.connect(self.return_reg)
        self.pushButton.clicked.connect(self.created)

    def return_reg(self):
        self.addform = MainReg()
        self.addform.show()
        self.close()

    def created(self):
        username = self.textEdit.toPlainText().strip()
        login = self.textEdit_2.toPlainText().strip()
        password = self.textEdit_3.toPlainText().strip()

        if (not username or username == self.default_texts[self.textEdit] or
                not login or login == self.default_texts[self.textEdit_2] or
                not password or password == self.default_texts[self.textEdit_3]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля ввода!")
            return

        conn = sqlite3.connect("bd's/Main.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, login, hashed_password) VALUES (?, ?, ?)",
                (username, login, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Ошибка", "Пользователь с таким логином уже существует!")
            conn.close()
            return
        finally:
            conn.close()

        self.addform = MainWindow()
        self.addform.show()
        self.close()

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.FocusIn:
            if watched in self.default_texts:
                current_text = watched.toPlainText().strip()
                trigger = self.default_texts[watched]
                if current_text.startswith(trigger) or current_text == trigger:
                    watched.clear()
        return super().eventFilter(watched, event)


class MainReg(QMainWindow, Reg_Main):
    def __init__(self, *objects):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Магазин цветов")
        self.setGeometry(100, 100, 761, 600)
        self.pushButton_2.clicked.connect(self.new_reg)
        self.pushButton.clicked.connect(self.old_reg)

    def new_reg(self):
        self.addform = NewReg()
        self.addform.show()
        self.close()

    def old_reg(self):
        self.addform = OldReg()
        self.addform.show()
        self.close()


class MainWindow(QMainWindow, MainWd):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Главное окно")



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainReg()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
