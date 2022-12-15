import socket
import tkinter as tk
from PIL import ImageTk,Image
import hashlib
import time
import os
import pickle
HOST="127.0.0.1"
PORT=8080
last=None
explorerCanvasImage=None
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
window=tk.Tk()
def init():
    global window,explorer,editor
    window.title("Remote File Explorer")
    window.geometry("1920x1080")
    explorer=explorerInterface()
    editor=fileEditor()
    #loginWindow()
    window.mainloop()

def loginWindow():
    global window,loginInterface,canvas,usernameEntry,passwdEntry,loginButtonImage,loginButton
    loginInterface=Image.open("images/loginInterface.png")
    (w,h)=loginInterface.size
    loginInterface=loginInterface.resize((w//5,h//5))
    loginInterface=ImageTk.PhotoImage(loginInterface)
    canvas=tk.Canvas(window,width=1920,height=1080,background="black")
    canvas.create_image(1920/2,1080/2,image=loginInterface)
    entry_x=1920/2-100
    entry_y=1080/2-37
    usernameEntry=tk.Entry(canvas,background="#ED7D31",width=22,fg="white",relief=tk.GROOVE,font=("微軟正黑體",16))
    passwdEntry=tk.Entry(canvas,background="#ED7D31",width=22,fg="white",relief=tk.GROOVE,font=("微軟正黑體",16),show="*")
    usernameEntry.place(x=entry_x,y=entry_y)
    passwdEntry.place(x=entry_x,y=entry_y+45)
    canvas.place(x=0,y=0)
    loginButtonImage=Image.open("images/loginButton.png")
    loginButtonImage=ImageTk.PhotoImage(loginButtonImage)
    loginButton=tk.Button(canvas,image=loginButtonImage,border=0,relief=tk.GROOVE,command=login)
    loginButton.place(x=entry_x-82,y=entry_y+103)
    passwdEntry.bind("<Return>",login)
    window.mainloop()
def changeLoginInterface(filename):
    global loginInterface
    loginInterface=Image.open(f"images/{filename}.png")
    (w,h)=loginInterface.size
    loginInterface=loginInterface.resize((w//5,h//5))
    loginInterface=ImageTk.PhotoImage(loginInterface)
    canvas.create_image(1920/2,1080/2,image=loginInterface)
    window.update()
    time.sleep(3)
    canvas.place_forget()
def login(args=0):
    global s,loginButton
    loginButton.place_forget()
    connectWindow=showConnectionWindow()
    connectWindow.createImage('connecting')
    window.update()
    username=usernameEntry.get()
    passwd=passwdEntry.get()
    passwd=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    try:
        s.connect((HOST,PORT))
        connectWindow.createImage('connected')
        result=sendData(username+":"+passwd)
    except:
        connectWindow.createImage('error')
        result='error'
    connectWindow.destroyWindow()
    if result=="ok":
        changeLoginInterface("loginSuccess")
    else:
        changeLoginInterface("loginFaild")
        loginWindow()
class explorerInterface():
    def __init__(self):
        global explorerImage
        self.explorerCanvas=tk.Canvas(window,width=1920,height=1080)
        explorerImage=ImageTk.PhotoImage(Image.open("images/explorerInterface.png"))
        self.explorerCanvas.create_image(0,0,image=explorerImage,anchor="nw")
        self.explorerCanvas.place(x=0,y=0)
        self.explorerPwd=tk.Text(self.explorerCanvas,background="black",width=55,height=1,fg="white",font=("微軟正黑體",20),bd=0)
        self.explorerPwd.insert(1.0,"./")
        self.explorerPwd.place(x=635,y=65)
        self.explorerPwd.bind("<Return>",self.getDirInfo)
        self.file=[]
        self.getDirInfo()
        window.update()
    def getDirInfo(self,event=None):
        global fileImages,dirImages
        os.chdir(self.explorerPwd.get(1.0,"end").strip('\n'))
        dirImages=[]
        fileImages=[]
        startX,startY=220,260
        margin=100
        self.file=list(os.scandir())
        for i in range(len(self.file[:40])):
            if self.file[i].is_file():
                self.file[i]=file(self.file[i].name)
            elif self.file[i].is_dir():
                self.file[i]=dir(self.file[i])
            self.file[i].place(startX+(i%8)*margin,startY+(i//8)*(margin+20))
    

class fileEditor():
    def __init__(self):
        global fileEditorImage,closeButtonImage,saveButtonImage
        fileEditorImage=Image.open("images/fileEditor.png")
        w,h=fileEditorImage.size
        fileEditorImage=ImageTk.PhotoImage(fileEditorImage.resize((w//3,h//3)))   
        self.intextForm=tk.Text(explorer.explorerCanvas,width=50,height=20,font=("微軟正黑體",12),bg="black",fg="white")
        closeButtonImage=tk.PhotoImage(file="images/closeButton.png")
        saveButtonImage=tk.PhotoImage(file="images/saveButton.png")
        self.closeButton=tk.Label(image=closeButtonImage,bd=0)
        self.saveButton=tk.Label(image=saveButtonImage,border=0)
    def show(self,filename,fileintext):
        global explorerCanvasImage
        self.filename=filename
        self.filenameEditor=tk.Label(explorer.explorerCanvas,text=filename,background="black",font=("微軟正黑體",12),fg="white")
        self.filenameEditor.place(x=1020,y=300,anchor="sw")
        if explorerCanvasImage==None:
            explorerCanvasImage=explorer.explorerCanvas.create_image(1000,300,image=fileEditorImage,anchor="nw")
        self.intextForm.place(x=1025,y=325,anchor="nw")
        self.intextForm.delete(1.0,'end')
        self.intextForm.insert("insert",fileintext)
        self.saveButton.place(x=1522,y=462)
        self.closeButton.place(x=1522,y=360)
        self.closeButton.bind("<Button-1>",self.close)
        self.saveButton.bind("<Button-1>",self.save)
        window.update()
    def close(self,event=None):
        global explorerCanvasImage
        self.filenameEditor.place_forget()
        explorer.explorerCanvas.delete(explorerCanvasImage)
        explorerCanvasImage=None
        self.closeButton.unbind("<Button-1>")
        self.saveButton.unbind("<Button-1>")
        self.intextForm.place_forget()
        self.saveButton.place_forget()
        self.closeButton.place_forget()
    def save(self,event):
        data=[self.filename,self.intextForm.get(1.0,"end")]
        print(data)
        self.close()
class file():
    def __init__(self,filename) -> None:
        global fileImages
        self.filename=filename
        fileImage=Image.open("images/file.png")
        w,h=fileImage.size
        fileImage=ImageTk.PhotoImage(fileImage.resize((w//5,h//5)))
        fileImages.append(fileImage)
        fileImage=fileImages[-1]
        self.label=tk.Label(image=fileImage,background="black")
        self.filenameLabel=tk.Label(text=filename,background="black",fg="white",justify="center",font=("微軟正黑體",12),wraplength=80,width=7)
        self.label.bind("<Button-1>",self.open)
        self.intext="foobarfoobarfoobar\nfoobarfoobarfoobar\nfoobarfoo"
    def open(self,event):
        global last
        if (last!=None):
            last.config(background="black")
        self.label.config(background="gray")
        last=self.label
        editor.show(self.filename,self.intext)
        window.update()
    def place(self,x,y):
        self.label.place(x=x,y=y,anchor="center")
        self.filenameLabel.place(x=x,y=y+40,anchor="n")
        window.update()

class dir():
    def __init__(self,dir) -> None:
        global dirImages
        self.dirname=dir.name
        self.dirpath=dir.path
        dirImage=Image.open("images/directory.png")
        w,h=dirImage.size
        dirImage=ImageTk.PhotoImage(dirImage.resize((w//5,h//5)))
        dirImages.append(dirImage)
        dirImage=dirImages[-1]
        self.label=tk.Label(image=dirImage,background="black")
        self.dirnameLabel=tk.Label(text=self.dirname,background="black",fg="white",justify="center",font=("微軟正黑體",12),wraplength=80,width=7)
        self.label.bind("<Button-1>",self.open)
    def open(self,event):
        explorer.explorerPwd.insert(1.0,self.dirpath)
        explorer.getDirInfo()
    def place(self,x,y):
        self.label.place(x=x,y=y,anchor="center")
        self.dirnameLabel.place(x=x,y=y+40,anchor="n")
        window.update()
class showConnectionWindow():
    def __init__(self) -> None:
        self.connectionWindow=tk.Toplevel()
        self.conW=750//3
        self.conH=500//3
        self.connectionWindow.geometry(f"{self.conW}x{self.conH}+{(1920-self.conW)//2}+{40+(1080-self.conH)//2}")
        self.connectionWindow.overrideredirect(True)
    def createImage(self,filename):
        global connectionImage
        connectionImage=ImageTk.PhotoImage(Image.open(f"images/{filename}.png").resize((self.conW-10,self.conH-10)))
        connectionCanvas=tk.Canvas(self.connectionWindow,width=self.conW,height=self.conH,background="black")
        connectionCanvas.create_image(self.conW//2,self.conH//2,image=connectionImage,anchor='center')
        connectionCanvas.place(x=0,y=0)
        self.connectionWindow.update()
        time.sleep(3)
    def destroyWindow(self):
        self.connectionWindow.destroy()
    
def sendData(string):
    global s
    s.send(string.encode())
    return s.recv(1024).decode()
if __name__=="__main__":
    init()