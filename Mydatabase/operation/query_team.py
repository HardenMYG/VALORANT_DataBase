import pymysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QInputDialog, \
    QDesktopWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QFrame
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont
from PyQt5.QtCore import Qt
from db import Database

class QueryTeam(QWidget):
    def __init__(self, is_admin=False):  # 添加 is_admin 参数
        super().__init__()
        self.db = Database()
        self.is_admin = is_admin  # 保存 is_admin 作为实例属性
        self.initUI()
        self.query_all_teams()

    def initUI(self):
        self.setWindowTitle('查询队伍')
        self.setMinimumSize(1000, 700)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)
        
        # 标题 - 使用更深的红色
        title_label = QLabel("队伍查询系统")
        title_label.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #FFFFFF; background-color: rgba(100, 20, 20, 220); "
                                 "border-radius: 15px; padding: 15px;")
        main_layout.addWidget(title_label)
        
        # 查询区域 - 降低透明度
        query_frame = QFrame()
        query_frame.setStyleSheet("background-color: rgba(255, 245, 245, 100); border-radius: 15px; border: 1px solid #E0D0D0;")
        query_layout = QVBoxLayout(query_frame)
        query_layout.setContentsMargins(30, 30, 30, 30)
        query_layout.setSpacing(20)
        
        # 队伍查询
        team_group = QHBoxLayout()
        team_label = QLabel("队伍名称:")
        team_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        team_label.setFixedWidth(120)
        team_label.setStyleSheet("color: #303030;")
        self.team_name = QLineEdit()
        self.team_name.setPlaceholderText('请输入队伍名称')
        self.team_name.setStyleSheet("background-color: rgba(255, 255, 255, 100); border: 1px solid #D0C0C0; border-radius: 8px; padding: 8px;")
        self.team_name.setMinimumHeight(40)
        team_group.addWidget(team_label)
        team_group.addWidget(self.team_name)
        query_layout.addLayout(team_group)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        
        self.query_button = QPushButton('查询队伍')
        self.query_button.setStyleSheet(
            "QPushButton { background-color: #A52A2A; color: white; border-radius: 10px; padding: 12px; font-weight: bold; font-size: 20px; }"
            "QPushButton:hover { background-color: #B53A3A; }"
            "QPushButton:pressed { background-color: #951A1A; }"
        )

        self.query_button.setMinimumHeight(45)
        self.query_button.clicked.connect(self.query_team)
        
        if self.is_admin:
            # 修改按钮文本
            self.modify_team_name_button = QPushButton('修改队伍名')
            self.modify_team_name_button.setStyleSheet(
                "QPushButton { background-color: #A52A2A; color: white; border-radius: 10px; padding: 12px; font-weight: bold; font-size: 20px; }"
                "QPushButton:hover { background-color: #B53A3A; }"
                "QPushButton:pressed { background-color: #951A1A; }"
            )
            self.modify_team_name_button.setMinimumHeight(45)
            # 修改连接的方法名称
            self.modify_team_name_button.clicked.connect(self.modify_team_name)
            button_layout.addWidget(self.modify_team_name_button) 

        button_layout.addWidget(self.query_button)
        query_layout.addLayout(button_layout)
        
        main_layout.addWidget(query_frame)
        
        # 结果表格区域 - 降低透明度
        result_frame = QFrame()
        result_frame.setStyleSheet("background-color: rgba(255, 245, 245, 100); border-radius: 15px; border: 1px solid #E0D0D0;")
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(20, 20, 20, 20)
        
        result_label = QLabel("查询结果")
        result_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("color: #303030; padding: 8px; background-color: rgba(230, 200, 200, 200); border-radius: 8px;")
        result_layout.addWidget(result_label)
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(['队伍名称', '所属地', '世界排名', '教练', '荣誉', '近期胜率'])
        self.result_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #A52A2A; color: white; font-weight: bold; "
            "padding: 10px; border: none; font-size: 20px; }"
        )
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setStyleSheet(
            "QTableWidget { background-color: rgba(255, 255, 255, 100); border: 1px solid #E0D0D0; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #F0E0E0; color: #404040; }"
            "QTableWidget::item:selected { background-color: #F0C0C0; color: #000000; }"
            "QScrollBar:vertical { background: #F0F0F0; width: 12px; }"
            "QScrollBar::handle:vertical { background: #D0C0C0; min-height: 20px; border-radius: 6px; }"
        )
        self.result_table.setAlternatingRowColors(True)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setMinimumHeight(300)
        
        result_layout.addWidget(self.result_table)
        main_layout.addWidget(result_frame, 1)  # 添加伸缩因子
        
        self.setLayout(main_layout)
        self.center()
        self.update_background()

    def query_all_teams(self):
        try:
            self.db.cursor.execute("SELECT * FROM teams")
            teams = self.db.cursor.fetchall()
            self.result_table.setRowCount(len(teams))
            if teams:
                columns = ['team_name', 'country', 'world_ranking', 'coach_name', 'honors', 'recent_win_rate']
                for row_idx, team in enumerate(teams):
                    for col_idx, column in enumerate(columns):
                        data = str(team.get(column, ''))
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到队伍记录')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def query_team(self):
        team_name = self.team_name.text()
        if not team_name:
            QMessageBox.warning(self, '错误', '请输入队伍名称')
            return

        try:
            self.db.cursor.execute("SELECT * FROM teams WHERE team_name=%s", (team_name,))
            team = self.db.cursor.fetchone()
            self.result_table.setRowCount(1)
            if team:
                columns = ['team_name', 'country', 'world_ranking', 'coach_name', 'honors', 'recent_win_rate']
                for col_idx, column in enumerate(columns):
                    data = str(team.get(column, ''))
                    self.result_table.setItem(0, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到匹配的队伍')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def modify_team_name(self):
        team_name = self.team_name.text()
        if not team_name:
            QMessageBox.warning(self, '错误', '请先输入队伍名称')
            return
        
        new_name, ok = QInputDialog.getText(self, '修改队伍名', '请输入新的队伍名:')
        if ok:
            try:
                # 调用存储过程 update_team_name
                self.db.cursor.callproc('update_team_name', (team_name, new_name))
                # 提交事务
                self.db.conn.commit()
                QMessageBox.information(self, '成功', '队伍名修改成功')
                self.query_team()  # 刷新显示
            except pymysql.Error as err:
                QMessageBox.warning(self, '错误', f'修改队伍名失败: {err}')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.update_background()
        return super().resizeEvent(event)

    def update_background(self):
        palette = QPalette()
        pixmap = QPixmap("images/teams.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)