

class team:
    def __init__(self,name):
        self.name=name
        self.players=[]

    def add_player(self,player):
        self.players.append(player)
    
    def __str__(self):
        return f"Equipe {self.name} : {len(self.players)} membres"

class red:
    def __init__(self,team):
        self.team=team
        self.team.add_player(self)
        self.name="Joueur rouge"
    
    def __str__(self):
        return f"{self.name} fait partie de l'équipe {self.team.name}"
    
if __name__=="__main__":
    red_team=team("red")
    red_player1=red(red_team)
    print(red_player1.team)
    red_player2=red(red_team)
    print(red_player2.team)
    print(red_team)
    print(red_player1==red_player1)
