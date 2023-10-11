import time
import copy


i1 = 1
j1 = 0

class JeuDeLaVie:
  def __init__(self, tableau):
    """
    Affecte un tableau à l'attribut tableau

    Entrée : tableau: list de list
    """
    self.tableau = tableau
    self.symboleVivant = "X"
    self.symboleMort = "-"
    self.preconfs = {
      "spaceship":
      [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
      ]
    }

  def setPreconf(self, nom):
    if nom not in self.preconfs:
      print("Il n'existe aucune préconfiguration avec le nom", nom)
    self.tableau = self.preconfs[nom]

  def afficherPreconfs(self):
    print("Liste des préconfigurations: ")
    for preconf in self.preconfs.keys():
      print("-", preconf)
    return self.preconfs

  def getTableau(self):
    return self.tableau
  
  def setTableau(self, nouveau_tableau):
    self.tableau = nouveau_tableau
    return nouveau_tableau
  
  def setSymboleVivant(self, nouveau_symbole):
    self.symboleVivant = nouveau_symbole
  
  def setSymboleMort(self, nouveau_symbole):
    self.symboleMort = nouveau_symbole


  # def __repr__(self) -> str:
  #   texte = ""
  #   for line in self.tableau:
  #     texte += str(line)
  #     texte += "\n"
  #   return texte
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

  def affiche(self):
    print(self.__repr__())

  def valeur_case(self, i, j):
    """
      Renvoie la valeur de la case [i][j] ou 0 si la case n'existe pas
    """
    if i < 0 or j < 0:
      return 0
    if i >= len(self.tableau) or j >= len(self.tableau[i]):
      return 0
    # print(i, j, self.tableau[i][j])
    # # if len(self.)
    # if(self.tableau[i] and self.tableau[i][j]):
    return self.tableau[i][j]
  
  def total_voisins(self, i, j):
    """
      Renvoie la somme des valeurs des 8 voisins de la case [i][j].
    """
    somme_voisins = 0
    for line in range(i-1, i+2): # On parcourt i-1, i et i+1
      for case in range(j-1, j+2): # On parcourt j-1, j et j+1
        somme_voisins += self.valeur_case(line, case)

    # for line in range(i-1, i+2): # On parcourt i-1, i et i+1
    #   if(len(self.tableau) > line): # On vérifie qu'on est toujours dans le tableau pour éviter un out of range
    #     for case in range(j-1, j+2): # On parcourt j-1, j et j+1
    #       if len(self.tableau[line]) > case: # On vérifie aussi qu'on est pas en out of range
    #         somme_voisins += self.tableau[line][case] # On ajoute à la somme
    somme_voisins -= self.valeur_case(i, j) # On retire la valeur de la case à la somme
 
    return somme_voisins
  
  def resultat(self, valeurcase, totalvoisins):
    """
    Entrée : valeurcase: la valeur de la cellule (0 ou 1))
             totalvoisins: la somme des valeurs des voisins
    Sortie : int, la valeur de la cellule au tour suivant
    Rôle : Renvoie la valeur suivante d'une cellule
    """
    if totalvoisins == 3:
      return 1
    elif totalvoisins == 2:
      return valeurcase
    elif totalvoisins < 2 or totalvoisins > 3:
      return 0
    else:
      print("erreur", totalvoisins)
      return valeurcase
    
    # if valeurcase == 0: # une cellule morte possédant exactement trois voisines vivantes devient vivante: elle naît
    #   if totalvoisins == 3:
    #     return 1
    # elif valeurcase == 1: # une cellule vivante possédant deux ou trois voisines vivantes le reste, sinon elle meurt
    #   if totalvoisins == 2 or totalvoisins == 3: 
    #     return 1
    #   else:
    #     return 0
    # else:
    #   print("La valeur de la case est invalide")
    #   return -1
    # return valeurcase # Sinon, la cellule ne change pas d'état
  
  def tour(self):
    """
      Met à jour toutes les cellules du tableau en respectant les règles du jeu de la vie.
    """
    # On parcourt chaque case du tableau
    nouveautab = copy.deepcopy(self.tableau)
    # nouveautab = []
    
    for ligne in range(len(self.tableau)):
      # nouveautab.append([])
      for case in range(len(self.tableau[ligne])):
        # nouveautab[ligne].append(0)
        valeur = self.valeur_case(ligne, case)
        voisins = self.total_voisins(ligne, case)
        resultat = self.resultat(valeur, voisins)
        nouveautab[ligne][case] = resultat
    if(nouveautab == self.tableau):
      return False
    self.tableau = nouveautab
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
    while continuer == True and tour < nombre_tours:
    # for tour in range(nombre_tours):
      print("Tour", str(tour) + "/" + str(nombre_tours))
      self.affiche()
      continuer = self.tour()
      time.sleep(delai)
      tour += 1
    if continuer == False:
      print("Le tableau ne change plus, arrêt du programme...")
    else:
      print("Fin du programme")

tableau1 = [
  [0, 1, 1, 0],
  [0, 1, 0, 0],
  [1, 1, 1, 0],
  [1, 0, 1, 0],
]

tableau2 =[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

tableau3 =[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

# mon_jeu = JeuDeLaVie([
#   [0, 0, 0],
#   [1, 1, 1],
#   [0, 0, 0]
# ])
# mon_jeu = JeuDeLaVie(tableau3)
# mon_jeu.afficherPreconfs()
# mon_jeu.setPreconf('spaceship')

# mon_jeu = JeuDeLaVie([
#   [0, 0, 1, 0],
#   [1, 0, 0, 1],
#   [0, 0, 1, 0],
#   [1, 1, 0, 0]
# ])
# mon_jeu = JeuDeLaVie([
#   [0, 0, 0, 0],
#   [0, 0, 0, 1],
#   [1, 0, 0, 0],
#   [0, 0, 0, 0]
# ])
mon_jeu.run(600, 0.5)