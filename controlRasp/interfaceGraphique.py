import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time 
from MQTTController import publishMessageOnTopic
class App:
    def __init__(self, window, window_title, video_source=0):
        window.geometry("1000x600")
        self.window = window
        self.window.title(window_title)
        
               # Capture de la vidéo à partir de la source vidéo
        self.vid = MyVideoCapture(video_source)
        
        # Création d'un canvas pour afficher la vidéo
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height/2)
        self.canvas.pack()
        
        # Boutons pour contrôler la vidéo
        self.btn_snapshot=tk.Button(window, text="Snapshot", width=20, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)
        self.btn_snapshot.place(x=400, y=250)
     
        # Ajout des boutons de télécommande
        self.btn_up1 = tk.Button(window, text="↑")
        self.btn_down1 = tk.Button(window, text="↓")
        self.btn_left1 = tk.Button(window, text="←")
        self.btn_right1 = tk.Button(window, text="→")
        
        self.btn_up2 = tk.Button(window, text="forward")
        self.btn_down2 = tk.Button(window, text="backward")
        
        self.btn_up3 = tk.Button(window, text="↑")
        self.btn_down3 = tk.Button(window, text="↓")

        self.btn_up4 = tk.Button(window, text="↑")
        self.btn_down4 = tk.Button(window, text="↓")
        
        self.btn_up5 = tk.Button(window, text="↑")
        self.btn_down5 = tk.Button(window, text="↓")

        self.btn_up6 = tk.Button(window, text="↑")
        self.btn_down6 = tk.Button(window, text="↓")
        
        self.tir = tk.Button(window, text="TIR")

        #Commande pour detecter press and release buttons 
        self.btn_up1.bind("<Button-1>", lambda event :self.btn_up1_pressed("UP"))
        self.btn_up1.bind("<ButtonRelease-1>",lambda event :self.btn_up1_pressed("STOP"))

        self.btn_down1.bind("<Button-1>", lambda event :self.btn_up1_pressed("DOWN"))
        self.btn_down1.bind("<ButtonRelease-1>",lambda event :self.btn_up1_pressed("STOP"))

        self.btn_left1.bind("<Button-1>",lambda event : self.btn_up1_pressed("LEFT"))
        self.btn_left1.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOP"))


        self.btn_right1.bind("<Button-1>",lambda event :self.btn_up1_pressed("RIGHT"))
        self.btn_right1.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOP"))
    
        self.btn_up3.bind("<Button-1>",lambda event :self.btn_up1_pressed("CHANNEL12UP"))
        self.btn_down3.bind("<Button-1>",lambda event :self.btn_up1_pressed("CHANNEL12DOWN"))
        self.btn_up4.bind("<Button-1>",lambda event :self.btn_up1_pressed("CHANNEL13UP"))
        self.btn_down4.bind("<Button-1>",lambda event :self.btn_up1_pressed("CHANNEL13DOWN"))
        self.btn_up5.bind("<Button-1>",lambda event :self.btn_up1_pressed("CHANNEL14UP"))
        self.btn_down5.bind("<Button-1>",lambda event :self.btn_up1_pressed("CHANNEL14DOWN"))
        self.btn_up6.bind("<Button-1>",lambda event :self.btn_up1_pressed("CHANNEL15UP"))
        self.btn_down6.bind("<Button-1>",lambda event :self.btn_up1_pressed("CHANNEL15DOWN"))
        
        self.tir.bind("<Button-1>",lambda event :self.btn_up1_pressed("TIR"))
        self.tir.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))

        self.btn_up3.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))
        self.btn_down3.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))
        self.btn_up4.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))
        self.btn_down4.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))
        self.btn_up5.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))
        self.btn_down5.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))
        self.btn_up6.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))
        self.btn_down6.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOPPED"))


        self.my_label = tk.Label(window, text="Hello, World!")
        self.my_label.pack(padx=500, pady=500)
        # Positionnement des boutons de télécommande
        self.btn_up1.pack(side=tk.TOP, padx=10)
        self.btn_up1.place(x=100, y=350)
        self.btn_left1.pack(side=tk.LEFT,padx=10)
        self.btn_left1.place(x=20,y=420)
        self.btn_right1.pack(side=tk.RIGHT,padx=10)
        self.btn_right1.place(x=180,y=420)
        self.btn_down1.pack(side=tk.BOTTOM, padx=10)
        self.btn_down1.place(x=100,y=490)
         
        self.tir.place(x=450, y=300)

        self.btn_up2.pack(side=tk.RIGHT, padx=20)
        self.btn_up2.place(x=250, y=350)
       
        self.btn_up3 .place(x=450, y=350)
        self.btn_down3.place(x=450, y=450)
        self.btn_up4.place(x=650, y=350)
        self.btn_down4.place(x=650, y=450)
        self.btn_up5.place(x=800, y=350)
        self.btn_down5.place(x=800, y=450)
        self.btn_up6.place(x=900, y=350)
        self.btn_down6.place(x=900, y=450)

        self.btn_down2.pack(side=tk.RIGHT, padx=20)
        self.btn_down2.place(x=250, y=490)
        # Boucle d'exécution de la fenêtre
        self.delay = 15
        self.update()
        self.window.mainloop()

    
    def snapshot(self):
        # Sauvegarde d'une image du flux vidéo
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Mise à jour de la vidéo
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        
        self.window.after(self.delay, self.update)
    
    def btn_up1_pressed(self,message):
        # Call your publishMessageOnTopic function here
        publishMessageOnTopic(message,"Walt/mouvement")
           


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Ouverture de la capture vidéo
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Impossible d'ouvrir la source vidéo", video_source)
        
        # Obtention de la taille de la vidéo
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Retourne un frame RGB
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Fermeture de la capture vidéo
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Démarre l'application
App(tk.Tk(), "Interface de contrôle du robot avec stream vidéo")