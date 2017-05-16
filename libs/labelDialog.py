try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from lib import newIcon, labelValidator, distanceValidator

BB = QDialogButtonBox


class LabelDialog(QDialog):

    def __init__(self, text="Enter object label",dis = 0.0, parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)
        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        self.editdis = QLineEdit()
        self.editdis.setText(str(dis))
        self.editdis.setValidator(distanceValidator())
        self.editdis.editingFinished.connect(self.dispostProcess)
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.editdis)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemDoubleClicked.connect(self.listItemClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    def validate(self):
        flag = False
        try:
            if self.editdis.text().trimmed():
                flag = True
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                flag = True
        try:
            if self.editdis.text().trimmed():
                flag &= True
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.editdis.text().strip():
                flag &= True
        if flag:
            self.accept()

    def postProcess(self):
        try:
            self.edit.setText(self.edit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text())

    def dispostProcess(self):
        try:
            self.editdis.setText(self.editdis.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.editdis.setText(self.editdis.text())

    def popUp(self, text='' ,distance = 0.0, move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)

        self.editdis.setText(str(distance))
        self.editdis.setSelection(0, len(str(distance)))
        self.editdis.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        print(self.editdis.text())
        return (self.edit.text(), float(self.editdis.text())) if self.exec_() else None

    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.edit.setText(text)
        self.validate()
