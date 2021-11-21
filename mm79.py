## Vintage Master Mind by Roberto Zaffanella (zaffaroby@gmail.com)
from constants import *
import pygame
from pygame.locals import *
import random
import time
import sys
import webbrowser  
import configparser
import distutils
from distutils import util
import os.path
import copy
import Mastermind_Engine

class Mastermind(Mastermind_Engine.Mastermind_Engine):
    def __init__(self):
        ### Variabili  ###
        self.row = 1                        #il numero del tentativo in progress
        self.lc = 0                         #numero di attuale di left codes - occorre settarla altrimenti "left_code" da errore
        self.db_ac = []                        #include tutte le combinazioni di codici possibili
        self.db_lc = []                     #db dei Left Codes (in precedenza chiamati Fit Codes). Sono tutti i codici eleggibili come codice segreto
        self.db_bc = []                     #db dei Best Codes. sono i migliori codici da giocare secondo l'algoritmo MinMax
        self.colors = 6                     #Numero di colori usati per tutte le modalità di gioco  
        self.pegcode_history = []           
        self.keycode_history = []
        self.scorecode_history = [0,0]
        self.leftcodes_history = []
        self.bestcodes_history = []
        self.arrow_left_rect = []
        self.arrow_best_rect = []
        self.left_index = 0
        self.ch = [0,0,0,0]
        self.print_multitext = False
        self.print_score = False
        self.score_games = [0,0]
        self.multitext = []
        self.path = "src/"
        self.peg_sound = pygame.mixer.Sound(self.path + "peg.mp3")
        self.open_sound = pygame.mixer.Sound(self.path + "open.mp3")
        self.close_sound = pygame.mixer.Sound(self.path + "close.mp3")
        self.sound_on = True
        self.color_bar_on = False
        self.lang = 1                       # 1 per italiano - 2 per inglese
        self.score_reset = False
        self.revert_flag = False
        self.about = False
        self.peg_sound_number = 0
        self.game2_start = False
        self.preset_secret_code = [1,5,3,4]         #cambiare i valori per avere un codice segreto fisso per GAME 1
        ### Dimensionamento e posizionamento oggetti grafici della GUI (Graphic User Interface) ###
        """ screen """
        self.SCREEN_SIZE = (800,600)     #dimensioni della finestra principale (larghezza * altezza)
        """ board """
        self.BOARD_IMAGE_WIDTH = 1834    #larghezza reale del file della game board in formato PNG
        self.BOARD_IMAGE_HEIGH = 3920    #altezza reale del file della game board in formato PNG
        self.BOARD_LEFT_MARGIN = 65      #modificabile. spazio tra il margine SX della finestra principale e il margine SX della game board
        self.BOARD_BOTTOM_MARGIN = 25    #modificabile. spazio tra il margine inferiore della finestra principale (screen) e il margine inferiore della game board
        self.BOARD_HEIGH = 550           #modificabile.  Altezza della game board desiderata. Larghezza e gli altri parametri vengono
        #calcolati in base a questo valore
        #le costanti che terminano con _STD (standard) sono riferiti alla board alta 550 (BOARD_HEIGH = 550)
        #e sono stati misurati con le coordinate del mouse sul video
        self.BOARD_HEIGH_STD = 550
        #la larghezza board_width_std verrà dimensionata in base alla seguente proporzione:
        #BOARD_IMAGE_HEIGH : BOARD_IMAGE_WIDTH = BOARD_HEIGH_STD : board_width_std   ,quindi:
        self.board_width_std = self.BOARD_IMAGE_WIDTH / self.BOARD_IMAGE_HEIGH * self.BOARD_HEIGH_STD
        #viene calcolato il rapporto tra l'altezza della game board impostata BOARD_HEIGH e quella della board standard BOARD_HEIGH_STD
        self.ratio = self.BOARD_HEIGH / self.BOARD_HEIGH_STD                   #calcolo del ratio da usare come moltiplicatore per le misure X e Y standard
        #i valori dei parametri della board game vengono calcolati moltiplicando i valori standard per "ratio"
        self.board_width = int (self.board_width_std * self.ratio)             #larghezza della board game da disegnare a video
        self.y_board=self.SCREEN_SIZE[1]- self.BOARD_BOTTOM_MARGIN             #coordinata Y della posizione del margine inferiore della board
        """ pegs """
        self.PEG_DIM_STD = 27                #diametro per i peg riferito alla board game standard
        self.FIRST_BIN_X_POSITION_STD = 70   #coordinata X del centro del primo buco della prima fila
        self.FIRST_BIN_Y_POSITION_STD = 28.4 #coordinata y del centro del primo buco della prima fila
        self.X_STEP_STD = 40                 #distanza tra un buco e un altro lungo la fila
        self.Y_STEP_STD = 48.6               #distanza tra i buchi di due file vicine 48.6
        self.peg_dim = int(self.PEG_DIM_STD * self.ratio)                      #diametro dei peg
        self.first_bin_x_position = self.FIRST_BIN_X_POSITION_STD * self.ratio #posizione del centro del primo buco della prima fila della board game
        self.first_bin_y_position = self.FIRST_BIN_Y_POSITION_STD * self.ratio #posizione del centro del primo buco della prima fila della board game
        self.x_step = self.X_STEP_STD * self.ratio                             #distanza tra un buco e un altro lungo la fila
        self.y_step = self.Y_STEP_STD * self.ratio
        #distanza tra i buchi di due file vicine per i PEG
        self.c1=self.BOARD_LEFT_MARGIN + self.first_bin_x_position + self.peg_dim/2 #coordinata X per disegnare il primo peg della prima fila
        self.r1=self.y_board - self.first_bin_y_position - self.peg_dim/2           #coordinata Y per disegnare il primo peg della prima fila
        """ Written Buttons """
        self.x_btn = 380
        """ Left and Best Codes """
        self.PEG_LIST_DIM_STD = 22                                      #diametro per i peg riferito alla board game standard
        self.peg_list_dim = int(self.PEG_LIST_DIM_STD * self.ratio)                     
        self.x_Best_btn = self.x_btn + 200
        """ Color Bar Codes """
        self.COLOR_BAR_DIM_STD = 22                                     #diametro per i peg riferito alla board game standard
        self.color_bar_dim = int(self.COLOR_BAR_DIM_STD * self.ratio)                      
        """ key pegs """
        self.KEY_DIM_STD = 16.5                     #diametro per i key peg riferito alla board game standard
        self.FIRST_BIN_KEY_X_POSITION_STD = 15.8    #coordinata X del centro del primo buco della prima fila dei key peg per la fila 1
        self.FIRST_BIN_KEY_Y_POSITION_STD = 16.2    #coordinata y del centro del primo buco della prima fila dei key peg per la fila 1
        self.XY_KEY_STEP_STD = 20                   #distanza tra i buchi dei key peg nello stesso gruppo
        self.ROW_KEY_STEP_STD = 48.9                #distanza tra due gruppi di key peg di due file adiacenti
        self.peg_key_dim = int(self.KEY_DIM_STD * self.ratio)              #diametro dei peg del codice chiave
        self.first_bin_key_x_position = self.FIRST_BIN_KEY_X_POSITION_STD * self.ratio #posizione del centro del primo buco della prima fila della board game
        self.first_bin_key_y_position = self.FIRST_BIN_KEY_Y_POSITION_STD * self.ratio #posizione del centro del primo buco della prima fila della board game
        self.xy_key_step = self.XY_KEY_STEP_STD * self.ratio                           #distanza tra un buco e un altro lungo la fila
        self.row_key_step = self.ROW_KEY_STEP_STD * self.ratio
        #distanza tra i buchi di due file vicine per i KEY PEG
        self.c1_key=self.BOARD_LEFT_MARGIN + self.first_bin_key_x_position + self.peg_key_dim/2 #coordinata X per disegnare il primo peg della prima fila
        self.r1_key=self.y_board - self.first_bin_key_y_position - self.peg_key_dim/2           #coordinata Y per disegnare il primo peg della prima fila
        """ score pegs - usati per segnare il punteggio"""
        self.SCORE_DIM_STD = 16.5                   #diametro per i score peg riferito alla board game standard
        self.FIRST_BIN_SCORE_X_POSITION_STD = 222   #coordinata X del centro del primo buco della prima fila dei score peg per la fila 1
        self.FIRST_BIN_SCORE_Y_POSITION_STD = 3.8   #coordinata y del centro del primo buco della prima fila dei score peg per la fila 1
        self.XY_SCORE_STEP_STD = 18                 #distanza tra i buchi dei score peg nello stesso gruppo
        self.ROW_SCORE_STEP_STD = 16.2              #distanza tra due gruppi di score peg di due file adiacenti
        self.peg_score_dim = int(self.SCORE_DIM_STD * self.ratio)                           #diametro dei peg del codice chiave
        self.first_bin_score_x_position = self.FIRST_BIN_SCORE_X_POSITION_STD * self.ratio  #posizione del centro del primo buco della prima fila della board game
        self.first_bin_score_y_position = self.FIRST_BIN_SCORE_Y_POSITION_STD * self.ratio  #posizione del centro del primo buco della prima fila della board game
        self.xy_score_step = self.XY_SCORE_STEP_STD * self.ratio                            #distanza tra un buco e un altro lungo la fila
        self.row_score_step = self.ROW_SCORE_STEP_STD * self.ratio
        #distanza tra i buchi di due file vicine per i SCORE PEG
        self.c1_score=self.BOARD_LEFT_MARGIN + self.first_bin_score_x_position + self.peg_score_dim/2 #coordinata X per disegnare il primo peg della prima fila
        self.r1_score=self.y_board - self.first_bin_score_y_position - self.peg_score_dim/2           #coordinata Y per disegnare il primo peg della prima fila
        """ checkmark e wrongmark """
        self.MARK_DIM_STD = 25                      #dimensione per il segno di spunta e della x rossa riferito alla board standard
        self.FIRST_MARK_X_POSITION_STD = 10         #è lo spazio tra il checkmark e x rossa e il bordo SX della game board
        self.FIRST_MARK_Y_POSITION_STD = 27         #è lo spazio tra il checkmark e x rossa e il bordo inferiore della game board
        self.x_mark_step_std = self.MARK_DIM_STD    #serve per stampare la x rossa dopo il segno di spunta
        self.ROW_MARK_STEP_STD = 48.6               #distanza tra due gruppi di checkmarks di due file adiacenti
        self.mark_dim = int(self.MARK_DIM_STD * self.ratio)       #dimensione del segno di spunta e della x rossa - sono quadrati
        self.first_mark_x_position = self.FIRST_MARK_X_POSITION_STD * self.ratio
        self.first_mark_y_position = self.FIRST_MARK_Y_POSITION_STD * self.ratio
        self.x_mark_step = self.x_mark_step_std * self.ratio
        self.row_mark_step = self.ROW_MARK_STEP_STD * self.ratio
        #coordinate per disegnare il primo checkmark
        self.c1_mark=self.BOARD_LEFT_MARGIN - self.first_mark_x_position - self.mark_dim  #coordinata X per disegnare checkmark con adiacente la x rossa
        self.r1_mark = self.y_board - self.first_mark_y_position - self.mark_dim/2
        """ Revert """
        self.REVERT_DIM_STD = 25                                    #diametro per l'icona di revert per la board game standard
        self.revert_dim = int(self.REVERT_DIM_STD * self.ratio)     #diametro dell'icona di revert
        self.FIRST_REVERT_X_POSITION_STD = 320                      #è lo spazio tra l'icona di revert e il bordo SX della game board
        self.FIRST_REVERT_Y_POSITION_STD = 27                       #è lo spazio tra l'icona di revert e il bordo inferiore della game board
        self.ROW_REVERT_STEP_STD = 48.6                             #distanza tra due revert in verticale
        self.first_revert_x_position = self.FIRST_REVERT_X_POSITION_STD * self.ratio
        self.first_revert_y_position = self.FIRST_REVERT_Y_POSITION_STD * self.ratio
        self.row_revert_step = self.ROW_REVERT_STEP_STD * self.ratio
        #coordinate per disegnare la prima icona di revert
        self.c1_revert=self.BOARD_LEFT_MARGIN + self.first_revert_x_position - self.revert_dim
        self.r1_revert = self.y_board - self.first_revert_y_position - self.revert_dim/2

    def config_ini_write (self):
        write_config = configparser.ConfigParser()
        write_config.add_section("Settings")
        write_config.set("Settings","sound_on",str (self.sound_on))
        write_config.set("Settings","lang",str(self.lang))
        write_config.set("Settings","color_bar_on",str(self.color_bar_on))
        write_config.set("Settings","colors",str(self.colors))
        write_config.set("Settings","score_games_human",str(self.score_games[0]))
        write_config.set("Settings","score_games_computer",str(self.score_games[1]))
        write_config.set("Settings","scorecode_history_human",str(self.scorecode_history[0]))
        write_config.set("Settings","scorecode_history_computer",str(self.scorecode_history[1]))
        cfgfile = open(ini_path+"\config.ini",'w')
        write_config.write(cfgfile)
        cfgfile.close()

    def config_ini_read (self):
        read_config = configparser.ConfigParser()
        read_config.read(ini_path+ "\config.ini")
        self.sound_on = read_config.get("Settings","sound_on")
        self.sound_on = bool(distutils.util.strtobool(self.sound_on))
        self.color_bar_on = read_config.get("Settings","color_bar_on")
        self.color_bar_on = bool(distutils.util.strtobool(self.color_bar_on))
        self.lang = int (read_config.get("Settings","lang"))  
        self.colors = int (read_config.get("Settings","colors"))
        self.score_games = []
        self.score_games.append(int(read_config.get("Settings","score_games_human")))
        self.score_games.append(int(read_config.get("Settings","score_games_computer")))
        self.scorecode_history = []
        self.scorecode_history.append(int(read_config.get("Settings","scorecode_history_human")))
        self.scorecode_history.append(int(read_config.get("Settings","scorecode_history_computer")))

    ### inizializza la parte per la grafica ###
    def gui_init (self):
        """ screen background """
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)   #dimensiona la finestra principale
        pygame.display.set_caption("Vintage MASTER MIND")
        surf_tile = pygame.image.load(self.path + "concrete01.jpg") #carica l'immagine di background
        self.tile_surface(surf_tile, self.screen)              #riempi screen ripetendo la piccola immagine
        self.screen_backup = self.screen.copy()                #crea una nuova Surface con le stesse dimensioni dello schermo
        """ board """
        self.board_surf = pygame.image.load(self.path + "game_board_closed.jpg").convert_alpha()           #carica l'immagine della game board
        self.board_surf = pygame.transform.smoothscale(self.board_surf, (self.board_width, self.BOARD_HEIGH))   #adegua le dimensioni a quelle specificate da BOARD_HEIGH
        self.board_closed_surf = self.board_surf
        self.board_open_surf = pygame.image.load(self.path + "game_board_open.jpg").convert_alpha()        #carica l'immagine della game board con shield aperto
        self.board_open_surf = pygame.transform.smoothscale(self.board_open_surf, (self.board_width, self.BOARD_HEIGH))   #adegua le dimensioni a quelle specificate da BOARD_HEIGH
        self.board_rect = self.board_surf.get_rect()                                                  #crea board-rect delle stesse dim di board_surf
        self.board_rect.bottom = self.y_board                                                         #coordinata del lato inferiore della board game
        self.board_rect.left = self.BOARD_LEFT_MARGIN                                                 #coordinata del lato SX della board game
        self.board_back = self.board_surf.copy()
        """ pegs """
        self.peg_images = [] #array delle immagini dei pegs
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "00_empty.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "01_blue.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "02_red.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "03_yellow.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "04_green.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "05_white.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "06_black.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "07_orange.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        self.peg_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "08_brown.png").convert_alpha(),(self.peg_dim, self.peg_dim)))
        """ pegs for Left and Best Codes """
        self.peg_list_images = []
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "00_empty.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "01_blue.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "02_red.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "03_yellow.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "04_green.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "05_white.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "06_black.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "07_orange.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        self.peg_list_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "08_brown.png").convert_alpha(),(self.peg_list_dim, self.peg_list_dim)))
        """ pegs for Color Bar """
        self.pegs_for_Color_Bar()
        """ key pegs """
        self.key_images =[] #array delle immagini del codice chiave
        self.key_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "00_empty.png").convert_alpha(),(self.peg_key_dim, self.peg_key_dim)))
        self.key_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "00_key_white.png").convert_alpha(),(self.peg_key_dim, self.peg_key_dim)))
        self.key_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "01_key_black.png").convert_alpha(),(self.peg_key_dim, self.peg_key_dim)))
        self.all_keys = pygame.sprite.Group()
        self.key = pygame.sprite.Sprite(self.all_keys) #definizione dello sprite
        """ score pegs """
        self.score_images =[] #array delle immagini del codice chiave
        self.score_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "00_empty.png").convert_alpha(),(self.peg_score_dim, self.peg_score_dim)))
        self.score_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "00_key_white.png").convert_alpha(),(self.peg_score_dim, self.peg_score_dim)))
        self.score_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "01_key_black.png").convert_alpha(),(self.peg_score_dim, self.peg_score_dim)))
        self.all_scores = pygame.sprite.Group()
        self.score = pygame.sprite.Sprite(self.all_scores) #definizione dello sprite
        """ checkmark e wrongmark """
        self.mark_images =[] #array delle immagini del segno di spunta e x rossa
        self.mark_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "00_empty.png").convert_alpha(),(self.mark_dim, self.mark_dim)))
        self.mark_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "checkmark10.png").convert_alpha(),(self.mark_dim, self.mark_dim)))
        self.mark_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "wrongmark10.png").convert_alpha(),(self.mark_dim, self.mark_dim)))
        self.all_marks = pygame.sprite.Group()
        self.mark = pygame.sprite.Sprite(self.all_marks) #definizione dello sprite        
        """ Revert """
        self.revert_images = []
        self.revert_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "revert.png").convert_alpha(),(self.revert_dim, self.revert_dim)))
        self.all_reverts = pygame.sprite.Group()
        self.revert = pygame.sprite.Sprite(self.all_reverts) #definizione dello sprite
        """ arrows """
        self.arrow_images =[] #array delle immagini del segno di spunta e x rossa
        self.arrow_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "freccia_giu.png").convert_alpha(),(self.mark_dim, self.mark_dim)))
        self.arrow_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "freccia_su.png").convert_alpha(),(self.mark_dim, self.mark_dim)))
        """ shield """
        self.shield_surf = (pygame.transform.smoothscale(pygame.image.load(self.path + "00_empty.png").convert_alpha(),(175, 60)))
        self.shield_rect = self.shield_surf.get_rect()                    #crea board-rect delle stesse dim di board_surf
        self.shield_rect.bottom = 85                                      #coordinata del lato inferiore della board game
        self.shield_rect.left = 120                                       #coordinata del lato SX della board game
        self.shield_back = self.shield_surf.copy()
        """ written buttons """
        self.btn_play_color = BROWN
        self.btn_play2_color = BROWN
        self.btn_6colors_color = BORDEAUX
        self.btn_8colors_color = BROWN
        self.btn_score_color = BROWN
        self.btn_demo_color = BROWN
        self.btn_help_color = BROWN
        self.btn_options_color = BROWN
        self.btn_left_codes_color = BROWN
        self.btn_best_codes_color = BROWN
        """ options buttons """
        self.btn_english_color = BROWN
        self.btn_italiano = BROWN
        self.btn_sound_on_color = BROWN
        self.btn_sound_off_color = BROWN
        self.btn_color_bar_on_color = BROWN
        self.btn_color_bar_off_color = BROWN

    def pegs_for_Color_Bar (self):
        self.color_bar_images = []
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "01_blue.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "02_red.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "03_yellow.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "04_green.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "05_white.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "06_black.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "07_orange.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "08_brown.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "01_blue_x.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "02_red_x.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "03_yellow_x.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "04_green_x.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "05_white_x.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "06_black_x.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "07_orange_x.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        self.color_bar_images.append(pygame.transform.smoothscale(pygame.image.load(self.path + "08_brown_x.png").convert_alpha(),(self.color_bar_dim, self.color_bar_dim)))
        
        
    def tile_surface(self,surf_little, surf_big):  # surf_little e' la mattonella, surf_big l'area da ricoprire
        w_little = surf_little.get_width()         # larghezza della mattonella
        h_little = surf_little.get_height()        # altezza della mattonella
        w_big = surf_big.get_width()               # larghezza da ricoprire
        h_big = surf_big.get_height()              # altezza da ricoprire
        for y in range(0, h_big, h_little):        # incremento della y
            for x in range(0, w_big, w_little):    # incremento della x
                surf_big.blit(surf_little, (x, y)) # posizionia la mattonella sulle coordinate (x, y)

    def gui_refresh(self, row):
        self.display_background ()
        if self.row > 9:
            self.st[1] = "closed"
        if self.st[1] == "closed":
            self.board_surf = self.board_closed_surf
        if self.st[1] == "open":
            self.board_surf = self.board_open_surf
        self.display_board()
        self.display_shield()
        self.display_written_buttons()
        if self.st[3] == "Options_active":
            self.display_options_buttons()
            print ("len self.btn_x", len(self.btn_x))
        self.print_peg_code_history (self.pegcode_history, row)
        if self.st[1] == "open":
            self.print_row (self.secret_code, 11)
        self.print_keycode_history (self.keycode_history)
        self.print_scorecode_history ()
        self.print_row ([0,0,0,0], self.row)        #visualizza i peg trasparenti per evitare che collidepoint(click) vada in errore
        self.print_checkmarks([0,0], self.row)
        if self.st[0] == "current_row":
            self.print_checkmarks([1,2], self.row)
        self.print_key_row ( self.ch, self.row)
        self.print_left_code_history()
        self.print_best_code_history()
        self.print_color_bar()
        self.print_revert(self.row)

    def display_background (self):
        self.screen.blit(self.screen_backup, (0, 0))            #per fare refresh del background senza richiamare la funzione

    def display_board (self):
        self.screen.blit(self.board_surf, self.board_rect)      #visualizza la bord game - 0,0 è l'angolo in alto a SX

    def display_shield (self):
        self.screen.blit(self.shield_surf, self.shield_rect)    #Imposta l'area dello shield per essere cliccato

    def display_written_buttons (self):
        if self.colors == 6:
            self.btn_6colors_color = BORDEAUX
            self.btn_8colors_color = BROWN
        if self.colors == 8:
            self.btn_6colors_color = BROWN
            self.btn_8colors_color = BORDEAUX
        if self.st[2] == "Game1_current": 
            self.btn_play_color = BORDEAUX
        else:
            self.btn_play_color = BROWN
        if self.st[2] == "Game2_current":   
            self.btn_play2_color = BORDEAUX
        else:
            self.btn_play2_color = BROWN
        if self.st[2] == "Demo_current":
            self.btn_demo_color = BORDEAUX
        else:
            self.btn_demo_color = BROWN            
        if self.st[4] == "LeftCodes_printed":
            self.btn_left_codes_color = BORDEAUX
        if self.st[4] == "LeftCodes_no_printed":
            self.btn_left_codes_color = BROWN
        if self.st[5] == "BestCodes_printed":
            self.btn_best_codes_color = BORDEAUX
        if self.st[5] == "BestCodes_no_printed":
            self.btn_best_codes_color = BROWN
        if self.st[3] == "Help_active":
            self.btn_help_color = BORDEAUX
        else:
            self.btn_help_color = BROWN
        self.btn_x = []
        self.display_single_button ("Game 1", 21, [self.x_btn,90], self.btn_play_color)
        self.display_single_button ("Game 2", 21, [self.x_btn,120], self.btn_play2_color)
        self.display_single_button ("6 Colors", 21, [self.x_btn + 100,90], self.btn_6colors_color)
        self.display_single_button ("8 Colors", 21, [self.x_btn + 100,120], self.btn_8colors_color)
        self.display_single_button ("Score", 21, [self.x_btn + 200,90], self.btn_score_color)
        self.display_single_button ("Demo", 21, [self.x_btn + 200,120], self.btn_demo_color)
        self.display_single_button ("Help", 21, [self.x_btn + 280,90], self.btn_help_color)
        self.display_single_button ("Options", 21, [self.x_btn + 280,120], self.btn_options_color)
        if self.st[4] == "LeftCodes_printed":
            self.display_single_button ("Left Codes: " + str(self.lc), 21, [self.x_btn,190], self.btn_left_codes_color)
        else:
            self.display_single_button ("Left Codes", 21, [self.x_btn,190], self.btn_left_codes_color)
        if self.st[5] == "BestCodes_printed":
            self.display_single_button ("Best Codes: " + str(self.bc), 21, [self.x_Best_btn,190], self.btn_best_codes_color)
        else:
            self.display_single_button ("Best Codes", 21, [self.x_Best_btn,190], self.btn_best_codes_color)
        self.display_single_button ("Master Mind", 55, [self.x_btn,15], LIGHT_GREY)
        if self.st[3] == "Game2_wait":
            self.btn_Game2_wait_color = BORDEAUX
            if self.lang == 0: 
                self.display_single_button ("Click here to start", 21, [self.x_btn + 80, 390], self.btn_Game2_wait_color)
            if self.lang == 1:
                self.display_single_button ("Clicca qua per iniziare", 21, [self.x_btn + 60, 390], self.btn_Game2_wait_color)
        if self.print_multitext == True:
            for i in range (len(self.multitext)):
                self.display_single_button (self.multitext[i][0:], 21, [self.x_btn,300+i*30], YELLOW, button=False) 
            self.print_multitext = False
            self.multitext = []

    def display_options_buttons (self):
        if self.lang == 0:
            self.btn_english_color = BORDEAUX
            self.btn_italiano_color = BROWN
        if self.lang == 1:
            self.btn_english_color = BROWN
            self.btn_italiano_color = BORDEAUX
        if self.sound_on == True:
            self.btn_sound_on_color = BORDEAUX
            self.btn_sound_off_color = BROWN
        if self.sound_on == False:
            self.btn_sound_on_color = BROWN
            self.btn_sound_off_color= BORDEAUX
        if self.color_bar_on == True:
            self.btn_color_bar_on_color = BORDEAUX
            self.btn_color_bar_off_color = BROWN
        if self.color_bar_on == False:
            self.btn_color_bar_on_color = BROWN
            self.btn_color_bar_off_color= BORDEAUX
        if self.score_reset == True:
            self.btn_score_reset_color = BORDEAUX
            self.score_reset = False
        else:
            self.btn_score_reset_color = BROWN
        self.btn_about = BROWN            
        self.display_single_button ("English", 21, [self.x_btn,300], self.btn_english_color)
        self.display_single_button ("Italiano", 21, [self.x_btn,330], self.btn_italiano_color)
        self.display_single_button ("Sound On", 21, [self.x_btn + 110,300], self.btn_sound_on_color)
        self.display_single_button ("Sound Off", 21, [self.x_btn + 110,330], self.btn_sound_off_color)
        self.display_single_button ("ColorBar On", 21, [self.x_btn + 230,300], self.btn_color_bar_on_color)
        self.display_single_button ("ColorBar Off", 21, [self.x_btn + 230,330], self.btn_color_bar_off_color)
        self.display_single_button ("Score Reset", 21, [self.x_btn, 390], self.btn_score_reset_color)
        self.display_single_button ("About", 21, [self.x_btn + 140, 390], self.btn_about)


    def display_single_button (self, testo, dim_car, pos, color, button=True):
        self.btn_pos = pos
        self.fnt = pygame.font.SysFont("Times New Roman", dim_car, bold=True)
        self.btn = self.fnt.render(testo, True, color)
        self.btn_size = self.btn.get_size()
        self.btn_surface = pygame.Surface(self.btn_size, pygame.SRCALPHA)
        self.btn_surface.blit(self.btn, (0, 0))
        self.btn_rect = pygame.Rect(self.btn_pos[0], self.btn_pos[1], self.btn_size[0], self.btn_size[1])
        if button == True:
            self.btn_x.append(self.btn_rect)            #save the RECT info
        self.screen.blit(self.btn_surface, (self.btn_pos))


    def print_peg_code_history (self, pegcode_history, row):
        for r in range (0, len(pegcode_history)):
            self.print_row (self.pegcode_history[r], r+1)

    def print_row (self, cp, row):          #visualizza la riga del codice giocato
        self.peg_x = []                     #valorizzta con i RECT dei 4 peg della giocata
        for c in range(4):                  #viene visualizzato un peg alla volta
            self.print_peg(cp[c], c, row)   #viene passato il colore e la posizione

    def print_peg(self,peg_num, c, row):
        self.all_pegs = pygame.sprite.Group()
        self.peg = pygame.sprite.Sprite(self.all_pegs)  #definizione dello sprite
        self.peg.image = self.peg_images[peg_num]       #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
        self.peg.rect = self.peg.image.get_rect()       #peg.rect assume la stessa dimensione di peg.image
        self.peg_x.append(self.peg.rect)                #save the RECT info
        if row < 11:
            self.peg.rect.topright = (int(self.c1)+c*self.x_step, int(self.r1-(row-1)*self.y_step)) #assegna le coordinate per il print del peg
        if row == 11:
            self.peg.rect.topright = (int(self.c1)+c*self.x_step, int(self.r1-(row-1)*50)) 
        self.all_pegs.draw(self.screen)

    def print_color_bar (self):          #visualizza la barra dei pioli
        if self.color_bar_on == False or self.st[2] == "Game2_current" or self.st[2] == "Demo_current":
            return
        self.color_bar_x = []                   #valorizzata con i RECT dei peg della color bar
        for c in range(self.colors):            #viene visualizzato un peg alla volta
            self.print_color_bar_peg(c)   

    def print_color_bar_peg(self,c):
        self.color_bar_all_pegs = pygame.sprite.Group()
        self.color_bar = pygame.sprite.Sprite(self.color_bar_all_pegs)  #definizione dello sprite
        self.color_bar.image = self.color_bar_images[c]                 #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
        self.color_bar.rect = self.color_bar.image.get_rect()           #peg.rect assume la stessa dimensione di peg.image
        self.color_bar_x.append(self.color_bar.rect)                    #salva the RECT info
        self.color_bar.rect.topright = (self.x_btn + 20 + 25*c, 155)    #assegna le coordinate per il print del peg
        self.color_bar_all_pegs.draw(self.screen)

    def print_checkmarks(self, mark_num, row):
        self.mark.image = self.mark_images[mark_num[0]]     #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
        self.mark.rect = self.mark.image.get_rect()         #peg.rect assume la stessa dimensione di peg.image
        self.mark_rect_0 = self.mark.rect
        self.mark.rect.topright = (int(self.c1_mark + 0*self.x_mark_step), int(self.r1_mark-(row-1)*self.row_mark_step)) #assegna le coordinate per il print del peg
        self.all_marks.draw(self.screen)
        #
        self.mark.image = self.mark_images[mark_num[1]]     #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
        self.mark.rect = self.mark.image.get_rect()         #peg.rect assume la stessa dimensione di peg.image
        self.mark_rect_1 = self.mark.rect
        self.mark.rect.topright = (int(self.c1_mark + 1*self.x_mark_step), int(self.r1_mark-(row-1)*self.row_mark_step)) #assegna le coordinate per il print del peg
        self.all_marks.draw(self.screen)

    def print_revert(self, row):
        if self.st[2] != "Game1_current" or self.revert_flag == False or self.st[0] == "stop_row":
            return
        self.revert.image = self.revert_images[0]       #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
        self.revert.rect = self.revert.image.get_rect() #peg.rect assume la stessa dimensione di peg.image
        self.revert_rect_0 = self.revert.rect
        self.revert.rect.topright = (int(self.c1_revert), int(self.r1_revert-(row-1)*self.row_revert_step)) #assegna le coordinate per il print del peg
        self.all_reverts.draw(self.screen)        

    def print_arrows_left(self, x_arrow, y_arrow):
        self.all_arrows_left = pygame.sprite.Group()
        self.arrow_left = pygame.sprite.Sprite(self.all_arrows_left) 
        self.arrow_left_rect = []
        self.arrow_left.image = self.arrow_images[0]            
        self.arrow_left.rect = self.arrow_left.image.get_rect() 
        self.arrow_left_rect.append (self.arrow_left.rect)
        self.arrow_left.rect.topright = (x_arrow, y_arrow)      
        self.all_arrows_left.draw(self.screen)
        self.arrow_left.image = self.arrow_images[1]            
        self.arrow_left.rect = self.arrow_left.image.get_rect() 
        self.arrow_left_rect.append (self.arrow_left.rect)
        self.arrow_left.rect.topright = (x_arrow + 25, y_arrow) 
        self.all_arrows_left.draw(self.screen)
        
    def print_arrows_best(self, x_arrow, y_arrow):
        self.all_arrows_best = pygame.sprite.Group()
        self.arrow_best = pygame.sprite.Sprite(self.all_arrows_best) 
        self.arrow_best_rect = []
        self.arrow_best.image = self.arrow_images[0] 
        self.arrow_best.rect = self.arrow_best.image.get_rect() 
        self.arrow_best_rect.append (self.arrow_best.rect)
        self.arrow_best.rect.topright = (x_arrow, y_arrow) 
        self.all_arrows_best.draw(self.screen)
        self.arrow_best.image = self.arrow_images[1] 
        self.arrow_best.rect = self.arrow_best.image.get_rect() 
        self.arrow_best_rect.append (self.arrow_best.rect)
        self.arrow_best.rect.topright = (x_arrow + 25, y_arrow) 
        self.all_arrows_best.draw(self.screen)

    def print_keycode_history (self,keycode_history):
        row = 0
        for ch in keycode_history:
            row += 1
            self.print_key_row (ch, row)

    def print_key_row (self, ch, row):      #riceve ch[0,1,2,0] 0=trasp 1= bianco 2=nero
        adjust = 0
        if row == 4 or row == 5:
            adjust = -3
        if row == 10:
            adjust = 2
        self.key_x = []
        ch_x_step = []
        ch_y_step = []
        ch_x_step.append(0)
        ch_y_step.append(0)
        ch_x_step.append(self.xy_key_step)
        ch_y_step.append(0)
        ch_x_step.append(self.xy_key_step)
        ch_y_step.append(-self.xy_key_step)
        ch_x_step.append(0)
        ch_y_step.append(-self.xy_key_step)
        for i in range (4):
            self.key.image = self.key_images[ch[i]]     
            self.key.rect = self.key.image.get_rect()   
            self.key_x.append(self.key.rect)            
            self.key.rect.topright = (int(self.c1_key+ ch_x_step[i]), int(-(row-1)*self.row_key_step + self.r1_key + ch_y_step[i])+ adjust) #assegna le coordinate per il print del peg
            self.all_keys.draw(self.screen)

    def print_scorecode_history (self):                 #usa self.scorecode_history [0] = score "Game1" - [1] score "Game2"
        for i in range (2):     
            self.score.image = self.score_images[i+1]   #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
            if self.scorecode_history[i] == 0 or self.scorecode_history[i] > 29:
                self.score.image = self.score_images[0]
            self.score.rect = self.score.image.get_rect() #peg.rect assume la stessa dimensione di peg.image
            self.score.rect.topright = (int (self.c1_score + i * self.xy_score_step), int (self.r1_score - self.scorecode_history[i] * self.row_score_step))
            self.all_scores.draw(self.screen)

