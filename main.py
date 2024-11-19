# /// script
# dependencies = [
#   "pygame_textinput",
#   "platform",
#   "json"
# ]
# ///
 # import Pygame Paket
import os  # import Paket Betriebssystem
import sys  # import Paket System
import math
import random
import ctypes
import asyncio
import pygame
from pygame.locals import *
if __import__("sys").platform == "emscripten":
    from platform import window
import pygame_textinput
import platform
import json

print("Version 1")


Liste_res =[(2,"960x540"),(1.5,"1280x720"),(1.2,"1600x900"),(1,"1920,1080")]

global n_resolution
#n_resolution = window.localStorage.getItem("n_resolution")
n_resolution = int(1)
#if n_resolution == None:
window.localStorage.setItem("n_resolution",n_resolution)
s = Liste_res[n_resolution%4][0]


#region variabeln
#initialisierung

canvas_width = int(1920/s) # Breite des Leinwand
canvas_height = int(1080/s) # Höhe des Leinwand
frames_per_second = 60



boden = int(150/s)


# Farbdefintionen
#            R    G    B
WHITE =     (255, 255, 255)
BLACK =     (0,     0,   0)
GRAY =      (100, 100, 100)
RED =       (255, 000,   0)
GREEN =     (  0, 255,   0)
BLUE =      (  0,   0, 255)
LIGHT_GRAY =(200, 200, 200)


font_arial = "arial"

how_text =[ "Hallo!",
            "Du musst mich so lange wie möglich vor den Angriffen des Drachen beschützen.",
            "Pass gut auf: Der Drache hat verschiedene Attacken, die dir Leben abziehen.",
            "Außerdem befinden wir uns in einer Höhle, wo gelegentlich Stalaktiten herabfallen,",
            "die dir ebenfalls schaden können. Am Anfang hast du eine bestimmte Anzahl an Leben.",
            "Wenn du getroffen wirst, verlierst du ein Leben. Hast du keine Leben mehr,",
            "ist das Spiel vorbei. In regelmäßigen Abständen erscheinen Herzen an verschiedenen",
            "Stellen auf dem Boden oder knapp darüber. Sammle sie ein, um Leben zurückzugewinnen.",
            "Hier ist die Steuerung:",
            "Bewege mich nach links mit „A“ und nach rechts mit „D“.",
            "Mit der Leertaste springst du. Wenn du die Leertaste drückst, ",
            "während du in der Luft bist, machst du einen Doppelsprung.Nun liegt es an dir,",
            "mir beim Überleben zu helfen! Ich will so lange wie möglich durchhalten! :)"]
how_text_eng =[ "Hello!",
            "I need you to protect me from the dragons attacks for as long as possible.",
            "Watch out carefully: The dragon has various attacks that drain your life.",
            "We are also in a cave where stalactites occasionally fall down",
            "which can also damage you. You have a certain amount of life at the beginning.",
            "If you get hit, you lose a life. If you have no more lives,",
            "the game is over. Hearts appear at regular intervals at various",
            "places on the ground or just above it. Collect them to regain lives.",
            "Here are the controls:",
            "Move to the left with ‘A’ and to the right with ‘D’.",
            "Use the space bar to jump. If you press the space bar ",
            "while you are in the air, you do a double jump, now it's up to you",
            "to help me survive! I want to last as long as possible! :)"]

#logic
#movement

max_speed_x = 9/s
x_beschleunigung = 1.2/s
counter_x_beschleunigung = 2/s

max_speed_y = 12/s
Schwerkraft = 0.3/s
max_jumps = 2
jump_beschleunigung = 7/s
jump_time = 12
jump_nerf = 0.5

pound = 20


unsterblichkeits_time = 20

#objekte:

#bullet:
bullet_Hwidth,bullet_Hheigth = 15/s,15/s

#player
player_Hwidth, player_Hheight = 30/s, 50/s




#ATTACKEN:
spawn_y = 230/s


#dif:
divisor = 4800
exponent = 1.0
speedeffect = 0.2
timeeffect  = 1

#attacke 1: Randomkreis
damage1 = 1
anzahl1 = 15
speed1 = 10/s
zeit1 = 120

#attacke 2: in richtung ritter
damage2 = 1
anzahl2 = 5
zeitwellen2 = 5
speed2 = 80*s
zeit2 = 60

#attacke 3: flach in richtung ritter
damage3 = 1
anzahl3 = 5
speed3 = 80*s
zeit3 = 200

#attacke 4: flach mehrmals in richtung ritter
damage4 = 1
anzahl4 = 3
anzahlwellen4 = 3
zeitwellen4 = 15
speed4 = 80*s
zeit4 = 140

#attacke 5: spirale in all richtungen
damage5 = 1
anzahl5 = 9
anzahlwellen5 = 6
zeitwellen5 = 15
speed5 = 50*s
zeit5 = 120


#attacken 6: stalaktiten
damage6 = 3
anzahl6 = 10
speed6 = 10/s
zeit6 = 200


#boden attacke:
damageBoden = 1
anzahlBoden = 4
speedBoden = 9/s

