#George Marchment + Clemence Sebe
#Script Fonction aidant aux arbres
import numpy as np

#-----------------------------------------------------------------------
def distance_euclidienne(a, b):
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

#-----------------------------------------------------------------------
def read(file):
    names=[]
    with open(file, "r") as text:
        lignes= text.readlines()
        #print(lignes)
        for i in range(1, len(lignes)):
            lignes[i]=lignes[i]
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
        
#-----------------------------------------------------------------------
def calculScore(ali1, ali2, similarity_matrix):
    #initialistation
    score = 0

    #Verif meme taille => Cela ne devrait pas arriver 
    if len(ali1) != len(ali2):
        print("ATTENTION : les deux alignements ne sont pas de meme taille")
    
    #Sinon ok :
    else:
        for i in range (len(ali1)):
            score += similarity_matrix.score(ali1[i], ali2[i])
    return score

#-----------------------------------------------------------------------
#Retourne un tableau de taille lxc (l lignes et c colones) avec rien à l'intérieur
def createTable(l,c):
    return [['.' for _ in range (c)] for _ in range (l)]

#-----------------------------------------------------------------------
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


#-----------------------------------------------------------------------
#Fonction qui retourne le lettre correspondant à l'indice max de la formule Mij (écris juste audessus) 
def symbole(entier):
    if entier == 0:
        return 'd'
    elif entier == 1:
        return 'l'
    return 'u'

#-----------------------------------------------------------------------
#Fonction qui retourne les alignements des deux séquences, et qui donne le score de l'alignement (permet d'afficher les matrices M et T si l'utilisateur le souhaite): en utilisant l'Algorithme de Needleman-Wunsch
def NeedlmanWunsch(A, B, matSim, affiche=False):

    n =  len(A) #nb lignes (dans cette fonction correspondant à i)
    m = len(B) #nb colonnes (dans cette fonction correspondant à j)
    
    #initialisation des deux 'matrices' M et T => on utilise des tableaux et non des arrays car on n'a pas prévu de faire des produits matricielles donc on prèfères de manipuler des tableaux mais en soit cela ne change pas grand chose
    M = createTable(n+1, m+1)
    T =  createTable(n+1, m+1)
    
    #Initialisation de M => lignes et colones multiplent de -5
    for j in range (len(M[0])):
        M[0][j] = j * (calculScore('A','-', matSim)) # -5 = calculScore('A','-', matSim) avec matSim = SimilarityMatrix('dna_matrix')
    for i in range (len(M)):
        M[i][0] = i * (calculScore('A','-', matSim))# -5 = calculScore('A','-', matSim) avec matSim = SimilarityMatrix
    
    #Initialisation de T => 1er ligne à 'l', 1er colone à 'u' et première element 'o'
    T[0][0] = 'o'
    for j in range (1,len(T[0])):
        T[0][j] = 'l'
    for i in range (1,len(T)):
        T[i][0] = 'u'
    
    #Fonction Mij qui retourne la valeur pour la matrice M à l'indice i, j et la valeur pour la matrice T à l'indice i, j: ceci correspondant à l'expression Mij audessus
    def fonction_Mij(i,j):
        tab = [M[i-1][j-1] + calculScore(A[i-1],B[j-1], matSim), M[i][j-1] + calculScore(A[i-1], '-', matSim), M[i-1][j] + calculScore(B[j-1], '-', matSim)]
        score = np.max(tab)
        lettre = symbole(np.argmax(tab))
        return score, lettre
    
    #Remplissage des matrices grâce à la fonction_Mij
    for i in range (1, len(T)):
        for j in range (1, len(T[0])):
            M[i][j], T[i][j] = fonction_Mij(i,j)
    
    #Affichage des deux matrices si l'utilisateur le souhaite
    if affiche:
        afficheTab(M, False)
        print()
        afficheTab(T, False)


    #Pour obtenir l'alignement on remonte la "trace" de la matrice T
    #Pour faire cela on commence au dernier 'lettre' (element) de T, puis on 'remonte' la matrice en fonction des lettre 'd' (diagonal), 'u' (up) ou 'l' (left), on fait ça à chaque étape avant d'atteindre 'o'
    i, j= -1, -1
    lettre=T[i][j]
    ali_A, ali_B= '', ''
    while(lettre != 'o'):
        #Cas si lettre = 'd':un match entre les deux séquences
        if lettre == 'd':
            ali_A= A[i]+ali_A
            ali_B= B[j]+ali_B
            i-=1
            j-=1
        #Cas si lettre = 'u': un gap dans la séquence B
        if lettre == 'u':
            ali_A= A[i]+ali_A
            ali_B= '-'+ali_B
            i-=1
        #Cas si lettre = 'l':un gap dans la séquence A
        if lettre == 'l':
            ali_A= '-'+ali_A
            ali_B= B[j]+ali_B
            j-=1
        lettre=T[i][j]

    #On retourne les deux alignements avec le score
    return ali_A , ali_B, M[-1][-1]

