from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
import os

class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.dir = None
        self.modified = 'modified/'
    def loadImage(self, filename, dir):
        self.filename = filename
        self.dir = dir
        image = os.path.join(self.dir, self.filename)
        self.image = Image.open(image)
    def showImage(self, path):
        picture.hide()
        pixmapimage = QPixmap(path)
        w, h = picture.width(), picture.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        path = os.path.join(self.dir, self.modified, self.filename)
        self.showImage(path)
    def saveImage(self):
        path = os.path.join(self.dir, self.modified)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.modified, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.modified, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.modified, self.filename)
        self.showImage(image_path)
    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.modified, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if lv_files.currentRow() >= 0:
        filename = lv_files.currentItem().text()
        workimage.loadImage(filename, workdir)
        path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(path)
workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(filename, extension):
    files = list()
    for file in filename:
        for ext in extension:
            if file.endswith(ext):
                files.append(file)
    return files

extension = ['.jpg', '.jpeg', '.png', '.gif']
def showFilenamesList():
    chooseWorkdir()
    global extension
    files = filter(os.listdir(workdir), extension)
    lv_files.clear()
    lv_files.addItems(files)

app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle('Easy Editor')
main_window.resize(650, 450)
btn_dir = QPushButton('Папка')
lv_files = QListWidget()
picture = QLabel('Картинка')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Отзеркалить')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

centralVline = QVBoxLayout()
centralVline.addWidget(picture)
leftVline = QVBoxLayout()
leftVline.addWidget(btn_dir)
leftVline.addWidget(lv_files)
centralHline = QHBoxLayout()
botHline = QHBoxLayout()
botHline.addWidget(btn_left)
botHline.addWidget(btn_right)
botHline.addWidget(btn_mirror)
botHline.addWidget(btn_sharp)
botHline.addWidget(btn_bw)

centralVline.addLayout(botHline)
centralHline.addLayout(leftVline)
centralHline.addLayout(centralVline)
main_window.setLayout(centralHline)

btn_dir.clicked.connect(showFilenamesList)
lv_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_mirror.clicked.connect(workimage.do_flip)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharp)
main_window.show()
app.exec()