############### print left codes ##

    def left_codes_print (self):         #preparazione per la stampa dei left
        self.st[4] = "LeftCodes_printed"
        self.st[3] = "Left_active"
        self.left_index = 0
        if self.db_lc [0][13] != 0:
            self.db_lc.sort(key=lambda x: x[13])
        self.leftcodes_history = []
        self.print_left_page()

    def left_codes_clean (self):         # cancella i left codes a video
        self.leftcodes_history = []
        self.st[4] = "LeftCodes_no_printed"
        if self.st[3] == "Options_active":
            return
        if self.st[2] == "Game1_current":
            self.st[3] = "Game1_active"
        if self.st[2] == "Game2_current":
            self.st[3] = "Game2_active"
        
    def left_codes_scroll (self):         # scorre in su e giù i left codes
        self.st[3] = "Left_active"
        self.left_index += (-self.ev[9])
        if self.left_index < 0:
            self.left_index =0
        if self.left_index > (self.lc-10):
            self.left_index = self.lc -10
        if self.lc < 11:
            self.left_index = 0
        self.print_left_page()

    def left_codes_picked_up (self):                             #gioca un left code scelto
        self.cp = self.db_lc[self.left_index + self.ev[7]-1]
        self.peg_play_sound_4 (self.cp)
        self.game1_played_code()
        
    def print_left_page (self):
        self.leftcodes_history = []
        for i in range (self.left_index, self.left_index+10):
            self.leftcodes_history.append(self.db_lc[i])
            if i == self.lc - 1:
                break

    def print_left_code_history (self):
        self.left_peg_x = []   
        self.len_left_his = len(self.leftcodes_history)
        if self.len_left_his == 10:
            self.print_arrows_left(x_arrow = self.x_btn + 50, y_arrow=550)
            self.display_single_button (str(self.left_index+1)+"-"+ str(self.left_index+10), 21, [self.x_btn + 80,550], self.btn_left_codes_color)
        for r in range (0, self.len_left_his):
            self.print_left_row (self.leftcodes_history[r],r)

    def print_left_row (self, cp, row):         #visualizza la riga del codice giocato
        self.delta_x_list = 0
        if self.st[2] == "Game2_current":
            self.delta_x_list = -25
        for c in range(-1,4):                   #viene visualizzato un peg alla volta
            self.print_left_peg(cp, c, row)     #viene passato il colore e la posizione

    def print_left_peg(self, cp, c, row):
        peg_num = cp[c]
        rank = str(cp[13])
        self.left_all_pegs = pygame.sprite.Group()
        self.left_peg = pygame.sprite.Sprite(self.left_all_pegs) #definizione dello sprite
        if c == -1:
            if self.st[2] == "Game1_current":
                self.left_peg.image = self.mark_images[1] #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
                delta_x = 0
            if self.st[2] == "Game2_current":
                self.left_peg.image = self.mark_images[0] #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
                delta_x = -20
        if c > -1:
            self.left_peg.image = self.peg_list_images[peg_num] #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
        self.left_peg.rect = self.left_peg.image.get_rect()     #peg.rect assume la stessa dimensione di peg.image
        if c == -1:
            self.left_peg_x.append(self.left_peg.rect)            
        self.left_peg.rect.topright = (self.x_btn + 50 + self.delta_x_list + 25*c, 220+row*33) #assegna le coordinate per il print del peg
        if c == 3 and rank != "0":
            self.display_single_button (rank, 18, [self.x_btn + self.delta_x_list + 130, 220+row*33], BORDEAUX)
        self.left_all_pegs.draw(self.screen)

