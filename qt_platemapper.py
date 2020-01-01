from PyQt5 import QtCore, Qt, QtGui, QtWidgets
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QApplication, QGridLayout, QButtonGroup, QGroupBox, QTableWidget,QVBoxLayout, QDir, QLineEdit, QInputDialog, QMainWindow, QHBoxLayout, QLabel
import sys
from shutil import copyfile

# input group names
# check boxes to highlight groups on plate
# explicit deselect aka click to deselect cells


# make sure boxes dont belong to multiple groups
# resize side panel
# any more features?
# output plate


class myPlate(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1500, 500)
        # Initialize variables
        self.current_selection = []
        self.groups = []
        self.groups_dict = {}
        # initialize components
        self.main_widg = QtWidgets.QWidget()
        self.table = QTableWidget()
        self.table.setSelectionMode(Qt.QAbstractItemView.ExtendedSelection)
        # self.table.resize(300,1000)
        self.table_layout = QHBoxLayout()

        self.side_layout = QVBoxLayout()
        self.input_box = QLineEdit()
        self.box_label = QLabel()
        # self.box_label.setVisible(False)
        self.box_label.setStyleSheet('color: red')
        self.enter_button = Qt.QPushButton("Enter")
        self.done_button = Qt.QPushButton("Done")
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        # Init plate stuff
        self.init_plate()
        # self.table.currentCellChanged.connect(self.table_click)
        self.setup_window()
        self.entry_done()
        self.button_group.buttonClicked.connect(self.select_group)
        self.done_button.clicked.connect(self.save_and_quit)
        # self.select_group()
        # Add the display to the general layout
        self.selections = Qt.QActionGroup(self.input_box)
        self.select = [self.selections.addAction(Qt.QAction(i)) for i in self.groups]

    def entry_done(self):
        self.input_box.returnPressed.connect(self.store_groups)
        self.enter_button.clicked.connect(self.store_groups)

    def save_and_quit(self):
        path, _ = Qt.QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV(*.csv)')
        if path != "":
            data = []
            for row in range(self.table.rowCount()):
                rows = []
                for col in range(self.table.columnCount()):
                    to_save = self.table.item(row, col)
                    if to_save is not None:
                        rows.append(to_save.text())
                    else:
                        rows.append("")
                data.append(rows)
            df = pd.DataFrame(data, index=pd.Index(list('ABCDEFGH')), columns=range(1, 13))
            df.to_csv(path)
        self.save_to_robot(path)

    def connect_to_robot(self):
        pass

    def save_to_robot(self, saved_path):
        robot_path = ""
        dest = copyfile(saved_path, robot_path)
        pass

    def setup_window(self):
        self.input_box.setFixedSize(70, 20)
        self.input_box.setAlignment(QtCore.Qt.AlignRight)
        self.input_box.setReadOnly(False)
        self.input_box.setPlaceholderText("Enter group name")
        # self.input_box.move(100, 100)
        self.side_layout.addWidget(self.enter_button, alignment=Qt.Qt.AlignBottom)
        self.side_layout.addWidget(self.done_button)
        self.side_layout.addWidget(self.box_label, alignment=Qt.Qt.AlignBottom)
        # add text box to secondary layout
        self.side_layout.addWidget(self.input_box, alignment=Qt.Qt.AlignBottom)
        self.table_layout.addWidget(self.table)
        self.table_layout.addLayout(self.side_layout)
        self.main_widg.setLayout(self.table_layout)
        self.setCentralWidget(self.main_widg)

    def store_groups(self):
        if self.input_box.text() not in self.groups:
            self.box_label.setText("")
            if self.input_box.text().lstrip(" ") != '':
                self.groups.append(self.input_box.text().lstrip(" ").rstrip(" "))
                self.add_checkbox()

        else:
            self.box_label.setText("That group already exists")

    def add_checkbox(self):
        button = Qt.QRadioButton(self.groups[-1])
        self.button_group.addButton(button)
        self.side_layout.addWidget(button)

    def init_toolbar(self):
        pass

    # def table_click(self):
    #     print(self.table.currentColumn(), self.table.currentRow())

    def select_group(self):
        checked = self.button_group.checkedButton().text()
        selections = [(i.row(), i.column()) for i in self.table.selectedIndexes()]
        # checked ends up
        # TODO: check replacing list comprehension in generators. Generators are better if slicing not necessary
        self.groups_dict.update({'{}'.format(checked): selections})
        self.fill_cells(selections)

    # if cell has items and is clicked, delete them
    # if cell is empty, populate with text from selected button
    def fill_cells(self, items):
        # check for empty

        for i in items:
            if self.table.item(*i) is None or self.table.item(*i).text() == "":
                # Fill and remove TableWidgetItem objects rather than fill text
                if self.table.item(*i) is None:
                    filler = Qt.QTableWidgetItem(self.button_group.checkedButton().text())
                    self.table.setItem(*i, filler)
                else:
                    self.table.item(*i).setText(self.button_group.checkedButton().text())

            else:
                self.table.setItem(*i, Qt.QTableWidgetItem())

    def init_plate(self):
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setRowCount(8)
        self.table.setColumnCount(12)
        self.table.setAutoScroll(True)
        self.table.setHorizontalHeaderLabels([str(i) for i in range(1, 12)])
        self.table.setVerticalHeaderLabels([i for i in 'ABCDEFGH'])
        self.table.dragEnabled()
        # self.table.columnResized(300, 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plate = myPlate()
    plate.show()
    sys.exit(app.exec_())