#heal:
heal_t_max = 1200
heal_t_min = 300
heal = 2
heallebenszeit = 600
#endregion
'''
Quellen:
v=BHr9jxKithk&t=120s&ab_channel=CodingWithRuss für Kollision
https://stackoverflow.com/questions/8265583/dividing-python-module-into-multiple-regions
https://stackoverflow.com/questions/31538506/how-do-i-maximize-the-display-screen-in-pygame
https://www.geeksforgeeks.org/how-to-get-the-size-of-pygame-window/
https://www.youtube.com/watch?v=GMBqjxcKogA&ab_channel=baraltech
https://www.pygame.org/docs/ref/music.html
https://www.pygame.org/docs/ref/surface.html#pygame.Surface.convert_alpha
'''
# Alle wichtigen initialisierungen
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
pygame.init()
fpsclock = pygame.time.Clock()  # Variable zur Speicherung der Bildwiderholung
display = pygame.display.set_mode((canvas_width, canvas_height), DOUBLEBUF, 32)  # setze den Spielmodus
pygame.mixer.init()
pygame.mixer.set_num_channels(20)
textinput = pygame_textinput.TextInputVisualizer()


display.convert()
#https://stackoverflow.com/questions/73268410/getting-display-resolution-with-python-isnt-accurate


frames_per_second = 60
global main_menu,play_menu,end_menu,options_menu,how_menu
main_menu = True
play_menu = False
end_menu = False
options_menu = False
how_menu = False
#region funktionen
def get_names_ranks_scores(data):
    """
    Extracts names, ranks, and scores from a leaderboard structure.

    Parameters:
        data (dict): A dictionary representing the leaderboard.

    Returns:
        list: A list of tuples containing (rank, name, score).
    """
    try:
        # Navigate to the "entry" key
        entries = data["dreamlo"]["leaderboard"]["entry"]

        # If `entries` is a dict (single entry), convert it to a list
        if isinstance(entries, dict):
            entries = [entries]

        # Enumerate to get the rank (starting from 1)
        names_ranks_scores = [
            (index + 1, entry["name"], int(entry["score"]))  # Convert score to integer
            for index, entry in enumerate(entries)
        ]
        return names_ranks_scores
    except KeyError as e:
        print(f"Missing key in data structure: {e}")
        return []
    except ValueError as e:
        print(f"Invalid score value: {e}")
        return []
def objekt(Asset, pos_x, pos_y, width, height, Hwidth, Hheight): #objekte erstellen:
    display.blit(Asset, (pos_x - width / 2, pos_y - height / 2)) #rendered das bild zentirert

    Hitbox = pygame.Rect(pos_x - Hwidth / 2, pos_y - Hheight / 2, Hwidth, Hheight) #erstellt eine entsprechende hitbox
    return Hitbox

#entities list format   [ausehen(0), position x (1), position y (2), x bewegung (3), y bewegung (4), breite (5), höhe (6),
                        #lebenszeit (7 ),hitbox breite (8), hitbox höhe (9), hitbox(10), damage (11)]

def entity(Asset, spawn_x, spawn_y, x_speed, y_speed, width, height, Hwidth, Hheigth, Lebenszeit, liste, damage): #restellt ein entitie und fügt es der entsprechenden liste zu
    liste.append([Asset, spawn_x, spawn_y, x_speed, y_speed, width, height, Lebenszeit, Hwidth, Hheigth, None, damage])
    return liste



def processentities(liste): #verarbeitung der enteties
    for bullet in liste:
        if bullet[7] > 0:#
            bullet[1] += bullet[3] #x bewegung
            bullet[2] += bullet[4] #y bewegung
            bullet[7] -= 1  #Lebenszeit
            bullet[10] = objekt(bullet[0], bullet[1], bullet[2], bullet[5], bullet[6], bullet[8], bullet[9]) #erstellt ein entsprechendes objekt
        else:
            liste.remove(bullet)#wenn lebenszeit vorbei ist löschen
        if bullet[1] < -100 or bullet[1] > (canvas_width + 100) or bullet[2] < -100 or bullet[2] > canvas_height:  # kugeln entferenen um leistung zu verbessern
            liste.remove(bullet)
    return liste

def angle(rando,winkel,start,end,faktor): #winkel berechnung zu y und x beschleunigung
    if rando == True:
        angle = random.uniform(start,end)

    else:
        angle = winkel
    x = math.cos(math.radians(angle))*faktor
    y = math.sin(math.radians(angle))*-faktor
    return x,y

#https://www.w3schools.com/python/module_random.asp
#https://www.w3schools.com/python/ref_math_degrees.asp

def track(x,y,start_x,start_y,faktor): #x und y finden um player zu treffen
    x_speed = (x - start_x)/faktor
    y_speed = ((y - start_y)/faktor)
    return x_speed,y_speed


#die text funktion aus dem pygame intro wurde korrigiert mit der prompt "korrigiere die text funktion für die buttons"CHATGPT
def draw_text(display, xy=(0, 0), text='', colour=(255, 0, 0), size=16, centered=True):
    """Draws text on the Pygame display at the specified position.
    Args:
        display: The Pygame display surface.
        xy: Tuple for the x and y position.
        text: The text string to display.
        colour: The color of the text.
        size: Font size.
        centered: If True, centers the text at (x, y); if False, uses (x, y) as the top-left corner.
    """
    font = pygame.font.SysFont(name="arial", size=size, bold=True)
    render_text = font.render(text, True, colour)
    # Center the text if centered=True
    if centered:
        text_rect = render_text.get_rect(center=xy)
    else:
        text_rect = render_text.get_rect(topleft=xy)

    display.blit(render_text, text_rect)


