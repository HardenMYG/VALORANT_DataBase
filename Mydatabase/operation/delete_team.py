
import pymysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDesktopWidget
from db import Database

class DeleteTeam(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('删除队伍')
        self.setGeometry(200, 100, 400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.team_name = QLineEdit()
        form_layout.addRow('队伍名称:', self.team_name)

        layout.addLayout(form_layout)

        self.delete_button = QPushButton('删除队伍', self)
        self.delete_button.clicked.connect(self.delete_team)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)
        self.center()

    def delete_team(self):
        team_name = self.team_name.text()
        if not team_name:
            QMessageBox.warning(self, '错误', '请输入队伍名称')
            return

        try:
            # 检查队伍是否存在
            self.db.cursor.execute("SELECT * FROM teams WHERE team_name=%s", (team_name,))
            team = self.db.cursor.fetchone()
            if not team:
                QMessageBox.warning(self, '错误', '队伍不存在')
                return
            
            # 确认删除
            reply = QMessageBox.question(self, '确认', f'确定要删除队伍"{team_name}"吗?', 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
            
            # 删除队伍
            self.db.cursor.execute("DELETE FROM teams WHERE team_name=%s", (team_name,))
            self.db.conn.commit()
            QMessageBox.information(self, '成功', '队伍删除成功')
            self.team_name.clear()
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'删除队伍失败: {err}')
            
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())