# Demineur
![image](https://github.com/user-attachments/assets/0da7102f-52a4-4451-93a2-15395b024395)


## Description
Ce projet est une implémentation en Python 3 du jeu Démineur. Le but du jeu est de dévoiler toutes les cases vides d'une grille tout en évitant les mines. Le joueur perd s'il dévoile une case contenant une mine.

## Auteur
- **Prénom** : Jawad
- **Nom** : Cherkaoui
- **Matricule** : 576517

## Fonctionnalités
- Création d'un plateau de jeu de taille variable.
- Placement aléatoire des mines.
- Dévoilement des cases adjacentes sans mines.
- Gestion des drapeaux pour marquer les mines suspectées.
- Vérification des conditions de victoire et de défaite.

## Prérequis
- Python 3.10 ou supérieur

## Installation
Clonez le dépôt et accédez au répertoire du projet :
```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_REPERTOIRE>
```

## Utilisation
Pour lancer le jeu, exécutez la commande suivante en remplaçant `<n>`, `<m>` et `<number_of_mines>` par les dimensions du plateau et le nombre de mines souhaité :
```bash
python demineur.py <n> <m> <number_of_mines>
```

## Règles du jeu
- Le jeu se joue sur une grille de taille `n` x `m`.
- Le joueur doit dévoiler les cases sans mines.
- Le joueur peut marquer les cases suspectées de contenir des mines avec des drapeaux (`f x y`).
- Le joueur gagne en dévoilant toutes les cases sans mines ou en plaçant des drapeaux sur toutes les mines.
- Le joueur perd s'il dévoile une case contenant une mine.

## Exemple de commande
```bash
python demineur.py 10 10 20
```

## Notes
- Ce fichier Python contient du code ANSI pour les couleurs, il peut donc être source de problème sous certains OS.
- Il doit être exécuté sous Python 3.10 sous peine de ne pas fonctionner correctement.
