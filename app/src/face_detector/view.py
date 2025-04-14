import customtkinter
import tkinter as tk
import cv2
from PIL import Image
from datetime import datetime

class App(customtkinter.CTk):

    def __init__(self, controller, *args, **kargs):
        super().__init__(*args, **kargs)
        self.controller = controller

        self.geometry("640x480")
        self.resizable(False, False)
        self.title("Face Detector App")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)

        self.user_data = None
        self.faces = None

        self.face_detection = False
        self.sign_up = False
        self.is_training = False

        self._create_img_frame()
        self._create_btn_frame()


        self._update_frame()

        
    def _create_btn_frame(self):
        self.btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")

        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)
        self.btn_frame.columnconfigure(3, weight=1)


        def toggle_face_detection():
            self.face_detection = not self.face_detection
        btn1 = customtkinter.CTkButton(self.btn_frame, text="Iniciar", command=toggle_face_detection)
        btn1.grid(row=0, column=0, sticky="nsew", padx=10) 

        btn2 = customtkinter.CTkButton(self.btn_frame, text="Cadastrar", command=self.controller.handle_sign_up)
        btn2.grid(row=0, column=1, sticky="nsew", padx=10)

        btn3 = customtkinter.CTkButton(self.btn_frame, text="Remover")
        btn3.grid(row=0, column=2, sticky="nsew", padx=10) 

        btn4 = customtkinter.CTkButton(self.btn_frame, text="Acessos")
        btn4.grid(row=0, column=3, sticky="nsew", padx=10)

        self.btn_frame.grid(row=1, column=0, sticky="ew", pady=10)
    

    def _create_img_frame(self):     
        self.img_frame = customtkinter.CTkFrame(self, fg_color="black")

        self.cam_src = 0
        self.cap = cv2.VideoCapture(self.cam_src)

        self.label = customtkinter.CTkLabel(master=self.img_frame, text="")
        self.label.pack(expand=True, fill="both")
        
        self.img_frame.grid(row=0, column=0, sticky="nsew")
        
    def set_face_coords(self, faces):
        self.faces = faces

    def _update_frame(self):
        
        if self.is_training:
            self.controller.handle_training()
            self.after(50, self._update_frame) 


        elif self.cap.isOpened():
            ret, frame = self.cap.read()  
            if ret:

                if self.face_detection:
                    self.faces = self.controller.handle_face_detection(frame)
                    for (x,y,w,h) in self.faces: 
                        id, pred = self.controller.handle_face_prediction(frame, (x,y,w,h))
                        color = (0,255,0)
                        text = f"Usuario:{id}"

                        if pred > 60:
                            color = (0,0,255)
                            text = "Desconhecido"

                        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), color)
                        tag = cv2.rectangle(frame, (x,y+h), (x+w,y+h+20), color, -1)
                        cv2.putText(frame, text, (x,y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1, cv2.LINE_AA)
                        #print(f"Usuário:{id}, Pred:{pred}")
                         
                if self.sign_up:
                    self.faces = self.controller.handle_face_detection(frame)
                    for (x,y,w,h) in self.faces:
                        self.controller.handle_sign_up(frame, self.faces)
                        frame = cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0,0), 2)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                self.img = customtkinter.CTkImage(light_image=frame, 
                                                  size=(self.label.winfo_width(), self.label.winfo_height()))
                self.label.configure(image=self.img)

            self.after(30, self._update_frame) 
        else:
            print("Não foi possível abrir a câmera, tentando reconexão")
            self.after(3000, self._retry)


    def _retry(self):
        if self.cap is not None:
            self.cap.release() 
            self.cap = None

        self.cap = cv2.VideoCapture(self.cam_src)

        if self.cap.isOpened():
            print("Câmera reaberta com sucesso")
            self._update_frame()
        else:
            print("Falha na reconexão, tentando novamente...")
            self.after(3000, self._retry)



    def _create_menubar(self):
        self.menubar = tk.Menu(self, tearoff=0)

        self.setup_menu = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Setup", menu=self.setup_menu)
        self.configure(menu=self.menubar)

    def open_sign_up_dialog(self):
        sign_up_dialog = SignUpDialog(self)
        self.wait_window(sign_up_dialog)
        print("Fim do diálogo")
        self.user_data = sign_up_dialog.user_data

class SignUpDialog(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.title("Cadastro de novo usuário")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=200)
        self.columnconfigure(1, minsize=200)


        self.user_data = None

        label1 = customtkinter.CTkLabel(self, text="Nome e Sobrenome:", justify="left", anchor="w")
        label1.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        entry1 = customtkinter.CTkEntry(self, placeholder_text="ex. João Gabriel")
        entry1.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        label2 = customtkinter.CTkLabel(self, text="CPF:", justify="left", anchor="w")
        label2.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

        entry2 = customtkinter.CTkEntry(self, placeholder_text="email@ufpe.br")
        entry2.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        label3 = customtkinter.CTkLabel(self, text="Vencimento do Cadastro:", justify="left", anchor="w")
        label3.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

        entry3 = customtkinter.CTkEntry(self, placeholder_text="DD/MM/YY")
        entry3.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        label4 = customtkinter.CTkLabel(self, text="Tipo", justify="left", anchor="w")
        label4.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        combobox1 = customtkinter.CTkComboBox(self, values=["Aluno", "Professor", "Técnico", "Visitante", "Terceirizado"])
        combobox1.set("Aluno")
        combobox1.grid(row=3, column=1, sticky="ew", padx=10, pady=5)


        (last_column, last_row) = self.grid_size()
         
        def close_dialog():
            self.destroy()
            print("Operação de Cadastro Cancelada!")
        
        btnCancel = customtkinter.CTkButton(self, 
                                            text="Cancelar", 
                                            command=close_dialog, 
                                            fg_color="#343638", 
                                            hover_color="#333333")

        btnCancel.grid(row=last_row, column=0, sticky="ew", padx=10, pady=5) 

        def set_user_data():
            self.user_data = {
                    "id": 0,
                    "name":entry1.get(), 
                    "CPU":entry2.get(), 
                    "valid":datetime.strptime(entry3.get(), "%d/%m/%Y").date(),
                    "type":combobox1.get()
            }
            
            print(self.user_data)

            self.destroy()

        btnConfirm = customtkinter.CTkButton(self, text="Confirmar", command=set_user_data)
        btnConfirm.grid(row=last_row, column=1, sticky="ew", padx=10, pady=5)
        
        self.resizable(False, False)



