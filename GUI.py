import time
import tkinter as tk
from PIL import Image, ImageTk
from JeuDeLaVie import JeuDeLaVie
import os
from threading import Thread
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
    
    self.page_actuelle = []
    
    
    # On créé le titre de la page
    title_label = tk.Label(self, text="Jeu de la Vie", font=("Arial", 20))
    title_label.pack(pady=10)
    self.running_loop = None

    self.delai = DEFAULT_DELAI
    self.tour_count = 0

    # On définit des variables pour certains boutons, pour pouvoir les modifier ensuite
    self.delai_input = None
    self.start_stop_btn = None
    self.info_label = None

    self.page_accueil()
    self.mainloop()

  def empty_page(self):
    """
    Entrées: - self: un objet GUIJeuDeLaVie
    Sortie: - self: un objet GUIJeuDeLaVie
    Rôle: Vider tous les éléments de la page actuelle (sauf le titre)
    """
    for element in self.page_actuelle:
      element.pack_forget() # Supprime l'élément de la page
    if self.canvas != None:
      self.canvas.pack_forget() 
    self.running_loop = False
    self.tour_count = 0

  def page_accueil(self):
    title_choose = tk.Label(self, text="Veuillez choisir une configuration:", font=("Arial", 12))
    title_choose.pack(pady=20)

    # Créer une frame pour les boutons des préconfigurations
    button_frame = tk.Frame(self)
    button_frame.pack(pady=8)

    # Ajouter un bouton pour chaque préconfiguration
    # for conf in range(len(grid_configs // 4))
    nb_rows = len(grid_configs) // 4
    print(nb_rows)
    if(len(grid_configs) % 4 > 0):
      nb_rows += 1
    print(nb_rows)
    print( len(grid_configs) / nb_rows)
    nb_cols = int(len(grid_configs) / nb_rows)
    for row in range(nb_rows):
      line = tk.Frame(self)
      line.pack()
      for el in range(nb_cols):
        print(row, el)
        config = grid_configs[row + el]
        if(os.path.isfile(config["image_path"])): # On vérifie que l'image existe
          image = Image.open(config["image_path"])
          image = image.resize((100, 100))
          photo = ImageTk.PhotoImage(image)
          button = tk.Button(line, image=photo, text=config["name"], compound="top", command=lambda c=config: self.choix_preconf(c))
          button.image = photo
        else:
          button = tk.Button(line, text=config["name"], compound="top", command=lambda c=config: self.choix_preconf(c))
        button.pack(side="left", padx=10)
      self.page_actuelle.append(line)
    # for config in grid_configs:
    #   if(os.path.isfile(config["image_path"])): # On vérifie que l'image existe
    #     image = Image.open(config["image_path"])
    #     image = image.resize((100, 100))
    #     photo = ImageTk.PhotoImage(image)
    #     button = tk.Button(button_frame, image=photo, text=config["name"], compound="top", command=lambda c=config: self.choix_preconf(c))
    #     button.image = photo
    #   else:
    #     button = tk.Button(button_frame, text=config["name"], compound="top", command=lambda c=config: self.choix_preconf(c))
    #   button.pack(side="left", padx=10)
    
    # On ajoute nos éléments à la liste de la page actuelle pour pouvoir les retirer
    self.page_actuelle.append(title_choose)
    self.page_actuelle.append(button_frame)
  
  def cell_clicked(self, event):
    cell = event.widget
    x, y = cell.grid_info()['row'], cell.grid_info()['column']
    tableau = self.jeu.getTableau()
    tableau[x][y] = 1 - tableau[x][y]
    self.jeu.setTableau(tableau)
    if cell['bg'] == 'white':
      cell.configure(bg='black')
    else:
      cell.configure(bg='white')

  def creer_canvas(self):
    self.canvas = tk.Frame(self)
    self.canvas.pack(pady=20, padx=10)
    tableau = self.jeu.getTableau()

    for line in range(len(tableau)):
      for case in range(len(tableau[line])):
        cell = tk.Frame(self.canvas, width=22, height=22, borderwidth=0.5, relief="solid")
        if tableau[line][case] == 0:
          cell.configure(bg="white")
        else:
          cell.configure(bg="black")
        cell.bind("<Button-1>", self.cell_clicked)
        cell.grid(row=line, column=case)

  def mettreajour_canvas(self):
    tableau = self.jeu.getTableau()
    for line in range(len(tableau)):
      for case in range(len(tableau[line])):
        cell = self.canvas.grid_slaves(row = line, column = case)[0]
        # Update the background color of the cell based on the value in the array
        if tableau[line][case] == 0:
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
    self.empty_page()
    home_btn = tk.Button(self, text="Retour", command=self.page_precedante)
    home_btn.pack(padx=10, pady=20)
    self.page_actuelle.append(home_btn)
    self.creer_canvas()

    random_btn = tk.Button(self, text="Aléatoire", command=self.grille_aleatoire)
    random_btn.pack(padx=10, pady=20)
    self.page_actuelle.append(random_btn)

    # Create a frame for the buttons
    info_label = tk.Label(self, text="")
    info_label.pack()
    self.info_label = info_label

    button_frame = tk.Frame(self)
    button_frame.pack()
    start_button = tk.Button(button_frame, text="Start")
    start_button.bind("<Button-1>", self.boutonStartStop)
    start_button.pack(side="left", padx=10, pady=20)
    next_button = tk.Button(button_frame, text="Tour Suivant", command=self.next)
    next_button.pack(side="left", padx=10, pady=20)
    self.start_stop_btn = start_button

    delai_label = tk.Label(button_frame, text="Delai (seconds):")
    delai_label.pack(side="left", padx=10, pady=7)
    delai_input = tk.Spinbox(button_frame, from_=0.1, to=10.0, increment=0.1, format="%.1f", width=10, borderwidth=2, relief="solid")
    delai_input.setvar(str(self.delai))
    delai_input.pack(side="left", padx=10, pady=7)
    # delai_input.bind("<Dec")
    self.delai_input = delai_input

    self.page_actuelle.append(button_frame)
    self.page_actuelle.append(delai_input)
    self.page_actuelle.append(delai_label)
    self.page_actuelle.append(info_label)

  def exec_jeu(self):
    # print(self.delai)
    # print(int(self.delai*1000))
    if self.running_loop == True:
      self.start_stop_btn.config(text="Pause")
      self.canvas.after(int(self.delai*1000), self.exec_jeu)
      self.mettreajour_canvas()
      self.tour_count += 1
      self.info_label.config(text="Tour N°" + str(self.tour_count))
      self.running_loop = self.jeu.tour()
      if(self.running_loop == False):
        self.info_label.config(text="Programme arrêté au tour N°" + str(self.tour_count) + " car la grille était identique")

    if self.running_loop == False:
      self.start_stop_btn.config(text="Démarrer")
    return self.running_loop
    
  def boutonStartStop(self, event):
    # print(self.delai_input.get())
    # print(self.delai_input.get().replace(".", "").isnumeric())
    if self.delai_input.get().replace(".", "").isdigit():
      self.delai = float(self.delai_input.get())
    else: 
      self.delai = self.delai

    self.running_loop = not self.running_loop
    # if self.running_loop == True:
    #   event.widget.config(text="Pause")
      # tour = 0
      # while self.running_loop == True:
      # # for tour in range(nombre_tours):
      #   self.mettreajour_canvas()
      #   self.running_loop = self.jeu.tour()
      #   time.sleep(self.delai)
      #   tour += 1
    # else: 
    #   event.widget.config(text="Démarrer")
    self.exec_jeu()
    # print(self.running_loop)
    # print(self.running_loop)
    pass

  def next(self):
    self.jeu.tour()
    self.mettreajour_canvas()

  def page_precedante(self):
    self.empty_page()
    self.page_accueil()

  def grille_aleatoire(self):
    self.jeu.grille_aleatoire()
    self.mettreajour_canvas()
    self.tour_count = 0

  # def isnombre =



GUIJeuDeLaVie()