from PyQt5.QtWidgets import QLabel, QHBoxLayout, QPushButton, QFrame, QListWidget, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QSize, QTimer, QTime
from PyQt5.QtGui import QIcon

class UIComponents:
    def __init__(self, parent):
        self.parent = parent
        self.window_time_label = QLabel()
        self.setup_timer()

    def setup_timer(self):
        """Настраиваем таймер для обновления метки текущего времени."""
        timer = QTimer(self.parent)
        timer.timeout.connect(self.update_time)
        timer.start(1000)


    def update_time(self):
        """Обновляем метку текущего времени."""
        current_time = QTime.currentTime().toString("HH:mm")
        self.window_time_label.setText(current_time)

    def create_top_panel(self):
        """Создаем верхнюю панель с функциями перетаскивания и текущим временем."""
        top_panel = QFrame(self.parent)
        top_panel.setStyleSheet("background-color: rgba(50, 50, 50, 200); border-radius: 7px;")
        top_panel.setFixedHeight(30)
        top_panel.mousePressEvent = self.parent.start_drag
        top_panel.mouseMoveEvent = self.parent.perform_drag
        top_panel.mouseReleaseEvent = self.parent.end_drag

        # Убираем фон у метки времени
        self.window_time_label.setStyleSheet("color: white; background: none;")

        # Создаем QLabel для изображения
        image_label = QLabel(top_panel)
        image_label.setPixmap(QIcon('images/grinch.png').pixmap(QSize(28, 28)))
        image_label.setFixedSize(28, 28)

        # Убираем фон у метки изображения
        image_label.setAttribute(Qt.WA_TranslucentBackground)
        image_label.setStyleSheet("background: none;")

        # Устанавливаем фиксированную позицию для изображения
        image_x = 435
        image_y = 1
        image_label.move(image_x, image_y)

        # Создаем горизонтальный компоновщик для метки времени и кнопок
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.window_time_label)
        control_layout.addStretch(1)
        control_layout.addLayout(self.create_control_buttons())

        # Устанавливаем компоновку на верхнюю панель
        top_panel_layout = QVBoxLayout(top_panel)
        top_panel_layout.addLayout(control_layout)

        top_panel.setLayout(top_panel_layout)

        return top_panel

    def create_track_list_widget(self):
        """Создаем виджет для списка треков."""
        track_list_widget = QListWidget()
        track_list_widget.setStyleSheet("""
            QListWidget {
                background-color: rgba(18, 18, 18, 200);
                color: #FFFFFF;
                border: none;
                border-radius: 12px;  /* Закругление углов списка */
            }
        """)
        return track_list_widget

    def create_control_panel(self, layout, progress_bar):
        """Создание панели управления с кнопками и прогресс-баром."""
        control_panel = QHBoxLayout()

        # Задаем стиль для панели управления
        control_panel_widget = QFrame()
        control_panel_widget.setLayout(control_panel)
        control_panel_widget.setStyleSheet("""
            background-color: rgba(50, 50, 50, 50);  /* Полупрозрачный фон */
            border-radius: 8px;  /* Закругление углов */
            padding: 0px;  /* Отступы внутри панели */
        """)

        # Кнопки управления
        self.prev_button = self.create_control_button('images/prev.png', self.parent.play_prev_track)
        self.play_pause_button = self.create_control_button('images/play.png', self.parent.play_pause)
        self.next_button = self.create_control_button('images/next.png', self.parent.play_next_track)

        # Добавляем кнопки на панель управления
        control_panel.addWidget(self.prev_button)
        control_panel.addWidget(self.play_pause_button)
        control_panel.addWidget(self.next_button)

        # Добавляем прогресс-бар, который был передан в метод
        control_panel.addWidget(progress_bar)

        # Добавляем фрейм с панелью управления в layout
        layout.addWidget(control_panel_widget)

    def create_progress_bar(self):
        """Создаем прогресс-бар для отображения времени воспроизведения трека."""
        print("Создаётся прогресс-бар") # log

        # Создаем прогресс-бар
        self.progress_bar = QProgressBar()  # Создаем атрибут класса
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 4px;  /* Закругление углов */
                background-color: rgba(29, 29, 29, 200);  /* Цвет фона прогресс-бара */
            }
            QProgressBar::chunk {
                background-color: rgba(200, 200, 200, 255);  /* Цвет заполненной части */
                border-radius: 4px;  /* Закругление углов заполненной части */
            }
        """)

        # Создаем метки для отображения времени
        self.current_time_label = QLabel("00:00")
        self.total_time_label = QLabel("00:00")
        self.current_time_label.setStyleSheet("color: #FFFFFF;")
        self.total_time_label.setStyleSheet("color: #FFFFFF;")

        # Создаем горизонтальное расположение для прогресс-бара и меток
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.current_time_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.total_time_label)

        return progress_layout  # Возвращаем компоновку

    def create_side_panel(self):
        """Создаем боковую панель для дополнительных функций."""
        side_panel = QFrame(self.parent)
        side_panel.setStyleSheet("background-color: rgba(37, 37, 37, 150); border-radius: 7px;")
        side_panel.setFixedWidth(140)
        side_panel.setMouseTracking(True)

        # Кнопка для управления плейлистами
        home_button = QPushButton("Главная", side_panel)
        home_button.setStyleSheet("background-color: rgba(29, 185, 84, 200); border: none; border-radius: 5px;")

        # Кнопка для управления плейлистами
        settings_button = QPushButton("Настройки", side_panel)
        settings_button.setStyleSheet("background-color: rgba(29, 185, 84, 200); border: none; border-radius: 5px;")

        # Устанавливаем фиксированную позицию для кнопки
        button_x = 5  # Задайте нужное значение x
        button_y = 80  # Задайте нужное значение y
        home_button.setGeometry(button_x, button_y, 120, 30)

        # Устанавливаем фиксированную позицию для кнопки
        button_x = 5  # Задайте нужное значение x
        button_y = 130  # Задайте нужное значение y
        settings_button.setGeometry(button_x, button_y, 120, 30)

        # Здесь можно добавить другие кнопки или элементы
        return side_panel

    def create_control_buttons(self):
        """Создаем кнопки управления."""
        control_buttons_layout = QHBoxLayout()

        # Кнопка закрытия
        close_button = self.create_icon_button('images/close1.png', self.parent.close, 'rgba(255, 95, 86, 255)')
        # Кнопка свернуть во весь экран
        maximize_button = self.create_icon_button('images/maximize1.png', self.parent.toggle_fullscreen, 'rgba(39, 201, 63, 255)')
        # Кнопка свернуть окно
        minimize_button = self.create_icon_button('images/minimize1.png', self.parent.showMinimized, 'rgba(255, 189, 46, 255)')

        # Добавляем кнопки управления в layout
        control_buttons_layout.addWidget(minimize_button)
        control_buttons_layout.addWidget(maximize_button)
        control_buttons_layout.addWidget(close_button)

        # Выравниваем кнопки вправо
        control_buttons_layout.setAlignment(Qt.AlignRight)

        return control_buttons_layout

    def create_control_button(self, icon_path, callback, icon_size=28):
        """Создаем кнопку управления с иконкой."""
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(icon_size, icon_size))
        button.setStyleSheet("background-color: rgba(29, 185, 84, 222); border: none; border-radius: 8px;")
        button.clicked.connect(callback)
        return button

    def create_icon_button(self, hover_icon_path, callback, background_color):
        """Создаем кнопку с иконкой и эффектом при наведении."""
        button = QPushButton()
        button.setFixedSize(15, 15)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {background_color};
                border-radius: 7px;
                background-repeat: no-repeat;
                background-position: center;
            }}
            QPushButton:hover {{
                background-image: url({hover_icon_path});  /* Изображение при наведении */
            }}
        """)
        button.clicked.connect(callback)
        return button
