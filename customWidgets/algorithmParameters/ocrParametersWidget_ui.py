# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mustafa/Desktop/FaceRecognition/Qt_Face_Recognition/customWidgets/algorithmParameters/ocrParametersWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(463, 681)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.comboBox_face_detection_model = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_face_detection_model.setObjectName("comboBox_face_detection_model")
        self.gridLayout.addWidget(self.comboBox_face_detection_model, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.comboBox_id_card_seg_model = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_id_card_seg_model.setObjectName("comboBox_id_card_seg_model")
        self.gridLayout.addWidget(self.comboBox_id_card_seg_model, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.comboBox_ocr_model = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_ocr_model.setObjectName("comboBox_ocr_model")
        self.gridLayout.addWidget(self.comboBox_ocr_model, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.lineEdit_rotation_interval = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_rotation_interval.setObjectName("lineEdit_rotation_interval")
        self.gridLayout.addWidget(self.lineEdit_rotation_interval, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.lineEdit_neighor_box_distance = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_neighor_box_distance.setObjectName("lineEdit_neighor_box_distance")
        self.gridLayout.addWidget(self.lineEdit_neighor_box_distance, 4, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Detection"))
        self.label_3.setText(_translate("Form", "Face Recognition Model"))
        self.label.setText(_translate("Form", "Segmentation Model"))
        self.label_2.setText(_translate("Form", "Ocr Model"))
        self.label_4.setText(_translate("Form", "Rotation Interval"))
        self.label_5.setText(_translate("Form", "Neighbor Box Distance"))
