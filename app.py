import customtkinter as ctk
from PIL import Image, ImageTk
import connection
from tkinter import messagebox
import cv2
import tkinter as tk
import os
from dotenv import load_dotenv
import base64
from io import BytesIO
import face_recognition

load_dotenv()
data_base_key = [os.getenv("host"),os.getenv("data_base_name"),os.getenv("user"),os.getenv("password"),os.getenv("port")]

def preguntar_si_no() -> bool:
    respuesta = messagebox.askyesno('Ventana de confirmacion','Este es el propietario correcto?')
    return respuesta
def conectar(conector: object) -> object:
    conector = connection.base_de_datos (data_base_key[0], 
                                data_base_key[1], 
                                data_base_key[2],
                                data_base_key[3],
                                data_base_key[4])
    return conector

base_datos = object
base_datos = conectar(base_datos)
base_datos.create_table()

class Ventana_de_propietarios(ctk.CTkToplevel):
    def __init__(self, variable_de_operacion: str, cedula_anterior: int, foto :str, cara: str, *args, **kwargs):
        super().__init__()
        self.title('Inserte los datos del propietario')
        self.geometry("720x480")
        self.configure(fg_color = ("#1C1B55","#02013A"))
        self.iconbitmap('apppics/logo.ico')
        self.columnconfigure((0,1), weight = 1, uniform = 'a')
        self.rowconfigure((0,1,2,3,4,5), weight = 1, uniform = 'a')
        self.name = ctk.CTkLabel(self, text = 'Nombre: ', text_color = '#07042E')
        self.last_name =  ctk.CTkLabel(self, text = 'Apellido: ', text_color = '#07042E')
        self.id = ctk.CTkLabel(self, text = 'Cedula: ', text_color = '#07042E')
        self.building = ctk.CTkLabel(self, text = 'Edificio: ', text_color = '#07042E')
        self.apartment = ctk.CTkLabel(self, text = 'Apartamento: ', text_color = '#07042E')
        self.name.grid(row = 0, column = 0)
        self.last_name.grid(row = 1, column = 0)
        self.id.grid(row = 2, column = 0)
        self.building.grid(row = 3, column = 0)
        self.apartment.grid(row = 4, column = 0)
        self.name_value = ctk.CTkEntry(self)
        self.last_name_value = ctk.CTkEntry(self)
        self.id_value = ctk.CTkEntry(self)
        self.building_value = ctk.CTkEntry(self)
        self.apartment_value = ctk.CTkEntry(self)
        self.name_value.grid(row = 0, column = 1)
        self.last_name_value.grid(row = 1, column = 1)
        self.id_value.grid(row = 2, column = 1)
        self.building_value.grid(row = 3, column = 1)
        self.apartment_value.grid(row = 4, column = 1)
        self.button = ctk.CTkButton(self, text="confirmar", command = lambda: self.update_data_base(variable_de_operacion, base_datos, cedula_anterior, foto, cara))
        self.button.grid(row = 5, column = 0, columnspan = 2)
    def update_data_base(self, variable_de_operacion: str, base_datos: object, cedula_anterior: int, foto: str, cara: str):
        if variable_de_operacion == 'agregar':
         base_datos = conectar(base_datos)
         base_datos.agregar_usuario(self.name_value.get(), self.last_name_value.get(), int(self.id_value.get()), int(self.building_value.get()), self.apartment_value.get(), foto, cara)
         self.destroy()
        else:
         base_datos = conectar(base_datos)
         base_datos.editar_usuario(self.name_value.get(), self.last_name_value.get(), int(self.id_value.get()), int(cedula_anterior), int(self.building_value.get()), self.apartment_value.get())
         self.destroy()
         
class ventana_de_camara(ctk.CTkToplevel):
    def __init__(self, cedula, **kwargs):
        super().__init__()
        self.title('Datos del propietario')
        self.geometry("480x480")
        self.configure(fg_color = ("#ffffff","#07042E"))
        self.iconbitmap('apppics/logo.ico')
        self.form = formulario_de_propietario(self)
        self.form.place(relx = 0.5,
                        rely = 0.5,
                        relwidth = 1,
                        relheight = 1,
                        anchor = 'center')
        self.form.encontrar_propietario(base_datos,cedula)
        
  
