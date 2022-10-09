# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mustafa/Desktop/FaceRecognition/Qt_Face_Recognition/customWidgets/IdCardOutput/ocroutputwidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(370, 798)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(7, -1, 13, -1)
        self.formLayout.setHorizontalSpacing(15)
        self.formLayout.setVerticalSpacing(25)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_tcno = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_tcno.setObjectName("lineEdit_tcno")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_tcno)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit_name = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_name)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_surname = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_surname.setObjectName("lineEdit_surname")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_surname)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_date_of_birth = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_date_of_birth.setObjectName("lineEdit_date_of_birth")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_date_of_birth)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_rotation_angle = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_rotation_angle.setObjectName("lineEdit_rotation_angle")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_rotation_angle)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_face = QtWidgets.QLabel(self.groupBox_2)
        self.label_face.setObjectName("label_face")
        self.gridLayout.addWidget(self.label_face, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Tc Identity Card Infos"))
        self.label_3.setText(_translate("Form", "Tr Identity No"))
        self.label.setText(_translate("Form", "Name"))
        self.label_2.setText(_translate("Form", "Surname"))
        self.label_4.setText(_translate("Form", "Date of Birth"))
        self.label_5.setText(_translate("Form", "Rotation angle of Id card"))
        self.groupBox_2.setTitle(_translate("Form", "Face Image"))
        self.label_face.setText(_translate("Form", "Face"))
        self.pushButton.setText(_translate("Form", "Save"))
