# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'files/qt/SearchGeocachesDialog.ui'
#
# Created: Tue Aug  3 13:52:34 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SearchGeocachesDialog(object):
    def setupUi(self, SearchGeocachesDialog):
        SearchGeocachesDialog.setObjectName("SearchGeocachesDialog")
        SearchGeocachesDialog.resize(874, 481)
        self.gridLayout = QtGui.QGridLayout(SearchGeocachesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(SearchGeocachesDialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_4 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setFrameShape(QtGui.QFrame.NoFrame)
        self.label.setObjectName("label")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lineEditName = QtGui.QLineEdit(self.groupBox)
        self.lineEditName.setObjectName("lineEditName")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditName)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 2, 1)
        self.dialogButtonBox = QtGui.QDialogButtonBox(SearchGeocachesDialog)
        self.dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.dialogButtonBox.setObjectName("dialogButtonBox")
        self.gridLayout.addWidget(self.dialogButtonBox, 6, 0, 1, 2)
        self.groupBox_4 = QtGui.QGroupBox(SearchGeocachesDialog)
        self.groupBox_4.setObjectName("groupBox_4")
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_10 = QtGui.QLabel(self.groupBox_4)
        self.label_10.setWordWrap(True)
        self.label_10.setObjectName("label_10")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_10)
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.listWidgetSize = QtGui.QListWidget(self.groupBox_4)
        self.listWidgetSize.setObjectName("listWidgetSize")
        item = QtGui.QListWidgetItem(self.listWidgetSize)
        item.setCheckState(QtCore.Qt.Checked)
        item = QtGui.QListWidgetItem(self.listWidgetSize)
        item.setCheckState(QtCore.Qt.Checked)
        item = QtGui.QListWidgetItem(self.listWidgetSize)
        item.setCheckState(QtCore.Qt.Checked)
        item = QtGui.QListWidgetItem(self.listWidgetSize)
        item.setCheckState(QtCore.Qt.Checked)
        item = QtGui.QListWidgetItem(self.listWidgetSize)
        item.setCheckState(QtCore.Qt.Checked)
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.listWidgetSize)
        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setObjectName("label_7")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_12 = QtGui.QLabel(self.groupBox_4)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_2.addWidget(self.label_12)
        self.doubleSpinBoxDifficultyMin = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBoxDifficultyMin.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.doubleSpinBoxDifficultyMin.setCorrectionMode(QtGui.QAbstractSpinBox.CorrectToNearestValue)
        self.doubleSpinBoxDifficultyMin.setPrefix("")
        self.doubleSpinBoxDifficultyMin.setDecimals(1)
        self.doubleSpinBoxDifficultyMin.setMinimum(1.0)
        self.doubleSpinBoxDifficultyMin.setMaximum(5.0)
        self.doubleSpinBoxDifficultyMin.setSingleStep(0.5)
        self.doubleSpinBoxDifficultyMin.setObjectName("doubleSpinBoxDifficultyMin")
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxDifficultyMin)
        self.label_11 = QtGui.QLabel(self.groupBox_4)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_2.addWidget(self.label_11)
        self.doubleSpinBoxDifficultyMax = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBoxDifficultyMax.setDecimals(1)
        self.doubleSpinBoxDifficultyMax.setMinimum(1.0)
        self.doubleSpinBoxDifficultyMax.setMaximum(5.0)
        self.doubleSpinBoxDifficultyMax.setSingleStep(0.5)
        self.doubleSpinBoxDifficultyMax.setProperty("value", 5.0)
        self.doubleSpinBoxDifficultyMax.setObjectName("doubleSpinBoxDifficultyMax")
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxDifficultyMax)
        self.formLayout_3.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_8 = QtGui.QLabel(self.groupBox_4)
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_3.addWidget(self.label_13)
        self.doubleSpinBoxTerrainMin = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBoxTerrainMin.setDecimals(1)
        self.doubleSpinBoxTerrainMin.setMinimum(1.0)
        self.doubleSpinBoxTerrainMin.setMaximum(5.0)
        self.doubleSpinBoxTerrainMin.setSingleStep(0.5)
        self.doubleSpinBoxTerrainMin.setObjectName("doubleSpinBoxTerrainMin")
        self.horizontalLayout_3.addWidget(self.doubleSpinBoxTerrainMin)
        self.label_14 = QtGui.QLabel(self.groupBox_4)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_3.addWidget(self.label_14)
        self.doubleSpinBoxTerrainMax = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBoxTerrainMax.setDecimals(1)
        self.doubleSpinBoxTerrainMax.setMinimum(1.0)
        self.doubleSpinBoxTerrainMax.setMaximum(5.0)
        self.doubleSpinBoxTerrainMax.setSingleStep(0.5)
        self.doubleSpinBoxTerrainMax.setProperty("value", 5.0)
        self.doubleSpinBoxTerrainMax.setObjectName("doubleSpinBoxTerrainMax")
        self.horizontalLayout_3.addWidget(self.doubleSpinBoxTerrainMax)
        self.formLayout_3.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.gridLayout.addWidget(self.groupBox_4, 2, 1, 2, 1)
        self.groupBox_2 = QtGui.QGroupBox(SearchGeocachesDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.comboBoxLocation = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxLocation.setObjectName("comboBoxLocation")
        self.comboBoxLocation.addItem("")
        self.comboBoxLocation.addItem("")
        self.comboBoxLocation.addItem("")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxLocation)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.spinBoxRadius = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxRadius.setEnabled(False)
        self.spinBoxRadius.setMinimum(1)
        self.spinBoxRadius.setMaximum(100)
        self.spinBoxRadius.setSingleStep(2)
        self.spinBoxRadius.setObjectName("spinBoxRadius")
        self.horizontalLayout_4.addWidget(self.spinBoxRadius)
        self.labelLocation = QtGui.QLabel(self.groupBox_2)
        self.labelLocation.setText("")
        self.labelLocation.setObjectName("labelLocation")
        self.horizontalLayout_4.addWidget(self.labelLocation)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(SearchGeocachesDialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.listWidgetType = QtGui.QListWidget(self.groupBox_3)
        self.listWidgetType.setObjectName("listWidgetType")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.listWidgetType)
        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBoxHideFound = QtGui.QCheckBox(self.groupBox_3)
        self.checkBoxHideFound.setChecked(True)
        self.checkBoxHideFound.setObjectName("checkBoxHideFound")
        self.horizontalLayout.addWidget(self.checkBoxHideFound)
        self.formLayout_2.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxShowOnlyMarked = QtGui.QCheckBox(self.groupBox_3)
        self.checkBoxShowOnlyMarked.setObjectName("checkBoxShowOnlyMarked")
        self.verticalLayout.addWidget(self.checkBoxShowOnlyMarked)
        self.formLayout_2.setLayout(4, QtGui.QFormLayout.FieldRole, self.verticalLayout)
        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 2, 1)

        self.retranslateUi(SearchGeocachesDialog)
        QtCore.QObject.connect(self.dialogButtonBox, QtCore.SIGNAL("accepted()"), SearchGeocachesDialog.accept)
        QtCore.QObject.connect(self.dialogButtonBox, QtCore.SIGNAL("rejected()"), SearchGeocachesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SearchGeocachesDialog)

    def retranslateUi(self, SearchGeocachesDialog):
        SearchGeocachesDialog.setWindowTitle(QtGui.QApplication.translate("SearchGeocachesDialog", "Search Geocaches", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SearchGeocachesDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "Geocache Name", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("SearchGeocachesDialog", "Details (2)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "If you change something here, only geocaches for which details have been downloaded will be shown in the result.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "Size", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listWidgetSize.isSortingEnabled()
        self.listWidgetSize.setSortingEnabled(False)
        self.listWidgetSize.item(0).setText(QtGui.QApplication.translate("SearchGeocachesDialog", "micro", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidgetSize.item(1).setText(QtGui.QApplication.translate("SearchGeocachesDialog", "small", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidgetSize.item(2).setText(QtGui.QApplication.translate("SearchGeocachesDialog", "regular", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidgetSize.item(3).setText(QtGui.QApplication.translate("SearchGeocachesDialog", "huge", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidgetSize.item(4).setText(QtGui.QApplication.translate("SearchGeocachesDialog", "other", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidgetSize.setSortingEnabled(__sortingEnabled)
        self.label_7.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "Difficulty", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "min.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "max.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "Terrain", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "min.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "max.", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("SearchGeocachesDialog", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLocation.setItemText(0, QtGui.QApplication.translate("SearchGeocachesDialog", "anywhere", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLocation.setItemText(1, QtGui.QApplication.translate("SearchGeocachesDialog", "around my position", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBoxLocation.setItemText(2, QtGui.QApplication.translate("SearchGeocachesDialog", "around the current map center", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "Radius", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRadius.setSuffix(QtGui.QApplication.translate("SearchGeocachesDialog", " km", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("SearchGeocachesDialog", "Details (1)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "Type(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxHideFound.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "hide found geocaches", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowOnlyMarked.setText(QtGui.QApplication.translate("SearchGeocachesDialog", "only marked geocaches", None, QtGui.QApplication.UnicodeUTF8))