#die Button class wurde generiert mit der prompt. "wie kann ich buttons mit pygame machen" CHATGPT
class Button:

    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font_size):
        # Center the button around (x, y)
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size

    def draw(self, screen):
        # Change color if mouse hovers over button
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # Center the text within the button
        font = pygame.font.SysFont(font_arial, self.font_size, bold=True)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)  # Center text within the button rect
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # Check if the button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            #pygame.mixer.Sound("sfx/click.ogg").play()
            return True
        return False

#https://stackoverflow.com/questions/2081836/how-to-read-specific-lines-from-a-file-by-line-number
#https://www.w3schools.com/python/python_file_write.asp




def play():
    global main_menu, play_menu, end_menu, options_menu, how_menu
    main_menu = False
    play_menu = True
    end_menu = False
    options_menu = False
    how_menu = False

def Mainmenu():
    global main_menu, play_menu, end_menu, options_menu, how_menu
    main_menu = True
    play_menu = False
    end_menu = False
    options_menu = False
    how_menu = False
def Gameover():
    global main_menu, play_menu, end_menu, options_menu, how_menu
    main_menu = False
    play_menu = False
    end_menu = True
    options_menu = False
    how_menu = False
def options():
    global main_menu, play_menu, end_menu, options_menu, how_menu
    main_menu = False
    play_menu = False
    end_menu = False
    options_menu = True
    how_menu = False
def how():
    global main_menu, play_menu, end_menu, options_menu, how_menu
    main_menu = False
    play_menu = False
    end_menu = False
    options_menu = False
    how_menu = True
def apply_colorkey(path, size_xy = (), colorkey = (0,255,0)):
    image = pygame.transform.scale(pygame.image.load(path),size_xy)
    new_image =  pygame.surface.Surface(size_xy)
    new_image.fill(colorkey)
    new_image.blit(image,(0,0))
    new_image.set_colorkey(colorkey)
    return new_image




#endregion

#region assets: Alle bilder und sounds
#region images
bullet_width, bullet_height = 40/s, 40/s
#https://www.pygame.org/docs/ref/transform.html für das scalieren der bilder data/data/bullethellarenabrowser/

bullet_skin = apply_colorkey('img/bullet.png',(bullet_width, bullet_height))
spike_width, spike_height = 36/s, 54/s
spike_skin = apply_colorkey('img/spike.png',(spike_width, spike_height))
player_width, player_height = 80/s, 100/s


global player_skin #spieler Ausehen

player_skin_right = apply_colorkey('img/Player.png',(player_width,player_height))
player_skin_left = pygame.transform.flip(player_skin_right,1,0)
player_skin_standing_right = apply_colorkey('img/PlayerStanding.png',(player_width,player_height))
player_skin_standing_left = pygame.transform.flip(player_skin_standing_right,1,0)

player_skin = player_skin_standing_right

boss_width, boss_height = 300/s,300/s

boss_skin = apply_colorkey('img/Boss.png',(boss_width, boss_height))
heal_width, heal_height = int(70/s), int(70/s)
heal_skin = apply_colorkey('img/heart.png',(heal_width, heal_height))
heart_width, heart_height = int(40/s), int(40/s)
heart_skin = apply_colorkey('img/heart.png',(heart_width, heart_height))
#Menu assets
main_menu_BG = pygame.transform.smoothscale(pygame.image.load('img/main_menu_BG.png'), (canvas_width,canvas_height)).convert()
menu_BG2 = pygame.transform.scale(pygame.image.load('img/MenuBG2.png'), (canvas_width, canvas_height)).convert()
game_BG = pygame.transform.scale(pygame.image.load('img/Game_BG.png'), (canvas_width, canvas_height)).convert()
board_skin = pygame.transform.scale(pygame.image.load('img/Board.png'), (450/s, 450/s)).convert_alpha().convert_alpha()
speech_skin = pygame.transform.smoothscale(pygame.image.load('img/SpeechBubble.png'), (1700/s,1200/s)).convert_alpha()
titel_skin = pygame.transform.smoothscale(pygame.image.load('img/Titel.png'), (650/s,400/s)).convert_alpha()
boden_skin = apply_colorkey('img/Floor.png',((canvas_width,180/s)))
#endregion
#region sounds

jump_sound = pygame.mixer.Sound("sfx/jump.ogg")
death_sound = pygame.mixer.Sound("sfx/Death_sound.ogg")
heal_sound = pygame.mixer.Sound("sfx/Heal_sound.ogg")
fireball_sound = pygame.mixer.Sound("sfx/Fireball_sound.ogg")
stone_sound = pygame.mixer.Sound("sfx/smal_rock_break_sound.ogg")
click_sound = pygame.mixer.Sound("sfx/click.ogg")
running_sound = pygame.mixer.Sound("sfx/Running.ogg")
hurt_sound = pygame.mixer.Sound("sfx/hurt.ogg")
Mainmenu_theme = pygame.mixer.Sound("sfx/MainTheme.ogg")
game_theme = pygame.mixer.Sound("sfx/Backround_music.ogg")

def Set_volumen(global_volume,music_volume): #Volumen verändernte funktion
    Mainmenu_theme.set_volume(music_volume)
    game_theme.set_volume(music_volume)
    heal_sound.set_volume(global_volume)
    jump_sound.set_volume(global_volume)
    death_sound.set_volume(global_volume)
    fireball_sound.set_volume(global_volume)
    stone_sound.set_volume(global_volume/20)
    click_sound.set_volume(global_volume)
    running_sound.set_volume(global_volume/1.8)
    hurt_sound.set_volume(global_volume)
