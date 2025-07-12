
import pymysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDesktopWidget
from db import Database

class DeletePlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('删除选手')
        self.setGeometry(200, 100, 400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.team_name = QLineEdit()
        self.player_name = QLineEdit()
        form_layout.addRow('队伍名称:', self.team_name)
        form_layout.addRow('选手姓名:', self.player_name)

        layout.addLayout(form_layout)

        self.delete_button = QPushButton('删除选手', self)
        self.delete_button.clicked.connect(self.delete_player)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)
        self.center()

    def delete_player(self):
        team_name = self.team_name.text()
        player_name = self.player_name.text()
        if not team_name or not player_name:
            QMessageBox.warning(self, '错误', '请输入队伍名称和选手姓名')
            return

        try:
            # 检查选手是否存在
            self.db.cursor.execute("SELECT * FROM players WHERE team_name=%s AND name=%s", 
                                  (team_name, player_name))
            player = self.db.cursor.fetchone()
            if not player:
                QMessageBox.warning(self, '错误', '选手不存在')
                return
            
            # 确认删除
            reply = QMessageBox.question(self, '确认', f'确定要删除选手"{player_name}"吗?', 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
            
            # 删除选手
            self.db.cursor.execute("DELETE FROM players WHERE team_name=%s AND name=%s", 
                                  (team_name, player_name))
            self.db.conn.commit()
            QMessageBox.information(self, '成功', '选手删除成功')
            self.team_name.clear()
            self.player_name.clear()
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'删除选手失败: {err}')
            
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())