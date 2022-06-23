import numpy as np
import colors
import pygame
import numpy.random as rd
import settings
import utils
import copy
import os

from team import red_team,green_team
import network as nt
from network import network

RED=pygame.image.load("static/Red.png")
GREEN=pygame.image.load("static/Green.png")



class player():
    
    #INIT
    def __init__(self,game,team,generation=0):
        """crée le player à l'aide des réglages de l'équipe, de génération nulle au départ, et ajoute le player à l'équipe"""

        #position
        self.x=team.settings.position[0]
        self.y=team.settings.position[1] #ne sont pas forcément des entiers !

        #image
        self.radius=team.settings.radius
        self.direction=team.settings.direction #0 c'est vers la droite, 0.25 vers le haut, 0.5 vers la gauche, on multiplie par 2pi ensuite
        self.image=pygame.transform.rotate(pygame.transform.scale(team.settings.image,(team.settings.radius*2,team.settings.radius*2)),-0.25*360) #on la met à l'horizontal quand direction=0

        #relations à l'environnement
        self.vision_distance=team.settings.vision_distance
        self.vision_angle=team.settings.vision_angle

        #état
        self.living=True
        self.age=0
        self.last_meal=0
        self.speed=team.settings.speed
        self.generation=generation

        #jeu et IA
        self.game=game
        self.brain=network(8,3)#on regarde à chaque fois dans 8 direction, plus c'est proche plus l'input est grand, et on regarde rouges puis verts

        self.team=team
        self.team.add_player(self)
        if team==green_team:
            self.other_team=red_team
        else:
            self.other_team=green_team
    
    
    
    #accès aux infos
    def is_team(self,team):
        """team = str or team object, returns true if self.team corresponds to entry"""
        if team in ["red","RED","Red","r","R"]:
            return self.team==red_team
        if team in ["green","GREEN","Green","g","G"]:
            return self.team==green_team
        return team==self.team

    #gestion de la position
    def position(self):
        """return integer value of center position"""
        return int(self.x),int(self.y)

    def is_on_screen(self):
        x,y=self.position()
        X,Y=self.game.get_size()
        return x-self.radius>0 and x + self.radius < X and y - self.radius > 0 and self.radius + y < Y
    
    def bring_back_on_screen(self):
        if not self.is_on_screen():
            X,Y=self.game.get_size()
            if self.x-self.radius<0 or self.x + self.radius > X:
                self.x=max(self.x,self.radius+1)
                self.x=min(self.x,X-self.radius-1)
                self.direction=0.5-self.direction
            else:
                self.y=min(self.y,Y-self.radius-1)
                self.y=max(self.y,self.radius+1)
                self.direction=-self.direction
        self.diection=self.direction%1

    def move(self,add_meal=True):
        """moves in direction"""
        x_move=np.cos(self.direction*2*np.pi)*self.speed
        y_move=-np.sin(self.direction*2*np.pi)*self.speed
        self.x+=x_move
        self.y+=y_move
        if add_meal:
            self.last_meal+=1
            self.age+=1
        self.bring_back_on_screen()
    
    def move_back(self):
        self.direction=-self.direction
        self.move(add_meal=False)
    
    def turn(self,angle):
        """change direction, 0<=angle<=1 """
        self.direction+=angle
        self.direction=self.direction%1
    
    def turn_left(self):
        """left 0.025° turn"""
        self.turn(angle=0.025)
    
    def turn_right(self):
        """right 0.025° turn"""
        self.turn(angle=-0.025)
    
    #gestion de l'affichage
    def image_position(self):
        """return top right corner of character"""
        return int(self.x)-self.radius,int(self.y)-self.radius #top head position

    def draw(self,draw_dead=False):
        """draws picture centered on self.position()"""
        if draw_dead or self.living:
            self.game.blit(pygame.transform.rotate(self.image,self.direction*360),self.image_position())
    
    def draw_vision(self,draw_dead=False):
        """draws vision lines"""
        if draw_dead or self.living:
            d=self.vision_distance
            a=self.vision_angle
            pygame.draw.line(self.game,self.team.settings.color,self.position(),(int(self.x+np.cos(2*np.pi*(self.direction+a/2))*d),self.y-int(np.sin(2*np.pi*(self.direction+a/2))*d)))
            pygame.draw.line(self.game,self.team.settings.color,self.position(),(int(self.x+np.cos(2*np.pi*(self.direction-a/2))*d),self.y-int(np.sin(2*np.pi*(self.direction-a/2))*d)))
    

    def mark(self,color=colors.yellow,draw_dead=False):
        """marks player with yellow circle"""
        if draw_dead or self.living:
            pygame.draw.circle(self.game,color,self.position(),radius=self.radius,width=1)
    
    #gestion de l'initialisation
    def random_turn(self,max_turn=1/10):
        """gives random direction between -max_turn and max_turn"""
        self.turn((rd.sample()*2-1)*max_turn)
    
    def random_direction(self):
        """gives random direction"""
        self.direction=rd.sample()
    
    def random_position(self):
        """gives random position. Doesn't handle collisions"""
        X,Y=self.game.get_size()
        self.x=rd.randint(self.radius,X-self.radius)
        self.y=rd.randint(self.radius,Y-self.radius)
    
    def random_weights(self):
        """gives random weights, will be changed"""
        return rd.sample(8)*2-1
    
    def randomize(self):
        """random initialisation"""
        self.random_position()
        self.random_direction()
        self.brain.randomize()

    #gestion des collisions
    def distance_to(self,player):
        """return distance to player"""
        x,y=self.position()
        x1,y1=player.position()
        return np.sqrt((x-x1)**2+(y-y1)**2)
    
    def collision(self):
        """returns first player where collision happens"""
        collisions=[]
        if not self.is_alive():
            return collisions
        for player in green_team.players:
            if (not self==player) and player.is_alive():
                infd=self.radius+player.radius
                if infd>self.distance_to(player):
                    collisions.append(player)
        
        for player in red_team.players:
            if (not self==player) and player.is_alive():
                infd=self.radius+player.radius
                if infd>self.distance_to(player):
                    collisions.append(player)
        return collisions
    
    def handle_collision(self,demo=False):
        """check for all the collisions, eats or changes position when they happen, and makes the splits if it's not a demo"""
        for player in self.collision():
            if self.is_team(player.team):
                self.move_back()
                self.give_valid_location()
            else:
                if self.is_team("red"):
                    #alors l'autre est vert
                    if not demo:
                        self.eats(player)
                        split(self)
                    if demo:
                        player.random_position()
                else:
                    #alors je suis vert et l'autre est rouge
                    if not demo:
                        player.eats(self)
                        split(self)
                    if demo:
                        self.random_position()

    
    #gestions des paramètres de santé    
    def is_alive(self):
        return self.living

    #gestion de la vision
    def how_close(self,player):
        """returns 1 if distance=1, 0 if distance > vision_range"""
        return max(0,1-(self.distance_to(player)/self.vision_distance)**3)
        #return max(0,self.vision_distance-self.distance_to(player))/self.vision_distance
    
    def is_in_range(self,player):
        """return true if"""
        return self.how_close(player)!=0
    
    def is_myself(self,player):
        return self==player
    
    def see_angle(self,player):
        """si from_angle==0.1, l'angle renvoyé est l'angle"""
        x0,y0=self.position()
        x,y=player.position()
        return (utils.phase(x0,y0,x,y)/np.pi/2-self.direction+self.vision_angle/2)%1 #le resultat est l'angle de vision positif par rapport à la limite basse de la vision
    
    def see(self,player):
        return self.is_in_range(player) and (self.see_angle(player)<=self.vision_angle)
    
    def see_between(self,player,low,high):
        if not self.is_in_range(player):
            return False
        teta=self.see_angle(player)
        return teta>=low and teta<high
    
    #duplication
    def add_generation(self):
        """ajoute une génération"""
        self.generation+=1
    
    def change_dna(self):
        """appelle la méthode change_dna de brain qui modifie aléatoirement un terme du biais ou des neurons"""
        self.brain.change_dna()
    
    def give_valid_location(self,try_nbr=0):
        """ici self a une position déjà occupée par un autre, donc on met la réplique pas loin"""
        if self.collision()==[]:
            return
        if try_nbr>10:
            return "fail"
        teta=rd.sample()*2*np.pi #on le met à une distance 2,2 * radius
        d=2.2*self.radius
        self.x+=np.cos(teta)*d
        self.y+=np.sin(teta)*d
        if not self.is_on_screen():
            self.x-=np.cos(teta)*d
            self.y-=np.sin(teta)*d
            return self.give_valid_location(try_nbr+1)
        if not self.collision()==[]:
            return self.give_valid_location(try_nbr+1) #tant que la position n'est pas valide je me divise

    def make_split_changes(self):
        """après un split, il faut ajouter une génération, changer l'ADN, donner une localisation valide à l'élément, et donner unedirection aléatoire.
        Renvoie 'fail' si l'algo n'a pas réussi à donner une localisation"""
        self.add_generation()
        self.change_dna()
        v=self.give_valid_location()
        self.random_direction()
        return v
    
    def eats(self,player):
        """resets last_meal et appelle la methode kill de la team"""
        self.last_meal=0
        player.team.kill(player)
    

    def apply_random_decision(self):
        """tourne à gauche ou a droite de manière aléatoire"""
        r=rd.sample()
        if r>2/3:
            self.turn_left()
        if r<1/3:
            self.turn_right()
        

    def apply_decision(self):
        players = [player for player in self.other_team.players if self.see(player)]
        
        if len(players)==0:
            self.apply_random_decision()
        else:
            inputs=self.eyes_response(players)
            decision=self.brain.decision(inputs)
            if decision==2: #pourquoi le zéro est-il plus probable ??
                self.turn_left()
            if decision==1:
                self.turn_right()
            
            if decision==None:
                self.apply_random_decision()

    def eyes_response(self,players):
        zone_nbr=self.brain.entries_nbr
        zone_size=self.vision_angle/zone_nbr
        out=np.zeros(zone_nbr)
        for player in players:
            for i in range(self.brain.entries_nbr):
                low=i*zone_size
                high=(zone_size+1)*i
                if self.see_between(player,low,high):
                    out[i]+=self.how_close(player)
        return out
    
    def save(self):
        """on enregistre le player après les précédents sous le nom player{n}.txt. Le forat du fichier est le suivant:
        couleur/position/brainfile/last_meal/generation"""
        n=len(os.listdir(os.getcwd()+"/player_data"))
        file_name=f"player_data/player{n}.txt"
        file=open(file_name,'w')
        file.write(f"{self.team.name}\n")
        file.write(f"{self.x} {self.y}\n")
        brain_file_name=f"brain_data/brain{n}.txt"
        file.write(f"{brain_file_name}\n")
        self.brain.save(brain_file_name)
        file.write(f"{self.last_meal}\n")
        file.write(f"{self.generation}\n")
        file.close()

