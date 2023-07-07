
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
        self.conn = sqlite3.connect( self.current_dir + './films_db.sqlite')
        cur = self.conn.cursor()
        current_dir = dirname(__file__)
        file_path = join(self.current_dir, "./1.ui")
        uic.loadUi(file_path , self)
        
        self.onClicked_clear()
        self.onClicked_upd()
        
        genre = cur.execute('SELECT distinct id FROM films').fetchall()
        for i in range(len(genre)):
            genre[i] = str(genre[i])[1:-2]
            genre[i] = self.tr((genre[i]))
            self.combo.addItem(genre[i], userData=genre[i])
        self.Add_Quest.clicked.connect(self.onClicked_add)
        self.B_Clear.clicked.connect(self.onClicked_clear)
        self.B_Upd_Table.clicked.connect(self.onClicked_upd)

    def reversedl(self,name):
        res=''
        for i in range(len(name)-1,-1,-1):
            res+=name[i]
        return res
    
    def onClicked_add(self):
        if (self.B_And.isChecked()):
            plus_str = "AND"
        else:
            plus_str = "OR"
        self.zprs
        if (self.zprs==' '):
            self.zprs = 'Where '+' films.id='+self.combo.currentData()
        else:
            self.zprs += ' '+plus_str+' films.id='+self.combo.currentData()
        self.Text_ed.setText(self.zprs)
        
    def onClicked_clear(self):
        if self.zprs!=' ':
            name =(self.conn.cursor().execute('SELECT films.title FROM films ' + self.zprs).fetchall())
            name = str(name[0])[1:-2]
            name = self.reversedl(name)
            self.conn.cursor().execute('update films set duration=duration+duration, year=year+1000, title='+ name+' ' + self.zprs)
        self.zprs =' '
        self.Text_ed.setText(' ')

    def onClicked_upd(self):
        
        res = self.conn.cursor().execute("SELECT films.id, films.title, year, genres.title, duration FROM films inner join genres on  genres.id  = films.genre "+self.zprs).fetchall()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        #self.name = str(self.conn.cursor().execute('SELECT title FROM films' + self.zprs).fetchall())[1:-2]
        #self.year = str(int(self.conn.cursor().execute('SELECT year FROM films' + self.zprs).fetchall())[1:-2] + 1000)
        #self.dur = str(int(self.conn.cursor().execute('SELECT duration FROM films' + self.zprs).fetchall())[1:-2] *2)
        



if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
