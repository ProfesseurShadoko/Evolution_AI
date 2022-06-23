from settings import green,red

class team:
    def __init__(self,settings):
        self.name=settings.name
        self.settings=settings
        self.players=[]
        self.alive=0
    

    def add_player(self,player):
        self.players.append(player)
        if player.is_alive():
            self.alive+=1
    
    def size(self):
        return self.alive
    
    def clean(self):
        self.players=[player for player in self.players if player.is_alive()]
        self.alive=len(self.players)
    
    def kill(self,player):
        if player.is_alive():
            self.alive-=1
            player.living=False
    
    def reset(self):
        self.alive=0
        self.players=[]

green_team=team(green())
red_team=team(red())