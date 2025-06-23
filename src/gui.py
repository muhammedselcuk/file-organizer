import os
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox,
    QLineEdit, QComboBox, QCheckBox, QLabel, QRadioButton, QButtonGroup,
    QHBoxLayout, QScrollArea, QSizePolicy, QApplication, QProgressBar,
    QTextEdit, QSplitter, QFrame, QGroupBox, QGridLayout
)
from PySide6.QtCore import Qt, QThread, Signal, QObject, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent, QFont, QPixmap, QPainter, QColor
from .organizer import organize_files, move_files_to_parent

class FileOrganizerWorker(QObject):
    finished = Signal()
    progress = Signal(int)
    status_update = Signal(str)

    def __init__(self, folder_path, criteria, options, include_subfolders, time_period=None):
        super().__init__()
        self.folder_path = folder_path
        self.criteria = criteria
        self.options = options
        self.include_subfolders = include_subfolders
        self.time_period = time_period

    def run(self):
        try:
            self.status_update.emit("Starting file organization...")
            self.progress.emit(10)
            
            organize_files(
                self.folder_path,
                criteria=self.criteria,
                options=self.options,
                include_subfolders=self.include_subfolders,
                time_period=self.time_period
            )
            
            self.progress.emit(100)
            self.status_update.emit("Organization completed successfully!")
        except Exception as e:
            self.status_update.emit(f"Error: {str(e)}")
        self.finished.emit()

class FlattenWorker(QObject):
    finished = Signal()
    progress = Signal(int)
    status_update = Signal(str)

    def __init__(self, folder_path, include_subfolders):
        super().__init__()
        self.folder_path = folder_path
        self.include_subfolders = include_subfolders

    def run(self):
        try:
            self.status_update.emit("Starting directory flattening...")
            self.progress.emit(20)
            
            move_files_to_parent(self.folder_path, self.include_subfolders)
            
            self.progress.emit(100)
            self.status_update.emit("Directory flattened successfully!")
        except Exception as e:
            self.status_update.emit(f"Error: {str(e)}")
        self.finished.emit()

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        super().enterEvent(event)
        # Add subtle scale animation on hover
        
    def leaveEvent(self, event):
        super().leaveEvent(event)
        # Reset animation

class FileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.worker = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('🗂️ Advanced File Organizer Pro')
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'logo.png')))
        self.setAcceptDrops(True)
        self.resize(800, 700)
        self.setObjectName("mainWindow")

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Title Section
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("🗂️ Advanced File Organizer Pro")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Organize your files with style and efficiency")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #a0a0a0; font-size: 14px; margin-bottom: 10px;")
        title_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(title_frame)

        # Main Content Splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left Panel - Controls
        left_panel = QFrame()
        left_panel.setFixedWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)

        # Directory Selection Group
        dir_group = QGroupBox("📁 Select Directory")
        dir_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 15px; }")
        dir_layout = QVBoxLayout(dir_group)
        
        # Directory input with better styling
        dir_input_layout = QHBoxLayout()
        self.directory_input = QLineEdit()
        self.directory_input.setPlaceholderText('🖱️ Drag & drop or click to select folder...')
        self.directory_input.textChanged.connect(self.update_file_count)
        
        self.select_button = AnimatedButton('📂 Browse')
        self.select_button.clicked.connect(self.select_folder)
        self.select_button.setFixedWidth(100)
        
        dir_input_layout.addWidget(self.directory_input)
        dir_input_layout.addWidget(self.select_button)
        dir_layout.addLayout(dir_input_layout)
        
        left_layout.addWidget(dir_group)

        # Organization Criteria Group
        criteria_group = QGroupBox("⚙️ Organization Settings")
        criteria_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 15px; }")
        criteria_layout = QVBoxLayout(criteria_group)
        
        # Criteria selection
        criteria_layout.addWidget(QLabel('Organize By:'))
        self.criteria_combo = QComboBox()
        self.criteria_combo.addItems([
            '🕐 Creation Time',
            '📝 Modified Time', 
            '👁️ Last Accessed Time',
            '📄 File Extension',
            '📏 File Size'
        ])
        self.criteria_combo.currentIndexChanged.connect(self.criteria_changed)
        criteria_layout.addWidget(self.criteria_combo)

        # Options Area with better styling
        self.options_area = QScrollArea()
        self.options_area.setWidgetResizable(True)
        self.options_area.setMaximumHeight(150)
        self.options_content = QWidget()
        self.options_layout = QVBoxLayout(self.options_content)
        self.options_layout.setContentsMargins(10, 10, 10, 10)
        self.options_layout.setSpacing(8)
        self.options_area.setWidget(self.options_content)
        criteria_layout.addWidget(self.options_area)

        # Include/Exclude Subfolders
        self.exclude_subfolders_checkbox = QCheckBox('🗂️ Exclude Subfolders')
        self.exclude_subfolders_checkbox.setToolTip("Check this to exclude files in subdirectories")
        criteria_layout.addWidget(self.exclude_subfolders_checkbox)
        
        left_layout.addWidget(criteria_group)

        # Action Buttons Group
        action_group = QGroupBox("🚀 Actions")
        action_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 15px; }")
        action_layout = QVBoxLayout(action_group)
        
        buttons_layout = QGridLayout()
        
        self.organize_button = AnimatedButton('🗂️ Organize Files')
        self.organize_button.setObjectName("organizeButton")
        self.organize_button.clicked.connect(self.organize_from_input)
        self.organize_button.setMinimumHeight(45)
        
        self.flatten_button = AnimatedButton('📤 Flatten Directory')
        self.flatten_button.setObjectName("flattenButton")
        self.flatten_button.clicked.connect(self.flatten_directory_structure)
        self.flatten_button.setMinimumHeight(45)
        
        buttons_layout.addWidget(self.organize_button, 0, 0)
        buttons_layout.addWidget(self.flatten_button, 0, 1)
        action_layout.addLayout(buttons_layout)
        
        left_layout.addWidget(action_group)
        
        # Progress Section
        progress_group = QGroupBox("📊 Progress")
        progress_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 15px; }")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4a9eff;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                color: white;
                background-color: #3c3c3c;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                           stop: 0 #4a9eff, stop: 1 #20c997);
                border-radius: 6px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #20c997; font-weight: bold;")
        progress_layout.addWidget(self.status_label)
        
        left_layout.addWidget(progress_group)

        # File Count
        self.file_count_label = QLabel('📁 Select a folder to see file count')
        self.file_count_label.setObjectName("fileCountLabel")
        self.file_count_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.file_count_label)

        left_layout.addStretch()
        splitter.addWidget(left_panel)

        # Right Panel - Log/Preview
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        
        log_group = QGroupBox("📋 Activity Log")
        log_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 15px; }")
        log_layout = QVBoxLayout(log_group)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 2px solid #4a9eff;
                border-radius: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        self.log_display.append("Welcome to Advanced File Organizer Pro! 🎉")
        self.log_display.append("Select a folder and choose your organization criteria to get started.")
        
        log_layout.addWidget(self.log_display)
        right_layout.addWidget(log_group)
        
        splitter.addWidget(right_panel)
        main_layout.addWidget(splitter)

        # Set Size Policy for responsiveness
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Load styles
        self.load_stylesheet()
        
        # Initialize criteria
        self.criteria_changed(0)

    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(__file__), 'styles.qss')
        try:
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Style file not found, using default styling")

    def log_message(self, message):
        """Add a timestamped message to the log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_display.append(f"[{timestamp}] {message}")
        self.log_display.ensureCursorVisible()

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.directory_input.setText(folder_path)
            self.log_message(f"📁 Selected folder: {folder_path}")
            self.update_file_count()

    def update_file_count(self):
        folder_path = self.directory_input.text().strip()
        if folder_path and os.path.isdir(folder_path):
            try:
                file_count = sum([len(files) for _, _, files in os.walk(folder_path)])
                self.file_count_label.setText(f'📊 Total files found: {file_count:,}')
                self.log_message(f"📊 Scanned {file_count:,} files in directory")
            except Exception as e:
                self.file_count_label.setText('❌ Error reading directory')
                self.log_message(f"❌ Error scanning directory: {str(e)}")
        else:
            self.file_count_label.setText('📁 Select a folder to see file count')

    def criteria_changed(self, index):
        # Clear previous options
        for i in reversed(range(self.options_layout.count())):
            widget = self.options_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        criteria_text = self.criteria_combo.currentText()

        if any(time_criterion in criteria_text for time_criterion in ['Creation Time', 'Modified Time', 'Last Accessed Time']):
            # Add radio buttons for time periods
            self.time_group = QButtonGroup(self)
            time_periods = ['📅 Yearly', '📆 Monthly', '📋 Daily']
            self.time_radio_buttons = []
            
            period_label = QLabel("Time Period:")
            period_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            self.options_layout.addWidget(period_label)
            
            for period in time_periods:
                radio = QRadioButton(period, self)
                self.options_layout.addWidget(radio)
                self.time_group.addButton(radio)
                self.time_radio_buttons.append(radio)
            
            # Set 'Monthly' as default
            for radio in self.time_radio_buttons:
                if 'Monthly' in radio.text():
                    radio.setChecked(True)
                    break
                    
        elif 'File Extension' in criteria_text:
            # Add checkboxes for common file extensions
            ext_label = QLabel("Select Extensions (leave unchecked for all):")
            ext_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            self.options_layout.addWidget(ext_label)
            
            self.extension_options = []
            extensions = [
                ('📷 Images', ['png', 'jpeg', 'jpg', 'gif', 'bmp', 'svg']),
                ('🎵 Audio', ['mp3', 'wav', 'flac', 'aac']),
                ('🎬 Video', ['mp4', 'avi', 'mkv', 'mov']),
                ('📄 Documents', ['txt', 'pdf', 'docx', 'xlsx', 'pptx']),
                ('💻 Code', ['py', 'js', 'html', 'css', 'cpp', 'java'])
            ]
            
            for category, exts in extensions:
                checkbox = QCheckBox(f"{category} ({', '.join(exts)})")
                checkbox.setToolTip(f"Include {category.lower()}: {', '.join(exts)}")
                self.options_layout.addWidget(checkbox)
                self.extension_options.append((checkbox, exts))

        elif 'File Size' in criteria_text:
            # Add checkboxes for file size ranges
            size_label = QLabel("Size Categories:")
            size_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            self.options_layout.addWidget(size_label)
            
            self.size_options = []
            size_ranges = [
                ('📦 Tiny (< 1MB)', 0, 1024*1024),
                ('📄 Small (1MB - 10MB)', 1024*1024, 10*1024*1024),
                ('📊 Medium (10MB - 100MB)', 10*1024*1024, 100*1024*1024),
                ('📁 Large (100MB - 1GB)', 100*1024*1024, 1024*1024*1024),
                ('🗄️ Huge (> 1GB)', 1024*1024*1024, float('inf'))
            ]
            
            for label, min_size, max_size in size_ranges:
                checkbox = QCheckBox(label)
                self.options_layout.addWidget(checkbox)
                self.size_options.append((checkbox, label.split(' (')[0].replace('📦 ', '').replace('📄 ', '').replace('📊 ', '').replace('📁 ', '').replace('🗄️ ', ''), min_size, max_size))

        # Add some spacing at the end
        self.options_layout.addStretch()

    def get_criteria_options(self):
        """Get the selected options based on current criteria"""
        criteria_text = self.criteria_combo.currentText()
        
        if any(time_criterion in criteria_text for time_criterion in ['Creation Time', 'Modified Time', 'Last Accessed Time']):
            # Get selected time period
            for radio in self.time_radio_buttons:
                if radio.isChecked():
                    return radio.text().split(' ')[1]  # Remove emoji
            return 'Monthly'  # Default
            
        elif 'File Extension' in criteria_text:
            # Get selected extensions
            selected_extensions = []
            for checkbox, extensions in self.extension_options:
                if checkbox.isChecked():
                    selected_extensions.extend(extensions)
            return selected_extensions if selected_extensions else None
            
        elif 'File Size' in criteria_text:
            # Get selected size ranges
            selected_ranges = []
            for checkbox, label, min_size, max_size in self.size_options:
                if checkbox.isChecked():
                    selected_ranges.append((label, min_size, max_size))
            return selected_ranges if selected_ranges else None
            
        return None

    def organize_files(self, folder_path, criteria, options, include_subfolders, time_period=None):
        """Start the file organization process"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Preparing to organize files...")
        
        # Disable buttons during operation
        self.organize_button.setEnabled(False)
        self.flatten_button.setEnabled(False)
        
        self.worker_thread = QThread()
        self.worker = FileOrganizerWorker(folder_path, criteria, options, include_subfolders, time_period)
        self.worker.moveToThread(self.worker_thread)
        
        # Connect signals
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.organize_complete)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status_update.connect(self.status_label.setText)
        self.worker.status_update.connect(self.log_message)
        
        self.worker_thread.start()

    def organize_complete(self):
        """Handle completion of organization"""
        self.worker_thread.quit()
        self.worker_thread.wait()
        
        self.organize_button.setEnabled(True)
        self.flatten_button.setEnabled(True)
        
        QTimer.singleShot(3000, lambda: self.progress_bar.setVisible(False))
        QTimer.singleShot(3000, lambda: self.status_label.setText(""))

    def organize_from_input(self):
        """Organize files based on current settings"""
        folder_path = self.directory_input.text().strip()
        
        if not folder_path:
            QMessageBox.warning(self, 'Warning', 'Please select a folder first!')
            self.log_message("⚠️ No folder selected")
            return
            
        if not os.path.isdir(folder_path):
            QMessageBox.warning(self, 'Warning', 'The specified path is not a valid directory!')
            self.log_message(f"⚠️ Invalid directory: {folder_path}")
            return

        # Get criteria and options
        criteria_map = {
            '🕐 Creation Time': 'creation_time',
            '📝 Modified Time': 'modified_time', 
            '👁️ Last Accessed Time': 'last_accessed_time',
            '📄 File Extension': 'file_extension',
            '📏 File Size': 'file_size'
        }
        
        criteria_text = self.criteria_combo.currentText()
        criteria = criteria_map.get(criteria_text, 'creation_time')
        options = self.get_criteria_options()
        include_subfolders = not self.exclude_subfolders_checkbox.isChecked()
        
        time_period = None
        if any(time_criterion in criteria_text for time_criterion in ['Creation Time', 'Modified Time', 'Last Accessed Time']):
            time_period = options
            options = None

        self.log_message(f"🚀 Starting organization by {criteria_text}")
        self.organize_files(folder_path, criteria, options, include_subfolders, time_period)

    def flatten_directory_structure(self):
        """Flatten the directory structure"""
        folder_path = self.directory_input.text().strip()
        
        if not folder_path:
            QMessageBox.warning(self, 'Warning', 'Please select a folder first!')
            self.log_message("⚠️ No folder selected for flattening")
            return
            
        if not os.path.isdir(folder_path):
            QMessageBox.warning(self, 'Warning', 'The specified path is not a valid directory!')
            self.log_message(f"⚠️ Invalid directory: {folder_path}")
            return

        reply = QMessageBox.question(
            self, 'Confirm Flatten', 
            'This will move all files to the root directory. Continue?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            self.log_message("❌ Flatten operation cancelled")
            return

        include_subfolders = not self.exclude_subfolders_checkbox.isChecked()
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Preparing to flatten directory...")
        
        # Disable buttons during operation
        self.organize_button.setEnabled(False)
        self.flatten_button.setEnabled(False)
        
        self.worker_thread = QThread()
        self.worker = FlattenWorker(folder_path, include_subfolders)
        self.worker.moveToThread(self.worker_thread)
        
        # Connect signals
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.flatten_complete)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status_update.connect(self.status_label.setText)
        self.worker.status_update.connect(self.log_message)
        
        self.worker_thread.start()
        self.log_message(f"📤 Starting directory flattening")

    def flatten_complete(self):
        """Handle completion of flattening"""
        self.worker_thread.quit()
        self.worker_thread.wait()
        
        self.organize_button.setEnabled(True)
        self.flatten_button.setEnabled(True)
        
        QTimer.singleShot(3000, lambda: self.progress_bar.setVisible(False))
        QTimer.singleShot(3000, lambda: self.status_label.setText(""))

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files and os.path.isdir(files[0]):
            self.directory_input.setText(files[0])
            self.log_message(f"📁 Dropped folder: {files[0]}")
            self.update_file_count()

# Ensure that the application can be run independently
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())