import pymysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDesktopWidget, \
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QFrame, QSizePolicy
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
from db import Database

class QueryPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()
        self.query_all_players()

    def initUI(self):
        self.setWindowTitle('查询选手')
        self.setMinimumSize(1000, 700)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)
        
        # 标题 - 使用更深的绿色
        title_label = QLabel("选手查询系统")
        title_label.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #FFFFFF; background-color: rgba(20, 80, 20, 220); "
                                 "border-radius: 15px; padding: 15px;")
        main_layout.addWidget(title_label)
        
        # 查询区域 - 降低透明度
        query_frame = QFrame()
        query_frame.setStyleSheet("background-color: rgba(245, 255, 245, 100); border-radius: 15px; border: 1px solid #D0E0D0;")
        query_layout = QVBoxLayout(query_frame)
        query_layout.setContentsMargins(30, 30, 30, 30)
        query_layout.setSpacing(20)
        
        # 名称查询
        name_group = QHBoxLayout()
        name_label = QLabel("选手姓名:")
        name_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        name_label.setFixedWidth(120)
        name_label.setStyleSheet("color: #303030;")
        self.player_name = QLineEdit()
        self.player_name.setPlaceholderText('请输入选手姓名')
        self.player_name.setStyleSheet("background-color: rgba(255, 255, 255, 100); border: 1px solid #C0D0C0; border-radius: 8px; padding: 8px;")
        self.player_name.setMinimumHeight(40)
        name_group.addWidget(name_label)
        name_group.addWidget(self.player_name)
        
        # 队伍查询
        team_group = QHBoxLayout()
        team_label = QLabel("所属队伍:")
        team_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        team_label.setFixedWidth(120)
        team_label.setStyleSheet("color: #303030;")
        self.team_name = QLineEdit()
        self.team_name.setPlaceholderText('请输入队伍名称')
        self.team_name.setStyleSheet("background-color: rgba(255, 255, 255, 100); border: 1px solid #C0D0C0; border-radius: 8px; padding: 8px;")
        self.team_name.setMinimumHeight(40)
        team_group.addWidget(team_label)
        team_group.addWidget(self.team_name)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        
        self.query_by_name_button = QPushButton('根据姓名查询')
        self.query_by_name_button.setStyleSheet(
            "QPushButton { background-color: #3A7A3A; color: white; border-radius: 10px; padding: 12px; font-weight: bold; font-size: 20px; }"
            "QPushButton:hover { background-color: #4A8A4A; }"
            "QPushButton:pressed { background-color: #2A6A2A; }"
        )
        self.query_by_name_button.setMinimumHeight(45)
        self.query_by_name_button.clicked.connect(self.query_player_by_name)
        
        self.query_by_team_button = QPushButton('根据队伍查询')
        self.query_by_team_button.setStyleSheet(
            "QPushButton { background-color: #3A7A3A; color: white; border-radius: 10px; padding: 12px; font-weight: bold; font-size: 20px; }"
            "QPushButton:hover { background-color: #4A8A4A; }"
            "QPushButton:pressed { background-color: #2A6A2A; }"
        )
        self.query_by_team_button.setMinimumHeight(45)
        self.query_by_team_button.clicked.connect(self.query_players_by_team)

        self.query_by_both_button = QPushButton('同时根据姓名和队伍查询')
        self.query_by_both_button.setStyleSheet(
            "QPushButton { background-color: #3A7A3A; color: white; border-radius: 10px; padding: 12px; font-weight: bold; font-size: 20px; }"
            "QPushButton:hover { background-color: #4A8A4A; }"
            "QPushButton:pressed { background-color: #2A6A2A; }"
        )
        self.query_by_both_button.setMinimumHeight(45)
        self.query_by_both_button.clicked.connect(self.query_players_by_both)
        
        button_layout.addWidget(self.query_by_name_button)
        button_layout.addWidget(self.query_by_team_button)
        button_layout.addWidget(self.query_by_both_button)
        
        # 添加到查询区域
        query_layout.addLayout(name_group)
        query_layout.addLayout(team_group)
        query_layout.addLayout(button_layout)
        main_layout.addWidget(query_frame)
        
        # 结果表格区域 - 降低透明度
        result_frame = QFrame()
        result_frame.setStyleSheet("background-color: rgba(245, 255, 245, 100); border-radius: 15px; border: 1px solid #D0E0D0;")
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(20, 20, 20, 20)
        
        result_label = QLabel("查询结果")
        result_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("color: #303030; padding: 8px; background-color: rgba(200, 230, 200, 200); border-radius: 8px;")
        result_layout.addWidget(result_label)
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(['队伍名称', '号码', '姓名', '出生日期', '国籍', '位置'])
        self.result_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #3A7A3A; color: white; font-weight: bold; "
            "padding: 10px; border: none; font-size: 20px; }"
        )
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setStyleSheet(
            "QTableWidget { background-color: rgba(255, 255, 255, 100); border: 1px solid #D0E0D0; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #E0F0E0; color: #404040; }"
            "QTableWidget::item:selected { background-color: #C1E1C1; color: #000000; }"
            "QScrollBar:vertical { background: #F0F0F0; width: 12px; }"
            "QScrollBar::handle:vertical { background: #C0D0C0; min-height: 20px; border-radius: 6px; }"
        )
        self.result_table.setAlternatingRowColors(True)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setMinimumHeight(300)
        
        result_layout.addWidget(self.result_table)
        main_layout.addWidget(result_frame, 1)  # 添加伸缩因子
        
        self.setLayout(main_layout)
        self.center()
        self.update_background()

    def query_all_players(self):
        try:
            self.db.cursor.execute("SELECT * FROM players")
            players = self.db.cursor.fetchall()
            self.result_table.setRowCount(len(players))
            if players:
                columns = ['team_name', 'player_number', 'name', 'birthdate', 'nationality', 'position']
                for row_idx, player in enumerate(players):
                    for col_idx, column in enumerate(columns):
                        data = str(player.get(column, ''))
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到选手记录')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def query_player_by_name(self):
        player_name = self.player_name.text()
        if not player_name:
            QMessageBox.warning(self, '错误', '请输入选手姓名')
            return

        try:
            self.db.cursor.execute("SELECT * FROM players WHERE name=%s", (player_name,))
            players = self.db.cursor.fetchall()
            self.result_table.setRowCount(len(players))
            if players:
                columns = ['team_name', 'player_number', 'name', 'birthdate', 'nationality', 'position']
                for row_idx, player in enumerate(players):
                    for col_idx, column in enumerate(columns):
                        data = str(player.get(column, ''))
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到匹配的选手')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def query_players_by_team(self):
        team_name = self.team_name.text()
        if not team_name:
            QMessageBox.warning(self, '错误', '请输入队伍名称')
            return

        try:
            self.db.cursor.execute("SELECT * FROM players WHERE team_name=%s", (team_name,))
            players = self.db.cursor.fetchall()
            self.result_table.setRowCount(len(players))
            if players:
                columns = ['team_name', 'player_number', 'name', 'birthdate', 'nationality', 'position']
                for row_idx, player in enumerate(players):
                    for col_idx, column in enumerate(columns):
                        data = str(player.get(column, ''))
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到匹配的选手')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def query_players_by_both(self):
        player_name = self.player_name.text()
        team_name = self.team_name.text()

        if not player_name or not team_name:
            QMessageBox.warning(self, '错误', '请输入选手姓名和队伍名称')
            return

        try:
            self.db.cursor.execute("SELECT * FROM players WHERE name=%s AND team_name=%s", (player_name, team_name))
            players = self.db.cursor.fetchall()
            self.result_table.setRowCount(len(players))
            if players:
                columns = ['team_name', 'player_number', 'name', 'birthdate', 'nationality', 'position']
                for row_idx, player in enumerate(players):
                    for col_idx, column in enumerate(columns):
                        data = str(player.get(column, ''))
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到匹配的选手')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

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
        pixmap = QPixmap("images/player.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)