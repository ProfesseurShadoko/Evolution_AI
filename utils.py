import cmath
import os,shutil
import time
from team import red_team,green_team

def phase(x0,y0,x,y):
    z=(x-x0)+(y0-y)*1j #mauvais systeme de coordonnées
    return cmath.polar(z)[1]

def reset_memory(reset_team=True):
    """efface tous les fichier player_data qui permettent de reprendre une simulation en cours après avoir arrêté le jeu, et efface red_team et gree_team"""
    here=os.getcwd()
    for filename in os.listdir(here+"/player_data"):
        os.remove("player_data/"+filename)
    for filename in os.listdir(here+"/brain_data"):
        os.remove("brain_data/"+filename)
    if reset_team:
        green_team.reset()
        red_team.reset()

def save_memory():
    """enregistre dans result les fichiers présent dans la mémoire temporaire qui permet de renprendre le jeu précédent"""
    here=os.getcwd()
    n_dir=len(os.listdir(here+"/results"))
    new_dir=here+f"/results/result{n_dir}"
    player_dir=new_dir+"/player_data"
    brain_dir=new_dir+"/brain_data"
    os.mkdir(new_dir)
    os.mkdir(player_dir)
    os.mkdir(brain_dir)

    for filename in os.listdir(here+"/player_data"):
        shutil.copy(here+"/player_data/"+filename,player_dir)
    for filename in os.listdir(here+"/brain_data"):
        shutil.copy(here+"/brain_data/"+filename,brain_dir)
    
    return

def bring_back_memory(ref):
    """écrase les fichiers de la mémoire temporaire pour y mettre un jeu ancien"""
    reset_memory()
    here=os.getcwd()
    player_dir = here+f"/results/result{ref}/player_data"
    brain_dir = here+f"/results/result{ref}/brain_data"
    player_data=here+"/player_data"
    brain_data=here+"/brain_data"
    
    for filename in os.listdir(player_dir):
        shutil.copy(player_dir+"/"+filename,player_data+"/"+filename)
    for filename in os.listdir(brain_dir):
        shutil.copy(brain_dir+"/"+filename,brain_data+"/"+filename)
    return