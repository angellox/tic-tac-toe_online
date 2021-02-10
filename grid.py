import pygame
import os

letterX = pygame.image.load(os.path.join('files_game/images', 'x_tic.png'))
letterO = pygame.image.load(os.path.join('files_game/images', 'o_tic.png'))
pygame.mixer.init()
pygame.init() 
_sound_library = {}

class Grid:
    def __init__(self):
        self.grid_lines = [((0,200),(600,200)),  #PRIMER LINEA HORIZONTAL
                           ((0,400),(600,400)),  #SEGUNDA LINEA HORIZONTAL
                           ((200,0),(200,600)),  #PRIMER LINEA VERTICAL
                           ((400,0),(400,600))]  #SEGUNDA LINEA VERTICAL
        
        self.grid = [[0 for x in range(3)] for y in range(3)] #LISTA DE COLUMNAS
        self.switch_player = True # BANDERA PARA RECONOCER AL JUGADOR QUE TIRA
        #print(self.grid)       
        # BUSCA DIRECCIONES  Norte    Noroe    Oeste   Suro     Sur   Sure    Este   Nore
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False
        self.string_player = ''
    
    def play_sound(self, path):
        global _sound_library, sound
        sound = _sound_library.get('files_game/audios/'+path)
        if sound == None:
            sound = pygame.mixer.Sound('files_game/audios/'+path)
            _sound_library[path] = sound  
        sound.play()

    def draw(self,screen):
        for line in self.grid_lines:
            pygame.draw.line(screen, (0,0,0), line[0], line[1], 3)
        
        for y in range(len(self.grid)): #DEL TAMAÑO DE LA MALLA
            for x in range(len(self.grid[y])): #DEL TAMAÑO DE CADA CELDA DE LA MALLA
                if self.get_cell_value(x, y) == "X": #SI ES X
                    screen.blit(letterX, (x*200, y*200)) # PINTA LA LETRA X
                     
                elif self.get_cell_value(x, y) == "O": # SI ES 0
                    screen.blit(letterO, (x*200, y*200)) # PINTA LA LETRA 0
                   
    
    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value #MODIFICA EL VALOR CONTENIDO EN LAS COLUMNAS (DEFAULT '0')
    
    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0: #NO SOBRESCRIBIR LA LETRA AL PULSAR DOS VECES EN ELLA
            self.set_cell_value(x, y, player)
            self.check_grid(x, y, player)

    def is_within_bounds(self, x, y):
        return x >= 0 and x < 3 and y >=0 and y < 3

    def check_grid(self, x, y, player):
        count = 1
        for index, (dirx, diry) in enumerate(self.search_dirs):
            if self.is_within_bounds(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.is_within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    if count == 3:
                        break
                if count < 3:
                    new_dir = 0
                    # LOCALIZANDO LOS INDICES EN LAS DIRECCIONES CONTRARIAS: 0-4 1-5 2-6 3-7 4-0 5-1 6-2 7-3
                    if index == 0:
                        new_dir = self.search_dirs[4] # N to S
                    elif index == 1:
                        new_dir = self.search_dirs[5] # NW to SE
                    elif index == 2:
                        new_dir = self.search_dirs[6] # W to E
                    elif index == 3:
                        new_dir = self.search_dirs[7] # SW to NE
                    elif index == 4:
                        new_dir = self.search_dirs[0] # S to N
                    elif index == 5:
                        new_dir = self.search_dirs[1] # SE to NW
                    elif index == 6:
                        new_dir = self.search_dirs[2] # E to W
                    elif index == 7:
                        new_dir = self.search_dirs[3] # NE to SW

                    if self.is_within_bounds(x + new_dir[0], y + new_dir[1]) \
                            and self.get_cell_value(x + new_dir[0], y + new_dir[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1

        if count == 3:
            print(player, 'wins!')
            self.string_player = player
            self.play_sound('replay.wav')
            self.game_over = True

        else:
            self.game_over = self.is_grid_full()

    def is_grid_full(self):
        for row in self.grid:
            for value in row:
                if value  == 0:
                    return False

        return True                

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    def print_grid(self):
        for row in self.grid:
            print(row)