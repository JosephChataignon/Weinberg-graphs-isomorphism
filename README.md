**English description below**
*MIT License. Use this code the way you want, and add a star if you find it useful.*
*License MIT. Utilisez ce code comme vous le voulez, ajoutez une �toile si vous le trouvez utile.*

# Algorithm de Weinberg sur les graphes isomorphes

## Pr�sentation
Ce programme est une impl�mentation en Python de l'algorithme pr�sent� par Louis Weinberg dans un article publi� en 1965, "A Simple and Efficient Algorithm for Determining Isomorphism of Planar Triply Connected Graphs", disponible sur ieeexplore.ieee.org/document/1082573 (en anglais). Cet algorithme permet de d�terminer si des graphes planaires de connexit� 3 sont isomorphes ou non.

## Fonctionement de l'algorithme
Cet algorithme consiste � associer � tout graphe des vecteurs repr�sentant un chemin eul�rien parcourant tout le graphe selon une proc�dure particuli�re. Il existe un vecteur pour chaque branche de d�part possible du chemin sur le graphe, et pour chaque sens de parcours des branches d'un noeud (horaire ou anti-horaire). On peut donc former une matrice avec ces vecteurs pour chaque graphe.
Pour deux graphes A et B, si un seul des vecteurs de A a un �gal parmi les vecteurs de B, alors A et B sont isomorphes (ainsi il n'est pas n�cessaire de g�n�rer une matrice enti�re pour chaque graphe).

## Encodage des graphes
Un graphe doit �tre mod�lis� par une liste o� chaque indice correspond � un noeud du graphe. Le i-�me emplacement de cette liste (correspondant au i-�me noeud) contient une liste des indices des noeuds auxquels le i-�me noeud est reli� par une ar�te. Notez qu'ainsi, chaque ar�te est mod�lis�e deux fois, une fois dans chaque sens.

Par exemple, le graphe complet K2 est mod�lis� par: `[ [1] , [0] ]`
De m�me, le graphe complet K3 est mod�lis� par: `[ [1,2] , [0,2] , [0,1] ]`
Et un graphe "carr�" (4 sommets et 4 ar�tes formant un carr�) est mod�lis� par: `[ [1,3] , [0,2] , [1,3] , [0,2] ]`

## Fonctions
Le programme comporte plusieurs fonctions. Celles qui sont directement utiles sont les suivantes:
- generateCodeVector: prenant en argument un graphe, un couple (noeud,branche) de d�part du chemin eul�rien, et �ventuellement une variable sur l'ordre de parcours des branches partant d'un noeud, cette fonction g�n�re le vecteur code correspondant � cette position de d�part:
- generateCodeMatrix: prenant en argument un graphe, g�n�re l'ensemble des vecteurs code de ce graphe et les renvoie sous la forme d'une matrice.
- eliminateDoubles: � partir d'une liste de graphes, renvoie la m�me liste mais sans graphes isomorphes: lorsque deux graphes sont isomorphes, un seul est gard�.





# Weinberg's algorithm for graph isomorphism

## Introduction
This program is an implementation in Python of the algorithm presented by Louis Weinberg in an article published in 1965, "A Simple and Efficient Algorithm for Determining Isomorphism of Planar Triply Connected Graphs", available at ieeexplore.ieee.org/document/1082573 (in english). This algorithm is able to determine if planar triply-connected graphs are isomorphic or not.

## How the algorithm works
This algorithm consists in associating to every graph, vectors that represent an eulerian path going through the whole graph following a precise procedure. A vector exists for every possible branch on which the eulerian path can start, and for the 2 possible rotation directions on the branches of a node (clockwise or counter-clockwise). Therefore it is possible to form a matrix made of these vectors for any graph.
For two graphs A and B, if one of the vectors of A is equal to one of the vectors of B, then A and B are isomorphic (so it is not necessary to generate the entire matrix for every graph).

## Graphs encoding
A graph must be modelised by a list where each index corresponds to a node of the graph. The i-th location of that list (corresponding to the i-th node) contains a list of the indices of the nodes linked by a vertex to the i-th node. Note that this way, every vertex is modelised two times, one time in each direction.
For instance, the complete graph K2 would be `[ [1] , [0] ]`
In the same way, K3 would be `[ [1,2] , [0,2] , [0,1] ]`
And a "square" graph(4 nodes and 4 vertices forming a square) would be `[ [1,3] , [0,2] , [1,3] , [0,2] ]`

## Functions
The program has several functions. The directly useful ones are the following:
- generateCodeVector: with, as arguments, a graph, a departure node and branch for the eulerian path, and maybe a variable on the rotation direction in the branches of a node (clockwise or counter-clockwise), this function generates the code vector corresponding to this departure location:
- generateCodeMatrix: with a graph as argument, generates all the code vectors of that graph and returns them as a matrix.
- eliminateDoubles: from a list of graphs, returns the same list but without isomorphic graphs: when two graphs are isomorphic, only one is kept.