# endregion
# endregion

#Globale Variabeln
global devmode
devmode = False

global n_language
n_language = window.localStorage.getItem("n_language")
print(type(n_language))
if n_language == None or type(n_language) == None:
    window.localStorage.setItem("n_language", 2)
n_language = int(window.localStorage.getItem("n_language"))
global volume
volume = window.localStorage.getItem("volume")
if volume == None or type(volume) == None:
    window.localStorage.setItem("volume", 0.5)
volume = float(window.localStorage.getItem("volume"))
global music_volume
music_volume = window.localStorage.getItem("music_volume")
if music_volume == None or type(music_volume) == None:
    window.localStorage.setItem("music_volume", 0.5)
music_volume = float(window.localStorage.getItem("music_volume"))

global score
score = window.localStorage.getItem("score")
if score == None or type(score) == None:
    window.localStorage.setItem("score", 0.0)
score  = float(window.localStorage.getItem("score"))
global highscore
highscore = window.localStorage.getItem("highscore")
if highscore == None or type(highscore) == None:
    window.localStorage.setItem("highscore", 0.0)
highscore = float(window.localStorage.getItem("highscore"))

global Name
Name = window.localStorage.getItem("Name")
if Name == None:
    window.localStorage.setItem("Name", "Guest")
Name = window.localStorage.getItem("Name")

global Mainmusic
Mainmusic = True

