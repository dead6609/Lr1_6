
import sys
import sqlite3
from os.path import dirname, join      
from PyQt5.Qt import *           # PyQt5
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel




class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.current_dir = dirname(__file__)
        self.load_ui()
        
    def load_ui(self):
        #os.chdir('F:\Project\Py\Widget_art')
        self.zprs =' '
        self.conn = sqlite3.connect(self.current_dir + './films_db.sqlite')
        cur = self.conn.cursor()
        file_path = join(self.current_dir, "./1.ui")
        uic.loadUi(file_path , self)
        
        self.onClicked_clear()
        self.onClicked_upd()
        
        genre = cur.execute('SELECT distinct duration FROM films').fetchall()
        for i in range(len(genre)):
            genre[i] = str(genre[i])[1:-2]
            genre[i] = self.tr((genre[i]))
            self.combo.addItem(genre[i])
        self.Add_Quest.clicked.connect(self.onClicked_add)
        self.B_Clear.clicked.connect(self.onClicked_clear)
        self.B_Upd_Table.clicked.connect(self.onClicked_upd)

    
    def onClicked_add(self):
        if (self.B_And.isChecked()):
            plus_str = "AND"
        else:
            plus_str = "OR"
        self.zprs
        if (self.zprs==' '):
            self.zprs = 'where '+' duration='+self.combo.currentText()
        else:
            self.zprs += ' '+plus_str+' duration='+self.combo.currentText()
        self.Text_ed.setText(self.zprs)
        
    def onClicked_clear(self):
        self.zprs =' '
        self.Text_ed.setText(' ')

    def onClicked_upd(self):
        if (self.zprs!=' '):
            self.conn.cursor().execute("delete FROM films " + self.zprs)
        res = self.conn.cursor().execute("SELECT films.id, films.title, year, genres.title, duration FROM films inner join genres on  genres.id  = films.genre").fetchall()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if i ==3 and (elem == None or elem == ' '):
                    self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(42)))
                else:
                    self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))



if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
