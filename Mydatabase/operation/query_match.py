# [file name]: query_match.py
import pymysql
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDesktopWidget, \
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QColor, QLinearGradient
from PyQt5.QtCore import Qt
from db import Database

class QueryMatch(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()
        # 默认查询所有比赛
        self.query_all_matches()

    def initUI(self):
        self.setWindowTitle('查询比赛')
        self.setMinimumSize(1000, 700)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)
        
        # 标题 - 使用更深的蓝色
        title_label = QLabel("比赛查询系统")
        title_label.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #FFFFFF; background-color: rgba(20, 40, 100, 220); "
                                 "border-radius: 15px; padding: 15px;")
        main_layout.addWidget(title_label)
        
        # 查询区域 - 降低透明度
        query_frame = QFrame()
        query_frame.setStyleSheet("background-color: rgba(245, 245, 255, 100); border-radius: 15px; border: 1px solid #D0D0E0;")
        query_layout = QVBoxLayout(query_frame)
        query_layout.setContentsMargins(30, 30, 30, 30)
        query_layout.setSpacing(20)
        
        # 名称查询
        name_group = QHBoxLayout()
        name_label = QLabel("比赛名称:")
        name_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        name_label.setFixedWidth(120)
        name_label.setStyleSheet("color: #303030;")
        self.match_name = QLineEdit()
        self.match_name.setPlaceholderText('请输入比赛名称')
        self.match_name.setStyleSheet("background-color: rgba(255, 255, 255, 100); border: 1px solid #C0C0D0; border-radius: 8px; padding: 8px;")
        self.match_name.setMinimumHeight(40)
        name_group.addWidget(name_label)
        name_group.addWidget(self.match_name)
        
        # 参与队伍查询
        team_group = QHBoxLayout()
        team_label = QLabel("参与队伍:")
        team_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        team_label.setFixedWidth(120)
        team_label.setStyleSheet("color: #303030;")
        self.team_name = QLineEdit()
        self.team_name.setPlaceholderText('请输入参与队伍名称')
        self.team_name.setStyleSheet("background-color: rgba(255, 255, 255, 100); border: 1px solid #C0C0D0; border-radius: 8px; padding: 8px;")
        self.team_name.setMinimumHeight(40)
        team_group.addWidget(team_label)
        team_group.addWidget(self.team_name)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        
        self.query_by_name_button = QPushButton('根据比赛名称查询')
        self.query_by_name_button.setStyleSheet(
            "QPushButton { background-color: #2A5CA7; color: white; border-radius: 10px; padding: 12px; font-weight: bold; font-size: 20px; }"
            "QPushButton:hover { background-color: #3A6CB7; }"
            "QPushButton:pressed { background-color: #1A4C97; }"
        )
        self.query_by_name_button.setMinimumHeight(45)
        self.query_by_name_button.clicked.connect(self.query_matches_by_name)
        
        self.query_by_team_button = QPushButton('根据参与队伍查询')
        self.query_by_team_button.setStyleSheet(
            "QPushButton { background-color: #2A5CA7; color: white; border-radius: 10px; padding: 12px; font-weight: bold; font-size: 20px; }"
            "QPushButton:hover { background-color: #3A6CB7; }"
            "QPushButton:pressed { background-color: #1A4C97; }"
        )
        self.query_by_team_button.setMinimumHeight(45)
        self.query_by_team_button.clicked.connect(self.query_matches_by_team)
        
        button_layout.addWidget(self.query_by_name_button)
        button_layout.addWidget(self.query_by_team_button)
        
        # 添加到查询区域
        query_layout.addLayout(name_group)
        query_layout.addLayout(team_group)
        query_layout.addLayout(button_layout)
        main_layout.addWidget(query_frame)
        
        # 结果表格区域 - 降低透明度
        result_frame = QFrame()
        result_frame.setStyleSheet("background-color: rgba(245, 245, 255, 100); border-radius: 15px; border: 1px solid #D0D0E0;")
        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(20, 20, 20, 20)
        
        result_label = QLabel("查询结果")
        result_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        result_label.setAlignment(Qt.AlignCenter)
        result_label.setStyleSheet("color: #303030; padding: 8px; background-color: rgba(200, 210, 230, 200); border-radius: 8px;")
        result_layout.addWidget(result_label)
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(['比赛名称', '主办方','开始日期', '结束日期', '参加队伍'])
        self.result_table.horizontalHeader().setStyleSheet(
            "QHeaderView::section { background-color: #2A5CA7; color: white; font-weight: bold; "
            "padding: 10px; border: none; font-size: 20px; }"
        )
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setStyleSheet(
            "QTableWidget { background-color: rgba(255, 255, 255, 100); border: 1px solid #D0D0E0; }"
            "QTableWidget::item { padding: 8px; border-bottom: 1px solid #E0E0F0; color: #404040; }"
            "QTableWidget::item:selected { background-color: #B8D1FF; color: #000000; }"
            "QScrollBar:vertical { background: #F0F0F0; width: 12px; }"
            "QScrollBar::handle:vertical { background: #C0C0D0; min-height: 20px; border-radius: 6px; }"
        )
        self.result_table.setAlternatingRowColors(True)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setMinimumHeight(300)
        
        result_layout.addWidget(self.result_table)
        main_layout.addWidget(result_frame, 1)  # 添加伸缩因子
        
        self.setLayout(main_layout)
        self.center()
        self.update_background()

    def query_all_matches(self):
        try:
            # 从视图中查询所有比赛信息
            self.db.cursor.execute("SELECT * FROM match_info_with_teams")
            matches = self.db.cursor.fetchall()
            self.result_table.setRowCount(len(matches))
            if matches:
                columns = ['match_name', 'organizer_name', 'start_date', 'end_date', 'participating_team']
                self.result_table.setColumnCount(len(columns))
                self.result_table.setHorizontalHeaderLabels(columns)
                for row_idx, match in enumerate(matches):
                    for col_idx, column in enumerate(columns):
                        data = str(match.get(column, ''))
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到比赛记录')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def query_matches_by_name(self):
        match_name = self.match_name.text()

        if not match_name:
            QMessageBox.warning(self, '错误', '请输入比赛名称')
            return

        try:
            # 根据比赛名从视图中查询
            self.db.cursor.execute("SELECT * FROM match_info_with_teams WHERE match_name=%s", (match_name,))

            matches = self.db.cursor.fetchall()
            self.result_table.setRowCount(len(matches))
            if matches:
                columns = ['match_name', 'organizer_name','start_date', 'end_date', 'participating_team']
                self.result_table.setColumnCount(len(columns))
                self.result_table.setHorizontalHeaderLabels(columns)
                for row_idx, match in enumerate(matches):
                    for col_idx, column in enumerate(columns):
                        data = str(match.get(column, ''))
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到匹配的比赛')
        except pymysql.Error as err:
            QMessageBox.warning(self, '错误', f'查询失败: {err}')

    def query_matches_by_team(self):
        team_name = self.team_name.text()

        if not team_name:
            QMessageBox.warning(self, '错误', '请输入参与队伍名称')
            return

        try:
            # 根据参与队伍名从视图中查询
            self.db.cursor.execute("SELECT * FROM match_info_with_teams WHERE participating_team=%s", (team_name,))

            matches = self.db.cursor.fetchall()
            self.result_table.setRowCount(len(matches))
            if matches:
                columns = ['match_name', 'organizer_name','start_date', 'end_date', 'participating_team']
                self.result_table.setColumnCount(len(columns))
                self.result_table.setHorizontalHeaderLabels(columns)
                for row_idx, match in enumerate(matches):
                    for col_idx, column in enumerate(columns):
                        data = str(match.get(column, ''))
                        self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(data))
            else:
                self.result_table.setRowCount(0)
                QMessageBox.information(self, '提示', '未找到该队伍参与的比赛')
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
        pixmap = QPixmap("images/match.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)