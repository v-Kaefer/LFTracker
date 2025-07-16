# cleanup/ui.py
import subprocess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QFrame, QScrollArea, QMainWindow, QHBoxLayout
)
from PyQt5.QtCore import Qt


def get_installed_packages():
    result = subprocess.run(['pacman', '-Qq'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().splitlines()


def get_reverse_dependencies(package_name):
    result = subprocess.run(['pactree', '-r', package_name], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().splitlines()

    # Remove a linha inicial se for o próprio pacote
    dependents = [line.strip() for line in lines if line.strip() != package_name]
    return dependents


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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("lftracker - Lightweight Package Tracker")
        self.resize(700, 500)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Área com rolagem
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        packages = get_installed_packages()
        for pkg in packages:
            deps = get_reverse_dependencies(pkg)
            if deps:  # só mostra pacotes com dependentes
                scroll_layout.addWidget(DependencyWidget(pkg, deps))

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        main_layout.addWidget(scroll_area)
        self.setCentralWidget(main_widget)
