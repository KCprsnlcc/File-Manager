import sys
import shutil
from PySide6.QtCore import Qt, QDir, QFileInfo, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMenu, QAction, QFileDialog, QLabel, QHBoxLayout
from PySide6.QtGui import QIcon, QPixmap


class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create the search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search files...")
        self.search_bar.textChanged.connect(self.searchFiles)  # Connect search to filtering
        layout.addWidget(self.search_bar)

        # File System Model
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        # File Explorer (Tree View)
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.showContextMenu)

        # File Preview Area
        self.preview_label = QLabel(self)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFixedSize(400, 300)

        # Layouts
        file_explorer_layout = QVBoxLayout()
        file_explorer_layout.addWidget(self.tree_view)
        file_explorer_layout.addWidget(self.preview_label)

        # Adding File Explorer and Preview to Main Layout
        layout.addLayout(file_explorer_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def searchFiles(self):
        query = self.search_bar.text()
        if query:
            self.model.setNameFilters([f"*{query}*"])
        else:
            self.model.setNameFilters([])

    def showContextMenu(self, position):
        context_menu = QMenu(self)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.deleteFile)
        context_menu.addAction(delete_action)

        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copyFile)
        context_menu.addAction(copy_action)

        move_action = QAction("Move", self)
        move_action.triggered.connect(self.moveFile)
        context_menu.addAction(move_action)

        context_menu.exec(self.tree_view.viewport().mapToGlobal(position))

    def deleteFile(self):
        index = self.tree_view.selectedIndexes()[0]
        file_path = self.model.filePath(index)
        confirm = QFileDialog.question(self, "Delete", f"Are you sure you want to delete {file_path}?", QFileDialog.Yes | QFileDialog.No)
        if confirm == QFileDialog.Yes:
            QFileInfo(file_path).dir().remove(file_path)

    def copyFile(self):
        index = self.tree_view.selectedIndexes()[0]
        source_path = self.model.filePath(index)
        destination = QFileDialog.getExistingDirectory(self, "Select Destination")
        if destination:
            shutil.copy(source_path, destination)

    def moveFile(self):
        index = self.tree_view.selectedIndexes()[0]
        source_path = self.model.filePath(index)
        destination = QFileDialog.getExistingDirectory(self, "Select Destination")
        if destination:
            shutil.move(source_path, destination)

    def showPreview(self, file_path):
        if file_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            pixmap = QPixmap(file_path)
            self.preview_label.setPixmap(pixmap)
        elif file_path.lower().endswith('pdf'):
            # For PDF, use QPdfDocument or a third-party library to render a preview
            self.preview_label.setText("PDF preview not implemented yet.")
        else:
            self.preview_label.setText(f"Preview not available for {file_path}")


        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
            file_url = event.mimeData().urls()[0]
            source_file = file_url.toLocalFile()
            destination_dir = self.model.filePath(self.tree_view.selectedIndexes()[0])
            destination_path = QDir(destination_dir).filePath(QFileInfo(source_file).fileName())
            shutil.move(source_file, destination_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileManager()
    window.show()
    sys.exit(app.exec())