main_menu, play_menu, end_menu, options_menu, how_menu = True,False ,False ,False ,False
async def play_loop():
    global main_menu, play_menu, end_menu, options_menu, how_menu
    global volume
    global player_skin
    global music_volume
    global score
    global highscore

    Set_volumen(volume,music_volume)
    pygame.mouse.set_visible(False) #https://stackoverflow.com/questions/49889064/how-can-i-make-the-cursor-invisible-but-still-allow-it-to-retain-a-x-and-y-valu
    frames_per_second = 60
    run = True

    #attacken
    attack_t = 10
    attackrunning = False
    n_temp = 1
    dif = 1

    #spawn
    x_pos = int(canvas_width / 2)
    y_pos = canvas_height+boden+player_height/2 +1

    #movement variabeln
    y_speed = 0.0
    x_speed = 0.0
    old_x_speed = 0.0
    right = False
    left = False
    floor = False
    jump = False
    jumps = 0

    #Zeitliche variabeln
    t_unsterblich = 0
    health = 10

    heal_t = 100
    jump_timer = 0
    t_right = 0
    t_left = 0
    zeit = 0
    t_run = 0

    bullets = []
    cheat_counter = 0

    #endregion
    game_theme.play(loops=True)

    while run == True: #Hauptgame schleife
        #region inputs: Inputs für das Spiel
        for event in pygame.event.get():
            # beende Pygame mit der Maus oder der Taste Escape

            if event.type == pygame.KEYDOWN: #jump Inputs
                if (event.key == pygame.K_SPACE or event.key== pygame.K_UP or event.key== pygame.K_w) and jumps < max_jumps :
                    jump_timer = 0
                    jump = True
                    jumps += 1
                    floor = False
                    jump_sound.play()

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:#links rechts gedrückt
                    if right == False:
                        t_right = zeit
                    right = True
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                    player_skin = pygame.transform.flip(player_skin, 1, 0)
                    if left == False:
                        t_left = zeit
                    left = True
                if event.key == pygame.K_r: #reset
                    health = 0

                if devmode: #Testmodus spezial tasten
                    if event.key == pygame.K_h:
                        health = 1000
                    if event.key == pygame.K_n:
                        zeit += 600

            #Tasten nichtmehr gedrückt
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    jump = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right = False
                    t_left = zeit
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left = False
                    t_right = zeit
        #endregion

        #region movement: Spieler Bewegung
        if jump and jump_timer < jump_time:#sprung
            y_speed -= (jump_beschleunigung - jump_nerf*(jumps-1))
            if y_speed <= -max_speed_y:
                y_speed = -max_speed_y
        jump_timer += 1
        #rechts bewegung
        if (right and t_right > t_left):
            #laufanimation
            if floor:
                if zeit%5 == 0:
                    player_skin = player_skin_right
                if zeit%10 == 0:
                    player_skin = player_skin_standing_right
            else:
                player_skin = player_skin_right
            if x_speed < 0 and floor:#entschnleunigung
                x_speed +=counter_x_beschleunigung
            else:
                x_speed += x_beschleunigung
            if x_speed > max_speed_x:#limit
                x_speed = max_speed_x
        #links bewegung
        if (left and t_right < t_left):
            #laufanimation
            if floor:
                if zeit%5 == 0:
                    player_skin = player_skin_standing_left
                if zeit%10 == 0:
                    player_skin = player_skin_left
            else:
                player_skin = player_skin_left
            if x_speed > 0 and floor:#entschleunigung
                x_speed -=counter_x_beschleunigung
            else:
                x_speed -= x_beschleunigung
            if x_speed < -max_speed_x:#limit
                x_speed = -max_speed_x

        #entschleunigung wenn kein input
        if left == False and right == False:
            if t_right < t_left:
                player_skin = player_skin_standing_right
            if t_right > t_left:
                player_skin = player_skin_standing_left
            if x_speed > 0:
                if x_speed -1 <= 0:
                    x_speed = 0
                else:
                    x_speed -= 1
            if x_speed < 0:
                if x_speed +1 >= 0:
                    x_speed = 0
                else:
                    x_speed += 1

        #Boden kollision
        if floor or y_pos + y_speed > canvas_height-boden-(player_height/2):
            floor = True
            jumps = 0
            y_speed = 0
            y_pos = canvas_height-boden-(player_height/2)
        else:
            floor = False
            y_speed += 1
            y_pos += y_speed
        #Wandkollision

        x_pos += x_speed
        old_x_speed = x_speed
        if x_pos + x_speed> canvas_width - (player_width/2):
            x_pos = canvas_width - (player_width/2)
            x_speed = 0
        if x_pos + x_speed < (player_width/2):
            x_pos = player_width/2
            x_speed = 0

        #Renn Sound
        if y_pos > canvas_height-boden-player_height/2 - 10/s and (right or left):
            if t_run%144 == 0:
                running_sound.play()
            t_run += 1
        else:
            running_sound.stop()
            t_run = 0

        #endregion
        #region render

        display.blit(game_BG,(0,0))#Hintergrund
        objekt(boss_skin,(canvas_width / 2)-5*math.cos(zeit/33*s)/s, 200/s-10*math.sin(zeit/20)/s, boss_width, boss_height, boss_width, boss_height) #Drachen rendern
        bullets = processentities(bullets) #Kugeln und heilung rendern und verarbeiten
        player = objekt(player_skin, x_pos, y_pos, player_width, player_height,player_Hwidth,player_Hheight)#spieler rendern
        if devmode:
            pygame.draw.rect(display,GREEN,player)#spieler hitbox

        for bullet in bullets: #kollisions dedektion
            if devmode:
                pygame.draw.rect(display,RED,bullet[10])#kugel hitboxes
            if player.colliderect(bullet[10]) and 0 > t_unsterblich:#treffer logik
                print('treffer')
                health -= bullet[11]
                bullets.remove(bullet)
                t_unsterblich = unsterblichkeits_time
                if bullet[11] < 0:
                    heal_sound.play()
                else:
                    hurt_sound.play()

            if bullet[1] < -100 or bullet[1] > (canvas_width+100) or bullet[2] < -100 or bullet[2] > canvas_height: #kugeln entferenen um leistung zu verbessern
                bullets.remove(bullet)
            for b in bullets: #stalaktiten geräusch
                if b[0] == spike_skin and b[2] >= canvas_height - boden + spike_height / 2 and b[2] <= canvas_height - boden + (speed6 * difspeed) + spike_height / 2:
                    stone_sound.play()
                    break
        t_unsterblich -= 1
        #region attacken
        if attack_t <= 0:
            if attackrunning == False:
                attacke = random.randint(1,6)#attacken selektion
            #random kreis
            if attacke == 1:
                fireball_sound.play()
                for i in range(anzahl1):
                    x_bullet, y_bullet = angle(True, 0, 180, 360, speed1*difspeed)
                    entity(bullet_skin, canvas_width / 2, spawn_y, x_bullet, y_bullet, bullet_width, bullet_height,bullet_Hwidth,bullet_Hwidth,1000, bullets, damage1)
                attack_t = zeit1/(dif*timeeffect)

            #in richtung ritter
            if attacke == 2:
                if n_temp == 1:
                    fireball_sound.play()
                if attackrunning == False:
                    n_temp = (anzahl2-1)*zeitwellen2
                if round(n_temp%zeitwellen2) == 0:
                    x_bullet, y_bullet = track(x_pos, y_pos, canvas_width / 2, 100/s, speed2/difspeed)
                    entity(bullet_skin, canvas_width / 2, spawn_y, x_bullet, y_bullet, bullet_width, bullet_height, bullet_Hwidth, bullet_Hheigth, 1000, bullets, damage2)
                n_temp -=1
                if n_temp < 0:
                    attack_t = zeit2/(dif*timeeffect)
                    attackrunning = False
                else:
                    attackrunning = True

            #flach in richtung ritter
            if attacke == 3:
                if n_temp == 1:
                    fireball_sound.play()
                for i in range(anzahl3):
                    i -= int(anzahl3-1/2)
                    x_bullet, y_bullet = track(x_pos+i*60, y_pos, canvas_width / 2, 100/s, speed3/difspeed)
                    entity(bullet_skin, canvas_width / 2, spawn_y, x_bullet, y_bullet, bullet_width, bullet_height, bullet_Hwidth, bullet_Hheigth, 1000, bullets, damage3)
                attack_t = zeit3/(dif*timeeffect)

            #flach mehrmals in richtung ritter
            if attacke == 4:
                if n_temp == 1:
                    fireball_sound.play()
                if attackrunning == False:
                    n_temp = (anzahlwellen4-1)*zeitwellen4
                if round(n_temp%zeitwellen4) == 0:
                    for i in range(anzahl4):
                        i -= int(anzahl4-1/2)
                        x_bullet, y_bullet = track(x_pos+i*(60/(dif/2)), y_pos, canvas_width / 2, 100/s, speed4/difspeed)
                        entity(bullet_skin, canvas_width / 2, spawn_y, x_bullet, y_bullet, bullet_width, bullet_height, bullet_Hwidth, bullet_Hheigth, 1000, bullets, damage4)
                n_temp -= 1
                if n_temp < 0:
                    attack_t = zeit4/(dif*timeeffect)
                    attackrunning = False
                else:
                    attackrunning = True

            #spirale in all richtungen
            if attacke == 5:
                if n_temp == 1:
                    fireball_sound.play()
                if attackrunning == False:
                    n_temp = (anzahlwellen5-1)*zeitwellen5
                if round(n_temp%zeitwellen5) == 0:
                    for i in range(anzahl5):
                        x_bullet, y_bullet = angle(False, 180 + (i * 360/anzahl5) + (n_temp * anzahl5), 0, 0, 5*difspeed)
                        entity(bullet_skin, canvas_width / 2, spawn_y, x_bullet, y_bullet, bullet_width, bullet_height, bullet_Hwidth, bullet_Hheigth, 1000, bullets, damage5)
                n_temp -= 1
                if n_temp < 0:
                    attack_t = zeit5/(dif*timeeffect)
                    attackrunning = False
                else:
                    attackrunning = True

            #stalaktiten
            if attacke == 6:
                n_temp = anzahl6*dif
                if n_temp > 20:
                    n_temp = 20
                for i in range(int(n_temp)):
                    entity(spike_skin,random.randint(0,canvas_width),0,0,speed6*difspeed,spike_width,spike_height,spike_width-20,spike_height,1000,bullets,damage6)
                attack_t = zeit6/(dif*timeeffect)

            if attackrunning == False:#boden zwischen attacken
                fireball_sound.play()
                n_temp = random.randint(1,2)
                if n_temp == 1:
                    for i in range(anzahlBoden):
                        entity(bullet_skin, 0-i*30/s,canvas_height-boden- 30/s, speedBoden*difspeed, 0, bullet_width, bullet_height, bullet_Hwidth, bullet_Hheigth, 1000, bullets, damageBoden)
                if n_temp == 2:
                    for i in range(anzahlBoden):
                        entity(bullet_skin, 0+i*30/s+canvas_width,canvas_height-boden- 30/s, -speedBoden*difspeed, 0, bullet_width, bullet_height, bullet_Hwidth, bullet_Hheigth, 1000, bullets, damageBoden)

        attack_t -= 1
        #schwierigkeits skalierung
        dif = ((zeit/divisor)**exponent+1)
        difspeed = ((zeit/divisor)**exponent)*speedeffect +1

        if heal_t <= 0: #heilungs spawning
            entity(heal_skin,random.randint(heal_width,int(canvas_width-heal_width/2)),random.randint(int(canvas_height-boden-heal_width/2-200/s),int(canvas_height-boden-heal_height/2)),0,0,heal_width,heal_height,heal_width,heal_height,heallebenszeit,bullets,-2)
            heal_t = random.randint(heal_t_min,heal_t_max)
        heal_t -= 1

        display.blit(boden_skin,(0,canvas_height-boden-5/s))
        #lebens anzeige
        draw_text(display,[40/s,canvas_height-50/s-boden/2],f'{health:.0f} hp',WHITE,int(50/s),False)
        for i in range(health):
            if i > 50:
                break
            objekt(heart_skin,60+i*45/s,canvas_height+30/s-boden/2,heart_width,heart_height,heart_width,heart_height)

        if health <= 0:#game fail
            score = round((zeit/60),4)
            if cheat_counter > 900 or devmode:
                score = 0.0
            if score > highscore:
                highscore = score
            window.localStorage.setItem("score", score)
            window.localStorage.setItem("highscore", highscore)
            if Name != "Guest":
                async with platform.fopen(f"http://dreamlo.com/lb/7VRjmV2gJ0-lO1aOP32Ylw3wEgu-zcX0ayGuz4fj8hCQ/add/{Name}/{int(score*1000)}", "r") as file:
                    data = file.read()



            pygame.mixer.stop()
            Gameover()
            run = False

        zeit += 1
        draw_text(display, [10/s, 10/s], f'{(zeit/frames_per_second):.3f}s', WHITE, int(70/s),False)
        draw_text(display, [canvas_width-180/s, 10/s], f'fps: {fpsclock.get_fps():.1f}', WHITE, int(40/s), False)
        draw_text(display, [canvas_width - 180 / s,40 / s], str(x_speed), WHITE, int(40 / s),False)
        #devmodus anzeigen
        if devmode:
            draw_text(display, [10/s, 100/s], 'dif: '+ str(round(dif,4)), WHITE, int(40/s), False)
            draw_text(display, [10/s, 180/s], 'speeddif: '+ str(round(difspeed,4)), WHITE, int(40/s), False)
            draw_text(display, [10/s, 260/s], 'entities: ' + str(len(bullets)), WHITE, int(40/s), False)
            draw_text(display, [10/s, 340/s], f'fps = {fpsclock.get_fps():.1f}', WHITE, int(40/s), False)

        #Dedektion um zu scheuen das niemand tiefe fps ausnutzen kann
        if fpsclock.get_fps() < 35:
            cheat_counter += 4
        else:
            cheat_counter -= 1
        if cheat_counter > 900:
            draw_text(display, [canvas_width/2, canvas_height/2], 'TO MANY FRAME DROPS', RED, int(150/s))

        pygame.display.update()  # aktualisiere die Leinwand
    #endregiond
    # aktualisierung fps, warte solange damit die Framerate eingehalten wird
        fpsclock.tick(frames_per_second)
        await asyncio.sleep(0)