###############  print best codes

    def best_codes_print (self):         #preparazione per la stampa dei best
        self.st[5] = "BestCodes_printed"
        self.st[3] = "Best_active"
        self.best_index = 0
        self.bestcodes_history = []
        self.print_best_page()

    def best_codes_clean (self):         # cancella a video i best codes
        self.bestcodes_history = []
        self.st[5] = "BestCodes_no_printed"
        if self.st[3] == "Options_active":
            return
        if self.st[2] == "Game1_current":
            self.st[3] = "Game1_active"
        if self.st[2] == "Game2_current":
            self.st[3] = "Game2_active"
        

    def best_codes_scroll (self):         # scorre in su e giù i best codes
        self.st[3] = "Best_active"
        self.best_index += (-self.ev[10])
        if self.best_index < 0:
            self.best_index =0
        if self.best_index > (self.bc - 10):
            self.best_index = self.bc - 10
        if self.bc < 11:
            self.best_index = 0
        self.print_best_page()

    def best_codes_picked_up (self):                             #gioca un best code scelto
        self.cp = self.db_bc[self.best_index + self.ev[8]-1]
        self.peg_play_sound_4 (self.cp)
        self.game1_played_code()

    def print_best_page (self):
        self.bestcodes_history = []
        for i in range (self.best_index, self.best_index+10):
            self.bestcodes_history.append(self.db_bc[i])
            if i == self.bc - 1:
                break

    def print_best_code_history (self):
        self.best_peg_x = []   
        self.len_best_his = len(self.bestcodes_history)
        if self.len_best_his == 10:
            self.print_arrows_best(x_arrow = self.x_Best_btn + 50, y_arrow=550)
            self.display_single_button (str(self.best_index+1)+"-"+ str(self.best_index+10), 21, [self.x_Best_btn + 80,550], self.btn_best_codes_color)
        for r in range (0, self.len_best_his):
            self.print_best_row (self.bestcodes_history[r],r)

    def print_best_row (self, cp, row):          #visualizza la riga del codice giocato
        self.delta_x_list = 0
        if self.st[2] == "Game2_current":
            self.delta_x_list = -25
        for c in range(-1,4):                  #viene visualizzato un peg alla volta
            self.print_best_peg(cp, c, row)   #viene passato il colore e la posizione

    def print_best_peg(self, cp, c, row):
        peg_num = cp[c]
        rank = str(cp[13])
        self.best_all_pegs = pygame.sprite.Group()
        self.best_peg = pygame.sprite.Sprite(self.best_all_pegs) #definizione dello sprite
        if c == -1:
            if self.st[2] == "Game1_current":
                self.best_peg.image = self.mark_images[1] #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
            if self.st[2] == "Game2_current":
                self.best_peg.image = self.mark_images[0] #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
        if c > -1:
            self.best_peg.image = self.peg_list_images[peg_num] #assegna all'attributo peg.image l'immagine presa dalla lista peg_images
        self.best_peg.rect = self.best_peg.image.get_rect() #peg.rect assume la stessa dimensione di peg.image
        if c == -1:
            self.best_peg_x.append(self.best_peg.rect)            
        self.best_peg.rect.topright = (self.x_Best_btn + 50 + self.delta_x_list + 25*c, 220+row*33) #assegna le coordinate per il print del peg
        if c == 3 and rank != "0":
            self.display_single_button (rank, 18, [self.x_Best_btn + self.delta_x_list + 130, 220+row*33], BORDEAUX)
        self.best_all_pegs.draw(self.screen)