################################################################################################################################




def copy_player(p):
    new=player(p.game,p.team,p.generation)
    new.x=p.x
    new.y=p.y #ce sont les seuls paramètre qui changent à partir du début
    new.brain=nt.copy(p.brain)
    return new

def split(player,p=1):
    if rd.sample()<=p:
        new=copy_player(player)
        v=new.make_split_changes()
        if v=="fail":
            new.team.kill(new)
            return
        return new
    return


def load(game,filename):
    """format du fichier : couleur/position/brainfile/last_meal/generation"""
    #for filename in os.listdir(os.getcwd()+"/player_data"): pour tous les réccupérer un à un
    fichier=open(filename)
    couleur=fichier.readline()
    if couleur=="RED\n":
        team=red_team
    if couleur=="GREEN\n":
        team=green_team
    l2=fichier.readline()
    x=float(l2.split(" ")[0])
    y=float(l2.split(" ")[1])
    brainfile=fichier.readline().replace("\n","")
    last_meal=int(fichier.readline())
    generation=int(fichier.readline())
    fichier.close()

    new=player(game,team,generation)
    new.last_meal=last_meal
    new.brain=nt.load(brainfile)
    new.x=x
    new.y=y
    new.random_direction()
    new.random_position()
    succes=new.give_valid_location()
    if succes=="fail":
        new.team.kill(new)

def load_all(game):
    for filename in os.listdir(os.getcwd()+"/player_data"):
        load(game,"player_data/"+filename)


#revisiter les méthodes pour tuer ou faire se diviser
#pour les rouges changer la structure du cerveau
#tout reprogrammer
#enlever toutes les créations de listes