async def main_menu_loop(): #Mainmenu
    global Mainmusic, Name
    text_edit = False
    text_display = False
    pygame.mouse.set_visible(True)
    manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 16)
    textinput_custom = pygame_textinput.TextInputVisualizer(manager=manager, font_object=pygame.font.SysFont("Consolas", int(50/s),True))
    textinput_custom.font_color = WHITE
    Set_volumen(volume,music_volume)
    text = ""
    if Mainmusic:
        Mainmenu_theme.play(loops=True)
        Mainmusic = False
    async with platform.fopen("http://dreamlo.com/lb/67372ac98f40bb0e14167d25/json", "r") as data:
        leaderboard = json.loads(data.read())
        leaderboard = get_names_ranks_scores(leaderboard)

    while main_menu:

        #Buttons
        start_button = Button(canvas_width/2, 400/s, 300/s, 80/s, "Start Game", GRAY, LIGHT_GRAY, WHITE, int(50/s))
        options_button = Button(canvas_width/2, 550/s, 300/s, 80/s, "options", GRAY, LIGHT_GRAY, WHITE, int(50/s))
        how_button = Button(canvas_width / 2, 700/s, 300/s, 80/s, "how to play", GRAY, LIGHT_GRAY, WHITE, int(50/s))
        text_square = Button(250/s, 700 / s, 400 / s, 80 / s, "", GRAY, LIGHT_GRAY, WHITE,int(50 / s))
        if text_edit:
            events = pygame.event.get()
            textinput_custom.update(events)
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    Name = (textinput_custom.value)

                    window.localStorage.setItem("Name", Name)
                    text_display = False
                    text_edit = False
                    pygame.mouse.set_visible(True)
                if event.type == pygame.MOUSEBUTTONDOWN:

                    text_edit = False
                    pygame.mouse.set_visible(True)

        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(event):
                        play()

                        Mainmenu_theme.stop()
                    if options_button.is_clicked(event):
                        options()
                    if how_button.is_clicked(event):
                        how()
                    if text_square.is_clicked(event):
                        text_edit = True
                        text_display = True
                        pygame.mouse.set_visible(False)

        scores = (highscore,score)

        display.fill(BLACK)
        display.blit(main_menu_BG,(0,0))#hintergrund

        display.blit(board_skin,(1375/s,canvas_height/2 - 325/s))
        draw_text(display, (1600/s, canvas_height / 2 - 60/s), 'highscore: ' + str(scores[0]),WHITE, int(30/s))
        draw_text(display, (1600/s, canvas_height / 2 - 100/s), 'latest score: ' + str(scores[1]),WHITE, int(30/s))

        draw_text(display,(canvas_width-190/2, canvas_height - 30/2),"made by Fopetix",WHITE,int(30/s))

        objekt(titel_skin,canvas_width/2, 150/s,650/s,400/s,0,0)#Titel
        #render Buttons
        options_button.draw(display)
        start_button.draw(display)
        how_button.draw(display)

        text_square.draw(display)
        if text_display == False:
            draw_text(display, (70/s, 685/s), f"Name: {Name}", WHITE, int(30 / s),centered=False)
        if text_display:
            display.blit(textinput_custom.surface, (70/s, 685/s))

        length = len(leaderboard)
        if length > 10:
            length = 10
        if length != 0:
            for i in range(length):
                draw_text(display,(100/s,100 + 30/s*i),str(leaderboard[i][0]) + " " + str(leaderboard[i][1]) + ": "+ str((leaderboard[i][2])/1000),WHITE,int(30/s),False)


        pygame.display.update()
        await asyncio.sleep(0)

