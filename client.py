import pygame, os, socket, threading
from grid import Grid
import sys, time, pickle

HOST_CLIENT = '127.0.0.1'
PORT_CLIENT = 65432
os.environ['SDL VIDEO WINDOW POS'] = '200,100' #VENTANA EN WINDOWS
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4, #TCP Protocol
client.connect((HOST_CLIENT, PORT_CLIENT))
player = "O"
running = True
playing = "True"
turn = False

# LIBRERIA DE SONIDOS
_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get('files_game/audios/'+path)
    if sound == None:     
        sound = pygame.mixer.Sound('files_game/audios/'+path)
        _sound_library[path] = sound  
    pygame.mixer.stop()
    sound.play()

#def main():

pygame.mixer.init() #INICIALIZANDO PYGAME SOUND
pygame.init() #INICIALIZANDO PYGAME

screen = pygame.display.set_mode((610,610))
pygame.display.set_caption('Juego Multijugador: Tic - Tac - Toe: Jugador 2')

def create_thread(target):
    thread = threading.Thread(target = target)
    thread.daemon = True #CIERRA TODO AUTOMÁTICAMENTE
    thread.start()

def receive_data():
    global turn
    while True:
        data = client.recv(1024)
        data_msg = pickle.loads(data)
        x,y = data_msg[0], data_msg[1]
        if data_msg[2] == "Vas":
            turn = True
        if data_msg[3] == "False":
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            play_sound('cross.wav')
            grid.set_cell_value(x, y, "X")
        print(data_msg)

create_thread(receive_data)
grid = Grid()

# The game over delay
time_sum = 0
clock = pygame.time.Clock()

#grid.print_grid() #IMPRESIÓN DE LAS COLUMNAS DIBUJADAS DEL GRID BY CONSOLE.
font_size=40
font_size_ing = 10
    


#############################INTRO DEL JUEGO###############################################

# REPRODUCIR SONIDO INICIAL
play_sound('splash_intro.wav')

while font_size<90:
        
    font = pygame.font.Font('files_game/fonts/crackman.ttf', font_size)
    font_ing = pygame.font.Font('files_game/fonts/crackman.ttf', font_size_ing)
    text_ing = font_ing.render('FI - UNAM TELECOM', True, (209, 13, 13))
    screen.blit(text_ing, (305 - text_ing.get_width() // 2, 105 - text_ing.get_height()+200 // 2))

    text = font.render('Tic Tac Toe', True, (0, 0, 0))
    screen.blit(text, (305 - text.get_width() // 2, 350 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(100)
    font_size=font_size+5
    font_size_ing=font_size_ing+4
    if ((font_size==90) and (font_size_ing==50)):
            pygame.time.wait(1500)
    screen.fill(pygame.Color("white"),(10,10,590,590))
 
###################################################################################

while running:

    delta_time = clock.tick(60) # 60 fps
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            #return

        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]: #CLIC EN EL MOUSE IZQUIERDO (1,0,0) POSICION [0]
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos() #OBTENEMOS LA POSICIÓN DONDE SE HA HECHO CLIC
                    #print(pos[0] // 200, pos[1] // 200) DIVISIÓN QUE REGRESA SOLO ENTERO PARA SABER POSICIÓN DEL CLIC
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = "False"
                    movements = [cellX, cellY, "Vas", playing]
                    send_data = pickle.dumps(movements)
                    #send_data = '{}-{}-{}-{}'.format(cellX, cellY, "Vas", playing).encode()
                    client.send(send_data)
                    turn = False

        if event.type == pygame.KEYDOWN and grid.game_over:
            if event.key == pygame.K_SPACE:# and grid.game_over: #TECLEAR BARRA ESPACIADORA PARA LIMPIAR PANTALLA
                screen.fill((255, 255, 255))
                play_sound('re_enter.wav')
                grid.clear_grid() #LIMPIA PANTALLA DESPUÉS DE TERMINAR EL JUEGO.
                grid.game_over = False
                playing = "True"
                grid.string_player = 'X'

                time_sum = 0

            elif event.key == pygame.K_ESCAPE:#TECLEAR 'ESC' PARA SALIR DEL JUEGO-
                running = False
                grid.game_over = False

                #return

    if grid.game_over:

        if time_sum < 1500:
            time_sum += delta_time

            grid.draw(screen)
            pygame.display.update()
        else:
            font_sec = pygame.font.Font('files_game/fonts/gomarice_no_continue.ttf', 50)
            replay = font_sec.render('¿JUGAR DE NUEVO?', True, (118, 49, 145))
            yes = font_sec.render('SI: PRESIONE ESPACIO', True, (227, 25, 59))
            nop = font_sec.render('NO: PRESIONE ESC', True, (227, 25, 59))

            if grid.string_player == 'O':
                winner = font_sec.render('O GANÓ', True, (79, 214, 126))
                
            elif grid.string_player == 'X':
                winner = font_sec.render('PERDISTE', True, (79, 214, 126))
            
            else:
                winner = font_sec.render('', True, (79, 214, 126))

            screen.fill((255, 255, 255)) #RELLENAR PANTALLA EN BLANCO.
            screen.blit(replay, (305 - replay.get_width() // 2, 105 - replay.get_height() // 2))
            screen.blit(yes, (305 - yes.get_width() // 2, 305 - replay.get_height() // 2))
            screen.blit(nop, (305 - nop.get_width() // 2, 380 - replay.get_height() // 2))
            screen.blit(winner, (305 - winner.get_width() // 2, 450 - replay.get_height() // 2))
            pygame.display.update()

    else:
        grid.draw(screen)

    pygame.display.flip()

#main()