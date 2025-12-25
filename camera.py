import customtkinter as ctk
import cv2
import webbrowser
import sys
from pathlib import Path
from PIL import Image, ImageTk
from ultralytics import YOLO

ctk.set_appearance_mode("light")

'''
Caminhos:
'''
logo_ico_caminho = Path(__file__).parent / "complementos" / "logo.ico"
logo_caminho = Path(__file__).parent / "complementos" / "logo.ico"
video_caminho = Path(__file__).parent / "complementos" / "video.mp4"
modelo_caminho = Path(__file__).parent / "complementos" / "modelo_customizado.pt"
modelo = YOLO(modelo_caminho)

def abrir_linkedin(event=None):
    webbrowser.open("https://www.linkedin.com/in/morettivns/")

def fechar():
    sys.exit() #Quando eu fechava pelo "X" a janela secundária o programa seguia rodando em segundo plano, acrescentei isso apenas para resolver esse problema.

def icone(nova_janela):
    nova_janela.iconbitmap(logo_ico_caminho) #Resolve o bug do ícone nas janelas secundárias.

def voltar(janela_atual, janela_anterior): #Fecha o video ou a câmera e volta para a janela anterior.
    global video, camera, rodando
    if video is not None:
        video.release()
        video = None

    rodando = False
    if camera is not None:
        camera.release()
        camera = None

    janela_atual.destroy()
    janela_anterior.deiconify()

'''
Janela do video:
'''
def janela_video():

    janela.withdraw()
    nova_janela = ctk.CTkToplevel(janela)
    
    nova_janela.title("Projeto de Inteligência Artificial - Video")
    nova_janela.after(200, lambda: icone(nova_janela))
    nova_janela.geometry(f"1200x720+{(janela.winfo_screenwidth() - 1200) // 2}+{(janela.winfo_screenheight() - 720) // 2}")
    nova_janela.resizable(False, False)

    texto = ctk.CTkLabel(nova_janela, text= "Video retornado pelo modelo:", font=("Segoe UI", 22, "bold"))
    texto.pack(padx= 20, pady= 20)

    label_Video = ctk.CTkLabel(nova_janela, text="")
    label_Video.pack(padx= 20, pady= 20)

    botao_fechar = ctk.CTkButton(nova_janela, text= "Fechar video", command= lambda: voltar(nova_janela, janela), fg_color= "#e1306c", hover_color= "#833ab4")
    botao_fechar.pack(padx= 10, pady= 10)

    nova_janela.protocol("WM_DELETE_WINDOW", fechar)
    rodar_video(label_Video)

def rodar_video(label_Video):
    global video

    if video is None:
        video = cv2.VideoCapture(video_caminho)
    
    ret, frame = video.read()
    if ret: #Se o frame foi lido corretamente:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Converte o frame para RGB.
        frame = cv2.resize(frame, (960, 540))          #Muda seu tamanho para 960, 540.

        img_Tk = ImageTk.PhotoImage(Image.fromarray(frame))  #Transforma a imagem em um padrão aceito pelo CustomTK.
        label_Video.imgtk = img_Tk                           #Atualiza o video label com a imagem mais recente.
        label_Video.configure(image=img_Tk)

        label_Video.after(15, lambda: rodar_video(label_Video)) #Loop.
    else:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        rodar_video(label_Video)

'''
Janela da câmera:
'''
def janela_camera():

    janela.withdraw()
    nova_janela = ctk.CTkToplevel(janela)

    nova_janela.title("Projeto de Inteligência Artificial - Câmera")
    nova_janela.after(200, lambda: icone(nova_janela))
    nova_janela.geometry(f"1200x720+{(janela.winfo_screenwidth() - 1200) // 2}+{(janela.winfo_screenheight() - 720) // 2}")
    nova_janela.resizable(False, False)

    frame_topo = ctk.CTkFrame(nova_janela, fg_color="transparent")
    frame_topo.pack(fill="x", pady=(20,0))
    texto = ctk.CTkLabel(frame_topo, text= "Câmera ao vivo utilizando o modelo:", font=("Segoe UI", 22, "bold"))
    texto.pack()

    frame_meio = ctk.CTkFrame(nova_janela, fg_color= "transparent")
    frame_meio.pack(fill="x", expand=True, padx=10, pady=10)
    label_Camera = ctk.CTkLabel(frame_meio, text="")
    label_Camera.pack()

    frame_baixo = ctk.CTkFrame(nova_janela, fg_color="transparent")
    frame_baixo.pack(fill="x", pady=(0, 40))
    botao_fechar = ctk.CTkButton(frame_baixo, text= "Fechar câmera", command= lambda: voltar(nova_janela, janela), fg_color= "#e1306c", hover_color= "#833ab4")
    botao_fechar.pack()
    
    nova_janela.protocol("WM_DELETE_WINDOW", fechar)
    iniciar_camera(label_Camera)

