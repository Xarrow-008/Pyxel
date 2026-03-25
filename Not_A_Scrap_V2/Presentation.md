Présentation globale du projet :
L'idée derrière Not A Scrap provient d'un entrainement pour la session 2025 de la Game Jam "Nuit du Code".
Celle-ci consiste en une séance de codage de 6h centrée autour de la librairie pyxel, qui permet de réaliser des jeux vidéos pixel art sur python
Comme nous ne pouvions pas connaitre le sujet de la Nuit du Code à l'avance, nous avions considéré le roguelike comme le genre de jeux vidéo le plus versatile, et nous nous sommes donc entrainés à celle-ci en réalisant un roguelike. En faisant des recherches sur des jeux qui pourraient nous inspirer, nous avons également repéré les jeux Lethal Company and R.E.P.O., centrés sur l'extraction de ressources dans des bunkers abandonnés par l'Homme et infestés de monstres.
C'est ce projet, initialement conçu comme un simple entrainement, qui deviendra "Not A Scrap" lorsque Léo décide de le réutiliser et l'améliorer comme projet de fin d'année de première de spécialité NSI.
C'est après cela qu'il nous est venu l'idée de créer une nouvelle version de "Not A Scrap" pour l'édition 2026 des Trophées NSI.
Not A Scrap se passe donc dans un futur où la Terre a été ruinée par une guerre entre l'Humanité et une race extraterrestre arachnoïde. Le personnage joueur est l'un des rares survivants de cette guerre, qui explore à bord de son vaisseau des bunkers, uniques restes de la civilisation humaine. Cependant, ces bunkers, bien que riches en restes (scrap) et en carburant, sont également infestés par les extraterrestres, et le joueur doit donc explorer ces batiments labyrinthiques tout en combattant ces enemis. De plus, l'intrusion du joueur au sein du bunker provoque l'arrivée d'une horde d'extraterrestres venus de dehors, et plus tard encore, l'explosion du bunker par le système de sécurité défaillant. Le joueur dispose donc d'un temps limité pour collecter le carburant nécessaire pour quitter le bunker et partir au suivant.
Notre objectif était donc de mettre au point un jeu complet et amusant qui respecte les codes traditionnels du Roguelike tout en imitant la formule du "Bunker Diving" de Lethal Company.

Organisation du travail :
Notre équipe est composée de deux personnes :
Léo :
    Léo s'est occupé de la dimension artistique du projet. Il a dessiné l'entièreté des images trouvées dans le jeu à l'aide d'une application "draw" (non incluse dans le projet) qu'il a développé et lui qui lui permet de réaliser des dessins pixel arts adaptés à pyxel de manière efficace et simple. Il a également mis au point l'entièreteté du système des animations du jeu.
    Il a également créé la génération aléatoire de l'environnement et des bunkers, qui permet à chaque partie du jeu d'être différent. Celle-ci relie entre elles un ensemble de salles préfaites afin de créer un labyrinthe unique à chaque partie. Parmis les nombreuses armoires contenues dans ces salles, certaines sont choisies aléatoirement pour contenir des objets, étant ainsi mises en surbrillance.
    Il a aussi mis au point l'algorithme de direction des ennemis. Ceux-ci peuvent ainsi naviguer leur environnement afin d'attaquer le joueur et peuvent changer de stratégie en cours de route pour pouvoir l'atteindre.
    Il était aussi reponsable de la mise en place de la game loop, c'est-à-dire, qu'il a créé le menu et le système par lequel le joueur peut quitter un bunker pour un autre.
Maximilien :
    Maximilien s'est occupé des éléments plus concrets du jeu en faisant grand usage de la Programmation Orientée Objet. Il a créé la classe entité afin de créer le joueur, les enemis, les projectiles et les attaques de melée. Ces entités ont ainsi accès à un ensemble de fonctions qui leur permet de se déplacer, d'attaquer etc... Et qui peuvent facilement intéragir entre-elles grâce à la classe InMission.
    Il a également créé les armes et les objets que le joueur peut utiliser, grâce à son inventaire. Ces objets, dont toutes les caractéristiques sont modifiables, permettant de créer une grande variété d'expérience à partir d'un modèle unique.