async def end_menu_loop():
    global main_menu, play_menu, options_menu, how_menu,Mainmusic
    pygame.mouse.set_visible(True)
    Set_volumen(volume,music_volume)
    death_sound.play()
    while end_menu:
        #Buttons
        start_button = Button(canvas_width/2+200/s, 700/s, 300/s, 60/s, "respawn",GRAY, LIGHT_GRAY, WHITE, int(50/s))

        main_button = Button(canvas_width/2 - 200/s, 700/s, 300/s, 60/s, "Main Menu", GRAY, LIGHT_GRAY, WHITE, int(50/s))

        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event):
                    play()
                if main_button.is_clicked(event):
                    Mainmenu()
                    Mainmusic = True

        scores = (highscore,score)
        display.fill(BLACK)

        draw_text(display, (canvas_width / 2, (canvas_height/2)-100/s), "You Died", RED, int(100/s))
        draw_text(display, (canvas_width / 2, (canvas_height / 2)), 'highscore:' + str(scores[0]), WHITE, int(30/s))
        draw_text(display, (canvas_width / 2, (canvas_height / 2) + 40/s), 'score: ' + str(scores[1]), WHITE, int(30/s))
        start_button.draw(display)

        main_button.draw(display)
        pygame.display.update()
        await asyncio.sleep(0)