def iniciar_camera(label_camera):
    global camera, rodando

    camera = cv2.VideoCapture(0) #(0) é a câmera principal.

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 854) #Dimensões.
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    rodando = True
    rodar_camera(label_camera)

def rodar_camera(label_Camera):
    global camera, rodando

    if not rodando:
        return
    
    ret, frame = camera.read()
    if not ret:
        return
    
    results = modelo(frame, conf = 0.60)
    frame = results[0].plot() #Pega os frames da câmera e aplica no modelo YOLO.

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Transforma o frame retornado pelo modelo em padrão RGB.
    imagem = Image.fromarray(frame)
    img_Tk = ImageTk.PhotoImage(imagem)

    label_Camera.configure(image= img_Tk) #Atualiza o camera label com a imagem mais recente.
    label_Camera.image = img_Tk #Consistência.
    label_Camera.after(5, lambda: rodar_camera(label_Camera)) #Repete tudo isso a cada 5 milissegundos.

'''
Função principal
'''
video = None
camera = None
rodando = False

janela = ctk.CTk()
janela.geometry(f"500x400+{(janela.winfo_screenwidth() - 500) // 2}+{(janela.winfo_screenheight() - 400) // 2}")
janela.title("Projeto Vinicius Moretti")
janela.iconbitmap(logo_ico_caminho)
janela.resizable(False, False)

logo = ctk.CTkImage(light_image= Image.open(logo_caminho), dark_image= Image.open(logo_caminho), size= (100,100))
logo_Label = ctk.CTkLabel(janela, text="", image= logo)
logo_Label.pack(padx= 10, pady= 10)

titulo = ctk.CTkLabel(janela, text= "Projeto de Inteligência Artificial", font=("Segoe UI", 22, "bold"))
titulo.pack(padx= 10, pady= (10, 1))

frame_credito = ctk.CTkFrame(janela, fg_color= "transparent")
frame_credito.pack(padx= 10, pady= (0, 10))
feito = ctk.CTkLabel(frame_credito, text= "Feito por ", font=("Segoe UI", 12, "bold"))
feito.pack(side= "left")
nome = ctk.CTkLabel(frame_credito, text= "Vinicius Moretti", font=("Segoe UI", 12, "bold", "underline"), text_color= "#e1306c", cursor = "hand2")
nome.pack(side= "right")
nome.bind("<Button-1>", abrir_linkedin)

texto = ctk.CTkLabel(janela, text= "Este projeto foca no desenvolvimento de um modelo customizado utilizando a arquitetura YOLO para a detecção automatizada de armas de fogo em tempo real. O ideia principal por tras deste pequeno projeto é a integração em redes de câmeras de segurança, permitindo uma resposta imediata a ameaças potenciais. Ao unir visão computacional de ponta com segurança pública, a iniciativa busca oferecer uma ferramenta tecnológica eficaz no combate à criminalidade e na preservação da vida.", width= 500, height= 100, wraplength= 450)
texto.pack(padx= 5, pady= (0, 10))

frame_dos_botoes = ctk.CTkFrame(janela, fg_color= "transparent")
frame_dos_botoes.pack(pady= 10)

botao1 = ctk.CTkButton(frame_dos_botoes, text= "Video", command= janela_video, fg_color= "#e1306c", hover_color= "#833ab4")
botao1.grid(row= 0, column= 0,padx= 10)

botao2 = ctk.CTkButton(frame_dos_botoes, text= "Câmera", command= janela_camera, fg_color= "#e1306c", hover_color= "#833ab4")
botao2.grid(row= 0, column= 1,padx= 10)

janela.mainloop()