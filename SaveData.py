import csv

def save_game_settings_data(data):
     with open("game_settings.txt","w") as f:
       fw = csv.writer(f, lineterminator = '\n')
       fw.writerow([data[4]])
      
     with open("control_settings.txt","w") as f:
       fw = csv.writer(f,lineterminator = '\n')
       fw.writerow([data[0]])
       fw.writerow([data[1]])
       fw.writerow([data[2]])
       fw.writerow([data[3]])

def load_game_data():
     game_data = []
     with open('game_settings.txt','r') as g_file:
             g_file_reader = csv.reader(g_file)
             print()

             for line in  g_file_reader:                
                     game_data.append(line[0])
     return game_data

def load_high_score():
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
