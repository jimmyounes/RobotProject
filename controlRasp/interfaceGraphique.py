import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time 
from MQTTController import publishMessageOnTopic
class App:
    def __init__(self, window, window_title, video_source=0):
        window.geometry("800x600")
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
        self.btn_snapshot.place(x=320, y=300)
     
        # Ajout des boutons de télécommande
        self.btn_up1 = tk.Button(window, text="↑")
        self.btn_down1 = tk.Button(window, text="↓")
        self.btn_left1 = tk.Button(window, text="←")
        self.btn_right1 = tk.Button(window, text="→")
        
        self.btn_up2 = tk.Button(window, text="↑")
        self.btn_down2 = tk.Button(window, text="↓")
        self.btn_left2 = tk.Button(window, text="←")
        self.btn_right2 = tk.Button(window, text="→")
        
        #Commande pour detecter press and release buttons 
        self.btn_up1.bind("<Button-1>", lambda event :self.btn_up1_pressed("UP"))
        self.btn_up1.bind("<ButtonRelease-1>",lambda event :self.btn_up1_pressed("STOP"))

        self.btn_down1.bind("<Button-1>", lambda event :self.btn_up1_pressed("DOWN"))
        self.btn_down1.bind("<ButtonRelease-1>",lambda event :self.btn_up1_pressed("STOP"))

        self.btn_left1.bind("<Button-1>",lambda event : self.btn_up1_pressed("LEFT"))
        self.btn_left1.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOP"))


        self.btn_right1.bind("<Button-1>",lambda event :self.btn_up1_pressed("RIGHT"))
        self.btn_right1.bind("<ButtonRelease-1>",lambda event : self.btn_up1_pressed("STOP"))
    

        

        # Positionnement des boutons de télécommande
        self.btn_up1.pack(side=tk.TOP, padx=10)
        self.btn_up1.place(x=100, y=350)
        self.btn_left1.pack(side=tk.LEFT,padx=10)
        self.btn_left1.place(x=20,y=420)
        self.btn_right1.pack(side=tk.RIGHT,padx=10)
        self.btn_right1.place(x=180,y=420)
        self.btn_down1.pack(side=tk.BOTTOM, padx=10)
        self.btn_down1.place(x=100,y=490)

        self.btn_up2.pack(side=tk.RIGHT, padx=20)
        self.btn_up2.place(x=620, y=350)
        self.btn_left2.pack(side=tk.RIGHT)
        self.btn_left2.place(x=540, y=420)
        self.btn_right2.pack(side=tk.RIGHT)
        self.btn_right2.place(x=700, y=420)
        self.btn_down2.pack(side=tk.RIGHT, padx=20)
        self.btn_down2.place(x=620, y=490)
        
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