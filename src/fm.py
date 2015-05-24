#!/usr/bin/python3
# fm.py

import os,sys,sip,random,time,subprocess
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QTimer
dir = ""
hiddenshow = False
cdirs=[]
modes=[]
cdir = ''
icons=[]
pagedeleting=False
l=[]
copylist=[]
pastelist=[]
stack=[]
selectlist=[]
lst=0 #index before tab switch
class FileManager(QtGui.QWidget):
	def __init__(self, parent=None):
		global dir,cdir,icons
		self.path=QLineEdit()
		pathname = (os.path.dirname(sys.argv[0]))
		dir = os.path.abspath(pathname)
		QtGui.QWidget.__init__(self, parent)
		#Loading icons
		icons.append(QIcon.fromTheme('folder'))
		icons.append(QIcon.fromTheme('gnome-fs-regular'))
		icons.append(QIcon(dir+'/icons/tab.png'))
		icons.append(QIcon(dir+'/icons/folder.png'))
		icons.append(QIcon(dir+'/icons/file.png'))
		icons.append(QIcon(dir+'/icons/copy.png'))
		icons.append(QIcon(dir+'/icons/paste.png'))
		icons.append(QIcon(dir+'/icons/cut.png'))
		icons.append(QIcon.fromTheme('folder-documents'))
		icons.append(QIcon.fromTheme('user-trash'))
		icons.append(QIcon.fromTheme('user-desktop'))
		#Tab widget init
		self.tabwidget = QtGui.QTabWidget(self)
		self.tabButton = QtGui.QToolButton(self)
		self.tabButton.setText('+')
		self.pagenum=0
		font = self.tabButton.font()
		font.setBold(True)
		cdir='/'
		self.add_page('/')
		self.tabButton.setFont(font)
		#self.tabwidget.setMovable(True)
		self.tabwidget.setCornerWidget(self.tabButton)
		self.tabwidget.setTabsClosable(True)
		self.tabwidget.tabCloseRequested.connect(self.delete_page)
		self.tabButton.clicked.connect(self.add_page)
		self.tabwidget.currentChanged.connect(self.process)
		#Other widgets init
		self.MainList=self.tabwidget.currentWidget().findChild(QtGui.QListWidget, 'List0')
		self.MainTable=self.tabwidget.currentWidget().findChild(QtGui.QTableWidget, 'Table0')
		self.setWindowTitle('Pantera 0.3b ')
		grid = QtGui.QGridLayout()
		grid.setSpacing(10)
		self.resize(640,480)
		#self.MainList.doubleClicked.connect(self.open)
		self.back=QToolButton()
		self.back.setIcon(QIcon.fromTheme('back'))
		self.back.setAutoRaise(True)
		self.forward=QToolButton()
		self.forward.setIcon(QIcon.fromTheme('forward'))
		self.forward.setAutoRaise(True)
		self.terminal=QToolButton()
		self.terminal.setIcon(QIcon(dir+'/terminal.png'))
		self.su = QToolButton()
		self.su.setIcon(QIcon.fromTheme('avatar-default'))
		self.search = QLineEdit('')
		self.search.setVisible(False)
		self.back.clicked.connect(self.up)
		self.search.textChanged.connect(self.filter)
		self.terminal.clicked.connect(self.run_terminal)
		self.su.clicked.connect(self.run_with_rights)
		self.timer=QTimer()
		self.timer.setInterval(1000)
		self.timer.start()
		self.timer.timeout.connect(self.updatelist)
		grid.addWidget(self.back,0,0,1,1)
		grid.addWidget(self.forward,0,1,1,1)
		grid.addWidget(self.terminal,0,7,1,1)
		grid.addWidget(self.su,0,8,1,1)
		grid.addWidget(self.path,0,2,1,5)
		grid.addWidget(self.tabwidget,1,0,4,9)
		grid.addWidget(self.search,5,0,1,9)
		#grid.addWidget(self.table,6,0,3,9)
		self.setLayout(grid)
	def cleartable(self,i):
			while self.MainTable.rowCount()>i:
				self.MainTable.removeRow(self.MainTable.rowCount()-1)
			a=''
			try:
				a=cdir+'/'+self.MainTable.item(0,0).text()
				if not os.path.isdir(a) and not os.path.isfile(a):
					self.MainTable.removeRow(0)	
			except:
				self.MainTable.removeRow(0)			
			
				
			
	def delete_page(self,index):
		global lst,pagedeleting
		interactor = self.tabwidget.widget(index)
		cdirs.pop(index)
		modes.pop(index)
		if not len(cdirs):
			exit(0)
		if lst>=index:
			lst-=1
		pagedeleting=True
		self.tabwidget.removeTab(index)
		interactor.close()
		interactor.deleteLater()
		pagedeleting=False
	# Multi-tab engine -start-
	def process(self):
		global cdir,lst
		k=self.tabwidget.currentWidget().objectName()
		self.MainList = self.tabwidget.currentWidget().findChild(QtGui.QListWidget, 'List'+k[4:len(k)])
		self.MainTable = self.tabwidget.currentWidget().findChild(QtGui.QTableWidget, 'Table'+k[4:len(k)])
		print (self.MainTable.objectName())
		if not pagedeleting:
			cdirs[lst]=cdir
		cdir=cdirs[self.tabwidget.currentIndex()]
		lst=self.tabwidget.currentIndex()
		self.path.setText(cdir)
	def add_page(self,dir):
		grid = QtGui.QGridLayout()
		page = QtGui.QWidget()
		#Listwidget
		m=QtGui.QListWidget()
		m.setObjectName('List'+str(self.pagenum))
		m.addItem('List'+str(self.pagenum))
		m.setParent(page)
		m.doubleClicked.connect(self.open)
		#Tablewidget
		table=QTableWidget()
		table.setObjectName('Table'+str(self.pagenum))
		table.setParent(page)
		table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		table.setShowGrid(True)	
		table.verticalHeader().setVisible(False)
		table.insertColumn(0)
		table.insertColumn(1)
		table.insertColumn(2)
		table.insertColumn(3)
		table.setColumnWidth(0,240)
		table.setColumnWidth(1,60)
		table.setColumnWidth(2,90)
		table.setColumnWidth(3,180)
		table.horizontalHeader().setResizeMode(0,QHeaderView.Stretch)
		table.setSelectionBehavior(QAbstractItemView.SelectRows)
		table.setVisible(False)
		table.cellDoubleClicked.connect(self.open)
		grid.addWidget(m, 1, 0)
		grid.addWidget(table, 1, 0)
		page.setLayout(grid)
		table.setContextMenuPolicy(Qt.CustomContextMenu)
		table.customContextMenuRequested.connect(self.OpenMenu)
		m.setContextMenuPolicy(Qt.CustomContextMenu)
		m.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		m.customContextMenuRequested.connect(self.OpenMenu)
		m.setMovement(False);
		m.setResizeMode(QtGui.QListView.Adjust)
		
		newname = 'Page'+str(self.pagenum)
		page.setObjectName(newname)
		self.tabwidget.addTab(page, newname)
		self.tabwidget.widget(self.pagenum)
		if not len(dir):
			cdirs.append('/')
		else:
			cdirs.append(dir)
			self.tabwidget.setTabText(len(cdirs)-1,os.path.basename(dir))
		modes.append(1)
		self.tabwidget.setCurrentIndex(self.pagenum)
		self.pagenum+=1
		self.MainList=m
		self.MainTable=table
		self.MainList.setViewMode(QtGui.QListView.ListMode)
		self.MainList.setGridSize(QSize(24,24))
		self.MainList.setIconSize(QSize(16,16))
		self.switchviewmode(modes[0])
		self.displaydir()
	# Multi-tab engine -end-
	def switchviewmode(self, mode):
		global modes
		if mode==1:
			self.MainList.setVisible(True)
			self.MainTable.setVisible(False)
			self.MainList.setViewMode(QtGui.QListView.ListMode)
			self.MainList.setGridSize(QSize(24,24))
			self.MainList.setIconSize(QSize(16,16))
			for i in range(len(modes)):
				modes[i]=1
			self.displaydir()
		elif mode==2:
			self.MainList.setVisible(True)
			self.MainTable.setVisible(False)
			self.MainList.setViewMode(QtGui.QListView.IconMode)
			self.MainList.setGridSize(QSize(96,96))
			self.MainList.setIconSize(QSize(48,48))
			for i in range(len(modes)):
				modes[i]=2
			self.displaydir()
		elif mode==3:
				self.MainList.setVisible(False)
				self.MainTable.setVisible(True)
				for i in range(len(modes)):
					modes[i]=3
				self.displaydir()
	def updatelist(self):
		if not len(self.search.text()) or not self.search.isVisible():
			global selectlist
			selectlist.clear()
			for i in range(self.MainList.count()):
				if self.MainList.item(i).isSelected():
					selectlist.append(self.MainList.item(i).text())
					
			global l
			os.chdir(cdir)
			dirs = sorted([x for x in os.listdir('.') if os.path.isdir(x) and (x[0] != '.' or hiddenshow)])
			l = dirs +sorted([x for x in os.listdir('.') if not os.path.isdir(x) and (x[0] != '.' or hiddenshow)])
			m=len(dirs)
			if (len(l)!=self.MainList.count() and modes[lst]!=3) or (len(l)!=self.MainTable.rowCount() and modes[lst]==3):
				print (len(l), self.MainList.count())
				self.MainList.clear()
				print ('displaying... '+cdir)
				if modes[lst]!=3:
					for i in range (m):
						self.MainList.addItem(l[i])
						self.MainList.item(i).setTextColor(QColor(0,0,255))
						self.MainList.item(i).setIcon(icons[0])
					for i in range (m, len(l)):
						self.MainList.addItem(l[i])
						self.MainList.item(i).setTextColor(QColor(0,0,0))
						self.MainList.item(i).setIcon(icons[1])
				else:
					n=self.MainTable.rowCount()
					i=0
					for i in range (m):
						if i>=n:
							self.MainTable.insertRow(i)
						self.MainTable.setRowHeight(i,24)
						self.MainTable.setItem(i,0,QTableWidgetItem(l[i]))
						self.MainTable.item(i,0).setIcon(icons[0])
						self.MainTable.setItem(i,2,QTableWidgetItem('-'))
						self.MainTable.item(i,2).setTextAlignment(Qt.AlignHCenter)
					for i in range (m, len(l)):
						if i>=n:
							self.MainTable.insertRow(i)
						self.MainTable.setRowHeight(i,24)
						self.MainTable.setItem(i,0,QTableWidgetItem(l[i]))
						self.MainTable.item(i,0).setIcon(icons[1])
						self.MainTable.setItem(i,1,QTableWidgetItem(os.path.splitext(l[i])[1]))
						size=round(os.path.getsize(cdir+'/'+l[i])/1024,2)
						self.MainTable.setItem(i,2,QTableWidgetItem(str(size)+' kb'))						
					self.cleartable(i+1)
					self.MainTable.setHorizontalHeaderItem(0,QTableWidgetItem('Name'))
					self.MainTable.setHorizontalHeaderItem(1,QTableWidgetItem('Type'))
					self.MainTable.setHorizontalHeaderItem(2,QTableWidgetItem('Size'))
					self.MainTable.setHorizontalHeaderItem(3,QTableWidgetItem('Date'))	
				self.path.setText(cdir)
				if len(cdir)>1:
					self.tabwidget.setTabText(lst,os.path.basename(cdir))
				else:
					self.tabwidget.setTabText(lst,'root')
			
			if len(selectlist):
				for i in selectlist:
					print (i)
					m=l.index(i)
					if m>=0:
						self.MainList.item(m).setSelected(True)
	
	def displaydir(self):
		global l
		print ('displaying... '+cdir)
		os.chdir(cdir)
		self.MainList.clear()
		dirs = sorted([x for x in os.listdir('.') if os.path.isdir(x) and (x[0] != '.' or hiddenshow)])
		l = dirs +sorted([x for x in os.listdir('.') if not os.path.isdir(x) and (x[0] != '.' or hiddenshow)])
		m=len(dirs)
		#ListWidget loading
		if modes[lst]!=3:
			for i in range (m):
				self.MainList.addItem(l[i])
				self.MainList.item(i).setTextColor(QColor(0,0,255))
				self.MainList.item(i).setIcon(icons[0])
			for i in range (m, len(l)):
				self.MainList.addItem(l[i])
				self.MainList.item(i).setTextColor(QColor(0,0,0))
				self.MainList.item(i).setIcon(icons[1])
			self.MainTable.clear()
		#TableWidget loading
		else:
			n=self.MainTable.rowCount()
			i=0
			for i in range (m):
				if i>=n:
					self.MainTable.insertRow(i)
				self.MainTable.setRowHeight(i,24)
				self.MainTable.setItem(i,0,QTableWidgetItem(l[i]))
				self.MainTable.item(i,0).setIcon(icons[0])
				self.MainTable.setItem(i,2,QTableWidgetItem('-'))
				self.MainTable.item(i,2).setTextAlignment(Qt.AlignHCenter)
				self.MainTable.setItem(i,3,QTableWidgetItem(time.ctime(os.path.getctime(l[i]))))
				self.MainTable.item(i,3).setTextAlignment(Qt.AlignHCenter)
			for i in range (m, len(l)):
				if i>=n:
					self.MainTable.insertRow(i)
				self.MainTable.setRowHeight(i,24)
				self.MainTable.setItem(i,0,QTableWidgetItem(l[i]))
				self.MainTable.item(i,0).setIcon(icons[1])
				self.MainTable.setItem(i,1,QTableWidgetItem(os.path.splitext(l[i])[1]))
				size=round(os.path.getsize(cdir+'/'+l[i])/1024,2)
				self.MainTable.setItem(i,2,QTableWidgetItem(str(size)+' kb'))
				self.MainTable.setItem(i,3,QTableWidgetItem(time.ctime(os.path.getctime(l[i]))))
				self.MainTable.item(i,2).setTextAlignment(Qt.AlignHCenter)
				self.MainTable.item(i,3).setTextAlignment(Qt.AlignHCenter)
			self.cleartable(i+1)
			#Table headers	
			self.MainTable.setHorizontalHeaderItem(0,QTableWidgetItem('Name'))
			self.MainTable.setHorizontalHeaderItem(1,QTableWidgetItem('Type'))
			self.MainTable.setHorizontalHeaderItem(2,QTableWidgetItem('Size'))
			self.MainTable.setHorizontalHeaderItem(3,QTableWidgetItem('Date'))
		self.path.setText(cdir)
		if len(cdir)>1:
			self.tabwidget.setTabText(lst,os.path.basename(cdir))
		else:
			self.tabwidget.setTabText(lst,'root')
	def keyPressEvent(self, event):
		global hiddenshow,cdir
		if event.key() == QtCore.Qt.Key_H:
			if event.modifiers() == QtCore.Qt.ControlModifier:
				if hiddenshow==False:
					hiddenshow=True
				else:
					hiddenshow=False
				self.displaydir()
		if event.key() == QtCore.Qt.Key_S:
			if event.modifiers() == QtCore.Qt.ControlModifier:
				if self.search.isVisible()==False:
					self.search.setVisible(True)
					self.search.setFocus()
				else:
					self.search.setText('')
					self.search.setVisible(False)
		if event.key() == QtCore.Qt.Key_Return:
			k=self.MainList.currentItem().text()
			if os.path.isdir(cdir+'/'+k) and os.access(cdir+'/'+k, os.R_OK):
				if len(cdir)>1:
					cdir+='/'
				cdir+=k
				os.chdir(cdir)
				self.displaydir()
			elif os.access(cdir+'/'+k, os.R_OK):
				os.system('xdg-open '+cdir+'/'+'"'+k+'"')
		if event.key() == QtCore.Qt.Key_1:
			if event.modifiers() == QtCore.Qt.ControlModifier:
				self.switchviewmode(1)
		if event.key() == QtCore.Qt.Key_2:
			if event.modifiers() == QtCore.Qt.ControlModifier:
				self.switchviewmode(2)
		if event.key() == QtCore.Qt.Key_3:
			if event.modifiers() == QtCore.Qt.ControlModifier:
				self.switchviewmode(3)
		if event.key() == QtCore.Qt.Key_C:
			if event.modifiers() == QtCore.Qt.ControlModifier:
				self.makecopy()
		if event.key() == QtCore.Qt.Key_V:
			if event.modifiers() == QtCore.Qt.ControlModifier:
				self.makepaste()
		if event.key() == QtCore.Qt.Key_Delete:
			self.makedelete()
	def open(self):
		global cdir
		print (modes[lst])
		if modes[lst]!=3:
			n=cdir+'/'+self.MainList.currentItem().text()
		else:
			n=cdir+'/'+self.MainTable.item(self.MainTable.currentRow(),0).text()
		if os.path.isdir(n) and os.access(n, os.R_OK):
			if cdir[len(cdir)-1]!='/':
				cdir+='/'
			cdir+=self.MainTable.item(self.MainTable.currentRow(),0).text() if modes[lst]==3 else self.MainList.currentItem().text()
			os.chdir(n)
			self.displaydir()
			
		elif os.access(n, os.R_OK):
			os.system('xdg-open "'+n+'"')
	def up(self):
		global cdir
		print ('do: '+cdir)
		if len(cdir)>1:
			cdir = cdir[0:cdir.rindex('/')]
			if len(cdir)==0:
				cdir='/'
			os.chdir(cdir)
			print ('posle: '+cdir)
			self.displaydir()
	def run_terminal(self):
		os.system('exo-open --launch TerminalEmulator')
	def run_with_rights(self):
		os.system('gksu '+dir+'/fm.py&')
	def makedelete(self):
		copylist.clear()
		if cdir[len(cdir)-1]!='/':
			mdir=cdir+'/'
		else:
			mdir=cdir
		if modes[lst]!=3:
			for i in range(0,self.MainList.count()):
				if self.MainList.item(i).isSelected():
					copylist.append(mdir+self.MainList.item(i).text())
		else:
			for i in range(0,self.MainTable.rowCount()):
				if self.MainTable.item(i,0).isSelected():
					copylist.append(mdir+self.MainTable.item(i,0).text())
		m='delete|'+cdir+'|'
		if len(copylist):
			for i in copylist:
				m+=i+'|'
			QtGui.QApplication.clipboard().setText(m, QClipboard.Clipboard)
		os.system('"'+dir+'/pactions.py" &')
	def makecopy(self):
		copylist.clear()
		if cdir[len(cdir)-1]!='/':
			mdir=cdir+'/'
		else:
			mdir=cdir
		if modes[lst]!=3:
			for i in range(0,self.MainList.count()):
				if self.MainList.item(i).isSelected():
					copylist.append(mdir+self.MainList.item(i).text())
			m=cdir+'|'
		else:
			for i in range(0,self.MainTable.rowCount()):
				if self.MainTable.item(i,0).isSelected():
					copylist.append(mdir+self.MainTable.item(i,0).text())
			m=cdir+'|'
		if len(copylist):
			for i in copylist:
				m+=i+'|'
			QtGui.QApplication.clipboard().setText(m, QClipboard.Clipboard)
	def makeinfo(self):
		copylist.clear()
		if cdir[len(cdir)-1]!='/':
			mdir=cdir+'/'
		else:
			mdir=cdir
		if modes[lst]!=3:
			for i in range(0,self.MainList.count()):
				if self.MainList.item(i).isSelected():
					copylist.append(mdir+self.MainList.item(i).text())
		else:
			for i in range(0,self.MainTable.rowCount()):
				if self.MainTable.item(i,0).isSelected():
					copylist.append(mdir+self.MainTable.item(i,0).text())
		m="info|"
		if len(copylist):
			for i in copylist:
				m+=i+'|'
			QtGui.QApplication.clipboard().setText(m, QClipboard.Clipboard)
		os.system('"'+dir+'/pactions.py" &')
	def makepaste(self):
			p=QtGui.QApplication.clipboard()
			m=p.text(QClipboard.Clipboard)
			m='copy|'+cdir+'|'+m
			QtGui.QApplication.clipboard().setText(m, QClipboard.Clipboard)
			os.system('"'+dir+'/pactions.py" &')
	def OpenMenu(self):
		menu = QMenu()
		newtab = menu.addAction(icons[2],'Open in a new tab')
		newtab.setIconVisibleInMenu(True)
		newfolder = menu.addAction(icons[3],'New Folder')
		newfolder.setIconVisibleInMenu(True)
		copyAction = menu.addAction(icons[5],"Copy")
		copyAction.setIconVisibleInMenu(True)
		pasteAction = menu.addAction(icons[6],"Paste")
		pasteAction.setIconVisibleInMenu(True)
		cutAction = menu.addAction(icons[7],"Cut")
		cutAction.setIconVisibleInMenu(True)
		deleteAction = menu.addAction(icons[9],"Delete")
		deleteAction.setIconVisibleInMenu(True)
		infoAction = menu.addAction(icons[10],"Info")
		infoAction.setIconVisibleInMenu(True)
		cursor =QtGui.QCursor()
		action = menu.exec(cursor.pos())
		if action == newfolder:
			text, ok = QtGui.QInputDialog.getText(self, 'Enter the name for a new folder', 
			'New Folder:', QLineEdit.Normal,"1")
			os.mkdir(cdir+'/'+text)
			self.displaydir()
		elif action == copyAction:
			self.makecopy()
		elif action == pasteAction:
			self.makepaste()
		elif action == infoAction:
			self.makeinfo()
		elif action == deleteAction:
			self.makedelete()
		elif action == newtab:
			lister=[]
			if modes[lst]!=3:
				for i in range (self.MainList.count()):
					if self.MainList.item(i).isSelected() and os.path.isdir(self.MainList.item(i).text()) and os.access(self.MainList.item(i).text(),os.R_OK):
						if len(cdir)>1:
							lister.append(cdir+'/'+self.MainList.item(i).text())
						else:
							lister.append(cdir+self.MainList.item(i).text())
			else:
				for i in range (self.MainTable.rowCount()):
					if self.MainTable.item(i,0).isSelected() and os.path.isdir(self.MainTable.item(i,0).text()) and os.access(self.MainTable.item(i,0).text(),os.R_OK):
						if len(cdir)>1:
							lister.append(cdir+'/'+self.MainTable.item(i,0).text())
						else:
							lister.append(cdir+self.MainTable.item(i,0).text())
			for i in lister:
				self.add_page(i)
	def displayfilter(self,text):
		text=text.lower()
		d=l.copy()
		i=0
		m=self.path.text()+'/'
		while i<len(d):
			if not text in d[i].lower():
				d.pop(i)
				i-=1
			i+=1
		self.MainList.clear()
		for i in range (len(d)):
			self.MainList.addItem(d[i])
			if os.path.isdir(m+d[i]):
				print (m)
				self.MainList.item(i).setIcon(icons[0])
				self.MainList.item(i).setTextColor(QColor(0,0,255))
			else:
				self.MainList.item(i).setIcon(icons[1])
				self.MainList.item(i).setTextColor(QColor(0,0,0))
		
	def filter(self):
		print (self.search.text())
		if len(self.search.text()):
			self.displayfilter(self.search.text())
			if self.MainList.count()==1:
				self.MainList.item(0).setSelected(True)
		else:
			self.displaydir()
app = QtGui.QApplication(sys.argv)
ex = FileManager()
ex.show()
sys.exit(app.exec_())
