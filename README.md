Plugin QGIS de cartographie des flux
=============

Ce plugin doit permettre l'analyse et la représentation des flux 
résultant des innovations de SLocal/SNet.

Etat
-------

### Bezier

* Fonctions globalement fonctionnelles
* Manque implémentation complète dans l'outil (BezierTool)
* Table de répartition prête
* Utiliser les fonctions snapTo pour plus de facilité

### FDEB

* Semble fonctionnel, mais résultats étranges
* Les déplacements peuvent être très forts (tours autour des lignes de
 départ) de même que très faibles (invisibles sans intersection).
* L'intégration dans le GUI du paramétrage est en cours
* Re-travailler sur la barre d'avancement, pas assez précise
* Travailler sur le threading pour que tout reste actif
 pendant le calcul
* Fixer un paramètrage par défaut correct
* Créer dans une nouvelle couche plutôt que modifier géometrie.

### Oursins : Great-circles

* Pas très long vraisemblablement
* Aucune chance de parvenir à l'avoir d'ici la fin du stage
* Je ne vais que le mentionner dans le rapport, peut-être que ce sera prêt
 pour la soutenance mais je n'y compte pas.

### Import de données

* Pour l'instant, rien de créé : import de lignes simples
* A fabriquer absolument d'ici la soutenance
* Priorité : Création de lignes depuis Ox-Oy / Dx-Dy
* Mettre rapidement en place aussi l'import SVG

### Export de données

* Pour l'instant : SVG basique
* A adapter pour FDEB et plus tard great-circles
* Mettre en place la symbologie, indispensable
* Créer un SVG spécialement formatté pour l'import.




TODO
------------

### Priorité absolue

* Finir FDEB
* Finir Bezier
* Export SVG symbologie
* Import table OD

### Important

* Affichage des flux selon selection / Export des flux selon selection
* Great circles
* Export SVG spécialisé

### Bonus

* Gérer d'autres formats d'entrée : Sans doute via une fenêtre différente
 -> table OD + shape, table OD + 2 shape, Matrice OD + shape



FIXME
------------

### FDEB :
* Comportement étrange, à vérifier
* Essayer de réduire le temps de calcul
* Bug quand aucun compatible
* Création nouvelle couche




