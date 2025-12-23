import customtkinter as ctk
import cv2
from pathlib import Path
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

#caminhos:
logo_ico_caminho = Path(__file__).parent / "imagens" / "logo.ico"
logo_caminho = Path(__file__).parent / "imagens" / "logo.ico"
video_caminho = Path(__file__).parent / "imagens" / "video.mp4"

def janela_nova():
    def icone():
        nova_janela.iconbitmap(logo_ico_caminho) #Para resolver o problema do icone não aparecer na segunda janela

    janela.withdraw()
    nova_janela = ctk.CTkToplevel(janela)

    global logo_ico_caminho
    nova_janela.title("Projeto de Inteligência Artificial")
    nova_janela.after(200, icone)
    nova_janela.geometry(f"1200x720+{(janela.winfo_screenwidth() - 1200) // 2}+{(janela.winfo_screenheight() - 720) // 2}")
    nova_janela.resizable(False, False)

    texto = ctk.CTkLabel(nova_janela, text= "Video retornado pelo modelo:", font=("Segoe UI", 22, "bold"))
    texto.pack(padx= 20, pady= 20)

    label_Video = ctk.CTkLabel(nova_janela, text="")
    label_Video.pack(padx= 20, pady= 20)

    botao_fechar = ctk.CTkButton(nova_janela, text= "Fechar video", command= nova_janela.destroy, fg_color= "#e1306c", hover_color= "#833ab4")
    botao_fechar.pack(padx= 10, pady= 10)


    def rodar_video():
        ret, frame = video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (960, 540))
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            
            label_Video.imgtk = img
            label_Video.configure(image=img)
            label_Video.after(10, rodar_video)
        else:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)  #Video em loop.
            rodar_video()
    
    rodar_video()

video = cv2.VideoCapture(video_caminho)
if not video.isOpened():
    print("Erro ao abrir video")

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

nome = ctk.CTkLabel(janela, text= "Feito por Vinicius Moretti", font=("Segoe UI", 12, "bold"))
nome.pack(padx= 10, pady= (0, 10))

texto = ctk.CTkLabel(janela, text= "Este projeto foca no desenvolvimento de um modelo customizado utilizando a arquitetura YOLO para a detecção automatizada de armas de fogo em tempo real. O ideia principal por tras deste pequeno projeto é a integração em redes de câmeras de segurança, permitindo uma resposta imediata a ameaças potenciais. Ao unir visão computacional de ponta com segurança pública, a iniciativa busca oferecer uma ferramenta tecnológica eficaz no combate à criminalidade e na preservação da vida.", width= 500, height= 100, wraplength= 450)
texto.pack(padx= 5, pady= (0, 10))

botao = ctk.CTkButton(janela, text= "Visualizar!", command= janela_nova, fg_color= "#e1306c", hover_color= "#833ab4")
botao.pack(padx= 10, pady= 10)

janela.mainloop()