Le temps passé sur le projet est équivalent pour les deux membres de notre équipe, et de grandes partie du projet ont été passées à coder ensemble, solicitant les connaissances de l'autre pour faciliter le travail. Nous utilisions l'application Github desktop afin de pouvoir transférer notre travail de manière efficace. Nous n'avons pas fait l'usage de l'Intelligence Artificielle pour réaliser notre projet.

Présentations des étapes du projet :
- Etape 1 : Fin d'année scolaire 2024-2025, avant la Nuit du Code 2025
Not A Scrap (qui ne porte alors pas encore ce nom) est un projet d'entrainement pour la Nuit du Code. Les fonctionnalités sont limitées et les méchaniques ne servent qu'à nous entrainer pour cette game jam.
- Etape 2 : Fin d'année scolaire 2024-2025, après la Nuit du Code 2025
Not A Scrap est nommé, et devient le projet de fin d'année de première NSI de Léo (auquel Maximilien participe pour le plaisr). C'est à ce moment que la fondation du projet est créée. Le projet est fonctionnel, mais simple, avec des fonctionnalités qui restent plutot limitées.
- Etape 3 : Début d'année scolaire 2025-2026
Reprise du projet à partir de rien, avec des graphismes améliorés (résolution 2 fois plus haute). L'objectif est de créer un jeu avec des mécaniques complexes pour les trophées NSI, comprenant notamment des boss, mutliples personnages et des succès.
- Etape 4 : Moitié d'année scolaire 2025-2026
Etant pris par le temps, nous abandonnons l'idée d'avoir plusieurs personnages, des boss et des succès afin de pouvoir rendre un projet complet à temps pour les Trophées NSI. Le jeu est néanmoins doté de multiples enemis uniques ainsi que d'une grande panoplie d'objets et d'armes. Nous décidons que nous continuerons de travailler sur le projet après l'avoir rendu afin de le finir tel que nous l'avions pensé à l'étape 3.

Validation de l'opérationalité et fonctionnement :
Au moment du dépot, notre projet est fonctionnel, bien qu'un certain nombre des fonctionnalités originellement prévues ont du être coupée du jeu, faute de temps. Il n'y a notamment plus le choix de multiples personnages, pas de boss et pas de succès. Le nombre d'ennemis est également plus réduit que prévu. Il y a également moins d'objets avec lequel le joueur peut intéragir que prévu.
Afin de vérifier l'absence de bugs, nous avons lancé le jeu de multiples fois après chaque modification, testant chaque élément de gameplay qui a été ajouté au jeu dans de multiples conditions, même les plus extrêmes, afin de s'assurer que tout fonctionne comme prévu. Nous communiquons de manière efficace les problèmes rencontrés à l'autre afin de pouvoir les résoudre le plus rapidement possible, et assurer un fonctionnement fluide du programme.
Nous avons également essayer de rendre notre code le plus lisible possible, même sans commentaires, afin de pouvoir modifier le code de l'autre facilement sans provoquer de problèmes.

Ouverture : 
Bien évidemment, le principal axe d'amélioration est d'ajouter les éléments de gameplay qui ont du être abandonnés, tels que les boss, les objets interactibles, les ennemis supplémentaires et les succès.
La principale chose qui nous a nuit est un manque d'organisation de notre temps. Si nous avions été plus assidus dans notre travail sur le projet (par exemple, en travaillant plus pendant les vacances), il est certain que celui-ci serait bien plus complet.
Notre travail sur ce projet nous a permit de développer une grande maitrise sur le language de programmation python, ainsi que la Programmation Orientée Objet. Cela nous a également permit d'apprendre à travailler en groupe, et à nous coordonner pour réaliser un projet.