class root(ctk.CTk):
    def __init__(self, size = tuple, fg_color = ("#FFFFFF","#07042E"), **kwards):
        super().__init__()
        self.title('')
        self.configure(fg_color = ("#FFFFFF","#07042E")) 
        self.geometry(f'{size[0]}x{size[1]}')
        self.iconbitmap('apppics/logo.ico')
        self.overrideredirect(False)   
        self.theme_pics = ctk.CTkImage(light_image=Image.open('apppics/sun.ico'),
                                       dark_image=Image.open('apppics/moon.ico'))
        self.theme_button = ctk.CTkButton(self,width=0.1,
                                          height=0.2,text='',
                                          image=self.theme_pics,
                                          compound='left',
                                          fg_color=("#ffffff","#07042E"),
                                          hover_color=("#ffffff","#07042E"),
                                          command = self.cambiar_tema)
        self.theme_button.place(relx = 1,
                                rely = 0, 
                                relwidth = 0.05, 
                                relheight = 0.05, 
                                anchor ='ne')
        self.welcome_image = ctk.CTkImage(light_image = Image.open('apppics/logo_entrada.png'),
                                          dark_image = Image.open('apppics/logo_entrada(1).png'),
                                          size = (200,200))
        self.welcome_logo = ctk.CTkButton(self,
                                          text = '',
                                          hover_color = ('#ffffff','#07042E'), 
                                          corner_radius = 20,
                                          image = self.welcome_image,
                                          compound = 'left',
                                          fg_color = 'transparent')
        self.welcome_message = ctk.CTkLabel(self, text = 'URBANIZACIÓN LA SABANA', 
                                            text_color = ("#4239B8",'#ffffff'), font = ('Arial Black', 32))
        self.welcome_description = ctk.CTkLabel(self, text = 'Sistema de entrada por reconocimiento facial',
                                                text_color = ("#4239B8",'#ffffff'), font = ('Times New Roman', 20))
        self.welcome_description.place(relx = 0.6,
                                       rely = 0.65,
                                       anchor = 'center')
        self.welcome_message.place(relx = 0.6,
                                   rely = 0.55,
                                   anchor = 'center')
        self.welcome_logo.place(relx = 0.6,
                                rely = 0.3,
                                relwidth = 0.3,
                                relheight = 0.3,
                                anchor = 'center')
        self.left_frame = left_side(self)
        self.right_frame = bienvenida(self)
        self.toplevel_window = None
        self.mainloop()     
    def cambiar_tema(self):
        if ctk.get_appearance_mode() == 'Light' :
            self.iconbitmap('apppics/logo(1).ico')
            ctk.set_appearance_mode('Dark')
        else:
            self.iconbitmap('apppics/logo.ico')
            ctk.set_appearance_mode('Light')    
