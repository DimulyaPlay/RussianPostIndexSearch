import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QStatusBar
from PyQt5.QtGui import QIcon
import pandas as pd
import os

#pyinstaller --onefile --windowed --icon "C:\Users\CourtUser\Desktop\release\RussianPostIndexSearch\index.png" --add-data "C:\Users\CourtUser\Desktop\release\RussianPostIndexSearch\index.png;." --add-data "C:\Users\CourtUser\Desktop\release\RussianPostIndexSearch\PIndx16.csv;." RussianPostIndexes.py

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def filter_dataframe(df, search_strings):
    search_strings = search_strings.split(' ')
    # Создаем переменную для хранения логических условий для каждой строки
    conditions = None

    # Проходим по каждой строке поисковых строк
    for search_string in search_strings:
        # Создаем логическое условие для текущей строки и объединяем его с предыдущими условиями
        if conditions is None:
            conditions = df['Location'].str.contains(search_string.upper())
        else:
            conditions &= df['Location'].str.contains(search_string.upper())

    # Фильтруем DataFrame с использованием объединенных условий
    filtered_df = df[conditions]

    # Возвращаем нужные столбцы
    return filtered_df[['index','Location', 'opsname', 'opssubm']]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path('index.png')))
        self.setWindowTitle("Поиск индекса по населенному пункту")
        self.setGeometry(100, 100, 800, 450)

        self.search_label = QLabel("Начните вводить название населенного пункта, несколько слов разделяйте пробелами:")
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.handle_search)
        self.statusbar = QStatusBar(self)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Индекс", "Расположение","Вышестоящий", "ОПС"])

        layout = QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.setContentsMargins(3,3,3,3)
        self.linkLabel = QLabel()
        self.linkLabel.setText('БД PIndx16 от 06.09.2023. Разработка: Краснокамский гс. <a href="https://github.com/dimulyaPlay">github.com/DimulyaPlay</a>')
        self.linkLabel.setOpenExternalLinks(True)  # Открывать ссылку во внешнем браузере
        self.statusbar.addWidget(self.linkLabel)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setStatusBar(self.statusbar)
        self.data_df = None

    def handle_search(self, search_string):
        if len(search_string) > 2:
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
    df = pd.read_csv(resource_path('PIndx16.csv'))
    app = QApplication(sys.argv)
    window = MainWindow()
    window.data_df = df
    window.show()
    sys.exit(app.exec_())
