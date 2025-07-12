import pymysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QListWidget, QLabel, \
    QDesktopWidget
from db import Database

class DeleteMatch(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('删除比赛')
        self.setGeometry(200, 100, 400, 400)

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.match_name = QLineEdit()  # 改为比赛名称
        self.form_layout.addRow('比赛名称:', self.match_name)  # 修改标签
        self.layout.addLayout(self.form_layout)

        self.query_button = QPushButton('查询比赛', self)
        self.query_button.clicked.connect(self.query_matches)
        self.layout.addWidget(self.query_button)

        self.results_list = QListWidget()
        self.layout.addWidget(self.results_list)

        self.confirm_delete_button = QPushButton('确定删除比赛', self)
        self.confirm_delete_button.setEnabled(False)
        self.confirm_delete_button.clicked.connect(self.delete_matches)
        self.layout.addWidget(self.confirm_delete_button)

        self.setLayout(self.layout)

    def query_matches(self):
        match_name = self.match_name.text()

        if not match_name:
            QMessageBox.warning(self, '错误', '比赛名称为必填项')
            return

        self.results_list.clear()

        try:
            # 查询比赛信息
            self.db.cursor.execute("""
                SELECT m.match_name, m.start_date, m.end_date
                FROM matches m
                WHERE m.match_name = %s
            """, (match_name,))
            
            matches = self.db.cursor.fetchall()

            if matches:
                for match in matches:
                    # 显示比赛详细信息
                    self.results_list.addItem(f"比赛名称: {match['match_name']}")
                    self.results_list.addItem(f"开始日期: {match['start_date']}")
                    self.results_list.addItem(f"结束日期: {match['end_date']}")
                    self.results_list.addItem("-----------------------")
                self.confirm_delete_button.setEnabled(True)
            else:
                QMessageBox.information(self, '结果', '未找到相关比赛记录')
                self.confirm_delete_button.setEnabled(False)

        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询比赛失败: {err}')
            self.confirm_delete_button.setEnabled(False)

    def delete_matches(self):
        
        match_name = self.match_name.text()

        if not match_name:
            QMessageBox.warning(self, '错误', '比赛名称为必填项')
            return

        # 确认对话框
        reply = QMessageBox.question(
            self, '确认删除', 
            f'确定要删除比赛 "{match_name}" 吗？\n此操作将自动删除所有相关的参赛记录。',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
    
        if reply == QMessageBox.No:
            return

        try:
            # 开启事务（可选，建议保留以确保原子性）
            self.db.start_transaction()

            # 直接删除 matches 表中的记录，MySQL 会自动级联删除 participations 中的相关记录
            self.db.cursor.execute("""
                DELETE FROM matches 
                WHERE match_name = %s
            """, (match_name,))

            # 提交事务
            self.db.commit_transaction()
        
            QMessageBox.information(self, '成功', '比赛删除成功')
            self.results_list.clear()
            self.confirm_delete_button.setEnabled(False)
            self.match_name.clear()
        
        except pymysql.Error as err:
            # 回滚事务
            self.db.rollback_transaction()
            QMessageBox.warning(self, '错误', f'删除比赛失败: {err}')


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())