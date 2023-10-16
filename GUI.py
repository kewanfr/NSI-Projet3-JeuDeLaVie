import tkinter as tk
from PIL import Image, ImageTk
from JeuDeLaVie import JeuDeLaVie
import os
# from threading import Thread
from config import grid_configs

DEFAULT_DELAI = 0.3

class GUIJeuDeLaVie(tk.Tk):
  def __init__(self):
    """
    Entrées:
      - self: un objet GUIJeuDeLaVie
      - jeu: un objet de la classe JeuDeLaVie
    Sorties: self: un objet GUIJeuDeLaVie
    Rôle : Initilise l'interface graphique du Jeu de la Vie avec Tkinter
    """
    self.jeu = JeuDeLaVie() # On instancie une classe du Jeu de la Vie

    # On définit notre fenettre
    super().__init__()
    self.title("Jeu de la Vie")
    self.resizable(0,0)
    self.canvas = None # Le canvas où l'on va créer notre grille
    
    self.page_actuelle = [] # Liste des éléments de notre page, pour pouvoir les supprimer en changeant de page
    
    
    # On créé le titre de la page
    title_label = tk.Label(self, text="Jeu de la Vie", font=("Arial", 20))
    title_label.pack()


    self.delai = DEFAULT_DELAI
    self.tour_count = 0
    self.running_loop = None # Variable si le programme est lancé

    # On définit des variables pour certains boutons, pour pouvoir les modifier ensuite
    self.delai_input = None
    self.start_stop_btn = None
    self.info_label = None

    # On affiche la page d'accueil et on lance le GUI
    self.page_accueil()
    self.mainloop()

  def empty_page(self):
    """
    Entrées: - self: un objet GUIJeuDeLaVie
    Sortie: - self: un objet GUIJeuDeLaVie
    Rôle: Vider tous les éléments de la page actuelle (sauf le titre)
    """
    for element in self.page_actuelle:
      element.pack_forget() # Supprime chaque élément de la page actuelle
    if self.canvas != None: # Si le tableau existe, on le supprime
      self.canvas.pack_forget() 
    self.running_loop = False # On arrête la boucle pour éviter des bugs
    self.tour_count = 0 # On reset aussi le compteur

  def page_accueil(self):
    """
    Rôle: Afficher la page d'accueil (choix de la conf)
    """

    title_choose = tk.Label(self, text="Veuillez choisir une configuration:", font=("Arial", 12))
    title_choose.pack(pady=12)

    # Créer une frame pour les boutons des préconfigurations
    button_frame = tk.Frame(self)
    button_frame.pack(pady=8)

    # Ajouter un bouton pour chaque préconfiguration
    for i, element in enumerate(grid_configs):
      if i % 3 == 0: # On crée une nouvelle ligne tous les 3 boutons pour avoir 3 boutons par ligne
        line = tk.Frame(button_frame)
        line.pack()
      config = element
      if(os.path.isfile(config["image_path"])): # On vérifie que l'image existe
        image = Image.open(config["image_path"]) # On ouvre l'image et on la redimensionne
        image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(image)
        button = tk.Button(line, image=photo, text=config["name"], compound="top", command=lambda c=config: self.choix_preconf(c))
        button.image = photo
        # On créé un bouton avec notre image
      else:
        # Ou sans si on ne l'a pas
        button = tk.Button(line, text=config["name"], compound="top", command=lambda c=config: self.choix_preconf(c))
      
      button.pack(side="left", padx=10) # On ajoute le bouton au GUI
      self.page_actuelle.append(line)

    # On ajoute nos éléments à la liste de la page actuelle pour pouvoir les retirer
    self.page_actuelle.append(title_choose)
    self.page_actuelle.append(button_frame)
  
  def cell_clicked(self, event):
    """
    Entrées: - self: un objet GUIJeuDeLaVie
             - event: un event tkinter
    Sortie: - self: un objet GUIJeuDeLaVie
    Rôle: Fonction exécutée lors du clic sur une cellule du tableau, inverse sa couleur et sa valeur
    """
    cell = event.widget
    x, y = cell.grid_info()['row'], cell.grid_info()['column'] # On récupère ses coordonnées

    tableau = self.jeu.getTableau() # On recupère le tableau
    tableau[x][y] = 1 - tableau[x][y] # On inverse sa valeur
    self.jeu.setTableau(tableau) # On met à jour le tableau

    if cell['bg'] == 'white': # On inverse sa couleur
      cell.configure(bg='black')
    else:
      cell.configure(bg='white')

  def creer_canvas(self):
    """
    Rôle: Créer la "grille" de notre jeu avec les cellules
    """
    self.canvas = tk.Frame(self)
    self.canvas.pack(pady=16, padx=3)
    tableau = self.jeu.getTableau()

    for line in range(len(tableau)): # On parcourt chaque case
      for case in range(len(tableau[line])):
        cell = tk.Frame(self.canvas, width=15, height=15, borderwidth=0.5, relief="solid") # On créé une case avec une bordure et une taille de 15
        if tableau[line][case] == 0: # Définit la couleur
          cell.configure(bg="white")
        else:
          cell.configure(bg="black")
        cell.bind("<Button-1>", self.cell_clicked) # L'évènement lorsqu'on clique sur le case
        cell.grid(row=line, column=case)

  def mettreajour_canvas(self):
    """
    Rôle: Mettre à jour le canvas avec les nouvelles valeurs du tableau
    """
    tableau = self.jeu.getTableau()
    for line in range(len(tableau)):
      for case in range(len(tableau[line])):
        cell = self.canvas.grid_slaves(row = line, column = case)[0] # On récupère la case
        
        if tableau[line][case] == 0: # On def sa couleur
          cell.configure(bg="white")
        else:
          cell.configure(bg="black")
  
  def choix_preconf(self, preconf):
    """
    Fonction exécutée lors du clic sur un bouton d'une préconfiguration
    """
    self.jeu.setTableau(preconf["grid"]) # On change notre grille de jeu avec notre configuration
    self.second_page() # On affiche la seconde page
  
  def second_page(self):
    """
    Rôle: Afficher la seconde page (grille et page du jeu)
    """
    self.empty_page() # Vide la page

    # Bouton pour retourner sur la page d'accueil
    home_btn = tk.Button(self, text="Retour", command=self.page_precedante)
    home_btn.pack(padx=4, pady=8)
    self.page_actuelle.append(home_btn)

    self.creer_canvas()

    # Bouton pour générer une grille aléatoire
    random_btn = tk.Button(self, text="Aléatoire", command=self.grille_aleatoire)
    random_btn.pack()
    self.page_actuelle.append(random_btn)

    # Texte pour le nombre de tours
    info_label = tk.Label(self, text="")
    info_label.pack(padx=1)
    self.info_label = info_label
    self.page_actuelle.append(info_label)

    button_frame = tk.Frame(self)
    button_frame.pack()
    start_button = tk.Button(button_frame, text="Start")
    start_button.bind("<Button-1>", self.boutonStartStop) # Event lorsque bouton start cliqué: fonction boutonStartStop
    start_button.pack(side="left", padx=8, pady=5)

    # Passer au tour suivant
    next_button = tk.Button(button_frame, text="Tour Suivant", command=self.next)
    next_button.pack(side="left", padx=10, pady=5)
    self.start_stop_btn = start_button

    self.page_actuelle.append(button_frame)


    delai_label = tk.Label(button_frame, text="Delai (seconds):")
    delai_label.pack(side="left", padx=8, pady=5)
    self.page_actuelle.append(delai_label)

    # Input pour changer le délai
    delai_input = tk.Spinbox(button_frame, from_=0.1, to=10.0, increment=0.1, format="%.1f", width=10, borderwidth=2, relief="solid")
    delai_input.setvar(str(self.delai))
    delai_input.pack(side="left", padx=8, pady=5)
    self.delai_input = delai_input
    self.page_actuelle.append(delai_input)


  def exec_jeu(self):
    """
    Rôle: Executer le jeu (chaque tour de boucle)
    Cette boucle s'auto execute tant que la variable self.running_loop est True
    """
    if self.running_loop == True: # Si la boucle est lancé
      self.start_stop_btn.config(text="Pause") # On change le texte du bouton

      self.canvas.after(int(self.delai*1000), self.exec_jeu) # Méthode de tkinter pour être exécutée après chaque tour de la boucle mainloop (évite de bloquer le GUI) avec un délai

      self.mettreajour_canvas() # On met à jour le canvas
      self.tour_count += 1
      self.info_label.config(text="Tour N°" + str(self.tour_count))

      self.running_loop = self.jeu.tour() # On effectue un tour

      if(self.running_loop == False):
        self.info_label.config(text="Programme arrêté au tour N°" + str(self.tour_count) + " car la grille était identique")

    if self.running_loop == False:
      self.start_stop_btn.config(text="Démarrer")
    return self.running_loop
    
  def boutonStartStop(self, event):
    """
    Rôle:
      - Démarrer la boucle si elle n'est pas lancée
      - Arrêter la boucle si elle est lancée
    """
    if self.delai_input.get().replace(".", "").isdigit():
      self.delai = float(self.delai_input.get())
    else: 
      self.delai = self.delai

    self.running_loop = not self.running_loop # On inverse la valeur de la variable
  
    self.exec_jeu()
    pass

  def next(self):
    """
    Rôle: Passer au tour suivant
    """
    self.jeu.tour()
    self.mettreajour_canvas()

  def page_precedante(self):
    """
    Rôle: Retourner à la page précédente (page d'accueil)
    """
    self.empty_page()
    self.page_accueil()

  def grille_aleatoire(self):
    """
    Rôle: Générer une grille aléatoire et mettre à jour la grille
    """
    self.jeu.grille_aleatoire()
    self.mettreajour_canvas()
    self.tour_count = 0

GUIJeuDeLaVie()