# -*- coding: utf-8 -*-
from linkedin_api import Linkedin
import urllib
# Authenticate using any Linkedin account credentials
import pandas as pd
from time import sleep
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from Alfred_linkedin import *
import Alfred_linkedin as alf
import linkedin_people_search as lps
import Alfred_linkedin_people as alp
import csv

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):

    def on_press_start_button(self):
        try:
            user_name = self.name_email_text_edit.text()
            user_pass = self.password_text_edit.text()
            print(user_name)
            print(user_pass)
        except:
            pass
        self.table.setRowCount(0)

        
        self.login_list = []
        self.country_code = self.industry_code = self.job_code = self.job2_code = self.target = ""
        self.link_list = []

        self.get_login()
        self.get_settings()
        self.add_to_table()
        #All the Variables you need to run your scrapes
        print (self.tab)
        print (self.login_list)
        print ([self.country_code , self.industry_code , self.job_code , self.job2_code , self.target])
        print(self.link_list)


        if self.tab =="url":

            if self.target=="companies":
                print("Scrape to be done based on Url and under Companies")
            else :
                print("Scrape to be done based on Url and under People")
            print("Parameters : Job and link list")
        else:
            print("Scrape to be done based on Url and under People")
            print("Parameters : country , industry and job")

    def add_to_table(self):

        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem("text1"))
        self.table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem("text2"))
        self.table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem("text3"))


    def preset_values(self):
        print("Setting Values")
        #account types
        account_type_list = ['Sales Navigator','Normal']
        self.account_select_list.clear()
        self.account_select_list.addItems(account_type_list)

        #country list
        self.select_country_list = pd.read_json("Countries.json")
        self.country_list.clear()
        self.country_list.addItems(self.select_country_list['Country Name'].values)

        #industry list
        self.select_industry_list = pd.read_json("Industries.json")
        self.industry_list.clear()
        self.industry_list.addItems(self.select_industry_list['Industry Name'].values)

        #job list
        self.select_job_list = pd.read_json("Jobtitles.json")
        self.job_position_list.clear()
        self.job_position_list.addItems(self.select_job_list['GUI'].values)

        self.job_position_list_2.clear()
        self.job_position_list_2.addItems(self.select_job_list['GUI'].values)

    def get_login(self):
        print("logging in")
        user_name = self.name_email_text_edit.text()
        user_pass = self.password_text_edit.text()
        account_type = self.account_select_list.currentText()
        if account_type == "Normal":
            limit=100
        else:
            limit=1000

        if (user_name == "" or user_pass=="" ):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Login Error !"
                        "\n User name or Password cannot be empty")
            msg.setWindowTitle("Login Error !")
            msg.setStandardButtons(QMessageBox.Ok )
            ret = msg.exec_()

        else:
            self.login_list = ([user_name, user_pass, account_type, limit])
            pass

    def get_settings(self):
        print ("getting settings")
        #self.select_country_list  = pd.read_json("Countries.json")
        #self.select_industry_list = pd.read_json("Industries.json")
        #self.select_job_position_list    = pd.read_json("Jobtitles.json")


        self.tab = ""
        if (self.tabWidget.currentIndex()==0):
            self.tab="url"
        else:
            self.tab = "search"


        country = self.country_list.currentText()
        for k in (self.select_country_list.values):
            if country == k[0]:
                self.country_code = k[1]
                #print(k[0] ,k[1])

        industry = self.industry_list.currentText()
        for k in (self.select_industry_list.values):
            if industry == k[0]:
                #print(k[0],k[1])
                self.industry_code = k[1]

        job = self.job_position_list.currentText()
        for k in (self.select_job_list.values):
            if job == k[0]:
                #print(k[0],k[1])
                self.job_code=k[1]
        job2 = self.job_position_list_2.currentText()
        for k in (self.select_job_list.values):
            if job2 == k[0]:
                # print(k[0],k[1])
                self.job2_code = k[1]

        self.target = ""
        if   self.company_radio.isChecked():
            self.target = ("company")
        else:
            self.target = ("people")

        try:
            self.link_list = self.target_text_edit.toPlainText().split(",")
        except:
            pass
        #print (link_list)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(1163, 735)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 341, 331))
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 110, 321, 101))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_13 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.name_email_text_edit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.name_email_text_edit.setObjectName("name_email_text_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_email_text_edit)
        self.label_14 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.password_text_edit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.password_text_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_text_edit.setObjectName("password_text_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.password_text_edit)
        self.label_15 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.account_select_list = QtWidgets.QComboBox(self.formLayoutWidget)
        self.account_select_list.setObjectName("account_select_list")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.account_select_list)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 30, 321, 31))
        self.label_6.setStyleSheet("border: 1px solid gray;")
        self.label_6.setObjectName("label_6")

        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(360, 20, 541, 331))
        self.groupBox_2.setStyleSheet("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(10, 30, 521, 31))
        self.label_12.setStyleSheet("border: 1px solid gray;")
        self.label_12.setObjectName("label_12")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_2)
        self.tabWidget.setGeometry(QtCore.QRect(10, 68, 521, 271))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")




        self.job_position_list_2 = QtWidgets.QComboBox(self.tab)
        self.job_position_list_2.setGeometry(QtCore.QRect(270, 80, 154, 25))
        self.job_position_list_2.setObjectName("job_position_list_2")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(10, 80, 154, 25))
        self.label_16.setObjectName("label_16")


        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(10, 50, 154, 24))
        self.label_11.setObjectName("label_11")


        self.target_text_edit = QtWidgets.QPlainTextEdit(self.tab)
        self.target_text_edit.setGeometry(QtCore.QRect(10, 110, 511, 110))
        self.target_text_edit.setObjectName("target_text_edit")
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 511, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.company_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.company_radio.setObjectName("company_radio")
        self.company_radio.setChecked(True)
        self.horizontalLayout.addWidget(self.company_radio)
        self.people_radio = QtWidgets.QRadioButton(self.layoutWidget)
        self.people_radio.setObjectName("people_radio")

        self.horizontalLayout.addWidget(self.people_radio)
        self.layoutWidget.raise_()
        self.label_11.raise_()
        self.target_text_edit.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(27, 10, 471, 41))
        self.label_7.setObjectName("label_7")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(30, 70, 481, 61))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 1, 1, 1)
        self.industry_list = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.industry_list.setObjectName("industry_list")
        self.gridLayout_3.addWidget(self.industry_list, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.job_position_list = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.job_position_list.setObjectName("job_position_list")
        self.gridLayout_3.addWidget(self.job_position_list, 1, 2, 1, 1)
        self.country_list = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.country_list.setObjectName("country_list")
        self.gridLayout_3.addWidget(self.country_list, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.widget_4 = QtWidgets.QWidget(Dialog)
        self.widget_4.setGeometry(QtCore.QRect(10, 350, 1141, 81))
        self.widget_4.setObjectName("widget_4")
        self.text_box = QtWidgets.QLabel(self.widget_4)
        self.text_box.setGeometry(QtCore.QRect(0, 10, 1141, 71))
        self.text_box.setStyleSheet("border: 1px solid gray;")
        self.text_box.setObjectName("text_box")
        self.widget_5 = QtWidgets.QWidget(Dialog)
        self.widget_5.setGeometry(QtCore.QRect(10, 430, 1141, 291))
        self.widget_5.setObjectName("widget_5")
        self.table = QtWidgets.QTableWidget(self.widget_5)
        self.table.setGeometry(QtCore.QRect(0, 10, 1141, 271))
        self.table.setStyleSheet("border: 1px solid gray;")
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table.setRowCount(6)
        self.table.setObjectName("table")
        self.table.setColumnCount(11)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(10, item)
        self.table.horizontalHeader().setDefaultSectionSize(100)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().setMinimumSectionSize(10)
        self.table.verticalHeader().setStretchLastSection(True)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(920, 20, 231, 341))
        self.widget.setObjectName("widget")
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setGeometry(QtCore.QRect(0, 10, 231, 331))
        self.widget_3.setObjectName("widget_3")
        self.gridGroupBox_2 = QtWidgets.QGroupBox(self.widget_3)
        self.gridGroupBox_2.setGeometry(QtCore.QRect(-10, -10, 241, 331))
        self.gridGroupBox_2.setObjectName("gridGroupBox_2")
        self.personal_profiles = QtWidgets.QLabel(self.gridGroupBox_2)
        self.personal_profiles.setGeometry(QtCore.QRect(14, 300, 211, 19))
        self.personal_profiles.setObjectName("personal_profiles")
        self.label_18 = QtWidgets.QLabel(self.gridGroupBox_2)
        self.label_18.setGeometry(QtCore.QRect(14, 30, 221, 31))
        self.label_18.setStyleSheet("border: 1px solid gray;")
        self.label_18.setObjectName("label_18")
        self.current_date = QtWidgets.QLabel(self.gridGroupBox_2)
        self.current_date.setGeometry(QtCore.QRect(14, 230, 221, 19))
        self.current_date.setObjectName("current_date")
        self.start_button = QtWidgets.QPushButton(self.gridGroupBox_2)
        self.start_button.setGeometry(QtCore.QRect(14, 70, 221, 34))
        self.start_button.setObjectName("start_button")
        self.company_profiles = QtWidgets.QLabel(self.gridGroupBox_2)
        self.company_profiles.setGeometry(QtCore.QRect(14, 260, 221, 31))
        self.company_profiles.setObjectName("company_profiles")
        self.save_button = QtWidgets.QPushButton(self.gridGroupBox_2)
        self.save_button.setGeometry(QtCore.QRect(14, 150, 221, 34))
        self.save_button.setObjectName("save_button")
        self.number_profile = QtWidgets.QLabel(self.gridGroupBox_2)
        self.number_profile.setGeometry(QtCore.QRect(14, 200, 221, 21))
        self.number_profile.setObjectName("number_profile")
        self.stop_button = QtWidgets.QPushButton(self.gridGroupBox_2)
        self.stop_button.setGeometry(QtCore.QRect(14, 110, 221, 34))
        self.stop_button.setObjectName("stop_button")
        self.personal_profiles.raise_()
        self.label_18.raise_()
        self.current_date.raise_()
        self.start_button.raise_()
        self.company_profiles.raise_()
        self.save_button.raise_()
        self.number_profile.raise_()
        self.stop_button.raise_()
        self.text_box.raise_()

        self.preset_values()
        self.start_button.clicked.connect(self.on_press_start_button)


        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_13.setText(_translate("Dialog", "User Name/Emails :"))
        self.label_14.setText(_translate("Dialog", "Password :"))
        self.label_15.setText(_translate("Dialog", "Select Account :"))
        self.label_6.setText(_translate("Dialog", "Login Details"))
        self.label_12.setText(_translate("Dialog", "Search Target"))
        self.label_11.setText(_translate("Dialog", "Please paste bellow target companies/ people profile "))
        self.label_16.setText(_translate("Dialog", "Select Job"))
        self.company_radio.setText(_translate("Dialog", "For Companies"))
        self.people_radio.setText(_translate("Dialog", "For People"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Based on Target Url"))
        self.label_7.setText(_translate("Dialog", "Please select your search filters"))
        self.label_10.setText(_translate("Dialog", "Job Position"))
        self.label_9.setText(_translate("Dialog", "Industry"))
        self.label_8.setText(_translate("Dialog", "Country"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Search People"))
        self.text_box.setText(_translate("Dialog", "Bla Bla Bla Text"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Column1"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Column2"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Column3"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Column4"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Column5"))
        item = self.table.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "Column6"))
        item = self.table.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "Column7"))
        item = self.table.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "Column8"))
        item = self.table.horizontalHeaderItem(8)
        item.setText(_translate("Dialog", "Column9"))
        item = self.table.horizontalHeaderItem(9)
        item.setText(_translate("Dialog", "Column10"))
        item = self.table.horizontalHeaderItem(10)
        item.setText(_translate("Dialog", "Column12"))
        self.personal_profiles.setText(_translate("Dialog", "yz - personal profiles"))
        self.label_18.setText(_translate("Dialog", "Scrape Progress"))
        self.current_date.setText(_translate("Dialog", "For Current Date"))
        self.start_button.setText(_translate("Dialog", "Start Collection"))
        self.company_profiles.setText(_translate("Dialog", "xy - company profiles"))
        self.save_button.setText(_translate("Dialog", "Save Output"))
        self.number_profile.setText(_translate("Dialog", "No. of Profiles Visited"))
        self.stop_button.setText(_translate("Dialog", "Stop Collection"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    app.setStyle("fusion")
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

