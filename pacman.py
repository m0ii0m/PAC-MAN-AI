import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################


# Plan du labyrinthe


class Map:
    Wall      = 1
    GhostHome = 2
    Gum       = 4
    PacGum    = 5
    Empty     = 6
    



# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,5,4,4,4,1,4,4,4,4,4,4,4,4,1,4,4,4,5,1],
        [1,4,1,1,4,1,4,1,1,1,1,1,1,4,1,4,1,1,4,1],
        [1,4,1,4,4,4,4,4,4,4,4,4,4,4,4,4,4,1,4,1],
        [1,4,1,4,1,1,4,1,1,2,2,1,1,4,1,1,4,1,4,1],
        [1,4,4,4,4,4,4,1,2,2,2,2,1,4,4,4,4,4,4,1],
        [1,4,1,4,1,1,4,1,1,1,1,1,1,4,1,1,4,1,4,1],
        [1,4,1,4,4,4,4,4,4,4,4,4,4,4,4,4,4,1,4,1],
        [1,4,1,1,4,1,4,1,1,1,1,1,1,4,1,4,1,1,4,1],
        [1,5,4,4,4,1,4,4,4,4,4,4,4,4,1,4,4,4,5,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ])
# attention, on utilise TBL[x][y], considérez que le (0,0) est en bas à gauche


HAUTEUR = TBL.shape [1]
LARGEUR = TBL.shape [0]


G = 1000
M = 100
# tableau de poids pour les cases
poids = np.zeros_like(TBL)
for x in range(LARGEUR):
   for y in range(HAUTEUR):
      if TBL[x][y] == Map.Wall:
         poids[x][y] = G
      elif TBL[x][y] == Map.PacGum:
         continue
      else:
         poids[x][y] = M



PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange"] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   ]     )         



### Debug
debugInfo = {}

def SetInfo(id,x,y,info):
   debugInfo[(id,x,y)] = str(info)


## Paramètre affichage

ZOOM   = 40   # taille d'une case en pixels
EPAISS = 8    # epaisseur des murs bleus en pixels

 
####################################################
#
#   Partie II :  Création de la Fenêtre Tkinter
#  
#   ne pas toucher
#
####################################################


screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
 
####################################################
#
#   Partie III :  Fonctions  d'affichage
#
####################################################


# convertit coord grille =
def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == Map.Wall and TBL[x+1][y] == Map.Wall ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == Map.Wall and TBL[x][y+1] == Map.Wall ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == Map.Gum or TBL[x][y] == Map.PacGum):
            xx = To(x) 
            yy = To(y)
            e = 5
            if  TBL[x][y] == Map.PacGum : e = 8
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (1,x,y) in debugInfo:
            xx = To(x) 
            yy = To(y) - 11
            txt = debugInfo[(1,x,y)]
            canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if (2,x,y) in debugInfo:
            xx = To(x) + 10
            yy = To(y) 
            txt = debugInfo[(2,x,y)]
            canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
    
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

score = 0

def IncreaseScoreIfGum(x,y):
   global score
   global poids

   if(TBL[x][y] == Map.PacGum):
      score += 100
      poids[x][y] = M
   elif(TBL[x][y] == Map.Gum):
      score += 10

def Bellman_Ford():
   global poids

   for _ in range(LARGEUR * HAUTEUR - 1):
      anyChange = False
      for x in range(poids.shape[0]):
         for y in range(poids.shape[1]):
            if TBL[x][y] == Map.Wall:
               continue
            for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
               if poids[x+dx][y+dy] < poids[x][y]:
                     anyChange = True
                     poids[x][y] = poids[x+dx][y+dy] + 1
      if anyChange is False:
        break

def CanGo(x,y):
   return TBL[x,y] == Map.Gum or TBL[x,y] == Map.PacGum or TBL[x,y] == Map.Empty
   
def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if CanGo(x,y-1)    : L.append(( 0,-1))
   if CanGo(x,y+1)    : L.append(( 0, 1))
   if CanGo(x+1,y)    : L.append(( 1, 0))
   if CanGo(x-1,y)    : L.append((-1, 0))
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] == Map.GhostHome ): L.append((0,-1))
   if ( TBL[x  ][y+1] == Map.GhostHome ): L.append((0, 1))
   if ( TBL[x+1][y  ] == Map.GhostHome ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == Map.GhostHome ): L.append((-1,0))
   return L
   
def IAPacman():
   global PacManPos, Ghosts
   #deplacement Pacman
   L = PacManPossibleMove()
   choix = 0
   for i in range(1,len(L)):
      if poids[PacManPos[0]+L[i][0]][PacManPos[1]+L[i][1]] < poids[PacManPos[0]+L[choix][0]][PacManPos[1]+L[choix][1]]:
         choix = i
   PacManPos[0] += L[choix][0]
   PacManPos[1] += L[choix][1]
   IncreaseScoreIfGum(PacManPos[0],PacManPos[1])
   TBL[PacManPos[0]][PacManPos[1]] = Map.Empty
   
   # affichage des poids
   for x in range(poids.shape[0]):
      for y in range(poids.shape[1]):
         SetInfo(1,x,y,poids[x][y])
   
 
   
def IAGhosts():
   #deplacement Fantome
   for F in Ghosts:
      L = GhostsPossibleMove(F[0],F[1])
      choix = random.randrange(len(L))
      F[0] += L[choix][0]
      F[1] += L[choix][1]
      
  
 

 
#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
   global iteration

   if not PAUSE_FLAG : 
      Bellman_Ford()
      iteration += 1
      if iteration % 2 == 0 :   IAPacman()
      else:                     IAGhosts()
   
   Affiche(PacmanColor = "yellow", message = score)  
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()

 
   
   
    
   
   