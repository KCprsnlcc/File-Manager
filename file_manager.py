import sys
import os
import shutil
from PySide6.QtCore import Qt, QDir, QFileInfo, QUrl, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMenu, QFileDialog, QLabel, QHBoxLayout, QToolBar, QStatusBar, QHeaderView, QSplitter, QFileIconProvider
from PySide6.QtGui import QIcon, QPixmap, QAction


class FileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Manager")
        self.setGeometry(100, 100, 1000, 700)
        self.current_path = os.path.expanduser("~")  # Start in home directory
        self.initUI()
        self.setup_statusbar()
        self.setup_toolbar()
        self.update_status()

    def initUI(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Path bar
        path_layout = QHBoxLayout()
        self.path_display = QLineEdit(self.current_path)
        self.path_display.setReadOnly(True)
        path_layout.addWidget(self.path_display)
        main_layout.addLayout(path_layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter search terms...")
        self.search_bar.textChanged.connect(self.searchFiles)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_bar)
        main_layout.addLayout(search_layout)
        
        # Create splitter for file explorer and preview
        splitter = QSplitter(Qt.Horizontal)
        
        # File System Model
        self.model = QFileSystemModel()
        self.model.setRootPath(self.current_path)
        
        # File Explorer (Tree View)
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(self.current_path))
        self.tree_view.setAnimated(True)
        self.tree_view.setIndentation(20)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.showContextMenu)
        
        # Set up headers and make columns resize properly
        header = self.tree_view.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # Connect selection change to preview update
        self.tree_view.clicked.connect(self.on_item_clicked)
        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)

        # Preview panel
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        
        preview_header = QLabel("Preview")
        preview_header.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(preview_header)
        
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(300, 300)
        self.preview_label.setStyleSheet("border: 1px solid #cccccc; background-color: #f9f9f9;")
        self.preview_label.setText("Select a file to preview")
        preview_layout.addWidget(self.preview_label)
        
        # Add widgets to splitter
        splitter.addWidget(self.tree_view)
        splitter.addWidget(preview_widget)
        splitter.setSizes([600, 400])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set central widget
        self.setCentralWidget(main_widget)
        
        # Enable drag and drop
        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDropIndicatorShown(True)
        self.setAcceptDrops(True)

    def setup_toolbar(self):
        toolbar = QToolBar("Navigation")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        # Back action
        back_action = QAction(QIcon.fromTheme("go-previous", QIcon("icons/back.png")), "Back", self)
        back_action.setStatusTip("Go back to previous directory")
        back_action.triggered.connect(self.go_back)
        toolbar.addAction(back_action)
        
        # Up action
        up_action = QAction(QIcon.fromTheme("go-up", QIcon("icons/up.png")), "Up", self)
        up_action.setStatusTip("Go up one directory")
        up_action.triggered.connect(self.go_up)
        toolbar.addAction(up_action)
        
        # Home action
        home_action = QAction(QIcon.fromTheme("go-home", QIcon("icons/home.png")), "Home", self)
        home_action.setStatusTip("Go to home directory")
        home_action.triggered.connect(self.go_home)
        toolbar.addAction(home_action)
        
        # Refresh action
        refresh_action = QAction(QIcon.fromTheme("view-refresh", QIcon("icons/refresh.png")), "Refresh", self)
        refresh_action.setStatusTip("Refresh current directory")
        refresh_action.triggered.connect(self.refresh)
        toolbar.addAction(refresh_action)

    def setup_statusbar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.item_count_label = QLabel()
        self.status_bar.addPermanentWidget(self.item_count_label)
        
    def update_status(self):
        index = self.model.index(self.current_path)
        file_count = self.model.rowCount(index)
        self.item_count_label.setText(f"{file_count} items")
        self.path_display.setText(self.current_path)

    def go_back(self):
        # This is a simple implementation - a real one would need history
        parent_dir = os.path.dirname(self.current_path)
        if os.path.exists(parent_dir):
            self.navigate_to(parent_dir)
    
    def go_up(self):
        parent_dir = os.path.dirname(self.current_path)
        if os.path.exists(parent_dir):
            self.navigate_to(parent_dir)
    
    def go_home(self):
        home_dir = os.path.expanduser("~")
        self.navigate_to(home_dir)
    
    def refresh(self):
        self.model.setRootPath(self.current_path)
        self.tree_view.setRootIndex(self.model.index(self.current_path))
        self.update_status()
        
    def navigate_to(self, path):
        if os.path.exists(path):
            self.current_path = path
            self.tree_view.setRootIndex(self.model.index(path))
            self.update_status()

    def on_item_clicked(self, index):
        file_path = self.model.filePath(index)
        self.showPreview(file_path)
        
    def on_item_double_clicked(self, index):
        file_path = self.model.filePath(index)
        if os.path.isdir(file_path):
            self.navigate_to(file_path)
        else:
            # Try to open the file with default application
            url = QUrl.fromLocalFile(file_path)
            QDesktopServices.openUrl(url) if 'QDesktopServices' in dir() else None

    def searchFiles(self):
        query = self.search_bar.text()
        if query:
            self.model.setNameFilters([f"*{query}*"])
            self.model.setNameFilterDisables(False)
        else:
            self.model.setNameFilters([])
            self.model.setNameFilterDisables(True)
        self.update_status()

    def showContextMenu(self, position):
        index = self.tree_view.indexAt(position)
        if not index.isValid():
            return
            
        file_path = self.model.filePath(index)
        
        context_menu = QMenu(self)
        
        # Open action
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.openFile(file_path))
        context_menu.addAction(open_action)
        
        context_menu.addSeparator()
        
        # Copy action
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(lambda: self.copyFile(file_path))
        context_menu.addAction(copy_action)
        
        # Move action
        move_action = QAction("Move", self)
        move_action.triggered.connect(lambda: self.moveFile(file_path))
        context_menu.addAction(move_action)
        
        # Rename action
        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(lambda: self.renameFile(file_path))
        context_menu.addAction(rename_action)
        
        context_menu.addSeparator()
        
        # Delete action
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.deleteFile(file_path))
        context_menu.addAction(delete_action)
        
        context_menu.exec(self.tree_view.viewport().mapToGlobal(position))

    def openFile(self, file_path):
        if os.path.isdir(file_path):
            self.navigate_to(file_path)
        else:
            # Try to open the file with default application
            url = QUrl.fromLocalFile(file_path)
            from PySide6.QtGui import QDesktopServices
            QDesktopServices.openUrl(url)

    def deleteFile(self, file_path):
        confirm = QFileDialog.question(self, "Delete", f"Are you sure you want to delete {os.path.basename(file_path)}?", QFileDialog.Yes | QFileDialog.No)
        if confirm == QFileDialog.Yes:
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                self.refresh()
            except Exception as e:
                QFileDialog.critical(self, "Error", f"Failed to delete file: {str(e)}")

    def copyFile(self, source_path):
        destination = QFileDialog.getExistingDirectory(self, "Select Destination")
        if destination:
            try:
                dest_path = os.path.join(destination, os.path.basename(source_path))
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, dest_path)
                else:
                    shutil.copy2(source_path, dest_path)
            except Exception as e:
                QFileDialog.critical(self, "Error", f"Failed to copy file: {str(e)}")

    def moveFile(self, source_path):
        destination = QFileDialog.getExistingDirectory(self, "Select Destination")
        if destination:
            try:
                dest_path = os.path.join(destination, os.path.basename(source_path))
                shutil.move(source_path, dest_path)
                self.refresh()
            except Exception as e:
                QFileDialog.critical(self, "Error", f"Failed to move file: {str(e)}")
                
    def renameFile(self, file_path):
        from PySide6.QtWidgets import QInputDialog
        filename = os.path.basename(file_path)
        new_name, ok = QInputDialog.getText(self, "Rename", "New name:", text=filename)
        if ok and new_name:
            try:
                new_path = os.path.join(os.path.dirname(file_path), new_name)
                os.rename(file_path, new_path)
                self.refresh()
            except Exception as e:
                QFileDialog.critical(self, "Error", f"Failed to rename file: {str(e)}")

    def showPreview(self, file_path):
        if not os.path.exists(file_path):
            self.preview_label.setText("File not found")
            return
            
        if os.path.isdir(file_path):
            self.preview_label.setText(f"Directory: {os.path.basename(file_path)}\n{len(os.listdir(file_path))} items")
            return
            
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        file_info = f"File: {file_name}\nSize: {self.format_size(file_size)}"
        
        # Handle image preview
        if file_path.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.preview_label.setPixmap(pixmap)
                self.preview_label.setToolTip(file_info)
                return
        
        # Handle text preview for small files
        if file_path.lower().endswith(('txt', 'py', 'html', 'css', 'js', 'json', 'xml', 'md')) and file_size < 1024 * 10:  # Less than 10KB
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)  # Read first 1000 chars
                self.preview_label.setText(f"{file_info}\n\n{content}")
                return
            except:
                pass
        
        # Default preview
        icon_provider = QFileIconProvider()
        file_info_obj = QFileInfo(file_path)
        icon = icon_provider.icon(file_info_obj)
        self.preview_label.setText(file_info)

    def format_size(self, size):
        # Format file size into human-readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            source_file = url.toLocalFile()
            if os.path.exists(source_file):
                destination_path = os.path.join(self.current_path, os.path.basename(source_file))
                try:
                    if os.path.isdir(source_file):
                        shutil.copytree(source_file, destination_path)
                    else:
                        shutil.copy2(source_file, destination_path)
                except Exception as e:
                    self.status_bar.showMessage(f"Error: {str(e)}", 5000)
        self.refresh()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    window = FileManager()
    window.show()
    sys.exit(app.exec())