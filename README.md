# SUTOM-Resolver

<p align="center">
  <img src="https://user-images.githubusercontent.com/46728024/156399063-d08efd64-d631-4153-9899-0fe9f5f3f9b1.png">
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

# Configuration générale

```py
############# VARIABLE TO MODIFY ###############

headless = True # True pour activer le mode headless, False sinon
discord = True # True pour activer la sortie sur webhook discord (spécifier l'url), False sinon
windows = False # True si vous exécutez le script en environnement Windows (sert aux path des drivers), False sinon
webhook = "add your webhook url here" # L'url de votre webhook discord

############################
```
## Discord

Le mode discord vous permet d'avoir le résultat de l'exécution du script, directement dans un channel discord via les *webhook*. [De l'aide est disponile pour la configuration d'un webhook ici](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks). 

![Screenshot_1](https://user-images.githubusercontent.com/46728024/157642082-a55506f6-3790-428e-8e1e-977fbab74396.png)

## Mode Headless

Le mode headless n'affiche pas le nabigateur, mais uniquement la sortie standard. On peut alors s'éviter l'affichage inutile. On peut ainsi lancer le script sur un serveur sans GUI autre qu'un terminal. 

## Automatisation

Pour automatiser l'exécution du script, il faut activer le mode *headless*, et je vous recommande d'activer le mode Discord également, de sorte que vous aurez les sorties du script sur votre channel discord configuré. Une simple tâche planifiée ou *cron* fera l'affaire.

## Le JEU

### Règles

![regles](https://user-images.githubusercontent.com/46728024/156399043-dad9f73c-17df-464a-9b0e-60ac7a4635ae.png)

### La grille de jeu

<p align="center">
  <img src="https://user-images.githubusercontent.com/46728024/156399027-d10001c6-96e4-4b71-9ee8-ef3f4dac902c.png">
</p>


## Autre script

[Cet autre script](https://github.com/PierreChrd/py-sutom-cheat) fait par [PierreCH](https://github.com/PierreChrd) résoud également le jeu de la même manière.