#-----------------------------------------------------------------------
def jukes_cantor(x):
    return x
    #return -(3/4)*np.log(1-(4/3)*x)

#-----------------------------------------------------------------------
#Fonction pas optimiser, mais elle ne semble pas prendre beaucoup de temps donc on la laisse comme ça
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
    for c in range(1, len(matrice_distance[0])):#avant c'était len(matrice_distance) mais je me suis trompé 
        nom1=matrice_distance[0][c]
        for l in range(c+1, len(matrice_distance)):
            nom2=matrice_distance[l][0]
            matrice_distance[l][c]= jukes_cantor(distance(dico[nom1], dico[nom2]))
    return matrice_distance


#-----------------------------------------------------------------------
#Dans le titre
def max(a,b):
    if a>b:
        return a
    return b

#Dans le titre
def min(a,b):
    if a<b:
        return a
    return b

#-----------------------------------------------------------------------
#Fonction qui trouve la valeur minimum de la matrice, et les indices correspondnat 
def min_matrice_inf(matrice):
    min_val, min_i, min_j= np.inf, np.inf, np.inf
    #On parcourt seulement la matrice inférieur
    for j in range(1, len(matrice[0])):
        for i in range(j+1, len(matrice)):
            if(matrice[i][j]<min_val):
                min_val, min_i, min_j= matrice[i][j], i, j
    return min_val, min_i, min_j

#-----------------------------------------------------------------------
#Fonction qui prend une matrice 'normalle' et la transforme en forme struturalle 
def initia_matrice_distance(matrice_temp):
    matrice= matrice_temp.copy()
    for i in range(1, len(matrice)):
        matrice[i][0]={'text':matrice[i][0], 'last_dist':0, 'nb':1}
        matrice[0][i]={'text':matrice[0][i], 'last_dist':0, 'nb':1}
    return matrice

#-----------------------------------------------------------------------
#Fonction qui prends une matrice en forme structuralle et qui retourne un tableau des noms structurals
#Soit les noms des colonnes et lignes
def extract_names(matrice):
    names=[]
    for i in range(1, len(matrice[0])):
        names.append({'text':matrice[0][i]['text'], 'last_dist':matrice[0][i]['last_dist'], 'nb':matrice[0][i]['nb']})
    return names

#-----------------------------------------------------------------------
#Fonction qui fait bêtement le calcul de dij,k    
def calcule_truc(matrice, i, j, k):
    #on fait max et min des indices puisqu'on veut la matrice inférieur
    return (matrice[0][i]['nb']*matrice[max(i, k)][min(k, i)]+matrice[0][j]['nb']*matrice[max(j, k)][min(j, k)])/(matrice[0][i]['nb']+matrice[0][j]['nb'])

#-----------------------------------------------------------------------
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

#-----------------------------------------------------------------------
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

#-----------------------------------------------------------------------
#Fonction qui prends une matrice sous forme 'normalle' et qui retourne l'arbre phylogénétique en format Newick
def UPGMA(matrice):
    #On initialise la matrice: en le mettant en forme 'structurelle"
    matrice= initia_matrice_distance(matrice)
    #Tant qu'il reste des séquences à regrouper
    while(len(matrice)!=2):
        #On fusionne la matrice
        matrice= fuse_matrice(matrice)
    return matrice[0][1]['text']+';'



#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#Fonction qui prend en paramètre une matrice de distance (Inférieur) et deux indices, et qui retourne la distance qui sépare les deux indices
def dist_matrice( matrice,a, b):
    #On prends les max et min comme c'est une matrice inférieure
    return matrice[max(a, b)][min(a, b)]

