# SUTOM-Resolver

<p align="center">
  <img src="images/titre.png">
</p>

## Description

SUTOM-Resolver est un script Python pour automatiser la recherche de solution au jeu en ligne SUTOM disponible à l'adresse suivante : https://sutom.nocle.fr
Le code source du jeu est disponible [ici](https://framagit.org/JonathanMM/sutom).

## Démonstration

https://user-images.githubusercontent.com/46728024/156398865-45565a2f-dd76-45d8-b897-d2cb91e25da5.mp4

## Fonctionnement

Le script envoie un premier mot commençant par la lettre donnée par le jeu, et ne contenant que des lettres uniques (pour diminuer au maximum le nombre de possibilités). La réponse du jeu des lettres présentes à la bonne position, des lettres présentes mais à la mauvaise position et les autres (non présentes dans le mot) est analysée par le script qui recherche alors les mots correspondant à ces critères. Sur les essais accordés par le jeu, le script tentera de déterminer un unique mot au final. Le script utilise un dictionnaire des noms communs français pour cela.

## Fonctionnement détaillé

Le script teste le jeu à partir des mots du dictionnaire. Le dictionnaire étant plus exhaustif que celui du jeu, certains mots ne sont pas reconnus par le jeu. Pour pallier ce problème, je script ajoute à un autre fichier dictionnaire les mots non reconnus par le jeu. Le script ne les testera que s'il n'a pas trouvé de mots disponibles parmi le dictionnaire initial. Ainsi on réduit le temps de recherche, sans pour autant se priver des mots qui pourraient éventuellement être rajoutés dans le jeu.
A la fin de l'execution, le script effectue une capture d'écran de la fenêtre du navigateur qu'il a ouvert, sous le nom `screenshot.png`. Il envoie également dans la sortie standard terminal des informations sur l'execution courante.

## Installation

Le script Python utilise `selenium` pour le *scraping* et l'intéraction avec la page web. Il faut donc l'installer de la manière suivante : 

```bash
pip install selenium
```

Enfin, il utilise au choix les drivers Chrome ou Firefox pour afficher la page web et la contrôler. On peut ainsi voir le script en action sur la page.
Pour activer le driver Chrome, il convient de commenter la ligne Firefox et de décommenter celle avec le driver Chrome.

## Execution

```bash
python3 resolver.py
```

## Le JEU

### Règles

![Règles](images/regles.png)

### La grille de jeu

![Grille](images/grille.png)

## Autre script

[Cet autre script](https://github.com/PierreChrd/py-sutom-cheat) fait par [PierreCH](https://github.com/PierreChrd) résoud également le jeu de la même manière.
