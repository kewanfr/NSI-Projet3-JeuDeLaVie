import time
import copy
import random
from config import grid_configs, TableauVide30

class JeuDeLaVie:
  def __init__(self, tableau = []):
    """
    Entrée : self, tableau: list de list
    Sortie : self
    Role: Instancie un objet JeuDeLaVie, initialise le tableau et les symboles par défaut

    """
    # On initialise le tableau et les symboles par défaut
    self.tableau = tableau
    self.symboleVivant = "X"
    self.symboleMort = "-"

  def __repr__(self) -> str:
    texte = ""
    for line in self.tableau:
      for e in line:
        if e == 1:
          texte += " " + self.symboleVivant + " "
        else:
          texte += " " + self.symboleMort + " "
      texte += "\n"
    return texte

  def affichage_simple(self) -> str:
    texte = ""
    for line in self.tableau:
      texte += str(line)
      texte += "\n"
    return texte

  def affiche(self):
    print(self.__repr__())

  def setPreconf(self, id):
    """
    Entrées: self, id: int, l'identifiant de la préconfiguration
    Sortie: rien ou False si l'identifiant n'existe pas
    Rôle: Définir la grille du jeu à partir d'une préconfiguration
    """
    if id >= len(grid_configs) or id < 0:
      print("Il n'existe aucune préconfiguration numéro", id, ". Utilisation de la configuration par défaut")
      return False
    print("Préconfiguration définie sur", grid_configs[id]["name"])
    self.tableau = grid_configs[id]["grid"]

  def afficherPreconfs(self):
    """
    Entrées: self
    Sortie: Affichage
    Rôle: Afficher la liste des préconfigurations
    """
    print("Liste des préconfigurations: ")
    for i, preconf in enumerate(grid_configs):
      print(i, "-", preconf["name"])
    return grid_configs

  def getPreconfs(self):
    """
    Entrées: self
    Sortie: grid_configs
    Rôle: Renvoyer le tableau de la liste des préconfigurations
    """
    return grid_configs

  def getTableau(self):
    """
    Entrées: self
    Sortie: self.tableau
    Rôle: Renvoyer la grille de jeu
    """
    return self.tableau
  
  def setTableau(self, nouveau_tableau):
    """
    Entrées: self, nouveau_tableau: list de list, la nouvelle grille de jeu
    Sortie: self.tableau
    Rôle: Change la grille de jeu par une nouvelle
    """
    self.tableau = nouveau_tableau
    return nouveau_tableau

  def choixSymbole(self):
    """
    Entrées: self
    Sortie: self.symboleVivant, self.symboleMort
    Rôle: Deamnde à l'utilisateur de choisir les symboles pour les cellules vivantes et mortes
    """
    choix = input("Symbole d'une cellule vivante (Défaut: X): ")
    if choix != "":
      self.symboleVivant = choix
    choix = input("Symbole d'une cellule morte (Défaut: -): ")
    if choix != "":
      self.symboleMort = choix

  def valeur_case(self, i, j):
    """
    Entrée : i, j: int, les coordonnées de la case
    Sortie : int, la valeur de la case
    Rôle : Renvoie la valeur de la case [i][j] ou 0 si la case n'existe pas
    """
    if i < 0 or j < 0:
      return 0
    if i >= len(self.tableau) or j >= len(self.tableau[i]): # Si la case n'existe pas, on renvoie 0
      return 0
    return self.tableau[i][j] # Sinon on renvoie la valeur de la case
  
  def total_voisins(self, i, j):
    """
    Entrée : i, j: int, les coordonnées de la case
    Sortie : int, la somme des valeurs des voisins
    Rôle : Renvoie la somme des valeurs des 8 voisins de la case [i][j].
    """
    somme_voisins = 0
    for line in range(i-1, i+2): # On parcourt i-1, i et i+1
      for case in range(j-1, j+2): # On parcourt j-1, j et j+1
        somme_voisins += self.valeur_case(line, case) # On ajoute la valeur de la case à la somme des voisins

    somme_voisins -= self.valeur_case(i, j) # On retire la valeur de la case à la somme
 
    return somme_voisins
  
  def resultat(self, valeurcase, totalvoisins):
    """
    Entrée : valeurcase: la valeur de la cellule (0 ou 1))
             totalvoisins: la somme des valeurs des voisins
    Sortie : int, la valeur de la cellule au tour suivant
    Rôle : Renvoie la valeur suivante d'une cellule
    """
    # Si une cellule à 3 voisins, elle devient vivante
    # Si elle a 2 voisins, ça ne change pas
    # Si elle a moins de 2 ou plus de 3, elle meurt
    if totalvoisins == 3:
      return 1
    elif totalvoisins == 2:
      return valeurcase
    elif totalvoisins < 2 or totalvoisins > 3:
      return 0

  def tour(self):
    """
    Entrée : self
    Sortie : bool, True si le tableau a changé, False sinon
    Rôle : Met à jour toutes les cellules du tableau en respectant les règles du jeu de la vie.
    """
    nouveautab = copy.deepcopy(self.tableau) # On copie le tableau pour pas modifier le tableau actuel
    
    for ligne in range(len(self.tableau)): # On parcourt chaque case du tableau
      for case in range(len(self.tableau[ligne])):
        valeur = self.valeur_case(ligne, case) # On récupère la valeur actuelle de la case
        voisins = self.total_voisins(ligne, case) # On récupère les valeurs de voisins
        resultat = self.resultat(valeur, voisins) # On calcule la prochaine valeur à donner à la case
        nouveautab[ligne][case] = resultat # On modifie la case dans le tableau
    if(nouveautab == self.tableau):
      return False # Si le tableau n'a pas changé on arrête le programme
    self.tableau = nouveautab # On mets à jour le tableau
    return True                   

  def run(self, nombre_tours, delai):
    """
    Méthode principale du jeu.
    Entrée : nombre_tours: int, nombre de tours à effectuer
             delai : int, temps d'attente entre chaque tour
    Rôle : Fait tourner le jeu de la vie pendant nombre_tours.
      Elle rafraichit l'affichage à chaque tour
      et attend delai entre chaque tour.
    """
    continuer = True
    tour = 0
    while continuer == True and tour < nombre_tours: # On continue tant que le tableau change et que le nombre de tours n'est pas atteint
      print("Tour", str(tour) + "/" + str(nombre_tours))
      self.affiche() # On affiche le tableau
      continuer = self.tour() # On fait un tour, la variable continuer vaut False si le tableau a changé, True sinon
      time.sleep(delai) # On attend delai secondes
      tour += 1 # On incrémente le nombre de tours
    if continuer == False: # Si le tableau n'a pas changé, on arrête le programme
      print("Le tableau ne change plus, arrêt du programme...")
    else:
      print("Fin du programme")

  def grille_aleatoire(self):
    """
    Entrée : self
    Sortie : self.tableau
    Rôle : Remplit le tableau avec des 0 et des 1 aléatoirement
    """
    for ligne in range(len(self.tableau)): # On parcourt chaque case du tableau
      for case in range(len(self.tableau[ligne])):
        self.tableau[ligne][case] = random.randint(0, 1) # On met un 0 ou un 1 aléatoirement avec la méthode randint

if __name__ == "__main__": # Cette condition n'est pas exécutée si le fichier est importé
  print("-------------------- Jeu de la Vie --------------------\n")

  mon_jeu = JeuDeLaVie(TableauVide30)
  mon_jeu.choixSymbole()

  aleatoire = input("Voulez-vous générer une grille aléatoire ? (y/N)")

  if aleatoire == "Y" or aleatoire == "y":
    mon_jeu.grille_aleatoire()

  else:
    print("Veuillez choisir une préconfiguration:")
    mon_jeu.afficherPreconfs()

    preconf = input("\nPréconfiguration (N°): ")
    if not preconf.isdigit():
      print("Vous n'avez pas entré un nombre, utilisation de la configuration par défaut")
      preconf = len(grid_configs) - 1
    else:
      preconf = int(preconf)

    mon_jeu.setPreconf(preconf)

  nombre_tours = int(input("\nNombre de tours: "))
  
  delai = float(input("\nDélai entre chaque tour: "))

  print("Lancement du jeu de la vie", "pour", nombre_tours, "tours avec un délai de", delai, "secondes entre chaque tour...")
  
  mon_jeu.run(nombre_tours, delai)
  print("\n-------------------- Jeu de la Vie --------------------")