############# events() #####################
    def events(self):
        save_pos_bin = self.ev[0]
        self.ev = [0,0,0,0,0,0,"",0,0,0,0,0]
        self.ev[0] = save_pos_bin
        done = False
        while not done:
            time.sleep(0.3)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.config_ini_write()
                    pygame.quit()
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
##                    mouse_x = event.pos[0]
##                    mouse_y = event.pos[1]
##                    print("Hai fatto click in (", mouse_x, " , ", mouse_y, ")")
                    click = event.pos
                    for i in range (0,len(self.btn_x)):                       #ripete per tutti i bottoni
                        if self.btn_x [i].collidepoint(click):  #controlla se uno dei bottoni è stato cliccato
                            if i == 0:
                                self.ev [6] = "Game1"
                                done = True
                            if i == 1:
                                self.ev [6] = "Game2"
                                done = True
                            if i == 2:
                                self.ev [6] = "6Colors"
                                done = True
                            if i == 3:
                                self.ev [6] = "8Colors"
                                done = True
                            if i == 4:
                                self.ev [6] = "Score"
                                done = True
                            if i == 5:
                                self.ev [6] = "Demo"
                                done = True
                            if i == 6:
                                self.ev [6] = "Help"
                                done = True
                            if i == 7:
                                self.ev [6] = "Options"
                                done = True
                            if i == 8:
                                self.ev [6] = "LeftCodes"
                                done = True
                            if i == 9:
                                self.ev [6] = "BestCodes"
                                done = True
                            if i == 10:
                                self.ev [6] = "MasterMind"
                                done = True
                            if i == 11:
                                self.ev [6] = "English"
                                done = True
                            if i == 11 and self.st[3] == "Game2_wait":
                                self.ev [6] = "Click here to start"
                                done = True
                            if i == 12:
                                self.ev [6] = "Italiano"
                                done = True
                            if i == 13:
                                self.ev [6] = "Sound On"
                                done = True
                            if i == 14:
                                self.ev [6] = "Sound Off"
                                done = True
                            if i == 15:
                                self.ev [6] = "Color Bar ON"
                                done = True
                            if i == 16:
                                self.ev [6] = "Color Bar Off"
                                done = True
                            if i == 17:
                                self.ev [6] = "Score Reset"
                                done = True
                            if i == 18:
                                self.ev [6] = "About"
                                done = True
                    if self.mark_rect_0.collidepoint(click):
                        self.ev [6] = "Checkmark"
                        done = True
                    if self.mark_rect_1.collidepoint(click):
                        self.ev [6] = "Wrongmark"
                        done = True
                    try:
                        if self.revert_rect_0.collidepoint(click):
                            self.ev [6] = "Revert"
                            done = True
                    except:
                        pass
                    if self.shield_rect.collidepoint(click):
                        self.ev [6] = "Shield"
                        done = True
                    for i in range (0,4):                       #ripete per i 4 peg
                        if self.peg_x [i].collidepoint(click):  #controlla se uno dei peg è stato cliccato
                            self.ev[0] = i                      #setta la posizione del peg
                            self.ev[1] = 1                      #se cliccato incrementa di un colore
                            done = True
                    for i in range (0,4):                       #ripete per i 4 key code
                        if self.key_x [i].collidepoint(click):  #controlla se uno dei peg è stato cliccato
                            self.ev[2] = i                      #setta la posizione del key
                            self.ev[3] = 1                      #se cliccato incrementa di uno il colore
                            done = True
                    for i in range (self.len_left_his):             #ripete per il numero di checkmark della visualizzazione dei left codes
                        if self.left_peg_x [i].collidepoint(click): #controlla se un mark  è stato cliccato
                            self.ev[7] = i+1                        #memorizza quale checkmark è stato cliccato
                            done = True
                    for i in range (self.len_best_his):             #ripete per i 10 checkmark della visualizzazione dei best codes
                        if self.best_peg_x [i].collidepoint(click): #controlla se un mark  è stato cliccato
                            self.ev[8] = i+1                        #memorizza quale checkmark è stato cliccato
                            done = True
                    try:
                        for i in range (0,self.colors):                     #ripete per il numero di colori della color bar
                            if self.color_bar_x [i].collidepoint(click):    #controlla se uno dei peg è stato cliccato
                                self.ev[11] = i + 1                         #se cliccato incrementa di un colore
                                done = True
                    except:
                        pass
                    try:
                        if self.arrow_left_rect[0].collidepoint(click):
                            self.ev [9] = -1                #freccia in giu
                            done = True
                        if self.arrow_left_rect[1].collidepoint(click):
                            self.ev [9] = 1                 #freccia in su
                            done = True
                    except IndexError:
                        pass
                    try:
                        if self.arrow_best_rect[0].collidepoint(click):
                            self.ev [10] = -1               #freccia in giu
                            done = True
                        if self.arrow_best_rect[1].collidepoint(click):
                            self.ev [10] = 1                #freccia in su
                            done = True
                    except IndexError:
                        pass
                    if event.button==4:                 #rotella verso su
                        if self.st[3] == "Game1_active":
                            self.ev[5] = 1         
                        if self.st[3] == "Left_active":
                            self.ev[9] = 10         
                        if self.st[3] == "Best_active":
                            self.ev[10] = 10         
                        done = True
                    if event.button==5:                 #rotella verso giù
                        if self.st[3] == "Game1_active":
                            self.ev[5] = -1             #incrementa il colore del peg corrente
                        if self.st[3] == "Left_active":
                            self.ev[9] = -10        
                        if self.st[3] == "Best_active":
                            self.ev[10] = -10         
                        done = True
                    #else:
                        #print ("Hai cliccato fuori dalle superfici")
                if event.type == KEYDOWN:             # e' stato premuto un tasto
                    if event.key == K_UP:
                        if self.st[3] == "Game1_active":
                            self.ev[5] = 1         #incrementa il colore del peg corrente
                        if self.st[3] == "Left_active":
                            self.ev[9] = 1         
                        if self.st[3] == "Best_active":
                            self.ev[10] = 1         
                        done = True
                    if event.key == K_DOWN:
                        if self.st[3] == "Game1_active":
                            self.ev[5] = -1         
                        if self.st[3] == "Left_active":
                            self.ev[9] = -1         
                        if self.st[3] == "Best_active":
                            self.ev[10] = -1         
                        done = True
                    if event.key == K_RIGHT:
                        self.ev [4] = 1                 #si sposta di un peg a dx
                        done = True
                    if event.key == K_LEFT:             #si sposta di un peg a sx
                        self.ev [4] = -1
                        done = True
                    if event.key == K_RETURN:           #conferma che il codice è stato scelto
                        self.ev [6] = "Invio"
                        done = True

