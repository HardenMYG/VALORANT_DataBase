import pymysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDesktopWidget
from db import Database

class AddTeam(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('添加队伍')
        self.setGeometry(200, 100, 400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.team_name = QLineEdit()
        self.country = QLineEdit()
        self.world_ranking = QLineEdit()
        self.coach_name = QLineEdit()
        self.honors = QLineEdit()
        self.recent_win_rate = QLineEdit()

        form_layout.addRow('队伍名称:', self.team_name)
        form_layout.addRow('队伍所属地:', self.country)
        form_layout.addRow('世界排名:', self.world_ranking)
        form_layout.addRow('教练:', self.coach_name)
        form_layout.addRow('荣誉:', self.honors)
        form_layout.addRow('最近胜率:', self.recent_win_rate)

        layout.addLayout(form_layout)

        self.add_button = QPushButton('添加队伍', self)
        self.add_button.clicked.connect(self.add_team)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_team(self):
        team_name = self.team_name.text()
        country = self.country.text()
        world_ranking = self.world_ranking.text()
        coach_name = self.coach_name.text()
        honors = self.honors.text()
        recent_win_rate = self.recent_win_rate.text()

        if not (team_name and country and world_ranking and coach_name and honors and recent_win_rate):
            QMessageBox.warning(self, '错误', '所有字段均为必填项')
            return

        try:
            self.db.cursor.execute("""
                INSERT INTO teams (team_name, country, world_ranking, coach_name, honors,recent_win_rate)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (team_name, country, world_ranking, coach_name, honors,recent_win_rate))
            self.db.conn.commit()
            QMessageBox.information(self, '成功', '队伍添加成功')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'添加队伍失败: {err}')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())