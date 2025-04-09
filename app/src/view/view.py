import customtkinter
import cv2
from PIL import Image

class ImgFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kargs):
        super().__init__(master, **kargs)

class BtnFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kargs):
        super().__init__(master, **kargs)

        #self.rowconfigure(0, weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        #l_sep = customtkinter.CTkFrame(self)
        #l_sep.grid(row=0, column=0)

        btn1 = customtkinter.CTkButton(self, text="Botão 1", command= (lambda x: print("Você apertou o Botão 1")))
        btn1.grid(row=0, column=0, sticky="nsew", padx=10) 

        btn2 = customtkinter.CTkButton(self, text="Botão 2", command= (lambda x: print("Você apertou o Botão 2")))
        btn2.grid(row=0, column=1, sticky="nsew", padx=10)

        btn3 = customtkinter.CTkButton(self, text="Botão 3", command= (lambda x: print("Você apertou o Botão 3")))
        btn3.grid(row=0, column=2, sticky="nsew", padx=10) 

        btn4 = customtkinter.CTkButton(self, text="Botão 4", command= (lambda x: print("Você apertou o Botão 4")))
        btn4.grid(row=0, column=3, sticky="nsew", padx=10)

        #r_sep = customtkinter.CTkFrame(self)
        #r_sep.grid(row=0, column=5)

class App(customtkinter.CTk):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        #self.geometry("640x480")
        self.title("Face Detector App")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)

        self.img_frame = ImgFrame(master=self, fg_color="black")
        self.img_frame.grid(row=0, column=0, sticky="nsew")

        self.btn_frame = BtnFrame(master=self, fg_color="transparent", height=50)
        self.btn_frame.grid(row=1, column=0, sticky="ew", pady=10)

        self.geometry("800x600")
