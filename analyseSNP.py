#George Marchment + Clemence Sebe
#Script Analyse SNP
import os
import variables as v
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import arbreSNP as a
from sklearn.cluster import KMeans
from ete3 import Tree, TreeStyle


def mainAnalyseSNP(analyse):
	print("DEBUT SCRIPT ANALYSE SNP")
	lien = v.vcf + "SNP/POST_FILTRE/SNP_PASS.vcf"
	sortie = v.graphs + "SNP/"
	
	if analyse:
		# R
		print("PCA avec R")
		cmd = "Rscript pca.R " + lien + " " + sortie
		os.system(cmd)
		os.remove(sortie + "tmp.gds")
		
		#Figure avec python
		print("Figure avec Python")
		
		file = open(sortie + "tabDonnees.txt", 'r')
		
		#Pallette de couleur "foncee"
		colorNames = list(matplotlib.colors.cnames.keys())
		cmap =[]
		for i in range (len(colorNames)):
			if colorNames[i][0] == 'd':
				cmap.append(colorNames[i])
		cmap.append('aqua')
		cmap.append('brown')
		
		#Lecture fichier
		line = file.readlines()
		sample = []
		dico = {}
		for i in range(1,len(line)):
			etude = line[i].split()
			sample.append(etude[1])
			dico.update({etude[1] : [float(etude[2]), float(etude[3])]})
		file.close()

		#Premiere image non zoomee
		fig, ax = plt.subplots(figsize=(10, 10))
		idx =0
		for name in sample:
			ax.scatter(dico[name][0], dico[name][1], label=name, color= cmap[idx])
			idx += 1
		ax.legend()
		ax.set_title("PCA")
		plt.savefig(sortie +'PcaNonZoomee.png')

		#Teste image non zoommee annote
		fig, ax = plt.subplots(figsize=(5, 5)) 
		for name in sample:  
			ax.scatter(dico[name][0], dico[name][1], s=100, alpha=0.5,linewidths=1, color='blue')  
			ax.annotate(name,xy=(dico[name][0], dico[name][1])) 
		ax.set_title("PCA")
		plt.savefig(sortie +'PcaNonZoomeeAnnote.png')

		#Kmeans pour creer des clusters
		X = []
		for name in sample:
			X.append([dico[name][0], dico[name][1]])
		X = np.array(X)
		
		#on a choisit 4 clusters apres visualisations des premiers resultats
		nbCluster = 4
		y_pred = KMeans(n_clusters=nbCluster, random_state=5).fit_predict(X)

		fig, ax = plt.subplots()
		ax.scatter(X[:, 0], X[:, 1], c=y_pred)
		ax.set_title("Kmeans")
		plt.savefig(sortie +'Kmeans.png')


		fichier = open(sortie +"infoCluster.txt", "w")
		fichier.write(f"{nbCluster} clusters :\n")
		for i in range (len(X)):
			ecrire = sample[i] + " : " + str(y_pred[i]) + "\n"
			fichier.write(ecrire)
		fichier.close()
		
		#Arbre de distance
		#On applique l'algo sur nos donnees
		#UPGMA
		arbre = a.UPGMA(a.read(sortie + "tabDonnees.txt"))   
		
		#Affichage 
		newick_tree = arbre
		t = Tree(newick_tree)
		ts = TreeStyle()
		ts.show_branch_length = True
		t.render(sortie + "UPGMA_treeSNP.png", w=180, units="mm", tree_style=ts)
		
		#Autre arbre - autre méthode
		#neighbor_joining
		arbre = a.neighbor_joining(a.read(sortie + "tabDonnees.txt"))   
		
		#Affichage 
		newick_tree = arbre
		t = Tree(newick_tree)
		ts = TreeStyle()
		ts.show_branch_length = True
		t.render(sortie + "NEIGHBOR_JOINING_treeSNP.png", w=180, units="mm", tree_style=ts)

	print("FIN SCRIPT ANALYSE SNP")
