from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from Field import Field
from Snake import Snake
from Obstacles import Obstacles
from GameAudio import Audio
from Jewell import Jewell
from Controls import Controls
import csv
import pprint

class Game(DirectObject):

    def __init__(self):
        
        self.controls = Controls()
        self.field =  Field(25,25)
        self.snake = Snake(self.field,self.controls.control_keys)
        self.obstacle = Obstacles(self.field)
        self.jewell =  Jewell(self.field)
        self.score = 0
        self.bgame_over = False
        self.level = 1
        self.level_jump = 0
        self.level_bar = 0
        #self.audio = Audio()
        self.current_high_score = 0
        taskMgr.add(self.update, "UpdateGame")
       
    def set_level(self):
        self.snake.speed_lim = (self.snake.speed_lim*(1-(5.0/100.0))**((3*self.level)))
        self.level_jump = self.level
        return
    def pause_game(self):

        self.snake.pause()
        taskMgr.remove('UpdateGame')
        
    def resume_game(self):

        self.snake.resume()
        taskMgr.add(self.update, "UpdateGame")
        
    def save_game(self):

        with open('saved_game.txt','w') as save_game_file:

             save_game_file_writer = csv.writer(save_game_file,lineterminator = '\n')
             save_game_file_writer.writerow(str(self.score))
             save_game_file_writer.writerow([int(self.obstacle.type)])
             save_game_file_writer.writerow([int(self.jewell.model.getX()),int(self.jewell.model.getZ())])
             save_game_file_writer.writerow([int(self.snake.head.model.getX()),int(self.snake.head.model.getZ()),int(self.snake.head.model.getR())])
             for n in range(1,len(self.snake.nodes)):

                 save_game_file_writer.writerow([int(self.snake.nodes[n].model.getX()),int(self.snake.nodes[n].model.getZ())])
             print(str(self.jewell.model.getX()))
             print('Data_Saved')
        self.save_high_score()
        return
    
    def load_game(self,game_data):

        self.jewell.destroy()
        self.obstacle.destroy() 
        self.obstacle = Obstacles(self.field,int(game_data[1][0]))
        self.jewell =  Jewell(self.field)
        self.snake.pause()
        scr = ''
        for x in game_data[0]: scr = scr + x
        self.score = int(scr)
        if self.score > 0: self.level = int(self.score/3)
        self.snake.speed_lim = (self.snake.speed_lim*(1-(5.0/100.0))**(self.score - 1))
        self.snake.head.model.setPos(int(game_data[3][0]),38,int(game_data[3][1]))
        self.snake.head.model.setR(int(game_data[3][2]))
        self.snake.load_body(game_data[4:])
        self.jewell.place_jewell([int(game_data[2][0]),int(game_data[2][1])])
        self.current_high_score = self.load_high_score()
        #print(game_data[4:])
       
        return
    
    def game_over(self):
        
        taskMgr.remove('UpdateGame')
        self.save_high_score()
        self.jewell.destroy()
        self.obstacle.destroy()
        self.field.destroy()
        self.bgame_over = True
        self.jewell = None
        self.obstacle = None
        self.filed = None
        self.snake = None
        self.controls = None
        return
            
       
    def save_high_score(self):
        if(self.current_high_score < self.score):
           with open('high_score.txt','w') as save_high_score_file:
               save_high_score_writer = csv.writer(save_high_score_file,lineterminator = '\n')
               save_high_score_writer.writerow(str(self.score))
                 
        return

    def load_high_score(self):
        with open('high_score.txt','r') as high_score_file:
             hs_file_reader = csv.reader(high_score_file)
             current_high_score_string = ""
             for line in  hs_file_reader:                
                     current_high_score_row = line
             for c in current_high_score_row:
                 if c != ",":
                    current_high_score_string = current_high_score_string + c
             current_high_score = int(current_high_score_string)
             
                     
        return current_high_score
            
        
        
    def update(self,task):
        
        if self.snake.found_jewell:
            self.jewell.destroy()
            self.score += 1
            self.level_bar = +1
            self.jewell = Jewell(self.field)
            self.snake.found_jewell = False
            if self.score > 3: self.level = int(self.score/3) + self.level_jump
            self.snake.speed_lim = self.snake.speed_lim  - ((5.0/100.0)*self.snake.speed_lim)
        if not self.snake.alive:
            self.game_over()
        return task.cont
        


        
