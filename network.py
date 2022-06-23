import numpy as np
import numpy.random as rd
from copy import deepcopy

class network:
    """Ce machin est constitué d'une couche, qui relie les entrées aux sorties. On a donc une matrice de poids par sortie"""
    def __init__(self,entries_nbr,outputs_nbr):
        self.entries_nbr=entries_nbr
        self.outputs_nbr=outputs_nbr
        self.neurons=np.zeros((outputs_nbr,entries_nbr)) #chaque ligne est une matrice de poids
        self.b=np.zeros(outputs_nbr)
    
    
    def __str__(self):
        return f"Nombre de couches = 1\n Nombre d'entrées = {self.entries_nbr}\n Nombre de sorties = {self.outputs_nbr}\nNeurons : \n {self.neurons} \n Offset = {self.b}"
    
    def randomize(self):
        self.neurons=rd.sample((self.outputs_nbr,self.entries_nbr))*2-1
        self.b=rd.sample((self.outputs_nbr))*2-1

    def change_dna(self):
        """makes random changes to the network between -0.05 and +0.05"""
        change_b=rd.sample()>=0.80
        modif=(rd.sample()*2-1)/20
        i,j=rd.randint(0,self.outputs_nbr),rd.randint(0,self.entries_nbr)

        if change_b:
            self.b[i]+=modif
        else:
            self.neurons[i,j]+=modif
        
    
    def decision(self,inputs):
        """return wich out has been activated"""
        output_values=np.dot(self.neurons,inputs)+self.b
        if output_values.max()==0.0:
            return
        return output_values.argmax()
    
    def save(self,filename):
        """enregistre dans un fichier texte le cerveau"""
        fichier=open(filename,'w')
        fichier.write(f"({self.entries_nbr},{self.outputs_nbr})\n")
        for i in range(self.outputs_nbr): #les lignes
            for j in range(self.entries_nbr):
                fichier.write(f"{self.neurons[i,j]} ")
            fichier.write("\n")
        for i in range(self.outputs_nbr):
            fichier.write(f"{self.b[i]}\n")
        fichier.close()
    



def copy(brain):
    new_network=network(brain.entries_nbr,brain.outputs_nbr)
    new_network.neurons=deepcopy(brain.neurons)
    new_network.b=deepcopy(brain.b)
    return new_network

def load(filename):
    fichier=open(filename,'r')
    l1=fichier.readline()#je sais pas s'il y a le \n...
    l1=l1.replace("(","")
    l1=l1.replace(")","")
    l1=l1.split(",")
    entries_nbr=int(l1[0])
    outputs_nbr=int(l1[1])
    brain=network(entries_nbr,outputs_nbr)
    for i in range(outputs_nbr):
        l=fichier.readline()
        l=l.split(" ")
        for j in range(entries_nbr):
            brain.neurons[i,j]=float(l[j])
    
    for i in range(outputs_nbr):
        l=fichier.readline()
        brain.b[i]=float(l)

    return brain

if __name__=="__main__":
    brain=network(8,3)
    brain.randomize()
    brain.save("brain_data/brain.txt")
    brain2=load(filename="brain_data/brain.txt")
    print("brain1 :")
    print(brain)
    print()
    print("brain2 :")
    print(brain2)
    


        

