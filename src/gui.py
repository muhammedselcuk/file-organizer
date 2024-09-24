import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox,
    QLineEdit, QComboBox, QCheckBox, QLabel, QRadioButton, QButtonGroup,
    QHBoxLayout, QScrollArea, QSizePolicy, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QDragEnterEvent, QDropEvent
from .organizer import organize_files, move_files_to_parent

class FileOrganizerWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, folder_path, criteria, options, include_subfolders, time_period=None):
        super().__init__()
        self.folder_path = folder_path
        self.criteria = criteria
        self.options = options
        self.include_subfolders = include_subfolders
        self.time_period = time_period

    def run(self):
        try:
            organize_files(
                self.folder_path,
                criteria=self.criteria,
                options=self.options,
                include_subfolders=self.include_subfolders,
                time_period=self.time_period
            )
        except Exception as e:
            print(f"Error during organization: {e}")
        self.finished.emit()

class FlattenWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, folder_path, include_subfolders):
        super().__init__()
        self.folder_path = folder_path
        self.include_subfolders = include_subfolders

    def run(self):
        try:
            move_files_to_parent(self.folder_path, self.include_subfolders)
        except Exception as e:
            print(f"Error during flattening: {e}")
        self.finished.emit()

class FileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Organizer')
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), '..', 'assets', 'images', 'logo.png')))
        self.setAcceptDrops(True)
        self.resize(600, 500)

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Instructions Label
        instructions = QLabel("Drag and drop a folder onto the window or select it manually.")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 16px;")
        main_layout.addWidget(instructions)

        # Directory Selection Layout
        dir_layout = QHBoxLayout()
        dir_layout.setSpacing(10)

        # Select Folder Button
        self.select_button = QPushButton('Select Folder', self)
        self.select_button.clicked.connect(self.select_folder)
        self.select_button.setFixedWidth(120)
        dir_layout.addWidget(self.select_button)

        # Line Edit for Manual Input
        self.directory_input = QLineEdit(self)
        self.directory_input.setPlaceholderText('Enter directory path here...')
        dir_layout.addWidget(self.directory_input)

        main_layout.addLayout(dir_layout)

        # Criteria Layout
        criteria_layout = QHBoxLayout()
        criteria_layout.setSpacing(10)

        criteria_label = QLabel('Organize By:')
        criteria_label.setFixedWidth(80)
        criteria_layout.addWidget(criteria_label)

        self.criteria_combo = QComboBox(self)
        self.criteria_combo.addItems([
            'Select Criterion',
            'Creation Time',
            'Modified Time',
            'Last Accessed Time',
            'File Extension',
            'File Size'
        ])
        self.criteria_combo.currentIndexChanged.connect(self.criteria_changed)
        criteria_layout.addWidget(self.criteria_combo)

        main_layout.addLayout(criteria_layout)

        # Options Area
        self.options_area = QScrollArea(self)
        self.options_area.setWidgetResizable(True)
        self.options_content = QWidget()
        self.options_layout = QVBoxLayout(self.options_content)
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        self.options_layout.setSpacing(5)
        self.options_area.setWidget(self.options_content)
        self.options_area.setFixedHeight(100)
        main_layout.addWidget(self.options_area)

        # Exclude Subfolders Checkbox
        self.exclude_subfolders_checkbox = QCheckBox('Exclude Subfolders', self)
        self.exclude_subfolders_checkbox.setToolTip("Check this to exclude files in subdirectories.")
        main_layout.addWidget(self.exclude_subfolders_checkbox)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Organize Button
        self.organize_button = QPushButton('Organize', self)
        self.organize_button.clicked.connect(self.organize_from_input)
        self.organize_button.setFixedWidth(100)
        buttons_layout.addWidget(self.organize_button)

        # Flatten Button
        self.flatten_button = QPushButton('Flatten Directory', self)
        self.flatten_button.clicked.connect(self.flatten_directory_structure)
        self.flatten_button.setFixedWidth(150)
        buttons_layout.addWidget(self.flatten_button)

        # Spacer to push buttons to the left
        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)

        # File Count Label
        self.file_count_label = QLabel('', self)
        self.file_count_label.setAlignment(Qt.AlignCenter)
        self.file_count_label.setStyleSheet("font-size: 14px; color: gray;")
        main_layout.addWidget(self.file_count_label)

        # Set Size Policy for responsiveness
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Load styles
        self.load_stylesheet()

    def load_stylesheet(self):
        style_path = os.path.join(os.path.dirname(__file__), 'styles.qss')
        with open(style_path, "r") as f:
            self.setStyleSheet(f.read())

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.directory_input.setText(folder_path)
            self.update_file_count()

    def criteria_changed(self, index):
        # Clear previous options
        for i in reversed(range(self.options_layout.count())):
            widget = self.options_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        criteria_text = self.criteria_combo.currentText()

        if criteria_text in ['Creation Time', 'Modified Time', 'Last Accessed Time']:
            # Add radio buttons for time periods
            self.time_group = QButtonGroup(self)
            time_periods = ['Yearly', 'Monthly', 'Daily']
            self.time_radio_buttons = []
            for period in time_periods:
                radio = QRadioButton(period, self)
                self.options_layout.addWidget(radio)
                self.time_group.addButton(radio)
                self.time_radio_buttons.append(radio)
            # Set 'Monthly' as default selected
            for radio in self.time_radio_buttons:
                if radio.text() == 'Monthly':
                    radio.setChecked(True)
                    break
        elif criteria_text == 'File Extension':
            # Add checkboxes for common file extensions
            self.extension_options = []
            extensions = ['png', 'jpeg', 'jpg', 'mp4', 'txt', 'pdf', 'docx', 'xlsx', 'pptx']
            for ext in extensions:
                checkbox = QCheckBox(f".{ext}", self)
                self.options_layout.addWidget(checkbox)
                self.extension_options.append(checkbox)
        elif criteria_text == 'File Size':
            # Add checkboxes for size ranges
            self.size_options = []
            size_ranges = [
                ('0 - 5 MB', 0, 5 * 1024 * 1024),
                ('5 - 50 MB', 5 * 1024 * 1024, 50 * 1024 * 1024),
                ('50 - 100 MB', 50 * 1024 * 1024, 100 * 1024 * 1024),
                ('100 - 500 MB', 100 * 1024 * 1024, 500 * 1024 * 1024),
                ('500 MB - 1 GB', 500 * 1024 * 1024, 1024 * 1024 * 1024),
                ('1 GB+', 1024 * 1024 * 1024, float('inf')),
            ]
            self.size_ranges = size_ranges
            for label, _, _ in size_ranges:
                checkbox = QCheckBox(label, self)
                self.options_layout.addWidget(checkbox)
                self.size_options.append(checkbox)
        else:
            # No additional options
            pass

    def organize_files(self, folder_path, criteria, options, include_subfolders, time_period=None):
        self.thread = QThread()
        self.worker = FileOrganizerWorker(
            folder_path, criteria, options, include_subfolders, time_period
        )
        self.worker.moveToThread(self.thread)

        # Connect signals
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.organize_complete)

        # Start the process
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def organize_complete(self):
        QMessageBox.information(self, 'Success', 'Files have been organized.')
        self.update_file_count()

    def organize_from_input(self):
        folder_path = self.directory_input.text()
        criteria_text = self.criteria_combo.currentText()

        if criteria_text == 'Select Criterion':
            QMessageBox.warning(self, 'No Criterion Selected', 'Please select an organizing criterion.')
            return

        criteria_mapping = {
            'Creation Time': 'creation_time',
            'Modified Time': 'modified_time',
            'Last Accessed Time': 'last_accessed_time',
            'File Extension': 'file_extension',
            'File Size': 'file_size'
        }
        criteria = criteria_mapping.get(criteria_text, None)
        include_subfolders = not self.exclude_subfolders_checkbox.isChecked()
        options = None
        time_period = None

        if criteria in ['creation_time', 'modified_time', 'last_accessed_time']:
            selected_period = None
            for radio in self.time_radio_buttons:
                if radio.isChecked():
                    selected_period = radio.text()
                    break
            time_period = selected_period if selected_period else 'Monthly'
        elif criteria == 'file_extension':
            selected_extensions = [cb.text().strip('.') for cb in self.extension_options if cb.isChecked()]
            options = selected_extensions if selected_extensions else None
        elif criteria == 'file_size':
            selected_ranges = []
            for idx, cb in enumerate(self.size_options):
                if cb.isChecked():
                    selected_ranges.append(self.size_ranges[idx])
            options = selected_ranges if selected_ranges else None

        if os.path.isdir(folder_path):
            self.organize_files(folder_path, criteria, options, include_subfolders, time_period)
        else:
            QMessageBox.warning(self, 'Invalid Directory', 'Please enter a valid directory path.')

    def flatten_directory_structure(self):
        folder_path = self.directory_input.text()
        include_subfolders = not self.exclude_subfolders_checkbox.isChecked()

        if os.path.isdir(folder_path):
            self.thread = QThread()
            self.worker = FlattenWorker(folder_path, include_subfolders)
            self.worker.moveToThread(self.thread)

            # Connect signals
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.finished.connect(self.flatten_complete)

            # Start the process
            self.thread.started.connect(self.worker.run)
            self.thread.start()
        else:
            QMessageBox.warning(self, 'Invalid Directory', 'Please enter a valid directory path.')

    def flatten_complete(self):
        QMessageBox.information(self, 'Success', 'Directory has been flattened.')
        self.update_file_count()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            local_path = urls[0].toLocalFile()
            if os.path.isdir(local_path):
                self.directory_input.setText(local_path)
                self.update_file_count()
            else:
                QMessageBox.warning(self, 'Invalid Directory', 'Please drop a valid directory.')
        event.acceptProposedAction()

    def update_file_count(self):
        folder_path = self.directory_input.text()
        include_subfolders = not self.exclude_subfolders_checkbox.isChecked()
        if os.path.isdir(folder_path):
            if include_subfolders:
                total_files = sum(len(files) for _, _, files in os.walk(folder_path))
            else:
                total_files = len([
                    name for name in os.listdir(folder_path)
                    if os.path.isfile(os.path.join(folder_path, name))
                ])
            self.file_count_label.setText(f"Total Files: {total_files}")
        else:
            self.file_count_label.setText("")

# Ensure that the application can be run independently
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec_())
