import pymysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDateEdit, \
    QDesktopWidget
from PyQt5.QtCore import QDate
from db import Database

class AddPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('添加选手')
        self.setGeometry(200, 100, 400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.team_name = QLineEdit()
        self.player_number = QLineEdit()
        self.name = QLineEdit()
        self.birthdate = QDateEdit(calendarPopup=True)
        self.birthdate.setDisplayFormat('yyyy-MM-dd')
        self.birthdate.setDate(QDate.currentDate())
        self.nationality = QLineEdit()
        self.position = QLineEdit()

        form_layout.addRow('队伍名称:', self.team_name)
        form_layout.addRow('号码:', self.player_number)
        form_layout.addRow('姓名:', self.name)
        form_layout.addRow('出生日期:', self.birthdate)
        form_layout.addRow('国籍:', self.nationality)
        form_layout.addRow('位置:', self.position)

        layout.addLayout(form_layout)

        self.add_button = QPushButton('添加选手', self)
        self.add_button.clicked.connect(self.add_player)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_player(self):
        team_name = self.team_name.text()
        player_number = self.player_number.text()
        name = self.name.text()
        birthdate = self.birthdate.date().toString('yyyy-MM-dd')
        nationality = self.nationality.text()
        position = self.position.text()

        if not (team_name and player_number and name and birthdate and nationality and position):
            QMessageBox.warning(self, '错误', '所有字段均为必填项')
            return

        try:
            self.db.cursor.execute("""
                INSERT INTO players (team_name, player_number, name, birthdate, nationality, position)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (team_name, player_number, name, birthdate, nationality, position))
            self.db.conn.commit()
            QMessageBox.information(self, '成功', '选手添加成功')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'添加选手失败: {err}')
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())