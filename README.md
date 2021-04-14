# Université Paris-Saclay - Janvier-Mai 2021

# Projet-Bioinformatique - L3 Double licence Mathématiques Informatique

## Pipeline de Préparation et d'Analyse de données de génomes 

## George Marchment - Clémence Sebe 


## But de ce projet : 

Analyser des génomes de levures domestiquées et naturelles pour estimer leur histoire évolutive.

## Informations :

Nous avons conçu un pipeline de préparation et d’analyses de données. Notre script permet le téléchargement des données, en effectue l'analyse  et présente sous forme d'images les résultats.

Lien vers notre rapport : (à rajouter quand tout est ok)

## Résultats : 

![mapping](Resultats/Graphs/General/MappingHisto.png)

Cette première figure a été obtenue après l’alignement des séquences. Tous les échantillons ont un pourcentage d’alignement avec le génome de référence supérieur à 50%. Comme nos séquences ont une longueur moyenne de 150 pb, ces résultats sont très satisfaisants.


![pca](Resultats/Graphs/SNP/png/pca.PNG)

Graphique représentant les vingt-six échantillons après une PCA. Chaque échantillon est représenté par un symbole et une couleur différente

![cluster](Resultats/Graphs/SNP/png/clustering.PNG)

Graphique représentant les vingt-six échantillons selon leur groupe d’appartenance

![arbre](Resultats/Graphs/SNP/png/arbre.PNG)

Arbre phylogénique de nos vingt-six échantillons

## Conclusion : 

A partir des graphiques obtenus, nous pouvons émettre plusieurs conclusions.

La **troisième figure** nous montre que les clusters obtenus respectent plutôt bien les groupes donnés dans l’article. Les levures appartenant aux groupes Wine et Cachaça1 sont toutes bien regroupées ensemble, elles forment deux clusters distincts mais très proches. Le groupe CachaçaMosaics « s’étale » un peu plus sur l’image et se mélange avec le groupe « Bread ». D’un point de vue général, on peut conclure que les données ont été analysées correctement car on retrouve bien les données d’un même groupe ensemble.


La **dernière figure** représente l’arbre phylogénique de nos vingt-six échantillons. On observe au premier regard, que les différents groupes ont bien été respectés (chaque couleur est regroupée). Si nous devions retracer l’évolution de ces groupes, nous pourrions supposer que le plus ancien groupe est BrazilB1, que CachaçaMosaics s’est séparé ensuite et que son évolution a pris plusieurs années car Y638, Y637 et Y628 ne sont ni aux mêmes niveaux ni sur les mêmes branches. Seraient arrivées ensuite les levures les plus récentes, Cachaça1, Cachaça2 et Wine qui possèdent un ancêtre commun plus proche que Bread qui est lui aussi une levure récente.


En comparant ces **deux figure**, on retrouve bien ces résultats. Les groupes de Cachaça1 et Wine sont très proches sur les figures 7 et 8. De plus, on retrouve bien un élément de CachaçaMosaics parmi les Bread. BrazilB1 est bien éloigné des autres groupes. Pour finir Cachaça2 est lui aussi étalé mais reste proche et possède un ancêtre commun à Wine et Cachaça1.


Nos résultats sont en accord aves les résultats présentés dans l’article. Les chercheurs expliquent dans leur conclusion que la levure de Cachaça est un mélange entre Bread et Wine. On retrouve bien ce résultat sur la dernière figure, on retrouve Cachaça2 qui fait le lien entre les groupes Wine et Bread. Les auteurs parlent aussi dans leur conclusion du temps de domestication de S. Cerevisiae, cette domestication ayant eu lieu en trois étapes. On retrouve bien ce résultat dans nos deux figures. BrazilB1 est séparé des autres levures dans le clustering ainsi que dans l’arbre (il se situe sur la branche extérieure). Les groupes de Cachaça sont des intermédiaires des groupes Wine et Bread.

D'autres résultats se trouvent dans le dossier : [Resultats](https://github.com/George-Marchment/Projet-Bioinformatique-L3/tree/main/Resultats)

