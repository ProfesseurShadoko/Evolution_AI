import pygame
import colors
import green as GREEN
import red as RED
import settings as settings
import player as PLAYER
import numpy.random as rd
import numpy as np
from utils import bring_back_memory, reset_memory,save_memory
import os,shutil

from team import red_team,green_team

UP="\033[F"
DEMO_DATA=0

def run(resume=True,show=True,demo=False):
    demo=show and demo #si show est faux c'est pas une demo
    print("")
    print("")
    if not resume:
        print("--> STARTING GAME")
        reset_memory()
        
    else:
        print("--> RESUMING GAME")
    print("")
    print("""Commandes :
    t --> train
    s --> show
    d --> demo
    r --> reset
    z --> save
    l --> load to demo
    """)
    print("")
    pygame.init()
    game=pygame.display.set_mode((settings.XSIZE,settings.YSIZE))
    if show:
        pygame.display.set_caption('IA EVOLUTION')
        game.fill(colors.black)
        pygame.display.update()
    
    
    loop_count=1
    PLAYER.load_all(game)
    
    while True:
        loop_count=(loop_count+1)

        if green_team.size()<=3:
            GREEN.create(game)
        
        if red_team.size()<=3:
            RED.create(game)

        events=pygame.event.get()

        #checking for events
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_d: #demo
                    show=True
                    demo=True
                if event.key==pygame.K_t: #train
                    show=False
                    demo=False
                    game.fill(colors.black)
                    pygame.display.update()
                if event.key==pygame.K_s:
                    show=True
                    demo=False
                if event.key==pygame.K_r:
                    return run(resume=False)
                if event.key==pygame.K_z:
                    reset_memory(reset_team=False) #on réenregistre tout le monde
                    for player in red_team.players:
                        player.save()
                    for player in green_team.players:
                        player.save()
                    save_memory()
                    return
                if event.key==pygame.K_l:
                    try:
                        bring_back_memory(DEMO_DATA) #peut-être eut-il été plus intéressant de mettre en argument de run le chemin vers la mémoire, comme ça on peut reprendre un projet et l'update
                    except:
                        print("Fail to bring back data")
                    return run(demo=True)

            if event.type==pygame.QUIT:
                reset_memory(reset_team=False)
                for player in red_team.players:
                    player.save()
                for player in green_team.players:
                    player.save()
                return #ajouter un enregistrement des réseaux de neurones atteints à la fin
        
        for player in green_team.players: #on fait d'bord bouger les verts parce que c'est facile
            player.apply_decision()
            player.move()
            player.handle_collision(demo=demo)
            
            if show:
                player.draw()

        for player in red_team.players:
            player.apply_decision()
            player.move()
            player.handle_collision(demo=demo)

            if show:
                player.draw()

        red_team.clean()
        green_team.clean()

        if not demo:
            #ici on gere la mort et la division (pas pour les rouges puisqu'ils se divisent en mangeant)
            #l'evolution naturelle se réalise par le fait que les rouges nuls sont les premiers à mourir et les verts fort on plus de temps pour se reproduire

            if red_team.size()>=settings.RED_NUMBER:
                #mort des rouges trop nombreux
                player_last_meal=[player.last_meal for player in red_team.players]
                i=player_last_meal.index(max(player_last_meal)) #peut-être trier la liste est-il plus simple car on a pas besoin de tout retrier à chaque fois, elle est plutot bien triée à chaque tour
                red_team.kill(red_team.players[i])
            
            if green_team.size()<=settings.GREEN_NUMBER:
                #division aléatoire des verts
                if len(green_team.players)!=0:
                    PLAYER.split(rd.choice(green_team.players))
                
        
        red_team.clean()
        

        if show:
            for red in red_team.players:
                red_sees=False
                for green in green_team.players:
                    if red.see(green):
                        if not demo:
                            green.mark()
                        red_sees=True
                        pass
                if red_sees:
                    if not demo:
                        red.draw_vision()
                    pass
        
        if show:        
            pygame.display.update() 
            pygame.time.delay(settings.MS_PER_FRAME*3)
            game.fill(colors.black)

        
        if loop_count%1000==0:
            gr=max([player.generation for player in red_team.players])
            gg=max([player.generation for player in green_team.players])

            print("\r",end="")
            print("RED   : ",end="")
            for i in range(gr//250):
                print("-",end="")
            print(">",end="")
            for i in range(10-gr//250):
                print(" ",end="")
            print(f"Training {min(100,gr//25)}% complete")

            print("GREEN : ",end="")
            for i in range(gg//100):
                print("-",end="")
            print(">",end="")
            for i in range(10-gg//100):
                print(" ",end="")
            print(f"Training {min(100,gg//10)}% complete",end="")
            print(UP,end="")



if __name__=="__main__":
    #reset_memory()
    run() #rajouter un paramètre qui permet de continuer d'évoluer ou juste de regarder le resultat
    #corriger les tests de collision + la mort des éléments

"""Pour créer un fichier .exe à partir de ça :
- pip install pyinstaller
- pyinstaller run.py
Supprimer main.spec and build, et dans dist il y a le fichier executable --> le ramener dans le fichier principal pour que python trouve les imports"""