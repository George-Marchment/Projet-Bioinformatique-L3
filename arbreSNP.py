#George Marchment + Clemence Sebe
#Contient les fonctions pour l'analyse des SNP
import numpy as np

#-----------------------------------------------------------------------------------------
#Fonction calcul de distance
def distance_euclidienne(a, b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
  
#-----------------------------------------------------------------------------------------  
#Retourne un tableau de taille lxc (l lignes et c colones) avec rien à l'intérieur
def createTable(l,c):
    return [['.' for _ in range (c)] for _ in range (l)]
 
#-----------------------------------------------------------------------------------------     
#Fonction qui affiche un tableau de la même manière que numpy affiche un array
def afficheTab(t, thing=True):
    if thing:
        form=""
        for i in range(len(t)):
            form+="{:6.5}"
        for l in t:
            p=[]
            for el in l:
                p.append(str(el))
            print(form.format(*p))
    else:
        for l in t:
            print(l)

#-----------------------------------------------------------------------------------------
#Fonction lisant un fichier et qui cree un tableau specifique a l'algorithme d'apres 
def read(file):
    names=[]
    with open(file, "r") as text:
        lignes= text.readlines()
        for i in range(1, len(lignes)):
            lignes[i]=lignes[i][2:]
            lignes[i]=lignes[i].strip()
            #print(lignes[i])
            lignes[i]=lignes[i].split(' ')
            #print(lignes[i])
            temp=[]
            for t in range(len(lignes[i])):
                if (lignes[i][t]!=' ' and lignes[i][t]!=''):
                    temp.append(lignes[i][t])
            names.append(temp)
        tab= createTable(len(names)+1, len(names)+1)
        for i in range(len(names)):
            tab[0][i+1]= names[i][0]
            tab[i+1][0]= names[i][0]
        #afficheTab(tab)
        for c in range(1, len(tab[0])):
            for l in range(c+1, len(tab)):
                a= [float(names[c-1][1]), float(names[c-1][2])]
                b= [float(names[l-1][1]), float(names[l-1][2])]
                tab[l][c]= distance_euclidienne(a, b)

        #afficheTab(tab)
        return tab

#-----------------------------------------------------------------------------------------
def jukes_cantor(x):
    return x
    #return -(3/4)*np.log(1-(4/3)*x)

#Creation matrice de distance
def matrice_distance(dico):
    #On créé la matrice vide
    matrice_distance= createTable(len(dico)+1, len(dico)+1)
    indice=1
    #On remplie: les lignes et les colones avec les noms correspondant
    for nom in dico:
        matrice_distance[indice][0]= nom
        matrice_distance[0][indice]= nom
        indice+=1
    #On remplie le reste de la matrice (partie bas), avec les valeurs correspondants (avec la formule)
    for c in range(1, len(matrice_distance[0])):
        nom1=matrice_distance[0][c]
        for l in range(c+1, len(matrice_distance)):
            nom2=matrice_distance[l][0]
            matrice_distance[l][c]= jukes_cantor(distance(dico[nom1], dico[nom2]))
    return matrice_distance


#-----------------------------------------------------------------------------------------
def max(a,b):
    if a>b:
        return a
    return b

#Dans le titre
def min(a,b):
    if a<b:
        return a
    return b

#-----------------------------------------------------------------------------------------
#Fonction qui trouve la valeur minimum de la matrice, et les indices correspondnat 
def min_matrice_inf(matrice):
    min_val, min_i, min_j= np.inf, np.inf, np.inf
    #On parcourt seulement la matrice inférieur
    for j in range(1, len(matrice[0])):
        for i in range(j+1, len(matrice)):
            if(matrice[i][j]<min_val):
                min_val, min_i, min_j= matrice[i][j], i, j
    return min_val, min_i, min_j

#-----------------------------------------------------------------------------------------
#Fonction qui prend une matrice 'normale' et la transforme en forme structuree 
def initia_matrice_distance(matrice_temp):
    matrice= matrice_temp.copy()
    for i in range(1, len(matrice)):
        matrice[i][0]={'text':matrice[i][0], 'last_dist':0, 'nb':1}
        matrice[0][i]={'text':matrice[0][i], 'last_dist':0, 'nb':1}
    return matrice

#-----------------------------------------------------------------------------------------
#Fonction qui prends une matrice en forme structuree et qui retourne un tableau avec des noms structures
#Soit les noms des colonnes et lignes
def extract_names(matrice):
    names=[]
    for i in range(1, len(matrice[0])):
        names.append({'text':matrice[0][i]['text'], 'last_dist':matrice[0][i]['last_dist'], 'nb':matrice[0][i]['nb']})
    return names

#-----------------------------------------------------------------------------------------
#Fonction qui fait bêtement le calcul de dij,k  
def calcule_truc(matrice, i, j, k):
    #on fait max et min des indices puisqu'on veut la matrice inférieur
    return (matrice[0][i]['nb']*matrice[max(i, k)][min(k, i)]+matrice[0][j]['nb']*matrice[max(j, k)][min(j, k)])/(matrice[0][i]['nb']+matrice[0][j]['nb'])


#-----------------------------------------------------------------------------------------
#Fonction qui fusionne ou regroupe le tableaux des noms des deux séquences le plus proche
#Donc c'est cette fonction qui gère la construction du format Newick de l'arbre 
def fuse_names(nom, i, j, dist):
    #On est obligé de faire ceci puisqu'on se trouve dans le tableau de nom
    i, j= i-1, j-1
    tab=[]
    #Costruction du nouveau regroupement. A noté: le nouveau regroupement se situe toujours au début du tableau de noms (structures)
    text="("+str(nom[i]['text'])+":"+str(dist/2 - nom[i]['last_dist'])+","+str(nom[j]['text'])+":"+str(dist/2 - nom[j]['last_dist'])+")"
    tab.append({'text':text, 'last_dist':dist/2, 'nb':nom[i]['nb']+nom[j]['nb']})
    #On ajoute le reste des 'noms'
    for indice in range(len(nom)):
        if((indice!=i) and (indice!=(j))):
            tab.append(nom[indice])
    return tab

#-----------------------------------------------------------------------------------------
#Fonction qui 'Fusionne' une matrice en regroupant les deux séquences les plus proches
#On suppose qur matrice (élément en paramètre) est sous forme structural
def fuse_matrice(matrice):
    #On récupère la valeur minimum de distance de la matrice et ces indices
    val, i, j=min_matrice_inf(matrice)
    #On extrait les 'noms' de la matrice
    names= extract_names(matrice)
    #On créé la matrice vide d'une ligne et colone plus petite que la matrice de départ, comme on regroupe deux séquences
    tab_fini= createTable(len(matrice)-1, len(matrice)-1)

    #1ER COLONNE DE VALEUR NUMERIQUE
    #Remplissage de la première colone avec les 'nouvelles' distances du séquences regroupé avec les autres 
    #On commence à la 3e ligne puisque la 1er correspend aux noms et la 2e est vide comme on compare la même chose
    indice=2
    #On ne calcule pas les distances du séquences regroupé (a, b) avec l'élément vide, a ou b donc on les enlèves
    range_l= list(range(len(matrice[0])))
    range_l.pop(i)
    range_l.pop(j)
    range_l.pop(0)
    #Sinon on calcule les distances
    for k in range_l:
        tab_fini[indice][1]= calcule_truc(matrice, i, j, k)
        indice+=1

    #LE RESTE DES COLONNES ON TRANSMET LES VALEURS DE LA MATRICE DE DEPART
    #On parcourt les colonnes de la nouvelle matrice un par un en remplissant les valeurs correspondant à l'ancienne matrice 
    #On commmence à la 4e ligne et la 3e colonne
    indice_l, indice_c=3, 2
    #On sauvegarde la denière ligne de 'commencement'
    last_l=indice_l
    #On sauvegarde la taille de la matrice
    size=len(tab_fini)
    for c in range(1, len(matrice[0])):
        for l in range(c+1, len(matrice)):
            #On veut les colonnes et les lignes différent des indices i et j
            if(l!= i and c!= i and l!=j and c!=j):
                tab_fini[indice_l][indice_c]= matrice[l][c]
                indice_l+=1
                #On 'réinitialise' les indices des colonnes et lignes pour la prochaine colonnes 
                if(indice_l>=size):
                    last_l+=1
                    indice_l=last_l
                    indice_c+=1

    #On fusionne les noms
    names=fuse_names(names, i, j, val)
    #On les reporte ensuite à la matrice finale
    for l in range(1, len(tab_fini)):
        tab_fini[0][l]=names[l-1]
        tab_fini[l][0]=names[l-1]

    return tab_fini

#-----------------------------------------------------------------------------------------
#Fonction qui prends une matrice sous forme 'normale' et qui retourne l'arbre phylogénétique en format Newick
def UPGMA(matrice):
    #On initialise la matrice: en le mettant en forme 'structurelle"
    matrice= initia_matrice_distance(matrice)
    #Tant qu'il reste des séquences à regrouper
    while(len(matrice)!=2):
        #On fusionne la matrice
        matrice= fuse_matrice(matrice)
    return matrice[0][1]['text']+';'



