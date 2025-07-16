import subprocess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QFrame, QScrollArea, QMainWindow, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import Qt

# Map example: packages -> sectors
SECTOR_MAP = {
    "vlc": "Media",
    "ffmpeg": "Media",
    "libx264": "Media",
    "curl": "Network",
    "wget": "Network",
    "openssl": "Network",
    "pacman": "System",
    "bash": "System",
    "python": "Development",
    "gcc": "Development",
    "make": "Development",
    # Default: "Others"
}


def get_installed_packages():
    result = subprocess.run(['pacman', '-Qq'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().splitlines()


def get_reverse_dependencies(package_name):
    result = subprocess.run(['pactree', '-r', package_name], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().splitlines()
    dependents = [line.strip() for line in lines if line.strip() != package_name]
    return dependents


def classify_package(package):
    return SECTOR_MAP.get(package, "Others")


class DependencyWidget(QFrame):
    def __init__(self, package_name, dependents):
        super().__init__()

        self.package_name = package_name
        self.dependents = dependents

        self.layout = QVBoxLayout(self)

        self.title_label = QLabel(f"📦 {self.package_name}")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.title_label)

        self.toggle_button = QPushButton("Show Dependencies ▼")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_dependencies)
        self.layout.addWidget(self.toggle_button)

        self.dependent_list = QListWidget()
        self.dependent_list.addItems(self.dependents)
        self.dependent_list.setVisible(False)
        self.layout.addWidget(self.dependent_list)

        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setStyleSheet("margin: 5px; padding: 5px;")

    def toggle_dependencies(self):
        visible = self.dependent_list.isVisible()
        self.dependent_list.setVisible(not visible)
        self.toggle_button.setText("Hide Dependencies ▲" if not visible else "Show Dependencies ▼")


class SectorGroup(QFrame):
    def __init__(self, sector_name, package_widgets):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.header = QLabel(f"🗂 {sector_name}")
        self.header.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(self.header)

        for widget in package_widgets:
            self.layout.addWidget(widget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LFTracker - Lightweight Package Tracker")
        self.resize(800, 600)

        self.all_packages = {}  # sector -> [widgets]
        self.total_count = 0

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # HEADER
        self.header_layout = QHBoxLayout()
        self.package_count_label = QLabel("📦 Packages Found: 0")
        self.sector_selector = QComboBox()
        self.sector_selector.addItems(["All", "Media", "Network", "System", "Development", "Others"])
        self.sector_selector.currentTextChanged.connect(self.update_display)

        self.header_layout.addWidget(self.package_count_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(QLabel("Filter:"))
        self.header_layout.addWidget(self.sector_selector)
        self.main_layout.addLayout(self.header_layout)

        # SCROLL AREA
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        self.setCentralWidget(self.main_widget)

        self.build_package_list(include_all=True)  # Show all
        self.update_display()

    def build_package_list(self, include_all=False):
        installed = get_installed_packages()
        sector_data = {}

        for pkg in installed:
            deps = get_reverse_dependencies(pkg)
            if not deps and not include_all:
                continue  # ignore packages without dependencies
            sector = classify_package(pkg)
            sector_data.setdefault(sector, []).append((pkg, deps))

        self.all_packages = sector_data
        self.total_count = sum(len(widgets) for widgets in sector_data.values())
        self.package_count_label.setText(f"📦 Packages Found: {self.total_count}")


    def update_display(self):
        selected_sector = self.sector_selector.currentText()
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for sector, data_list in self.all_packages.items():
            if selected_sector == "All" or selected_sector == sector:
                widgets = [DependencyWidget(pkg, deps) for pkg, deps in data_list]
                group = SectorGroup(sector, widgets)
                self.scroll_layout.addWidget(group)