async def options_menu_loop():
    global main_menu, play_menu, options_menu, how_menu
    global volume,music_volume,devmode,score,highscore,n_language,n_resolution
    pygame.mouse.set_visible(True)
    Set_volumen(volume,music_volume)

    while options_menu:
        # Buttons
        if n_language % 2 == 1:
            lang = "Deutsch"
        elif n_language % 2 == 0:
            lang = "English"

        main_button = Button(300/s, canvas_height-140/s, 400/s, 80/s, "Main Menu & Save", GRAY, LIGHT_GRAY, WHITE,int(30/s))
        dev_button = Button(300/s, 140/s, 400/s, 80/s, "Devmode: " + str(devmode) , GRAY, LIGHT_GRAY, WHITE, int(30/s))
        volume_up = Button(140/s, 240/s, 80/s, 80/s, "↑", GRAY, LIGHT_GRAY, WHITE, int(30/s))
        volume_down = Button(230/s, 240/s, 80/s, 80/s, "↓", GRAY, LIGHT_GRAY, WHITE, int(30/s))
        music_volume_up = Button(140/s, 340/s, 80/s, 80/s, "↑", GRAY, LIGHT_GRAY, WHITE, int(30/s))
        music_volume_down = Button(230/s, 340/s, 80/s, 80/s, "↓", GRAY, LIGHT_GRAY, WHITE,int(30/s))
        reset_button = Button(300/s, 440/s, 400/s, 80/s, "Reset scores", GRAY,LIGHT_GRAY, RED, int(30/s))
        lang_button = Button(300 / s, 540 / s, 400 / s, 80 / s, "Language: "+str(lang), GRAY, LIGHT_GRAY, WHITE, int(30 / s))
        res_button = Button(300 / s, 640 / s, 400 / s, 80 / s, "Resulution: "+str(Liste_res[n_resolution % 4][1]), GRAY, LIGHT_GRAY, WHITE, int(30 / s))
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_button.is_clicked(event):
                    Mainmenu()


                if dev_button.is_clicked(event):
                    devmode = not devmode

                if volume_up.is_clicked(event):
                    volume += 0.1
                    if volume >= 1:
                        volume = 1
                if volume_down.is_clicked(event):
                    volume -= 0.1
                    if volume <= 0.08:
                        volume = 0
                if music_volume_up.is_clicked(event):
                    music_volume += 0.1
                    if music_volume >= 1:
                        music_volume = 1
                if music_volume_down.is_clicked(event):
                    music_volume -= 0.1
                    if music_volume <= 0.08:
                        music_volume = 0
                if reset_button.is_clicked(event):
                    score = 0.0
                    highscore = 0.0
                if lang_button.is_clicked(event):
                    n_language += 1
                if res_button.is_clicked(event):
                    n_resolution += 1

                Set_volumen(volume,music_volume)
                volume = round(volume,1)
                music_volume = round(music_volume, 1)
                window.localStorage.setItem("volume", volume)
                window.localStorage.setItem("music_volume", music_volume)
                window.localStorage.setItem("highscore", highscore)
                window.localStorage.setItem("score", score)
                window.localStorage.setItem("n_language", n_language)
                window.localStorage.setItem("n_resolution", n_resolution)



        display.fill(WHITE)
        display.blit(menu_BG2, (0, 0))


        pygame.draw.rect(display,GRAY,(280/s,200/s,220/s,80/s))
        draw_text(display, (290/s, 220/s), "Game Volume: " + str(round(volume,2)), WHITE, int(22/s),False)
        pygame.draw.rect(display, GRAY, (280/s, 300/s, 220/s, 80/s))
        draw_text(display, (290/s, 320/s), "Music Volume: " + str(round(music_volume, 2)), WHITE, int(22/s), False)
        if s != float(Liste_res[n_resolution % 4][0]):
            draw_text(display, (140 / s, canvas_height - 200/ s), "Please restart your game", RED, int(30 / s),False)


        reset_button.draw(display)
        music_volume_up.draw(display)
        music_volume_down.draw(display)
        volume_up.draw(display)
        volume_down.draw(display)
        main_button.draw(display)
        dev_button.draw(display)
        lang_button.draw(display)
        res_button.draw(display)
        #draw_text(display, (canvas_width/s,canvas_height/s),'COMING SOON',RED,int(150/s))
        pygame.display.update()
        await asyncio.sleep(0)

async def how_menu_loop():
    global main_menu, play_menu, options_menu, how_menu, n_language
    Set_volumen(volume,music_volume)
    pygame.mouse.set_visible(True)

    start = 40
    zeit = 0
    danny = pygame.transform.flip(pygame.transform.smoothscale_by(pygame.image.load('img/Player.png'), 1.5/s), 1, 0).convert_alpha()
    while how_menu:
        if zeit <= 40:
            start = 40 - zeit
        main_button = Button(300/s, 950/s, 300/s, 80/s, "Main Menu", GRAY, LIGHT_GRAY, WHITE,int(50/s))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_button.is_clicked(event):
                    Mainmenu()


        display.fill(WHITE)
        display.blit(menu_BG2, (0, 0))
        display.blit(speech_skin,(0,-200/s-start*25/s))
        if n_language % 2 == 1:
            text = how_text
        if n_language%2 == 0:
            text = how_text_eng
        for i in range(len(text)):
            draw_text(display,(canvas_width/2 - 150/s,100/s+i*35/s-start*25/s,),text[i],BLACK,int(32/s))



        display.blit(danny,(1300/s,550/s+start*10/s))

        main_button.draw(display)
        pygame.display.update()
        zeit += 1

        await asyncio.sleep(0)

async def Main():
    global main_menu, play_menu, end_menu, options_menu, how_menu

    while True:

        if main_menu:
            await main_menu_loop()
        elif play_menu:
            await play_loop()
        elif end_menu:
            await end_menu_loop()
        elif options_menu:
            await options_menu_loop()
        elif how_menu:
            await how_menu_loop()


asyncio.run(Main())