class left_side(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = 1 , border_width = None, bg_color = "transparent", fg_color = ("#4239B8","#000000"), border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.place(relx = 0,
                  rely = 0,
                  relwidth = 0.18,
                  relheight = 1,
                  anchor = 'nw')
        self.welcome_image = ctk.CTkImage(light_image = Image.open('apppics/logo_entrada.png'),
                                          dark_image = Image.open('apppics/logo_entrada(1).png'),
                                          size = (60,60))
        self.welcome_logo = ctk.CTkButton(self,
                                          text = '',
                                          hover_color = ('#ffffff','#07042E'), 
                                          corner_radius = 20,
                                          image = self.welcome_image,
                                          compound = 'left',
                                          fg_color = ('#ffffff',"#000000"))
        self.rowconfigure(1,weight = 2)
        self.rowconfigure((0,2,3), weight = 1, uniform = 'a')
        self.rowconfigure(4, weight = 8)
        self.columnconfigure(0, weight= 1)
        self.titulo = ctk.CTkLabel(self,
                                   bg_color= 'transparent', 
                                   padx = 20, 
                                   pady = 20, 
                                   text = 'Sistema de entrada\n Urb. La Sabana \n(Guarenas-Guatire)',
                                   anchor='center',
                                   text_color = ("#FFFFFF","#ffffff"))
        self.id_button = ctk.CTkButton(self,
                                        fg_color = 'transparent',
                                        text = 'Buscar propietario por cédula',
                                        text_color = ("#FFFFFF","#ffffff"),
                                        hover_color = ("#07042f","#423988"),
                                        corner_radius = 20,
                                        command = lambda : self.cambiar_frame(master,1)
                                        )
        self.face_button = ctk.CTkButton(self,
                                        fg_color = 'transparent',
                                        text = 'Reconocimiento facial',
                                        text_color = ("#FFFFFF","#FFFFFF"),
                                        hover_color = ("#07042f","#423988"),
                                        corner_radius = 20,
                                        command = lambda : self.cambiar_frame(master,2))
        self.welcome_logo.grid(row = 0)
        self.titulo.grid(row = 1, sticky = 'nsew')
        self.id_button.grid(row = 2)
        self.face_button.grid(row = 3)
    def cambiar_frame(self, master, frame: int) -> None:
        if frame == 1:
            self.face_button.configure(fg_color = 'transparent', state = 'normal')
            self.id_button.configure(fg_color = ("#2978e6","#07042E"), state = 'disabled')
            self.master.right_frame.place_forget()
            self.master.right_frame = busqueda_por_cedula(master)
        else:
            self.id_button.configure(fg_color = 'transparent', state = 'normal')
            self.face_button.configure(fg_color = ("#2978e6","#07042E"), state = 'disabled')
            self.master.right_frame.place_forget()
            self.master.right_frame = reconocimiento_facial(master)
            
        
class bienvenida(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = ("#ffffff","#07042E"), border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
class busqueda_por_cedula(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = ("#ffffff","#07042E"), border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.place(relx = 0.2,
                   rely = 0.05,
                   relwidth = 0.8,
                   relheight = 1,
                   anchor = 'nw')
        self.entry = ctk.CTkEntry(self,
                                fg_color = ("#9E9BD1","#0B1231"),
                                border_color = ("#000000",'#ffffff'))
        self.entry_text = ctk.CTkLabel(self,
                                       text = 'Ingrese la cédula del propietario: ',
                                       font = ('Times New Roman', 12))
        self.entry_text.place(relx = 0.05,
                         rely = 0)
        self.form = formulario_de_propietario(self)
        self.form.place(relx = 0.5,
                        rely = 0.4,
                        relwidth = 0.5,
                        relheight = 0.6,
                        anchor = 'center')
        self.entry.place(relx = 0.22,
                         rely = 0)
        self.form.columnconfigure(0, weight = 2)
        self.form.columnconfigure(1, weight= 1)
        self.form.columnconfigure(2, weight = 1)
        self.form.rowconfigure((0,1,2,3,4), weight = 1, uniform = 'a' )
        self.form.encontrar_propietario(base_datos, 27941647)
        self.button = ctk.CTkButton(self, text="Encontrar un propietario", 
                                    fg_color = ("#4239B8","#000000"),
                                    text_color = ("#FFFFFF","#ffffff"),
                                    hover_color = ("#07042f","#423988"),
                                    corner_radius = 20,
                                    command = lambda: self.form.encontrar_propietario(base_datos, int(self.entry.get())))
        self.button.place(relx = 0.15,
                          rely = 0.8)
        self.button2 = ctk.CTkButton(self, text="Borrar información de un propietario", 
                                    fg_color = ("#4239B8","#000000"),
                                    text_color = ("#FFFFFF","#ffffff"),
                                    hover_color = ("#07042f","#423988"),
                                    corner_radius = 20,
                                    command = lambda: self.form.borrar_propietario(master, base_datos, int(self.entry.get())))
        self.button2.place(relx = 0.4,
                           rely = 0.8)
        self.button3 = ctk.CTkButton(self, text="Editar información de un propietario", 
                                    fg_color = ("#4239B8","#000000"),
                                    text_color = ("#FFFFFF","#ffffff"),
                                    hover_color = ("#07042f","#423988"),
                                    corner_radius = 20,
                                    command = lambda: self.form.editar_propietario(master,base_datos, int(self.entry.get()), 'editar'))
        self.button3.place(relx = 0.7,
                          rely = 0.8)

class formulario_de_propietario(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = 2, bg_color = "transparent", fg_color = ("#4239B8","#0B1231"), border_color = ('#07042E',"#FFFFFF"), background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.name = ctk.CTkLabel(self, text = 'Nombre: ', text_color = ("#FFFFFF",'#ffffff'), font = ('Times New Roman', 12))
        self.last_name =  ctk.CTkLabel(self, text = 'Apellido: ', text_color = ("#FFFFFF",'#ffffff'), font = ('Times New Roman', 12))
        self.id = ctk.CTkLabel(self, text = 'Cedula: ', text_color = ("#FFFFFF",'#ffffff'), font = ('Times New Roman', 12))
        self.building = ctk.CTkLabel(self, text = 'Edificio', text_color = ("#FFFFFF",'#ffffff'), font = ('Helvetica', 24))
        self.apartment = ctk.CTkLabel(self, text = 'Apartamento', text_color = ("#FFFFFF",'#ffffff'), font = ('Helvetica', 24))
        self.photo = tk.Label(self)
        self.rowconfigure((4,5),weight=3)
        self.rowconfigure((1,2,3),weight=1)
        self.photo.grid(row = 0, column = 0, padx=5,pady=5, rowspan=3)
        self.name.grid(row = 0, column = 1)
        self.last_name.grid(row = 1, column = 1)
        self.id.grid(row = 2, column = 1)
        self.building.grid(row = 4 , column = 0)
        self.apartment.grid(row = 4, column = 1)
        self.name_value = ctk.CTkLabel(self, text_color = ("#FFFFFF","#ffffff"), font = ('Times New Roman', 12))
        self.last_name_value = ctk.CTkLabel(self, text_color = ("#FFFFFF","#ffffff"), font = ('Times New Roman', 12))
        self.id_value = ctk.CTkLabel(self, text_color = ("#FFFFFF","#ffffff"), font = ('Times New Roman', 12))
        self.building_value = ctk.CTkLabel(self, text_color = ("#FFFFFF","#ffffff"), font = ('Helvetica', 32))
        self.apartment_value = ctk.CTkLabel(self, text_color = ("#FFFFFF","#ffffff"), font = ('Helvetica', 32))
        self.name_value.grid(row = 0, column = 2)
        self.last_name_value.grid(row = 1, column = 2)
        self.id_value.grid(row = 2, column = 2)
        self.building_value.grid(row = 5, column = 0)
        self.apartment_value.grid(row = 5, column = 1)
    def encontrar_propietario(self,base_datos: object, cedula: int) -> None:
        base_datos = conectar(base_datos)
        form = base_datos.buscar_usuario(cedula)
        self.rellenar_forma(form)
    def rellenar_forma(self,list : list) -> None:
        self.name_value.configure(text = list[1])
        self.last_name_value.configure(text = list[2])
        self.id_value.configure( text = list[3])
        self.building_value.configure( text = list[4])
        self.apartment_value.configure(text = list[5])    
        photo_bytes = list[7]
        image_data = base64.b64decode(photo_bytes[1:-1])
        pil = Image.open(BytesIO(image_data))
        pil = pil.resize((180,180))
        img = ImageTk.PhotoImage(pil)
        self.photo.configure(image=img)
        self.photo.Image = img
    def borrar_propietario(self, master: object, base_datos: object,cedula: int) -> None:
        base_datos = conectar(base_datos)
        form = base_datos.buscar_usuario(cedula)
        if preguntar_si_no():
            base_datos = conectar(base_datos)
            base_datos.borrar_usuario(cedula)
        else:
            pass  
        self.rellenar_forma(form)
    def editar_propietario(self, master: object, base_datos: object, cedula: int, variable_de_operacion: str) -> None:
        base_datos = conectar(base_datos)
        form = base_datos.buscar_usuario(cedula)
        self.rellenar_forma(form)
        if preguntar_si_no():
            if master.toplevel_window is None or not master.toplevel_window.winfo_exists():
                master.toplevel_window = Ventana_de_propietarios(variable_de_operacion, cedula, None, None)  
            else:
                master.toplevel_window.focus() 
        else:
            pass                             
        
class reconocimiento_facial(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = ("#ffffff","#07042E"), border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.place(relx = 0.2,
                   rely = 0.05,
                   relwidth = 0.8,
                   relheight = 1,
                   anchor = 'nw')
        self.camera_on = cv2.VideoCapture(0)
        self.canvas = ctk.CTkCanvas(self)
        self.label = tk.Label(self.canvas, text = '')
        self.stoping = False
        self.frame = self.camera_on
        self.grid_rowconfigure((0,1,2,3,4,5), weight = 1)
        self.grid_columnconfigure((0,1,2,3), weight = 1)
        self.canvas.grid(row = 0, column = 1, columnspan = 2, rowspan = 2, sticky = "nsew", ipadx = 20)
        self.label.place(relx = 0,
                         rely = 0,
                         anchor = 'nw')        
        self.button = ctk.CTkButton(self, text = 'Encender Camara',
                                    fg_color = ("#4239B8","#000000"),
                                    text_color = ("#FFFFFF","#ffffff"),
                                    hover_color = ("#07042f","#423988"),
                                    corner_radius = 20,
                                    command = lambda: self.turn_on_camera())
        self.button.grid(row = 2, column = 1)
        self.button2 = ctk.CTkButton(self, text = 'Detener la Camara', 
                                    fg_color = ("#4239B8","#000000"),
                                    text_color = ("#FFFFFF","#ffffff"),
                                    hover_color = ("#07042f","#423988"),
                                    corner_radius = 20,
                                    command = lambda: self.turn_off_camera())
        self.button2.grid(row = 2, column = 2)
        self.button3 = ctk.CTkButton(self, text = 'Buscar Propietario en la base de datos',
                                     fg_color = ("#4239B8","#000000"),
                                    text_color = ("#FFFFFF","#ffffff"),
                                    hover_color = ("#07042f","#423988"),
                                    corner_radius = 20,
                                    command = lambda: self.compare(master, base_datos))
        self.button3.grid(row = 3, column = 1, ipadx = 5)
        self.button4 = ctk.CTkButton(self, text="Agregar usuario a la base de datos",
                                    fg_color = ("#4239B8","#000000"),
                                    text_color = ("#FDFDFD","#ffffff"),
                                    hover_color = ("#07042f","#423988"),
                                    corner_radius = 20,
                                    command = lambda: self.crear_propietario(master, 'agregar'))
        self.button4.grid(row = 3, column = 2, ipadx = 5)
        self.button5 = ctk.CTkButton(self, text="Editar la Foto de un Propietario",
                                    fg_color = ("#4239B8","#000000"),
                                    text_color = ("#FFFFFF","#ffffff"),
                                    hover_color = ("#07042f","#423988"),
                                    corner_radius = 20,
                                    command = lambda: self.editar_foto(master, base_datos))
        self.button5.grid(row = 4, column = 1)
        self.cedula_label = ctk.CTkEntry(self,
                                fg_color = ("#9E9BD1","#0B1231"),
                                border_color = ("#000000",'#ffffff'))
        self.cedula_label.grid(row = 4, column = 2)
    def crear_propietario(self, master: object, variable_de_operacion: str) -> None:
        cv2.imwrite('apppics/last_photo.png',self.frame)
        im = cv2.imread('apppics/last_photo.png')
        rgb_img = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
        rgb_img = cv2.resize(rgb_img,(480,480))
        with open("apppics/last_photo.png", "rb") as f:
            photo_bytes = base64.b64encode(f.read())
        img_encodings = face_recognition.face_encodings(rgb_img)[0]
        array_bytes = str(img_encodings.tolist())
        if master.toplevel_window is None or not master.toplevel_window.winfo_exists():
            master.toplevel_window = Ventana_de_propietarios(variable_de_operacion, 0, array_bytes, str(photo_bytes))  
        else:
            master.toplevel_window.focus()     
    def editar_foto(self, master: object, base_datos: object):
        cv2.imwrite('apppics/last_photo.png',self.frame)
        with open("apppics/last_photo.png", "rb") as f:
            photo_bytes = base64.b64encode(f.read())
        ventana_de_camara(self.cedula_label.get())
        if preguntar_si_no():
            base_datos = conectar(base_datos)
            base_datos.editar_photo(self.cedula_label.get(),photo_bytes)    
        
    def turn_on_camera(self) -> None:
        camera_on,self.frame = self.camera_on.read()
        if camera_on and not self.stoping:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = cv2.resize(self.frame,(480,480))
            im = Image.fromarray(self.frame)
            img = ImageTk.PhotoImage(image=im)
            
            self.label.configure(image=img)
            self.label.Image = img
            self.label.after(800, self.turn_on_camera)
        elif self.stoping:
            self.stoping = False
    def turn_off_camera(self) -> None:
        self.stoping = True
    def compare(self, master, base_datos: object) -> None:
        try:
            cv2.imwrite('apppics/last_photo.png',self.frame)
            im = cv2.imread('apppics/last_photo.png')
            rgb_img = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
            rgb_img = cv2.resize(rgb_img,(480,480))
            img_encodings = face_recognition.face_encodings(rgb_img)[0]
            array_bytes = str(img_encodings.tolist())
            base_datos = conectar(base_datos)
            tuple = base_datos.comparar_caras(array_bytes)
            if len(tuple) > 1:
                if master.toplevel_window is None or not master.toplevel_window.winfo_exists():
                    master.toplevel_window = ventana_de_camara(tuple[0])  
                else:
                    master.toplevel_window.focus()     
            else:
                print(tuple[0])
        except:
            pass
root((1280,720))  