############## GAME 1 ##########################

    def game1_init(self):                                         #partita dove il giocatore deve indovinare il codice segreto scelto dal programma
        if self.st[1] == "open" and self.sound_on == True:
            self.close_sound.play()
        self.db_ac, self.ac, self.db_lc, self.lc, self.db_bc, self.bc = self.init_db(self.colors)

        self.row = 1
        self.cp = [0,0,0,0]
        self.pos = 0
        self.ch = [0,0,0,0]
        self.pegcode_history = []                                 #memorizza le giocate
        self.pegcode_history.append([0,0,0,0])
        self.keycode_history = []                                 #memorizza i codici chiave
        self.leftcodes_history = []
        self.bestcodes_history = []
        self.pegs_for_Color_Bar()
        self.revert_flag = False
        if self.preset_secret_code == [0,0,0,0]:
            self.secret_code = self.db_ac[random.randrange(self.ac)]     #il programma sceglie il codice segreto tra tutti i codici possibili                             #ripeti fino a un massimo di 10 tentativi
        else:
            self.secret_code = self.code_adapter (self.preset_secret_code)
        if (self.scorecode_history[0] > 20 or self.scorecode_history[1] > 20) and self.score_games[0] == self.score_games[1]:
            self.scorecode_history = [0,0]
            self.score_games = [0,0]
        self.st=["current_row","closed","Game1_current","Game1_active","LeftCodes_no_printed","BestCodes_no_printed"] 

    def game1_input_guess (self):
        self.st[3] = "Game1_active"
        if self.ev[1] != 0:
            self.pos = self.ev[0]
            inc = self.ev[1]                            #incremento positivo o negativo di 1 del colore del peg della posizione corrente
        if self.ev[5] != 0:                             #se viene usata la rotella, genera anche un click sul peg, per cui solo ev[5] è da tenere
            inc = self.ev[5]
        self.cp[self.pos] += inc                        #incrementa in positivo/negativo il colore del peg in posizione pos
        if self.cp[self.pos] == self.colors+1:          #se viene superato il numero massimo di colori, il colore torna a 1
            self.cp[self.pos] = 0
        if self.cp[self.pos] < 0:                       #se i colori scendono al di sotto del primo, ripartono dal più alto
            self.cp[self.pos] = self.colors
        if self.cp[self.pos] != 0:
            self.peg_sound_number = 1
        self.pegcode_history[self.row-1] = self.cp
        self.print_row (self.cp, self.row)              #visualizza la fila corrente di pegs

    def game1_bin_change (self):
        sx_dx = self.ev[4]                  #-1 se è stato premuto il tasto freccia a sinistra. 1 se a destra
        self.pos += sx_dx
        if self.pos == 4:
            self.pos = 3                    #per non andare oltre al quarto peg
        if self.pos < 0:
            self.pos = 0                    #per non andare più a sinistra del primo peg

    def game1_buttons (self):
        self.st[3] = "Game1_active"
        btn = self.ev[6]                        # valorizzato se click su un bottone o se tasto invio
        if (btn == "Checkmark" or btn == "Invio") and self.cp[0]>0 and self.cp[1]>0 and self.cp[2]>0 and self.cp[3]>0:     #se click su segno di spunta e tutti peg sono scelti...
            self.game1_played_code()
        if btn == "Wrongmark":                  #click sulla x rossa
            self.pegcode_history[self.row-1] = [0,0,0,0]
            self.cp = [0,0,0,0]                 #azzera il cp
            self.pos=0
        if btn == "Shield":
            if self.st[1] == "closed":
                self.st[1] = "open"
                if self.sound_on == True and self.row < 10:
                    self.open_sound.play()
            else :
                self.st[1] = "closed"
                if self.sound_on == True:
                    self.close_sound.play()

    def game1_played_code(self):
        self.pegcode_history[self.row-1] = self.cp
        self.code_played = self.code_adapter (self.cp)
        self.whites, self.blacks = self.find_keycode(self.secret_code, self.code_played) #trova il codice chiave confrontando il cod tentativo con il cod segreto
        self.keycode = self.converti_keycode (self.whites, self.blacks)
        self.keycode_history.append(self.keycode)
        self.print_key_row(self.keycode, self.row)
        self.revert_flag = True
        self.cp_bck = copy.deepcopy(self.cp)
        self.leftcodes_history = []
        self.bestcodes_history = []
        self.left_codes_clean()
        self.best_codes_clean()
        self.st[0] = "new_row"
        self.cp = [0,0,0,0]
        self.pos = 0
        if self.blacks == 4:
            self.st[0] = "stop_row"
            if self.sound_on == True and self.st[1] == "closed":
                time.sleep(0.2)
                self.open_sound.play()
            self.st[1] = "open" 
            self.guessed()        

    def game1_new_row (self):
        self.row += 1
        if self.row == 10:
            self.close_sound.play()
        if self.row == 11:
            self.st[0] = "stop_row"
            self.scorecode_history [0] += 11
            self.score_games [0] +=1
            self.print_multitext = True
            self.multitext = []
            self.multitext.append (no_more_room_1 [self.lang])
            self.multitext.append (no_more_room_2 [self.lang])
            self.multitext.append (play_again [self.lang])
            self.left_codes_clean()
            self.best_codes_clean()
            return
        self.st[0] = "current_row"
        self.pegcode_history.append([0,0,0,0])
        self.db_ac_bck = copy.deepcopy(self.db_ac)
        self.db_lc_bck = copy.deepcopy(self.db_lc)
        self.db_bc_bck = copy.deepcopy(self.db_bc)
        self.bc_bck = self.bc
        self.lc_bck = self.lc
        self.db_ac, self.db_lc, self.lc = self.left_codes(self.db_ac, self.ac, self.code_played, (self.whites, self.blacks))
        start_time = time.time()
        self.db_lc, self.db_bc, self.bc = self.best_codes(self.lc, self.db_ac, self.db_lc )
        elapsed_time =(time.time() - start_time)                #calcola quanto tempo impiega a generare i best codes
        print ("Tempo di elaborazione Best Codes:", elapsed_time)
        if self.st[4] == "LeftCodes_printed":
            self.left_codes_print()
        if self.st[5] == "BestCodes_printed":
            self.best_codes_print()
        self.st[3]= "Game1_active"       