#-----------------------------------------------------------------------
#Fonction qui extrait les noms (sous le format Newick) d'une matrice de distance
def extract_names_NJ(matrice):
    tab=[]
    for i in range(1, len(matrice[0])):
        tab.append(matrice[0][i])
    return tab

#-----------------------------------------------------------------------
#Fonction qui calcule les S de la matrice de distance donnée en paramètre en suivant les règles défini dans le lien 
def calcul_S(matrice):
    tab=[]
    for l in range(1, len(matrice)):
        val=0
        for c in range(1, len(matrice[0])):
            if(c!=l):
                val+= dist_matrice(matrice, l, c)
        #-3 car -1 pour le tableau -2 dans la formule (-3= -2-1)
        tab.append(val/(len(matrice)-3))
    return tab

#-----------------------------------------------------------------------
#Fonction qui calcule le couple avec le plus petit Mij
def calcule_pair(matrice, S):
    val_min, l_min, c_min =np.inf, np.inf, np.inf
    for c in range(1, len(matrice[0])):
        #c+1 car matrice inférieur
        for l in range(c+1, len(matrice)):
            mij= dist_matrice(matrice, l, c) - S[l-1]- S[c-1]
            #Ici on peut mettre < ou <= car dans l'exemple ils utilisent les deux
            #Mais personnelement je trouve que les arbres sont plus beau avec <=
            #Plus tard aussi on observe avec le score Bootstrap que <= est meilleur de <
            if(mij<=val_min): 
                val_min, l_min, c_min= mij, l, c
    return val_min, l_min, c_min


#-----------------------------------------------------------------------
#Fonction qui fuse les noms sous le format Newick en suivant les règles du lien
def fuse_names_NJ(matrice, i, j, S):
    tab=[]
    names= extract_names_NJ(matrice)
    text1= names[i-1]+':'+str(dist_matrice(matrice, i, j)/2 +(S[i-1]-S[j-1])/2)
    text2= names[j-1]+':'+str(dist_matrice(matrice, i, j)/2 +(S[j-1]-S[i-1])/2)
    tab.append('('+text1+', '+text2+')')
    for k in range(len(names)):
        #On fait -1 pour faire correspondre les bons indices de i et j pour le tableau de noms  
        if(k!= i-1 and k!=j-1):
            tab.append(names[k])
    return tab

#-----------------------------------------------------------------------
#Fonction qui une étape en entière (5 'Steps') de l'algo Neighbor-joining définit comme l'example du lien
def fuse_matrice_NJ(matrice):
    #On créé la matrice qu'on retourne à la fin: une ligne et colonne de moins de la matrice 'original'
    tab_fini= createTable(len(matrice)-1, len(matrice)-1)
    #On calcule les 'S' de la matrice
    S=calcul_S(matrice)
    #On dtermine le couple avec le plus petit Mij
    val, i, j= calcule_pair(matrice, calcul_S(matrice))
    #On fussione les noms
    names= fuse_names_NJ(matrice, i, j, S)

    #1ER COLONNE 
    #Calcule du nouveaux clonne fussionné (de U) en suivant les règles de l'algo du lien
    #On commence à remplir le colonne à partir du 3e ligne
    indice=2
    #On ne calcule pas les distances du séquences regroupé (a, b) avec l'élément vide, a ou b donc on les enlèves
    range_l= list(range(len(matrice[0])))
    range_l.pop(i)
    range_l.pop(j)
    range_l.pop(0)
    #Sinon on calcule les distances
    for k in range_l:
        tab_fini[indice][1]= (dist_matrice(matrice, i, k) +dist_matrice(matrice, j, k) -dist_matrice(matrice, i, j))/2
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

    #On remplie les 'nouveaux' noms dans la nouvelle matrice
    for l in range(1, len(tab_fini)):
        tab_fini[0][l]=names[l-1]
        tab_fini[l][0]=names[l-1]

    return tab_fini

#-----------------------------------------------------------------------
#Fonction qui effectue l'algo complet de Neighbor-joining qui prend en paramètre une matrice de distance, et qui retourne l'arbre phylogénétique en format Newick
def neighbor_joining(matrice):
        while(len(matrice)>3):
            matrice= fuse_matrice_NJ(matrice)
        return '('+matrice[0][1]+':0,'+matrice[0][2]+': '+str(matrice[2][1])+');'

