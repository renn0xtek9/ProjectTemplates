#!/usr/bin/env python3
import sys, os
from os import listdir
from os.path import isfile, join, isdir
import re

from PyQt5.QtCore import(QSize, pyqtSignal)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout,QPushButton,QWidget, QHBoxLayout,QAction,qApp, QLineEdit,QFileDialog,QStackedWidget)
from PyQt5.QtGui import (QIcon ,QPixmap)


class Project(QPushButton):	
	m_name=""
	m_type=""
	m_comment=""
	m_iconurl=""
	m_folder=""
	def __init__(self):
		super().__init__("Button")
		self.m_icon=QIcon()
		
	def UpdateUI(self):
		self.m_icon.addPixmap(QPixmap(self.m_iconurl))
		self.setIcon(self.m_icon)
		self.setText(self.m_name)
		self.setToolTip(self.m_comment)
		self.setAutoDefault(True)
		self.clicked.connect(self.ProjectClickedEvent)
		
	projectClicked=pyqtSignal(object)
		
	def ProjectClickedEvent(self):
		print("Project is clicked "+self.m_name)
		self.projectClicked.emit(self)
	

class MainWindow(QMainWindow):

	mainwidget=None
	projlist=list()
	
	m_wmainwidget=None 
	m_wapplywidget=None
	m_stackedwidget=None
	def __init__(self):
		super().__init__()
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.projlist=ListAvailableProjects()
		self.setWindowIcon(QIcon.fromTheme("applications-development"))
		self.initUI()	
        
	def initUI(self):   
		self.m_stackedwidget=QStackedWidget(self)
		self.m_wmainwidget=QWidget(self)
		self.m_wapplywidget=QWidget(self)
		exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)
		self.statusBar()
		self.setWindowTitle('New Project')    
		self.showMaximized()	
		self.initApplyWidget()
		self.initMainWidget()
		self.m_stackedwidget.addWidget(self.m_wmainwidget)
		self.m_stackedwidget.addWidget(self.m_wapplywidget)
		self.setCentralWidget(self.m_stackedwidget)
		self.GoToMainView()
		
	def initApplyWidget(self):
		vlayout=QVBoxLayout()
		hlayout=QHBoxLayout()
		okbutton=QPushButton(QIcon.fromTheme("dialog-ok-apply"),"Ok")
		cancelbutton=QPushButton(QIcon.fromTheme("dialog-cancel"),"Cancel")
		cancelbutton.clicked.connect(self.GoToMainView)
		self.wfolderlineedit=QLineEdit("/home/max/")	#TODO use default path value form within templates
		wfolderbutton=QPushButton(QIcon.fromTheme("document-open-folder"),"Open")
		wfolderbutton.clicked.connect(self.OnFolderSelectionButton)
		wfolderselection=QWidget()
		wfolderselection.setLayout(QHBoxLayout())
		wfolderselection.layout().addWidget(wfolderbutton)
		wfolderselection.layout().addWidget(self.wfolderlineedit)
		projectnameedit=QLineEdit("ProjectName")	#TODO define focus on me TODO use default name value
		projectnameedit.setFocus()
		hlayout.addWidget(okbutton)
		hlayout.addWidget(cancelbutton)
		bottomwidget=QWidget()
		bottomwidget.setLayout(hlayout)
		vlayout.addWidget(projectnameedit)
		vlayout.addWidget(wfolderselection)
		vlayout.addWidget(bottomwidget)
		self.m_wapplywidget.setLayout(vlayout)
	
	def initMainWidget(self):
		self.m_wmainwidget.setLayout(QVBoxLayout())
		for p in self.projlist :
			print(p)
			p.UpdateUI()
			p.projectClicked.connect(self.ApplyWidget)
			self.m_wmainwidget.layout().addWidget(p)
		self.m_wmainwidget.layout().addStretch(1)
	
	def ApplyWidget(self,p_Project):
		print("Will apply "+p_Project.m_name)
		self.m_stackedwidget.setCurrentIndex(1)
	
	def OnFolderSelectionButton(self):
		selectedfolder=QFileDialog.getExistingDirectory(self,"Select directory where to place new project",os.path.expanduser('~'))
		print("user selected:"+selectedfolder)
		self.wfolderlineedit.setText(selectedfolder)
		
	def GoToMainView(self):
		self.m_stackedwidget.setCurrentIndex(0)
		
def ReadATemplateDesktopFile(file):
	with open(file) as f:  #This conserve the \namenamen at en of lines
		content = [line.rstrip('\n') for line in open(file)]	#while this approach does not	
	proj=Project()
	for line in content:
		if "Name=" in line:
			proj.m_name=re.sub(r'Name=','',line)
		if "Type=" in line:
			proj.m_type=re.sub(r'Type=','',line)
		if "Comment=" in line:
			proj.m_comment=re.sub(r'Comment=','',line)
		if "Icon=" in line:
			proj.m_iconurl=re.sub(r'Icon=','',line)
	return proj	

def ListAvailableProjects():
	folder="/home/max/Templates/Project_Templates"
	projectlist=list()
	onlyfiles = [f for f in listdir(folder) if (isdir(join(folder, f)) and isfile(join(folder,f,"template.desktop")))]
	for file in onlyfiles:
		proj=ReadATemplateDesktopFile(join(folder,file,"template.desktop"))
		proj.folder=join(folder,file)
		projectlist.append(proj)
	return projectlist

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MainWindow()
	sys.exit(app.exec_())
