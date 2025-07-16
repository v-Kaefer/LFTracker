#!/usr/bin/env python3
import sys
sys.path.insert(0, "/usr/share/lftracker")

from ui import MainWindow
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
