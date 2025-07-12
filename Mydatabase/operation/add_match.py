import pymysql
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, 
                             QMessageBox, QDateEdit, QDesktopWidget, QListWidget)  # 修正导入
from PyQt5.QtCore import QDate
from db import Database

class AddMatch(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('添加比赛')
        self.setGeometry(200, 100, 400, 400)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.match_name = QLineEdit()
        self.organizer_name = QLineEdit()
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDisplayFormat('yyyy-MM-dd')
        self.start_date.setDate(QDate.currentDate())
        self.end_date = QDateEdit(calendarPopup=True)
        self.end_date.setDisplayFormat('yyyy-MM-dd')
        self.end_date.setDate(QDate.currentDate())

        form_layout.addRow('比赛名称:', self.match_name)
        form_layout.addRow('主办方:', self.organizer_name)        
        form_layout.addRow('开始日期:', self.start_date)
        form_layout.addRow('结束日期:', self.end_date)

        layout.addLayout(form_layout)

        self.select_teams_button = QPushButton('选择参赛队伍', self)
        self.select_teams_button.clicked.connect(self.select_teams)
        layout.addWidget(self.select_teams_button)

        self.teams_list = QListWidget()  # 现在可以正确识别 QListWidget
        self.teams_list.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.teams_list)

        self.add_button = QPushButton('添加比赛', self)
        self.add_button.clicked.connect(self.add_match)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        self.center()

    def select_teams(self):
        try:
            self.db.cursor.execute("SELECT team_name FROM teams")
            teams = self.db.cursor.fetchall()
            self.teams_list.clear()
            for team in teams:
                self.teams_list.addItem(team['team_name'])  # 使用字典键名访问
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'获取队伍列表失败: {err}')

    def add_match(self):
        match_name = self.match_name.text()
        organizer_name = self.organizer_name.text()
        start_date = self.start_date.date().toString('yyyy-MM-dd')
        end_date = self.end_date.date().toString('yyyy-MM-dd')

        if not (match_name and start_date and end_date):
            QMessageBox.warning(self, '错误', '所有字段均为必填项')
            return

        try:
            # 检查比赛是否已存在
            self.db.cursor.execute("SELECT * FROM matches WHERE match_name=%s", 
                                  (match_name,))
            if self.db.cursor.fetchone():
                QMessageBox.warning(self, '错误', '该比赛已存在')
                return
            
            # 添加比赛
            self.db.cursor.execute("""
                INSERT INTO matches (match_name,organizer_name, start_date, end_date)
                VALUES (%s, %s, %s, %s)
            """, (match_name, organizer_name, start_date, end_date))

            # 添加参赛记录
            selected_items = self.teams_list.selectedItems()
            for item in selected_items:
                team_name = item.text()
                self.db.cursor.execute("""
                    INSERT INTO participations (team_name, match_name)
                    VALUES (%s, %s)
                """, (team_name, match_name))

            self.db.conn.commit()
            QMessageBox.information(self, '成功', '比赛添加成功')
            self.clear_fields()
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'添加比赛失败: {err}')
            
    def clear_fields(self):
        self.match_name.clear()
        self.start_date.setDate(QDate.currentDate())
        self.end_date.setDate(QDate.currentDate())
        self.teams_list.clear()
            
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())