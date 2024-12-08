from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QPushButton, QWidget, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt
from utils.tabs_management.tab_content import (create_tab_content)

class TabmanagerScreen(QMainWindow):
    def __init__(self, file_path="screens.yaml"):
        super().__init__()
        self.file_path = file_path
        self.setWindowTitle("Dynamic Tabs with Categories")
        self.setGeometry(100, 100, 800, 600)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Button to add new tabs
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.tab_widget.setCornerWidget(self.add_tab_button, Qt.TopRightCorner)

        self.setCentralWidget(self.tab_widget)

        # Add an initial tab
        self.add_new_tab()

    def add_new_tab(self):
        tab_count = self.tab_widget.count() + 1
        new_tab = QWidget()
        new_tab.setLayout(QGridLayout())
        new_tab.layout().addWidget(create_tab_content(new_tab, self.file_path))
        self.tab_widget.addTab(new_tab, f"Tab {tab_count}")
        self.tab_widget.setCurrentWidget(new_tab)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)
        # If no tabs remain, add a new one
        if self.tab_widget.count() == 0:
            self.add_new_tab()

if __name__ == "__main__":
    app = QApplication([])
    window = TabmanagerScreen()
    window.show()
    app.exec()
