#!/usr/bin/python3
# pactions.py

import os,sys,sip,random,time,subprocess,stat, shutil
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QTimer
from threading import Thread
dir = ""
hiddenshow = False
cdir = ''
mode=""
icons=[]
l=[]
k=0
size=0
size2=0
state=1
baselist=[]
copylist=[]
fromdir=""
todir=""
app = QtGui.QApplication(sys.argv)
def createpath(str):
	return os.path.normpath(todir+'/'+str[len(fromdir):len(str)])
def copymode(src, dst):
    if hasattr(os, 'chmod'):
        st = os.stat(src)
        mode = stat.S_IMODE(st.st_mode)
        os.chmod(dst, mode)
def copyfileobj(fsrc, fdst, length=1024*1024):
	global size2
	while 1:
		buf = fsrc.read(length)
		size2+=length
		if not buf:
			break
		fdst.write(buf)
def copyfile(src, dst):
	with open(src, 'rb') as fsrc:
		with open(dst, 'wb') as fdst:
			copyfileobj(fsrc, fdst)
def copy(src, dst):
	global size2
	if os.path.isdir(dst):
		dst = os.path.join(dst, os.path.basename(src))
	m=size2
	copyfile(src, dst)
	size2=m+os.path.getsize(src)
	copymode(src, dst)
def makeinfo():
	#Creating list of files
	global copylist,baselist,k,size,size2,state
	state=1
	k=0
	copylist.clear()
	size=0
	for i in baselist:
		if os.path.isdir(i):
			for d, dirs, files in os.walk(i):
				copylist.append(d)
				for f in files:
					k+=1
					path = os.path.join(d,f)
					copylist.append(path)
					size+=os.path.getsize(path)
		elif os.path.isfile(i):
			copylist.append(i)
			size+=os.path.getsize(i)

def makedelete():
	#Creating list of files
	global copylist,baselist,k,size,size2,state,mode
	state=1
	k=0
	copylist.clear()
	size=0
	for i in baselist:
		if os.path.isdir(i):
			for d, dirs, files in os.walk(i):
				for f in files:
					k+=1
					path = os.path.join(d,f)
					copylist.append(path)
					size+=os.path.getsize(path)
				copylist.append(d)
		elif os.path.isfile(i):
			copylist.append(i)
			size+=os.path.getsize(i)
	if not len(copylist[len(copylist)-1]):
		copylist.pop()
	if len(fromdir): #Deleting files 
		state=2
		size2=0
		k=0
		for i in copylist:
			print (i)
			if os.path.isfile(i):
				size2+=os.path.getsize(i)
				os.remove(i)
				k+=1
		mode="finish"
	for i in baselist:
		if os.path.isdir(i):
			shutil.rmtree(i)
	
	
def makecopy():
	#Creating list of files
	global copylist,baselist,k,size,size2,state,mode
	state=1
	k=0
	copylist.clear()
	size=0
	for i in baselist:
		if os.path.isdir(i):
			for d, dirs, files in os.walk(i):
				copylist.append(d)
				for f in files:
					k+=1
					path = os.path.join(d,f)
					copylist.append(path)
					size+=os.path.getsize(path)
		elif os.path.isfile(i):
			copylist.append(i)
			size+=os.path.getsize(i)
	state=2
	if not len(copylist[len(copylist)-1]):
		copylist.pop()
	if len(fromdir): #Processing copying
		state=2
		size2=0
		k=0
		for i in copylist:
			n=createpath(i)
			if os.path.isdir(i):
				if not os.path.isdir(n):
					os.mkdir(n)
			else:
				if os.path.isfile(n):
					os.remove (n)
				copy(i, n)
				k+=1
		mode="finish"
					
threadcopy = Thread(target = makecopy, args = ())
threadinfo = Thread(target = makeinfo, args = ())
threaddelete = Thread(target = makedelete, args = ())
class FileManager(QtGui.QWidget):
	def __init__(self, parent=None):
		global dir
		pathname = (os.path.dirname(sys.argv[0]))
		dir = os.path.abspath(pathname)
		QtGui.QWidget.__init__(self, parent)
		self.List=QtGui.QListWidget()
		self.setGeometry(450,350,480,160)
		self.setFixedSize(480,160)
		grid = QtGui.QGridLayout()
		grid.setSpacing(10)
		self.a=QtGui.QLabel('Privet! kljkl lj kjh ')
		self.pb=QProgressBar()
		self.pb.setValue(100)
		grid.addWidget(self.a,0,0,1,1)
		grid.addWidget(self.List,1,0,3,3)
		grid.addWidget(self.pb,1,0,1,3)
		self.timer=QTimer()
		self.timer.setInterval(100)
		self.timer.start()
		self.timer.timeout.connect(self.sync)
		self.setLayout(grid)		
		self.importlist()
	def sync(self):
		global k,size
		if mode=="info":
			self.a.setText(str(k)+' files counted, Total size: '+str(size/1048576)+' MB')
		elif mode=="copy":
			if state==1:
				self.a.setText(str(k)+' files counted, Total copied: '+str(round(size2/1048576,2))+'/'+str(round(size/1048576,2))+' MB')
			elif state==2:
				self.a.setText(str(k)+' files copied, Total copied: '+str(round(size2/1048576,2))+'/'+str(round(size/1048576,2))+' MB')
			pr=int(100*size2/size)
			if pr>100:
				pr=100
			self.pb.setValue(pr)
			self.setWindowTitle('('+str(pr)+'%) copied')
		elif mode=="delete":
			self.a.setText(str(k)+' files deleted, Total deleted: '+str(size2/1048576)+str(size/1048576)+' MB/')
			pr=int(100*size2/size)
			if pr>100:
				pr=100
			self.pb.setValue(pr)
			self.setWindowTitle('('+str(pr)+'%) removed')
		elif mode=="finish":
			exit(0)
	def importlist(self):
		global baselist,fromdir, todir, mode
		p=QtGui.QApplication.clipboard()
		baselist=p.text(QClipboard.Clipboard).split('|')
		mode = baselist.pop(0)
		if (mode=='info'):
			self.List.setVisible(False)
			self.pb.setVisible(False)
			threadinfo.start()
		elif (mode=='copy'):
			self.List.setVisible(False)
			todir=baselist.pop(0)
			fromdir=baselist.pop(0)
			print('FROM: ',fromdir)
			print('TO: ',todir)
			threadcopy.start()
		elif (mode=='delete'):
			self.List.setVisible(False)
			fromdir=baselist.pop(0)
			threaddelete.start()
ex = FileManager()
ex.show()
app.exec_()
