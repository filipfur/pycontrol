import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2.QtCore import QSettings, QFile
from PySide2.QtUiTools import QUiLoader

class MainWindow(QMainWindow):
    def __init__(self, ui_file, settings_file):
        super(MainWindow, self).__init__()
        self.load_ui(ui_file)
        self.load_settings(settings_file)
        self.window.pushButton.clicked.connect(self.open_file_dialog)
        self.window.confirmButton.clicked.connect(self.confirm)

        #check if integerSlider1 is changed
        self.window.integerSlider1.valueChanged.connect(lambda x: self.slider_changed(x, self.window.integerValue1))
        self.window.integerSlider2.valueChanged.connect(lambda x: self.slider_changed(x, self.window.integerValue2))

    def slider_changed(self, value, label):
        #check which slider
        label.setText(str(value))

    def load_ui(self, ui_file):
        loader = QUiLoader()
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

        self.setCentralWidget(self.window)

    def load_settings(self, settings_file):
        self.settings = QSettings(settings_file, QSettings.IniFormat)
        self.restoreGeometry(self.settings.value("MainWindow/geometry"))
        self.restoreState(self.settings.value("MainWindow/windowState"))
        #load file input and integer values and integer sliders from settings
        self.window.fileInput.setText(self.settings.value("MainWindow/fileInput"))
        self.window.integerValue1.setText(self.settings.value("MainWindow/integerValue1", "0"))
        self.window.integerValue2.setText(self.settings.value("MainWindow/integerValue2", "0"))
        self.window.integerSlider1.setValue(int(self.settings.value("MainWindow/integerValue1", "0")))
        self.window.integerSlider2.setValue(int(self.settings.value("MainWindow/integerValue2", "0")))

    def closeEvent(self, event):
        self.settings.setValue("MainWindow/geometry", self.saveGeometry())
        self.settings.setValue("MainWindow/windowState", self.saveState())
        # store file input and integer values in settings
        self.settings.setValue("MainWindow/fileInput", self.window.fileInput.text())
        self.settings.setValue("MainWindow/integerValue1", self.window.integerValue1.text())
        self.settings.setValue("MainWindow/integerValue2", self.window.integerValue2.text())


    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if file_name:
            # Perform an action with the selected file, e.g. open it, read its content, etc.
            self.window.fileInput.setText(file_name)
            print(f"Selected file: {file_name}")

    def confirm(self):
        print("Confirm button clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_file = "example.ui"
    settings_file = "settings.ini"
    mainWin = MainWindow(ui_file, settings_file)
    mainWin.show()
    mainWin.setWindowTitle("Test")
    sys.exit(app.exec_())