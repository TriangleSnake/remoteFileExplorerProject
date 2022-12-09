import socket
import tkinter as tk
from PIL import ImageTk,Image
import hashlib
HOST="140.116.100.86"
PORT=8080
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
window=tk.Tk()
def init():
    global window
    window.title("Remote File Explorer")
    window.geometry("1920x1080")
    loginWindow()
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
    window.update()
def login(args=0):
    username=usernameEntry.get()
    passwd=passwdEntry.get()
    passwd=hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    result=sendData(username+":"+passwd)
    print(result)
def sendData(string):
    s.send(string.encode())
    return s.recv(1024).decode()
if __name__=="__main__":
    init()