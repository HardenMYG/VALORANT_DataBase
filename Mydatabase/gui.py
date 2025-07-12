from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox, QDesktopWidget, QApplication, QGroupBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt
from db import Database
from operation.query_player import QueryPlayer
from operation.query_team import QueryTeam
from operation.query_match import QueryMatch
from operation.add_player import AddPlayer
from operation.add_team import AddTeam
from operation.add_match import AddMatch
from operation.delete_player import DeletePlayer
from operation.delete_team import DeleteTeam
from operation.delete_match import DeleteMatch


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin Login')
        self.setGeometry(100, 50, 1200, 800)
        self.center()

        layout = QVBoxLayout()

        # 保存背景图片路径
        self.background_image_path = "images/background.png"
        self.set_background_image()

        # 创建透明垫层
        title_container = QWidget()
        title_container.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 20px; padding: 20px;")
        title_layout = QVBoxLayout()

        title_label = QLabel('Valorant赛事数据库管理系统', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 28, QFont.Black))
        title_label.setStyleSheet("color: white; background-color: transparent;")
        title_layout.addWidget(title_label)

        title_container.setLayout(title_layout)
        layout.addWidget(title_container, alignment=Qt.AlignCenter)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('用户名')
        self.username_input.setFont(QFont('Arial', 20))
        self.username_input.setFixedSize(600, 100)
        # 设置 QLineEdit 的样式表，圆角矩形，透明度 50%
        self.username_input.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 128); border-radius: 25px;")
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont('Arial', 20))
        self.password_input.setFixedSize(600, 100)
        # 设置 QLineEdit 的样式表，圆角矩形，透明度 50%
        self.password_input.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 128); border-radius: 25px;")
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        self.admin_checkbox = QCheckBox('管理员登录(不勾选为用户登录)', self)
        self.admin_checkbox.setChecked(False)
        self.admin_checkbox.setFont(QFont('Arial', 12))
        self.admin_checkbox.setStyleSheet("color: white")
        layout.addWidget(self.admin_checkbox, alignment=Qt.AlignCenter)

        # 创建水平布局来放置登录和注册按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(1)  # 设置按钮之间的间距
        button_layout.setContentsMargins(400, 0, 400, 200)

        self.login_button = QPushButton('登录', self)
        self.login_button.setFont(QFont('Arial', 20))  # 增大字体
        self.login_button.setFixedSize(300, 100)  # 增大按钮尺寸
        self.login_button.clicked.connect(self.handle_login)
        # 设置 QPushButton 的样式表，圆角矩形，透明度 50%
        self.login_button.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 128); border-radius: 50px;")
        button_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.register_button = QPushButton('注册', self)
        self.register_button.setFont(QFont('Arial', 20))  # 增大字体
        self.register_button.setFixedSize(300, 100)  # 增大按钮尺寸
        self.register_button.clicked.connect(self.handle_register)
        # 设置 QPushButton 的样式表，圆角矩形，透明度 50%
        self.register_button.setStyleSheet("color: white;background-color: rgba(255, 255, 255, 128); border-radius: 50px;")
        button_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        # 修改这一行：正确设置布局的对齐方式
        layout.addLayout(button_layout)  # 移除 alignment 参数

        self.setLayout(layout)

    def set_background_image(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap(self.background_image_path)
        pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(self.backgroundRole(), QBrush(pixmap))
        self.setPalette(palette)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        is_admin = self.admin_checkbox.isChecked()

        # 显示加载提示
        loading = QMessageBox(self)
        loading.setWindowTitle("系统提示")
        loading.setText("正在验证登录信息...")
        loading.show()
        QApplication.processEvents()  # 强制刷新UI

        try:
            if is_admin:
                if self.db.verify_admin(username, password):
                    loading.accept()
                    self.main_window = MainWindow(is_admin=True)
                    self.main_window.show()
                    self.close()
                else:
                    loading.accept()
                    QMessageBox.warning(self, '错误', '管理员用户名或密码错误')
            else:
                if self.db.verify_user(username, password):
                    loading.accept()
                    self.main_window = MainWindow(is_admin=False)
                    self.main_window.show()
                    self.close()
                else:
                    loading.accept()
                    QMessageBox.warning(self, '错误', '用户用户名或密码错误')
        except Exception as e:
            loading.accept()
            QMessageBox.critical(self, '严重错误', f'数据库连接失败: {str(e)}')

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, '错误', '请输入用户名和密码')
            return

        try:
            self.db.register_user(username, password)
            QMessageBox.information(self, '成功', '注册成功，请登录')
        except Exception as err:
            QMessageBox.warning(self, '错误', f'注册失败: {err}')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.set_background_image()
        return super().resizeEvent(event)


