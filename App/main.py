from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from keras.applications.vgg16 import preprocess_input
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np
from matplotlib import pyplot as plt
from FlagImage import OuputModel
from FlagImage import SeeImage
from PyQt5.QtCore import QTimer


class UI(QMainWindow):
    classification_model = None
    image_path = ""
    directory_path = ""
    dir_img_files = []
    dir_img_index=0
    ui_path = os.path.dirname(os.path.abspath(__file__))

    # defite the constructor

    def __init__(self):
        super(UI, self).__init__()
        mainLayout = QVBoxLayout()
        full_path = os.path.join(self.ui_path, "PresentationUI.ui")
        uic.loadUi(f"{full_path}", self)

        self.timer = QTimer(self)
        self.display_duration=1400

        self.txt_image_path=self.findChild(QLineEdit,"txt_image_path")
        self.img_label=self.findChild(QLabel,"img_label")
        self.lbl_flag=self.findChild(QLabel,"lbl_flag")
        self.lbl_confidence=self.findChild(QLabel,"lbl_confidence")
        self.lbl_icon=self.findChild(QLabel,"lbl_icon")

        self.btn_image_browse=self.findChild(QPushButton, "btn_image_browse")       
        self.btn_dir_browse=self.findChild(QPushButton, "btn_dir_browse")

        self.btn_classify=self.findChild(QPushButton, "btn_classify")
        self.btn_simulate=self.findChild(QPushButton, "btn_simulate")

        #event handlers
        self.btn_image_browse.clicked.connect(self.btn_image_browse_clicked)
        self.btn_dir_browse.clicked.connect(self.btn_dir_browse_clicked)
        self.btn_classify.clicked.connect(self.btn_classify_click)
        self.btn_simulate.clicked.connect(self.btn_simulate_click)

        #constructing the object
        self.load_classification_model()
        self.setLayout(mainLayout)
        self.lbl_icon.hide()
        self.show()

    def load_classification_model(self):
        curr_path = os.path.dirname(os.path.abspath(__file__))
        model_path=os.path.join(curr_path, '../source/classifier_model.h5')
        self.classification_model = load_model(model_path)


    def btn_classify_click(self):
        if(self.image_path!=""):
            output = SeeImage(self.image_path, self.classification_model)
            self.lbl_flag.setText(output.classification_label)
            str_confidence='I am '+str(int(output.Confidence))+'% Confident.        -_-'
            self.lbl_confidence.setText(str_confidence)
            self.flag_ui(output.Flag)


    def btn_image_browse_clicked(self):
        filename=QFileDialog.getOpenFileName()
        path=filename[0]
        self.image_path=path
        self.txt_image_path.setText(path)
        self.Display_Image(path)
        print(path)
    

    def btn_simulate_click(self):
        self.process_directory_images(self.directory_path)


    def btn_dir_browse_clicked(self):
        dir_path = QFileDialog.getExistingDirectory()

        print(dir_path)
        if dir_path:
            self.directory_path = dir_path
            self.txt_image_path.setText(dir_path)
            print(dir_path)
        else:
            print("Selection canceled.")




    #custom methods

    def flag_ui(self,flag):
        warning_stylesheet="font-size:30px;color:red;text-align:center;font-style:bold;"
        normal_stylesheet="font-size:30px;color:#aaff7f;text-align:center;font-style:bold;"

        pixmap=None
        curr_path = os.path.dirname(os.path.abspath(__file__))

        if (flag):
            self.lbl_flag.setStyleSheet(normal_stylesheet)
            full_path=os.path.join(curr_path, 'icons/success.png')
            pixmap = QPixmap(full_path)
        else:
            self.lbl_flag.setStyleSheet(warning_stylesheet)
            full_path=os.path.join(curr_path, 'icons/wrong.png')
            pixmap = QPixmap(full_path)

        self.lbl_icon.setPixmap(pixmap.scaled(200,180))
        self.lbl_icon.show()


    def Display_Image(self, full_path):
        pixmap = QPixmap(full_path)
        self.img_label.setPixmap(pixmap.scaled(480,580))

    def process_next_image(self):
        if(self.dir_img_index < len(self.dir_img_files)):
            file_path=self.dir_img_files[self.dir_img_index]
            self.Display_Image(file_path)
            self.image_path = file_path
            self.btn_classify_click()
            self.repaint()
            self.dir_img_index+=1

        self.timer.start(self.display_duration)

    def process_directory_images(self,directory_path):
        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                self.dir_img_files.append(file_path)
        
        self.timer.timeout.connect(self.process_next_image)
        self.timer.start(self.display_duration)






##Runnig the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()


