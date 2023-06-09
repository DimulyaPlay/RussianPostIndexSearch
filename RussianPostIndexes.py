import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QStatusBar
from PyQt5.QtGui import QIcon
from difflib import SequenceMatcher
import pandas as pd
import sqlite3
import os

#pyinstaller --onefile --windowed --icon "C:\Users\CourtUser\Desktop\release\RussianPostIndexSearch\index.png" --add-data "C:\Users\CourtUser\Desktop\release\RussianPostIndexSearch\index.png;." --add-data "C:/PIndx10.db;." RussianPostIndexes.py

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def similarity_score(a, b):
    return SequenceMatcher(None, a, b).ratio()


def filter_dataframe(df, search_string):
    filtered_df = df[df['opsname'].str.contains(search_string.upper())]
    return filtered_df[['index','opsname', 'area', 'region', 'autonom']]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path('index.png')))
        self.setWindowTitle("Поиск индекса по населенному пункту")
        self.setGeometry(100, 100, 600, 400)

        self.search_label = QLabel("Начните вводить название населенного пункта:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.handle_search)
        self.statusbar = QStatusBar(self)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Индекс", "ОПС", "Район", "Регион", "Автоном"])

        layout = QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.setContentsMargins(3,3,3,3)
        self.linkLabel = QLabel()
        self.linkLabel.setText('БД PIndx10 от 06.06.2023. Разработка: Краснокамский гс. <a href="https://github.com/dimulyaPlay">github.com/DimulyaPlay</a>')
        self.linkLabel.setOpenExternalLinks(True)  # Открывать ссылку во внешнем браузере
        self.statusbar.addWidget(self.linkLabel)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setStatusBar(self.statusbar)
        self.data_df = None

    def handle_search(self, search_string):
        if len(search_string) > 3:
            filtered_df = filter_dataframe(self.data_df, search_string)
            self.populate_table(filtered_df)

    def populate_table(self, dataframe):
        dataframe.sort_values('index', ascending=True, inplace=True)
        self.table.setRowCount(len(dataframe))
        for row_index, row_data in enumerate(dataframe.values):
            self.table.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value).strip())
                self.table.setItem(row_index, col_index, item)
        self.table.resizeColumnsToContents()


if __name__ == "__main__":
    # Load your data into the dataframe
    con = sqlite3.connect(resource_path('PIndx10.db'))
    df = pd.read_sql('SELECT "index", region, autonom, area, opsname FROM PIndx10', con=con)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.data_df = df
    window.show()
    sys.exit(app.exec_())