class MainWindow(QWidget):
    def __init__(self, is_admin=True):
        super().__init__()
        self.db = Database()
        self.is_admin = is_admin
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Valorant赛事数据库管理系统')
        self.setGeometry(100, 50, 1200, 800)
        self.center()

        main_layout = QVBoxLayout()

        # 保存背景图片路径
        self.background_image_path = "images/background.png"
        self.set_background_image()

        # 上半部分 - 标题区域
        title_container = QWidget()
        title_container.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 20px; padding: 20px;")
        title_layout = QVBoxLayout()

        title_label = QLabel('Valorant赛事数据库管理系统', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 36, QFont.Black))
        title_label.setStyleSheet("color: white; background-color: transparent;")
        title_layout.addWidget(title_label)

        title_container.setLayout(title_layout)
        main_layout.addWidget(title_container, alignment=Qt.AlignTop)

        # 下半部分 - 操作分组区域
        groups_layout = QHBoxLayout()
        groups_layout.setSpacing(30)  # 增加分组之间的间距

        # 选手操作分组
        player_group = QGroupBox("选手操作")
        player_group.setFont(QFont('Arial', 18, QFont.Bold))  # 增大标题字体
        player_group.setStyleSheet("QGroupBox { color: white; border: 2px solid gray; border-radius: 12px; margin-top: 0.5em; background-color: rgba(0, 0, 0, 0.4); }"
                                   "QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px 0 5px; }")
        player_layout = QVBoxLayout()
        player_layout.setSpacing(15)  # 增加按钮之间的间距

        self.query_player_button = QPushButton('查询选手', self)
        self.query_player_button.setFont(QFont('Arial', 16))  # 增大按钮字体
        self.query_player_button.setFixedSize(240, 60)  # 增大按钮尺寸
        self.query_player_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                               "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
        self.query_player_button.clicked.connect(self.show_query_player)
        player_layout.addWidget(self.query_player_button, alignment=Qt.AlignCenter)

        if self.is_admin:
            self.add_player_button = QPushButton('添加选手', self)
            self.add_player_button.setFont(QFont('Arial', 16))  # 增大按钮字体
            self.add_player_button.setFixedSize(240, 60)  # 增大按钮尺寸
            self.add_player_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                                 "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
            self.add_player_button.clicked.connect(self.show_add_player)
            player_layout.addWidget(self.add_player_button, alignment=Qt.AlignCenter)

            self.delete_player_button = QPushButton('删除选手', self)
            self.delete_player_button.setFont(QFont('Arial', 16))  # 增大按钮字体
            self.delete_player_button.setFixedSize(240, 60)  # 增大按钮尺寸
            self.delete_player_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                                    "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
            self.delete_player_button.clicked.connect(self.show_delete_player)
            player_layout.addWidget(self.delete_player_button, alignment=Qt.AlignCenter)

        player_group.setLayout(player_layout)
        groups_layout.addWidget(player_group)

        # 比赛操作分组
        match_group = QGroupBox("比赛操作")
        match_group.setFont(QFont('Arial', 18, QFont.Bold))  # 增大标题字体
        match_group.setStyleSheet("QGroupBox { color: white; border: 2px solid gray; border-radius: 12px; margin-top: 0.5em; background-color: rgba(0, 0, 0, 0.4); }"
                                   "QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px 0 5px; }")
        match_layout = QVBoxLayout()
        match_layout.setSpacing(15)  # 增加按钮之间的间距

        self.query_match_button = QPushButton('查询比赛', self)
        self.query_match_button.setFont(QFont('Arial', 16))  # 增大按钮字体
        self.query_match_button.setFixedSize(240, 60)  # 增大按钮尺寸
        self.query_match_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                               "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
        self.query_match_button.clicked.connect(self.show_query_match)
        match_layout.addWidget(self.query_match_button, alignment=Qt.AlignCenter)

        if self.is_admin:
            self.add_match_button = QPushButton('创建比赛', self)
            self.add_match_button.setFont(QFont('Arial', 16))  # 增大按钮字体
            self.add_match_button.setFixedSize(240, 60)  # 增大按钮尺寸
            self.add_match_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                                "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
            self.add_match_button.clicked.connect(self.show_add_match)
            match_layout.addWidget(self.add_match_button, alignment=Qt.AlignCenter)

            self.delete_match_button = QPushButton('删除比赛', self)
            self.delete_match_button.setFont(QFont('Arial', 16))  # 增大按钮字体
            self.delete_match_button.setFixedSize(240, 60)  # 增大按钮尺寸
            self.delete_match_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                                   "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
            self.delete_match_button.clicked.connect(self.show_delete_match)
            match_layout.addWidget(self.delete_match_button, alignment=Qt.AlignCenter)

        match_group.setLayout(match_layout)
        groups_layout.addWidget(match_group)

        # 队伍操作分组
        team_group = QGroupBox("队伍操作")
        team_group.setFont(QFont('Arial', 18, QFont.Bold))  # 增大标题字体
        team_group.setStyleSheet("QGroupBox { color: white; border: 2px solid gray; border-radius: 12px; margin-top: 0.5em; background-color: rgba(0, 0, 0, 0.4); }"
                                   "QGroupBox::title { subcontrol-origin: margin; left: 15px; padding: 0 5px 0 5px; }")
        team_layout = QVBoxLayout()
        team_layout.setSpacing(15)  # 增加按钮之间的间距

        self.query_team_button = QPushButton('查询队伍', self)
        self.query_team_button.setFont(QFont('Arial', 16))  # 增大按钮字体
        self.query_team_button.setFixedSize(240, 60)  # 增大按钮尺寸
        self.query_team_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                             "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
        self.query_team_button.clicked.connect(self.show_query_team)
        team_layout.addWidget(self.query_team_button, alignment=Qt.AlignCenter)

        if self.is_admin:
            self.add_team_button = QPushButton('添加队伍', self)
            self.add_team_button.setFont(QFont('Arial', 16))  # 增大按钮字体
            self.add_team_button.setFixedSize(240, 60)  # 增大按钮尺寸
            self.add_team_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                               "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
            self.add_team_button.clicked.connect(self.show_add_team)
            team_layout.addWidget(self.add_team_button, alignment=Qt.AlignCenter)

            self.delete_team_button = QPushButton('删除队伍', self)
            self.delete_team_button.setFont(QFont('Arial', 16))  # 增大按钮字体
            self.delete_team_button.setFixedSize(240, 60)  # 增大按钮尺寸
            self.delete_team_button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0.8); border-radius: 8px; }"
                                                   "QPushButton:hover { background-color: rgba(255, 255, 255, 1); font-weight: bold; }")
            self.delete_team_button.clicked.connect(self.show_delete_team)
            team_layout.addWidget(self.delete_team_button, alignment=Qt.AlignCenter)

        team_group.setLayout(team_layout)
        groups_layout.addWidget(team_group)

        # 将水平布局添加到主布局的下半部分
        groups_widget = QWidget()
        groups_widget.setLayout(groups_layout)
        groups_widget.setMinimumHeight(400)  # 增加操作区域的最小高度
        groups_widget.setMaximumHeight(500)  # 增加操作区域的最大高度
        main_layout.addWidget(groups_widget, alignment=Qt.AlignBottom)

        self.setLayout(main_layout)

    def set_background_image(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap(self.background_image_path)
        pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(self.backgroundRole(), QBrush(pixmap))
        self.setPalette(palette)

    def show_query_player(self):
        self.query_player = QueryPlayer()
        self.query_player.show()

    def show_add_player(self):
        self.add_player = AddPlayer()
        self.add_player.show()

    def show_delete_player(self):
        self.delete_player = DeletePlayer()
        self.delete_player.show()

    def show_query_match(self):
        self.query_match = QueryMatch()
        self.query_match.show()

    def show_add_match(self):
        self.add_match = AddMatch()
        self.add_match.show()

    def show_delete_match(self):
        self.delete_match = DeleteMatch()
        self.delete_match.show()

    def show_query_team(self):
        self.query_team = QueryTeam(is_admin=self.is_admin)
        self.query_team.show()

    def show_add_team(self):
        self.add_team = AddTeam()
        self.add_team.show()

    def show_delete_team(self):
        self.delete_team = DeleteTeam()
        self.delete_team.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.set_background_image()
        return super().resizeEvent(event)
