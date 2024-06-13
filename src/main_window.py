import sys
import sqlite3

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, \
 QVBoxLayout, QFileDialog, QLineEdit, QMessageBox

import xml_converter as converter
import data_base_inserter as db_inserter

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = app
        self.plx_file_path: str = ''
        self.db_file_path: str = './DB.db'

        self.setMaximumSize(880, 440)
        self.setMinimumSize(660, 330)

        self.main_lay = QVBoxLayout(self)

        self.plx_layout = QHBoxLayout()
        self.plx_path_label = QLineEdit()
        self.plx_path_label.setText(self.plx_file_path)
        self.plx_path_label.setEnabled(False)
        self.set_plx_button = QPushButton()
        self.set_plx_button.setText('Choose *.plx file')
        self.set_plx_button.setMaximumWidth(200)
        self.set_plx_button.setMinimumWidth(200)
        self.plx_layout.addWidget(self.plx_path_label)
        self.plx_layout.addWidget(self.set_plx_button)

        self.db_layout = QHBoxLayout()
        self.db_path_label = QLineEdit()
        self.db_path_label.setText(self.db_file_path)
        self.db_path_label.setEnabled(False)
        self.set_db_button = QPushButton()
        self.set_db_button.setText('Choose *.db file')
        self.set_db_button.setMaximumWidth(200)
        self.set_db_button.setMinimumWidth(200)
        self.db_layout.addWidget(self.db_path_label)
        self.db_layout.addWidget(self.set_db_button)

        self.start_layout = QHBoxLayout()
        self.start_inserting_button = QPushButton()
        self.start_inserting_button.setText('Insert in DB')
        self.start_inserting_button.setMinimumHeight(50)
        self.start_inserting_button.setMaximumWidth(200)
        self.start_inserting_button.setMinimumWidth(200)
        self.start_inserting_button.setEnabled(False)
        self.start_layout.addWidget(self.start_inserting_button)

        self.main_lay.addLayout(self.plx_layout)
        self.main_lay.addLayout(self.db_layout)
        self.main_lay.addLayout(self.start_layout)

        self.setLayout(self.main_lay)

        self.set_plx_button.clicked.connect(self.on_set_plx_button_clicked)
        self.set_db_button.clicked.connect(self.on_set_db_button_clicked)
        self.start_inserting_button.clicked.connect(self.on_start_inserting_button_clicked)
    

    def on_set_db_button_clicked(self):
        dialog = QFileDialog()
        path = dialog.getOpenFileName(filter="db(*.db)")[0]
        if path == '':
            return
        self.db_file_path = path
        self.db_path_label.setText(self.plx_file_path)


    def on_set_plx_button_clicked(self):
        dialog = QFileDialog()
        path = dialog.getOpenFileName(filter="plx(*.plx)")[0]
        if path == '':
            return
        self.plx_file_path = path
        self.plx_path_label.setText(self.plx_file_path)
        self.start_inserting_button.setEnabled(True)


    def on_start_inserting_button_clicked(self):
        raw_data: dict = converter.xml_to_dict_convert(self.plx_file_path)
        sql_connection = sqlite3.connect(self.db_file_path)
        sql_cursor = sql_connection.cursor()

        db_inserter.initialize_data_base(sql_cursor)

        ed_program_inf: dict = converter.get_educational_program_inf(raw_data)
        discipline_list: list = converter.get_discipline_list(raw_data)
        competence_guide_list: list = converter.get_competence_guide(raw_data)
        competence_list: list = converter.get_competence_list(raw_data)

        laboriousness_list: list = []

        if ed_program_inf['form'] == 'Очная':
            laboriousness_list = converter.get_laboriousness_ochnoe(raw_data)
        else:
            laboriousness_list = converter.get_laboriousness_zaochnoe(raw_data)
        
        ed_id: str = db_inserter.insert_educational_program(ed_program_inf, sql_cursor)
        sql_connection.commit()

        db_inserter.insert_disciplines(discipline_list, ed_id, sql_cursor)
        sql_connection.commit()

        db_inserter.insert_competencies_guide(competence_guide_list, ed_id, sql_cursor)
        sql_connection.commit()

        db_inserter.insert_competencies_list(competence_list, ed_id, sql_cursor)
        sql_connection.commit()

        db_inserter.insert_laboriousness(laboriousness_list, ed_id, sql_cursor)
        sql_connection.commit()

        sql_connection.close()
        QMessageBox.information(self, 'Complite', 'Inserting complite!')


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())