###################### GAME 2 #######################
    def game2_wait (self):
        if self.st[1] == "open" and self.sound_on == True:
            self.close_sound.play()
        self.st=["stop_row","closed","Game2_current","Game2_wait","LeftCodes_no_printed", "BestCodes_no_printed"]
        self.db_ac, self.ac, self.db_lc, self.lc, self.db_bc, self.bc = self.init_db(self.colors)
        self.row = 1
        self.pegcode_history = []                                 #memorizza le giocate
        self.keycode_history = []
        self.leftcodes_history = []
        self.bestcodes_history = []
        self.ch = [0,0,0,0]
        self.secret_code = [0,0,0,0]
        if (self.scorecode_history[0] > 20 or self.scorecode_history[1] > 20) and self.score_games[0] == self.score_games[1]:
            self.scorecode_history = [0,0]
            self.score_games = [0,0]
        self.print_multitext = True
        self.multitext = []
        self.multitext.append (write_down_secret_code_1[self.lang])
        self.multitext.append (write_down_secret_code_2[self.lang])

    def game2_init(self):
        self.st=["current_row","closed","Game2_current","Game2_active","LeftCodes_no_printed", "BestCodes_no_printed"]
        self.code_played = self.db_bc[random.randrange(self.bc)]         ##il programma sceglie un codice da giocare tra i best codes
        self.print_row (self.code_played, self.row)
        self.peg_play_sound_4(self.code_played)
        
    def game2_input_keycode(self):
        pos = self.ev[2]            #info sulla posizione del bin cliccato. Default è 0 cioè primo bin a sx
        inc = self.ev[3]            #incremento positivo o negativo di 1 del colore del peg della posizione corrente
        self.ch[pos] += inc
        if self.ch[pos] == 3:       #se viene superato il numero massimo di colori, il colore torna a 1
            self.ch[pos] = 0
        self.print_key_row (self.ch, self.row)

    def game2_buttons(self):
        if self.ev[6] == "Wrongmark":
            self.ch = [0,0,0,0]
            self.print_key_row (self.ch, self.row)
        if self.ev[6] == "Shield":
            if self.st[1] == "closed":
                self.st[1] = "open"
                if self.sound_on == True:
                    self.open_sound.play()
            else:
                self.st[1] = "closed"
                if self.sound_on == True:
                    self.close_sound.play()
        if self.ev[6] == "Checkmark":
            self.whites = 0
            self.blacks = 0
            for i in range (4):
                if self.ch [i] == 1:
                    self.whites += 1
                if self.ch [i] == 2:
                    self.blacks += 1
            if self.whites == 1 and  self.blacks == 3:  #non accetta CH con 3 neri e 1 bianco
                self.print_multitext = True
                self.multitext = []
                self.multitext.append (keycode_not_allowed_1[self.lang])
                self.multitext.append (keycode_not_allowed_2[self.lang])
                if self.st[2] == "Game1_current":
                    self.st[3] = "Game1_active"
                if self.st[2] == "Game2_current":
                    self.st[3] = "Game2_active"
                self.left_codes_clean()
                self.best_codes_clean()
                return
            self.keycode_history.append (self.ch)
            if self.blacks == 4:                          #se inserisce 4 neri il codice segreto  è indovinato
                self.st[0] = "stop_row"
                self.guessed()
                return
            self.db_ac, self.db_lc, self.lc = self.left_codes(self.db_ac, self.ac, self.code_played, (self.whites, self.blacks))
            if self.lc==0:                                        #se non ci sono più codici possibili uno o più cod. chiave sono errati
                self.st[0] = "stop_row"
                self.st[4] = "LeftCodes_no_printed"
                self.st[5] = "BestCodes_no_printed"
                self.leftcodes_history = []
                self.bestcodes_history = []
                self.print_multitext = True
                self.multitext = []
                self.multitext.append (keycode_wrong [self.lang])
                self.multitext.append (play_again [self.lang])
                return
            start_time = time.time()
            self.db_lc, self.db_bc, self.bc = self.best_codes(self.lc, self.db_ac, self.db_lc )
            elapsed_time =(time.time() - start_time)
            self.st[0] = "new_row"          

    def game2_new_row (self):
        self.row += 1
        self.ch = [0,0,0,0]
        self.st[0] = "current_row"
        self.code_played = self.db_bc[random.randrange(self.bc)]         ##il programma sceglie un codice da giocare tra i best codes
        self.print_row (self.code_played, self.row)
        self.peg_play_sound_4(self.code_played)
        if self.lc==1:                                        #se il codice giocato è l'ultimo cioè è rimasto un solo fit code, il cod. segreto è indovinato
            self.st[0] = "stop_row"
            self.guessed()
            self.print_key_row ([2,2,2,2], self.row)
            self.keycode_history.append ([2,2,2,2])
            return
        if self.st[4] == "LeftCodes_printed":
            self.left_codes_print()
        if self.st[5] == "BestCodes_printed":
            self.best_codes_print()
        self.st[3]= "Game1_active"      

