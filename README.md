# Evolution_AI

## Installation

Clone this repository on your computer

```bash
  git clone  https://github.com/ProfesseurShadoko/Evolution_AI
```

Make shure you have pygame and pyautogui installed, else run :

```bash
  pip install pygame
  pip install pyautogui
```


## Documentation

Simply run 
```
  python run.py
```
and press key 'd' for a demo.

## Some explanations

I just wanted to see if it was possible to simulate natural selection. So I implemented a very simple ecosystem : red players that split when they eat, green players that split when they survive long enough. They all have a brain (a simple matrix) with input the angle at wich they see a player from the other color, and output if weather they have to turn left or right.<br>
At the start, their brains are empty. But each time the 'split', small random changes are made to their brain, hoping that a better brain will survive better and that its many children will inherit from this brain. <br>
The result is a success, with red players being able to hunt down green players, who try to run away from them. <br>
<br>
**So watch and enjoy !**<br>
https://user-images.githubusercontent.com/94191158/204925634-dda350fb-d386-46f3-bdb6-57fda00e9d5d.mp4

