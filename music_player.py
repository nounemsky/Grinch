import os
from PyQt5.QtWidgets import QFrame, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QListWidget
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from ui import UIComponents

class TrackLoaderThread(QThread):
    track_loaded = pyqtSignal(str)

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        """Метод для фоновой загрузки треков."""
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(('.mp3', '.wav', '.ogg')):
                self.track_loaded.emit(file_name)


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Музыкальный плеер')
        self.resize(900, 600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.tracks = []  # Список треков
        self.current_track_index = 0
        self.is_playing = False
        self.player = QMediaPlayer()

        self.ui_components = UIComponents(self)
        self.initUI()

        # Запуск загрузки треков в фоновом потоке
        self.start_loading_tracks()

        # Подключаем сигнал для обновления прогресс-бара
        self.player.positionChanged.connect(self.update_progress_bar)

    def start_loading_tracks(self):
        """Запуск фоновой загрузки треков."""
        self.track_loader_thread = TrackLoaderThread("Music")
        self.track_loader_thread.track_loaded.connect(self.add_track_to_list)
        self.track_loader_thread.start()

    def add_track_to_list(self, track_name):
        """Добавление трека в список в основном потоке."""
        self.track_list_widget.addItem(track_name)
        self.tracks.append(track_name)

        # Автоматически выбираем первый трек после загрузки первого элемента
        if len(self.tracks) == 1:
            self.track_list_widget.setCurrentRow(0)
            self.load_track(0)

    def initUI(self):
        """Инициализация пользовательского интерфейса."""
        main_layout = QVBoxLayout()

        # Создаем верхнюю панель
        top_panel = self.ui_components.create_top_panel()
        main_layout.addWidget(top_panel)

        # Создаем горизонтальное расположение для боковой панели и содержимого
        horizontal_layout = QHBoxLayout()

        # Создаем боковую панель
        side_panel = self.ui_components.create_side_panel()
        horizontal_layout.addWidget(side_panel)

        # Компоновка для треков и кнопок
        track_and_controls_layout = QVBoxLayout()
        self.track_list_widget = self.ui_components.create_track_list_widget()
        track_and_controls_layout.addWidget(self.track_list_widget)

        # Создаем прогресс-бар и метку времени
        progress_layout = self.ui_components.create_progress_bar()
        self.progress_bar = self.ui_components.progress_bar

        # Добавляем прогресс-бар и метку времени к основному layout
        track_and_controls_layout.addLayout(progress_layout)

        # Создаем панель управления и добавляем её на существующий layout
        self.ui_components.create_control_panel(track_and_controls_layout, self.progress_bar)

        # Добавляем содержимое в горизонтальное расположение
        horizontal_layout.addLayout(track_and_controls_layout)

        # Добавляем горизонтальное расположение в основное
        main_layout.addLayout(horizontal_layout)

        # Создаем центральный виджет и устанавливаем компоновку
        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet("background-color: rgba(80, 80, 80, 169); border-radius: 15px;")
        self.setCentralWidget(container)

        # Сохранение ссылки на play_pause_button
        self.play_pause_button = self.ui_components.play_pause_button

        # Подключаем обработчик события окончания трека
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)

    def load_tracks(self):
        """Загрузка треков из папки Music."""
        music_folder = "Music"
        for file_name in os.listdir(music_folder):
            if file_name.endswith(('.mp3', '.wav', '.ogg')):
                self.track_list_widget.addItem(file_name)
                self.tracks.append(file_name)

        if self.tracks:
            self.track_list_widget.setCurrentRow(0)
            self.load_track(0)
        else:
            # Обработка ситуации, если нет треков
            self.track_list_widget.addItem("Нет доступных треков")

    def toggle_fullscreen(self):
        """Переключение полноэкранного режима."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def start_drag(self, event):
        """Начало перетаскивания окна."""
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            self.setCursor(Qt.OpenHandCursor)

    def perform_drag(self, event):
        """Перетаскивание окна."""
        if self.offset is not None:
            self.move(self.pos() + event.pos() - self.offset)

    def end_drag(self, event):
        """Завершение перетаскивания окна."""
        self.offset = None
        self.setCursor(Qt.ArrowCursor)

    def load_track(self, index):
        """Загрузка выбранного трека (без автоматического воспроизведения)."""
        if index < 0 or index >= len(self.tracks):
            return
        track = self.tracks[index]
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.join("Music", track))))
        self.is_playing = False
        self.update_play_pause_button()

        # Устанавливаем максимальное значение прогресс-бара
        duration = self.player.duration()
        self.progress_bar.setMaximum(duration if duration > 0 else 1)

    def on_media_status_changed(self, status):
        """Обработка события окончания трека."""
        if status == QMediaPlayer.EndOfMedia:
            self.current_track_index = (self.current_track_index + 1) % len(self.tracks)  # Переход на следующий трек
            self.load_track(self.current_track_index)
            self.player.play()
            self.is_playing = True
            self.update_play_pause_button()

    def update_progress_bar(self):
        """Обновление прогресс-бара в зависимости от текущей позиции воспроизведения."""
        if self.is_playing and self.progress_bar is not None:
            position = self.player.position()
            duration = self.player.duration()

            print(f"Текущая позиция: {position}, Длительность: {duration}")

            if duration > 0:
                self.progress_bar.setMaximum(duration)
                self.progress_bar.setValue(position)

                current_time = self.format_time(position)
                total_time = self.format_time(duration)

                self.ui_components.current_time_label.setText(current_time)
                self.ui_components.total_time_label.setText(total_time)

    def format_time(self, milliseconds):
        print(f"Форматирование времени: {milliseconds} мс")
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02}:{seconds:02}"

    def play_prev_track(self):
        """Функция для воспроизведения предыдущего трека."""
        if self.tracks:
            self.current_track_index = (self.current_track_index - 1) % len(self.tracks)
            self.load_track(self.current_track_index)
            self.is_playing = True
            self.update_play_pause_button()

    def play_next_track(self):
        """Функция для воспроизведения следующего трека."""
        if self.tracks:
            self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
            self.load_track(self.current_track_index)
            self.player.play()
            self.is_playing = True
            self.update_play_pause_button()

    def play_pause(self):
        """Функция для воспроизведения/паузы трека."""
        if not self.tracks:
            return

        if not self.is_playing:
            self.player.play()
            self.is_playing = True
        else:
            self.player.pause()
            self.is_playing = False

        self.update_play_pause_button()

    def update_play_pause_button(self):
        """Обновление иконки кнопки воспроизведения/паузы."""
        if self.is_playing:
            self.play_pause_button.setIcon(QIcon('images/pause.png'))
        else:
            self.play_pause_button.setIcon(QIcon('images/play.png'))