############## DEMO #######################

    def demo(self):                                             #partita dove il computer invina il codice segreto random
        if self.st[1] == "open" and self.sound_on == True:
            self.close_sound.play()
            time.sleep(0.2)
        self.db_ac, self.ac, self.db_lc, self.lc, self.db_bc, self.bc = self.init_db(self.colors)
        self.row = 1
        self.ch = [0,0,0,0]
        self.pegcode_history = []                                 #memorizza le giocate
        self.keycode_history = []                                 #memorizza i codici chiave
        self.left_codes_clean()
        self.best_codes_clean()
        self.secret_code = self.db_ac[random.randrange(self.ac)]     #il programma sceglie il codice segreto tra tutti i codici possibili                             #ripeti fino a un massimo di 10 tentativi
        self.st=["current_row","closed","Demo_current","Demo_active","LeftCodes_no_printed","BestCodes_no_printed"] 
        while True:
            self.code_played = self.db_bc[random.randrange(self.bc)]         ##il programma sceglie un codice da giocare tra i best codes
            self.print_row (self.code_played, self.row)
            self.peg_play_sound_4(self.code_played)
            self.whites, self.blacks = self.find_keycode(self.secret_code, self.code_played) #trova il codice chiave confrontando il cod tentativo con il cod segreto
            self.keycode = self.converti_keycode (self.whites, self.blacks)
            self.keycode_history.append(self.keycode)
            self.print_key_row(self.keycode, self.row)
            self.gui_refresh(self.row)
            pygame.display.flip()
            self.st[0] = "new_row"            
            if self.blacks == 4:
                break    
            self.row += 1
            self.db_ac, self.db_lc, self.lc = self.left_codes(self.db_ac, self.ac, self.code_played, (self.whites, self.blacks))
            start_time = time.time()
            self.db_lc, self.db_bc, self.bc = self.best_codes(self.lc, self.db_ac, self.db_lc )
            elapsed_time =(time.time() - start_time)                #calcola quanto tempo impiega a generare i best codes
            if self.row > 3:
                time.sleep(1.5)
        self.st[0] = "stop_row"
        self.st[1] = "open"
        if self.sound_on == True:
            time.sleep(0.2)
            self.open_sound.play()
        self.print_multitext = True
        self.multitext = []
        message = guessed_in_1 [self.lang] + str(self.row) + guessed_in_2 [self.lang]
        self.multitext.append (message)
        
################## Altre funzioni ###################################

    def converti_keycode (self, whites, blacks):         #coverte i bianchi e i neri in key_code [0,1,2,0] da visualizzare sulla board game
        key_code = [0,0,0,0]
        for i in range (0, whites):
            key_code[i] = 1
        for i in range (0, blacks):
            key_code[i + whites] = 2
        return key_code

    def six_colors (self):
        self.colors = 6
        if self.st[2] == "Game1_current":
            self.game1_init()
        if self.st[2] == "Game2_current":
            self.game2_wait()

    def eight_colors (self):
        self.colors = 8
        if self.st[2] == "Game1_current":
            self.game1_init()
        if self.st[2] == "Game2_current":
            self.game2_wait()

    def guessed (self):
        if self.st[2] == "Game1_current":
            self.scorecode_history [0] += self.row
            self.score_games [0] +=1
        if self.st[2] == "Game2_current":
            self.scorecode_history [1] += self.row
            self.score_games [1] +=1
        self.print_multitext = True
        self.multitext = []
        message = guessed_in_1 [self.lang] + str(self.row) + guessed_in_2 [self.lang]
        self.multitext.append (message)
        self.multitext.append (" ")
        self.print_multitext = True
        self.score_message()
        
    def score_message(self):
        if self.st[2] == "Game1_current":
            self.st[3] = "Game1_active"
        if self.st[2] == "Game2_current":
            self.st[3] = "Game2_active"
        if self.st[2] == "Demo_current":
            self.st[3] = "Demo_active"
        self.print_multitext = True
        self.print_score = True
        message = score_human [self.lang] + str(self.score_games[0]) + score_message [self.lang] + str(self.scorecode_history[0])
        self.multitext.append (message)
        message = score_computer [self.lang] + str(self.score_games[1]) + score_message [self.lang] + str(self.scorecode_history[1])
        self.multitext.append (message)
        if self.scorecode_history [0] > 20 and self.scorecode_history [0] > self.scorecode_history [1] and self.score_games[0] == self.score_games[1]:
            self.multitext.append (" ")
            self.multitext.append (you_lost [self.lang])
        if self.scorecode_history [1] > 20 and self.scorecode_history [1] > self.scorecode_history [0] and self.score_games[0] == self.score_games[1]:
            self.multitext.append (" ")
            self.multitext.append (you_won [self.lang])    
        self.left_codes_clean()
        self.best_codes_clean()
            
    def help (self):
        if self.btn_help_color == BROWN:
            self.st[3] = "Help_active"
            self.btn_help_color = BORDEAUX
            self.multitext = []
            self.print_multitext = True
            self.multitext.append (help_message [self.lang])
            self.left_codes_clean()
            self.best_codes_clean()
            if self.lang == 1:
                webbrowser.open("https://mastermind.altervista.org/vintage-master-mind-help-ita/", new=0, autoraise=True)
            if self.lang == 0:
                webbrowser.open("https://mastermind.altervista.org/vintage-master-mind-help-eng/", new=0, autoraise=True)
        else:
            self.btn_help_color = BROWN

    def options(self):
        self.st[3] = "Options_active"
        self.left_codes_clean()
        self.best_codes_clean()

    def color_bar_set(self):
        temp = self.color_bar_images [self.ev[11] - 1 ]
        self.color_bar_images [self.ev[11] - 1] = self.color_bar_images [self.ev[11] - 1 + 8]
        self.color_bar_images [self.ev[11] - 1 + 8] = temp

    def revert_row(self):
        self.row -= 1
        self.revert_flag = False
        self.db_ac = copy.deepcopy (self.db_ac_bck)
        self.db_lc = copy.deepcopy (self.db_lc_bck)
        self.db_bc = copy.deepcopy (self.db_bc_bck)
        self.cp = copy.deepcopy(self.cp_bck)
        print ("cp bck", self.cp)
        self.lc = self.lc_bck
        self.bc = self.bc_bck
        self.pegcode_history [self.row] = [0,0,0,0]
        self.keycode_history [self.row -1] = [0,0,0,0]
        self.keycode_history.pop()
        if self.st[4] == "LeftCodes_printed":
            self.left_codes_print()
        if self.st[5] == "BestCodes_printed":
            self.best_codes_print()

    def peg_play_sound(self):
        if self.sound_on == True and self.peg_sound_number == 1:
             self.peg_sound.play()
        self.peg_sound_number = 0

    def peg_play_sound_4(self, code_played ):
        if self.st[2] == "Game1_current":
            self.pegcode_history[self.row-1] = [0,0,0,0]
            self.gui_refresh(self.row)
            pygame.display.flip()
            time.sleep(0.2)
        self.pegcode_history.append ([0,0,0,0,True, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for i in range (4):
            self.pegcode_history[self.row-1][i] = code_played [i]
            self.gui_refresh(self.row)
            pygame.display.flip()
            if self.sound_on == True:
                self.peg_sound.play()
            time.sleep(0.2)

    def credits (self):
        if self.about == True:
            self.st[3] = "About_active"
            self.multitext = []
            self.print_multitext = True
            self.multitext.append ("")
            self.multitext.append ("      Vintage Master Mind")
            self.multitext.append ("email: zaffaroby@gmail.com")
            self.multitext.append ("web:   mastermind.altervista.org")
        else:
            self.about = BROWN

##frozen = 'not'
##if getattr(sys, 'frozen', False):
##        # we are running in a bundle
##        frozen = 'ever so'
##        bundle_dir = sys._MEIPASS
##else:
##        # we are running in a normal Python environment
##        bundle_dir = os.path.dirname(os.path.abspath(__file__))
##print( 'we are',frozen,'frozen')
##print( 'os.getcwd is', os.getcwd() )
ini_path = os.getcwd()
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)
##print( 'os.getcwd is', os.getcwd() )  
random.seed()
pygame.init()
clk = pygame.time.Clock()
clk.tick(30)                #numero di frame per secondo da inserire nel loop di visualizzazione delle immagini
mm = Mastermind()           #crea l'istanza della classe mastermind
if os.path.isfile(ini_path + "\config.ini"):
    mm.config_ini_read()    
else:
    mm.config_ini_write()
mm.gui_init()               #crea il background e tutti gli oggetti grafici
mm.st=["current_row","closed","Game1_current","Game1_active","LeftCodes_no_printed","BestCodes_no_printed" ]
mm.game1_init()
mm.gui_refresh(mm.row)
mm.print_checkmarks([1,2], mm.row)
pygame.display.flip()


while True:
    mm.peg_play_sound()
    mm.ev = [0,0,0,0,0,0,"",0,0,0,0]
    if mm.st[0] == "stop_row":
        while mm.ev[6] not in ("Game1", "Game2", "6Colors", "8Colors", "Score", "Help", "Options", "Demo", "Sound On", "Sound Off", "English", "Italiano", "Score Reset", "Color Bar ON", "Color Bar Off", "About", "Click here to start"):
            mm.events()
    else:
        mm.events()
    print ("--------------------------------------------------")
    print ("ev", mm.ev)
    btn = mm.ev[6]
    if btn == "6Colors" and mm.colors == 8:
        mm.six_colors()
    if btn == "8Colors" and mm.colors == 6:
        mm.eight_colors()
    if btn == "Game1":
        mm.game1_init()
    if btn == "Game2":
        mm.game2_wait()
    if btn == "Click here to start":
        mm.game2_init()
    if mm.st[2] == "Game1_current":
        if mm.ev[1]!=0 or mm.ev[5]!=0:                      # incremento del peg o tasti freccia su/giù
            mm.game1_input_guess()
        if mm.ev[4]!=0:                                     # tasti freccia sx/dx
            mm.game1_bin_change()
        if btn in ["Shield", "Wrongmark", "Checkmark", "Invio"]:
            mm.game1_buttons()      
    if mm.st[2] == "Game2_current":
        if mm.ev[3] == 1:                                   # incremento del peg o tasti freccia su/giù
            mm.game2_input_keycode()
        if btn in ["Shield", "Wrongmark", "Checkmark"]:
            mm.game2_buttons()
    if btn == "LeftCodes":
        if mm.st[4] == "LeftCodes_no_printed":                          
            mm.left_codes_print()                           # stampa i left codes
        else:
            mm.left_codes_clean()                           # rimuovi i left codes dallo
            mm.st[4] = "LeftCodes_no_printed"
    if mm.st[4] == "LeftCodes_printed" and mm.ev[9]!=0:
        mm.left_codes_scroll()
    if mm.st[4] == "LeftCodes_printed" and mm.ev[7]>0:
        mm.left_codes_picked_up()
    if btn == "BestCodes":
        if mm.st[5] == "BestCodes_no_printed":                          
            mm.best_codes_print()                           # stampa i best codes
        else:
            mm.best_codes_clean()                           # rimuovi i best codes dallo
            mm.st[5] = "BestCodes_no_printed"
    if mm.st[5] == "BestCodes_printed" and mm.ev[10]!=0:
        mm.best_codes_scroll()
    if mm.st[5] == "BestCodes_printed" and mm.ev[8]>0:
        mm.best_codes_picked_up()       
    if mm.st[2] == "Game1_current" and mm.st[0] == "new_row":
            mm.game1_new_row()
    if mm.st[2] == "Game2_current" and mm.st[0] == "new_row":
            mm.game2_new_row()
    if btn == "Score":
        mm.score_message()
    if btn == "Help":
        mm.help()
    if btn == "Options":
        mm.options()
    if btn == "Sound On":
        mm.sound_on = True
    if btn == "Sound Off":
        mm.sound_on = False
    if btn == "English":
        mm.lang = 0
    if btn == "Italiano":
        mm.lang = 1
    if btn == "Color Bar ON":
        mm.color_bar_on = True
    if btn == "Color Bar Off":
        mm.color_bar_on = False
    if btn == "Score Reset":
        mm.scorecode_history = [0,0]
        mm.score_games = [0,0]
        mm.score_reset = True
    if btn == "Demo":
        mm.demo()
    if mm.ev[11] > 0:
        mm.color_bar_set()
    if btn == "Revert":
        mm.revert_row()
    if btn == "About":
        mm.about = True
        mm.credits()
    print ("st", mm.st)
    mm.gui_refresh(mm.row)
    pygame.display.flip()

"""
ev[0] 0-3  la posizione corrente della scelta del peg della combinazione tentativo
ev[1] 1 o -1 per passare al peg succesivo o precedente (INC peg)
ev[2] 0-3  la posizione del key peg corrente
ev[3] 1  passa dal vuoto, bianco al nero  posizione del key peg succesivo o precedente (INC key peg)
ev[4] -1 o 1 per i tasti sx e dx
ev[5] -1 o 1 per i tasti su e giu
ev[6] "", "invio", "Check", "Wrong", "Revert", "About"  è il bottone cliccato
ev[7] 1-10  il left code scelto dalla lista a video
ev[8] 1-10  il best code scelto dalla lista a video
ev[9] -1 o +1 bottoni freccia per scrolling lista left code
ev[10] -1 o +1 bottoni freccia per scrolling lista best code
ev[11] da 0 a colors - color bar
-----------------------
st[0] "new_row", "stop_row, "current_row"
st[1] board: "closed" o "open"
st[2] current game : "Game1_current" o "Game2_current" o "Demo" - contiene sempre uno di questi valori
st[3] what is active:  Game1_active o game2_active o Left_active o Best_active o Options_active o Demo_active o Help_active o Game2_wait usato da events()
st[4] LeftCodes_printed o LeftCodes_no_printed
st[5] BestCodes_printed o BestCodes_no_printed
"""


