### Bibliothek spiel.py
### Stand Sep 2018, Copyright Wilhelm Buechner Hochschule

### Eine Änderung an dieser Datei ist nicht erlaubt!!!
### Eine Änderung an dieser Datei ist nicht erforderlich. Kann aber gern geschehen. :-)
### Dann aber vorher Backup machen! 

from dis import show_code
import pygame, sys, time
import os
from configparser import ConfigParser

class Einstellungen():
    fps = 40 # Frames pro Sekunde

    # Dimensionen
    fensterBreite = 640
    fensterHoehe = 480
    linienDicke = 10
    abstand = 2*linienDicke
    schlaegerBreite = 10
    schlaegerHoehe = 50
    schriftGroesse = 16
    ballRadius = 5 # nur fuer runden Ball notwendig

    def __init__(self):
        # Notwendige Initialisierung fuer pygame
        pygame.init()
        pygame.display.set_caption('Pong')

    def fenster_mitte(self):
        return self.fensterHoehe // 2

    def schlaeger_mitte(self):
        return self.fenster_mitte() - self.schlaegerHoehe // 2

    def linker_rand(self):
        return self.abstand

    def rechter_rand(self):
        return self.fensterBreite - self.schlaegerBreite - self.abstand

    def schrift(self):
        return pygame.font.SysFont('arial', self.schriftGroesse, bold=True)

'''Idealer Weise waere dies kein globales Objekt'''
config = Einstellungen()


class Form(pygame.sprite.Sprite):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=pygame.Color('white')):
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.geschwindigkeit = geschwindigkeit
        self.farbe = farbe


class Rectangle(Form):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=pygame.Color('white')):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)

    def draw(self, fensterFlaeche):
        pygame.draw.rect(fensterFlaeche, self.farbe, self.rect)


class Circle(Form):
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=pygame.Color('white')):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.rect = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        self.radius = config.ballRadius

    def draw(self, fensterFlaeche):
        pygame.draw.circle(fensterFlaeche, self.farbe,
                           (self.rect.x, self.rect.y), self.radius)


class Willkommen():
    # Willkommensbildschirm beim Programmstart
    def __init__(self, fensterFlaeche):
        popupFenster = pygame.Rect((config.linker_rand()+80, config.linker_rand()+60),
                (config.fensterBreite*2//3, config.fensterHoehe*1//3))
        fensterFlaeche.fill(pygame.Color('white'), popupFenster)
        textZeile1='Willkommen zu Pong'
        textZeile2='Spielstart mit beliebiger Taste'
        textWidth1 , textHeight1 = config.schrift().size(textZeile1)
        textWidth2 , textHeight2 = config.schrift().size(textZeile2)
        zeile1 = config.schrift().render(textZeile1, False, pygame.Color('black'))
        xZeile1 = (config.fensterBreite-textWidth1)//2
        yZeile1 = (config.fensterHoehe*2//3-textHeight1)//2
        zeile2 = config.schrift().render(textZeile2, False, pygame.Color('black'))
        xZeile2 = (config.fensterBreite-textWidth2)//2
        yZeile2 = (config.fensterHoehe-config.abstand-textHeight2)//2
        fensterFlaeche.blit(zeile1, (xZeile1, yZeile1))
        fensterFlaeche.blit(zeile2, (xZeile2, yZeile2))

#Erweiterung Highscore
class InputBox():
    def __init__(self, fensterFlaeche):
        self.fensterFlaeche = fensterFlaeche
        
        box_breite = 140
        box_hoehe = 32

        self.popupFenster = pygame.Rect((config.linker_rand()+80, config.linker_rand()+60),
                (config.fensterBreite*2//3, config.fensterHoehe*2//3))
        fensterFlaeche.fill(pygame.Color('white'), self.popupFenster)

        self.input = pygame.Rect((config.fensterBreite-box_breite*1.5)//2, config.fensterHoehe//2, box_breite, box_hoehe)
        self.font = pygame.font.Font(None, 28)
        self.timer = pygame.time.Clock()

        self.color_focus = pygame.Color('red')
        self.color_not_focus = pygame.Color('yellow')
        self.color_finished_writing = pygame.Color('green')
        self.curr_color = self.color_not_focus

        textZeile='Type in name:'
        textWidth , textHeight = config.schrift().size(textZeile)
        self.zeile = config.schrift().render(textZeile, False, pygame.Color('black'))
        xZeile = (config.fensterBreite-textWidth)//2
        yZeile = (config.fensterHoehe*2//3-textHeight)//2
        self.zeilen_koordinate = (xZeile, yZeile)
        self.fensterFlaeche.blit(self.zeile, self.zeilen_koordinate)

    def ask_for_name(self):
        name=''
        focus = False
        writing = True
        while writing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    writing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if self.input.collidepoint(event.pos):
                        # Toggle the active variable.
                        focus = not focus
                    else:
                        focus = False
                    # Change the current color of the input box.
                    self.curr_color = self.color_focus if focus else self.color_not_focus
                    
                if event.type == pygame.KEYDOWN:
                    if focus:
                        if event.key == pygame.K_RETURN:
                            return name
                        elif event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            name += event.unicode

            self.fensterFlaeche.fill(pygame.Color('white'), self.popupFenster)
            txt_surface = self.font.render(name, True, self.curr_color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            self.input.w = width
            # Blit the text.
            self.fensterFlaeche.blit(txt_surface, (self.input.x+5, self.input.y+5))
            self.fensterFlaeche.blit(self.zeile, self.zeilen_koordinate)
            # Blit the input_box rect.
            pygame.draw.rect(self.fensterFlaeche, self.curr_color, self.input, 2)

            pygame.display.flip()
            self.timer.tick(30)

#Erweiterung Highscore
class Highscore():
    def __init__(self, fensterFlaeche):
        self.config_file = ConfigParser()
        self.config_file_path = './pong.ini'

        self.try_read_config()

        self.fensterFlaeche = fensterFlaeche

    def draw_highscore(self, new_highscore=False, name='', punkte_stand=0):
        if new_highscore: self.update_highscore_dict(name, punkte_stand)

        names_dict = dict(self.config_file.items('Highscore_Names'))
        highscore_dict = dict(self.config_file.items('Highscores'))

        margin_links = config.linker_rand()+80
        margin_oben = config.linker_rand()+60

        popupFenster = pygame.Rect((margin_links, margin_oben),
                (config.fensterBreite*2//3, config.fensterHoehe*2//3))
        self.fensterFlaeche.fill(pygame.Color('white'), popupFenster)

        textZeile='Highscores:'
        textWidth , textHeight = config.schrift().size(textZeile)
        zeile = config.schrift().render(textZeile, False, pygame.Color('black'))
        xZeile = (config.fensterBreite-textWidth)//2
        yZeile = (config.fensterHoehe*2//3-textHeight)//2
        self.fensterFlaeche.blit(zeile, (xZeile, yZeile))

        textZeile_first_highscore = f"1. {names_dict['first']} - {highscore_dict['first']}"
        textWidth_first_highscore , textHeight_first_highscore = config.schrift().size(textZeile_first_highscore)
        zeile_first_highscore = config.schrift().render(textZeile_first_highscore, False, pygame.Color('black'))
        xZeile_first_highscore = (config.fensterBreite-textWidth_first_highscore)//2
        yZeile_first_highscore = config.fensterHoehe*2//3-textHeight_first_highscore*12+margin_oben
        self.fensterFlaeche.blit(zeile_first_highscore, (xZeile_first_highscore, yZeile_first_highscore))

        textZeile_second_highscore = f"2. {names_dict['second']} - {highscore_dict['second']}"
        textWidth_second_highscore , textHeight_second_highscore = config.schrift().size(textZeile_second_highscore)
        zeile_second_highscore = config.schrift().render(textZeile_second_highscore, False, pygame.Color('black'))
        xZeile_second_highscore = (config.fensterBreite-textWidth_second_highscore)//2
        yZeile_second_highscore = config.fensterHoehe*2//3-textHeight_second_highscore*10+margin_oben
        self.fensterFlaeche.blit(zeile_second_highscore, (xZeile_second_highscore, yZeile_second_highscore))

        textZeile_third_highscore = f"3. {names_dict['third']} - {highscore_dict['third']}"
        textWidth_third_highscore , textHeight_third_highscore = config.schrift().size(textZeile_third_highscore)
        zeile_third_highscore = config.schrift().render(textZeile_third_highscore, False, pygame.Color('black'))
        xZeile_third_highscore = (config.fensterBreite-textWidth_third_highscore)//2
        yZeile_third_highscore = config.fensterHoehe*2//3-textHeight_third_highscore*8+margin_oben
        self.fensterFlaeche.blit(zeile_third_highscore, (xZeile_third_highscore, yZeile_third_highscore))      

        textZeile_continue='Spielstart mit beliebiger Taste'
        textWidth_continue , textHeight_continue = config.schrift().size(textZeile_continue)
        zeile_continue = config.schrift().render(textZeile_continue, False, pygame.Color('black'))
        xZeile_continue = (config.fensterBreite-textWidth_continue)//2
        yZeile_continue = config.fensterHoehe*2//3-textHeight_continue*2+margin_oben
        self.fensterFlaeche.blit(zeile_continue, (xZeile_continue, yZeile_continue))

        textZeile_exit='ESC = exit'
        textWidth_exit , textHeight_exit = config.schrift().size(textZeile_exit)
        zeile_exit = config.schrift().render(textZeile_exit, False, pygame.Color('black'))
        xZeile_exit = (config.fensterBreite-textWidth_exit)//2
        yZeile_exit = config.fensterHoehe*2//3-textHeight_exit+margin_oben
        self.fensterFlaeche.blit(zeile_exit, (xZeile_exit, yZeile_exit))

    def is_new_highscore(self, punkte):
        highscore_third = int(self.config_file['Highscores']['third'])
        return highscore_third < punkte

    def try_read_config(self):
        if os.path.exists(self.config_file_path):
            self.config_file.read(self.config_file_path)
        else:
            self.config_file.add_section('Highscore_Names')
            self.config_file.set('Highscore_Names', 'first', '')
            self.config_file.set('Highscore_Names', 'second', '')
            self.config_file.set('Highscore_Names', 'third', '')
            
            self.config_file.add_section('Highscores')
            self.config_file.set('Highscores', 'first', '0')
            self.config_file.set('Highscores', 'second', '0')
            self.config_file.set('Highscores', 'third', '0')

            with open(self.config_file_path, 'xt') as file:    # save
                self.config_file.write(file)
        
    def update_highscore_dict(self, name, punkte):
        highscore_dict = dict(self.config_file.items('Highscores'))
        if int(highscore_dict['first']) < punkte:
            self.config_file.set('Highscore_Names', 'third', self.config_file.get('Highscore_Names', 'second')) # 2 -> 3
            self.config_file.set('Highscores', 'third', self.config_file.get('Highscores', 'second'))
            self.config_file.set('Highscore_Names', 'second', self.config_file.get('Highscore_Names', 'first')) # 1 -> 2
            self.config_file.set('Highscores', 'second', self.config_file.get('Highscores', 'first'))

            self.config_file.set('Highscore_Names', 'first', name)
            self.config_file.set('Highscores', 'first', str(punkte))

        elif int(highscore_dict['second']) < punkte:
            self.config_file.set('Highscore_Names', 'third', self.config_file.get('Highscore_Names', 'second')) # 2 -> 3
            self.config_file.set('Highscores', 'third', self.config_file.get('Highscores', 'second'))
            self.config_file.set('Highscore_Names', 'second', name)
            self.config_file.set('Highscores', 'second', str(punkte))

        elif int(highscore_dict['third']) < punkte:
            self.config_file.set('Highscore_Names', 'third', name)
            self.config_file.set('Highscores', 'third', str(punkte))
        else:
            return
        
        with open(self.config_file_path, 'wt') as file:    # save
            self.config_file.write(file)

                
class Spiel():
    # Initialisierung (OOP Konstruktor)
    def __init__(self, spielfeld, spieler, computer, ball, punkteAnzeige):

        self.running = False
        self.exit_game = False

        self.punkte = 0
        self._fpsTimer = pygame.time.Clock()

        self._spielfeld = spielfeld
        self._fensterFlaeche = pygame.display.set_mode(
            (config.fensterBreite, config.fensterHoehe))
        self._spieler = spieler
        self._computer = computer
        self._ball = ball
        self._ball_start_geschwindigkeit = ball.geschwindigkeit
        self._ball_start_x = ball.x
        self._ball_start_y = ball.y
        self._allSchlaeger = [self._spieler, self._computer] # Liste
        self._punkteAnzeige = punkteAnzeige
        self.hornSound = pygame.mixer.Sound("Sounds/horn.wav")
        self.booSound = pygame.mixer.Sound("Sounds/boo.wav")

    def set_start_conditions(self):
        self.punkte = 0
        self._ball.geschwindigkeit = self._ball_start_geschwindigkeit
        self._ball.rect.x = self._ball_start_x
        self._ball.rect.y = self._ball_start_x 


    def run(self):
        '''
        Spielschleife - Game Loop Pattern, siehe auch:
        http://gameprogrammingpatterns.com/game-loop.html
        '''
        #Erweiterung Highscore
        show_welcome_screen = True
        while not self.exit_game:
            # Willkommensbildschirm anzeigen, weiter mit Taste
            if not show_welcome_screen: 
                pygame.mouse.set_visible(1)  # setze Mauszeiger sichtbar
                highscore_board = Highscore(self._fensterFlaeche)
                new_highscore = highscore_board.is_new_highscore(self.punkte)
                if new_highscore:
                    name_player = InputBox(self._fensterFlaeche).ask_for_name()
                    highscore_board.draw_highscore(new_highscore, name_player, self.punkte)
                highscore_board.draw_highscore()
                
            else: 
                Willkommen(self._fensterFlaeche)
                
            while not self.running:
                pygame.display.update()
                # Ueberpruefe ob Taste gedrueckt wurde
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN: self.running = True

            
            pygame.mouse.set_visible(0)  # setze Mauszeiger unsichtbar
            show_welcome_screen = False # The Welcome-screen should only be shown once at the beginning from the execution
            self.set_start_conditions()
            # Spielschleife
            while self.running:
                self._ereignisse_behandeln()
                self._update()
                self._zeichnen()
                pygame.display.update()
                self._fpsTimer.tick(config.fps)

    def _ereignisse_behandeln(self):
        # Ereignis abfragen
        for ereignis in pygame.event.get():
            self._behandle(ereignis)

    def _behandle(self, event):
        # Ueberpruefe ob Schliessen-Symbol im Fenster gedrueckt wurde
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            return
        # Ueberpruefe ob Maus bewegt wurde
        elif event.type == pygame.MOUSEMOTION:
            self._spieler.move(event.pos)
            return
        return event

    def _update(self):
        self._bewegen()
        self._aufprall_berechnen()

    def _bewegen(self):
        self._ball.move()
        self._computer.move(self._ball)

    def _aufprall_berechnen(self):
        if self._ball.hit_schlaeger(self._computer):
            self._ball.bounce('x')

        elif self._ball.hit_schlaeger(self._spieler):
            self._ball.bounce('x')
            self.punkte += 1
            self._ball.geschwindigkeit += 1
            print("Hit Schlaeger", self._ball.geschwindigkeit) 

        elif self._ball.trefferComputer():
            self.punkte += 5
            # horn-Sound abspielen
            self.hornSound.play()

        elif self._ball.trefferSpieler():
            # boo-Sound abspielen
            self.booSound.play()
            
            #Erweiterung Highscore
            self.running = False

    def _zeichnen(self):
        self._spielfeld.draw(self._fensterFlaeche)
        self._ball.draw(self._fensterFlaeche)
        for schlaeger in self._allSchlaeger:
            schlaeger.draw(self._fensterFlaeche)
        self._punkteAnzeige.draw(self.punkte, self._fensterFlaeche)


class Spielfeld():
    # Initialisierung (OOP Konstruktor)
    def __init__(self, farbe=pygame.Color('black')):
        self.farbe = farbe

    def draw(self, fensterFlaeche):
        fensterFlaeche.fill(self.farbe)
        self._umrandung(fensterFlaeche)
        self._mittellinie(fensterFlaeche)

    def _umrandung(self, fensterFlaeche):
        pygame.draw.rect(fensterFlaeche, pygame.Color('white'),
                ((0, 0), (config.fensterBreite, config.fensterHoehe)),
                config.linienDicke*2)

    def _mittellinie(self, fensterFlaeche):
        pygame.draw.line(fensterFlaeche, pygame.Color('white'),
                 (config.fensterBreite//2, 0),
                 (config.fensterBreite//2, config.fensterHoehe),
                  config.linienDicke//4)


class Ball(Circle): # Alternativer Parameter: Circle
    # Pfeiltasten
    LEFT = -1
    RIGHT = 1
    UP = -1
    DOWN = 1

    # Initialisierung (OOP Konstruktor)
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, farbe=pygame.Color('white')):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self.richtungX = self.LEFT
        self.richtungY = self.UP
        self.startGeschwindigkeit = geschwindigkeit
        #self.boingSound = pygame.mixer.Sound("Sounds/boing.wav") 

    # Funktion zum Bewegen des Balls, neue Position setzen
    def move(self):
        self.rect.x += (self.richtungX * self.geschwindigkeit)
        self.rect.y += (self.richtungY * self.geschwindigkeit)

        # Pruefe Kollision mit Wand
        if self.hit_ceiling() or self.hit_floor():
            self.bounce('y')
        if self.hit_wall():
            self.bounce('x')

    # Richtungsaenderung fuer Ball
    def bounce(self, axis):
        if axis == 'x':
            self.richtungX *= -1
        elif axis == 'y':
            self.richtungY *= -1
        # Bounce-Sound abspielen
        # self.boingSound.play() 

    # Treffen von Ball auf Schlaeger
    def hit_schlaeger(self, schlaeger):
        return pygame.sprite.collide_rect(self, schlaeger)

    # Treffen von Ball auf Wand links oder rechts
    def hit_wall(self):
        return (
            (self.richtungX == -1
                and self.rect.left <= self.breite) or
            (self.richtungX ==  1
                and self.rect.right >= config.fensterBreite - self.breite)
        )

    # Treffen von Ball auf Decke
    def hit_ceiling(self):
        return self.richtungY == -1 and self.rect.top <= self.breite

    # Treffen von Ball auf Boden
    def hit_floor(self):
        return (self.richtungY == 1
                and self.rect.bottom >= config.fensterHoehe - self.breite)

    def trefferSpieler(self):
        return self.rect.left <= self.breite

    def trefferComputer(self):
        return self.rect.right >= config.fensterBreite - self.breite


class Schlaeger(Rectangle):
    # Funktion zum Zeichnen des Schlaegers
    def draw(self, fensterFlaeche):
        # Stoppt Schlaeger am unteren Spielfeldrand
        if self.rect.bottom > config.fensterHoehe - config.linienDicke:
            self.rect.bottom = config.fensterHoehe - config.linienDicke
        # Stoppt Schlaeger am oberen Spielfeldrand
        elif self.rect.top < config.linienDicke:
            self.rect.top = config.linienDicke+1 # randkorrektur

        super().draw(fensterFlaeche)

    # Funktion zum Bewegen des Schlaegers mit Maus
    def move(self, pos):
        self.rect.y = pos[1]


class AutoSchlaeger(Schlaeger):
    # Initialisierung (OOP Konstruktor)
    def __init__(self, x, y, breite, hoehe, geschwindigkeit, ball, farbe=pygame.Color('white')):
        super().__init__(x, y, breite, hoehe, geschwindigkeit, farbe)
        self._ball = ball

    # Automatische Bewegung, richtet sich nach dem Ball
    def move(self, pos):
        # Wenn Ball sich vom Schlaeger wegbewegt, zentriere ihn
        if self._ball.richtungX == -1:
            self._zentrieren()
        # Wenn Ball sich auf Schlaeger zubewegt, beoachte seine Bewegung
        elif self._ball.richtungX == 1:
            self._beobachten()

    def _beobachten(self):
        if self.rect.centery < self._ball.rect.centery:
            self.rect.y += self.geschwindigkeit
        else:
            self.rect.y -= self.geschwindigkeit

    def _zentrieren(self):
        if self.rect.centery < config.fenster_mitte():
            self.rect.y += self.geschwindigkeit
        elif self.rect.centery > config.fenster_mitte():
            self.rect.y -= self.geschwindigkeit


class PunkteAnzeige():
    # Initialisierung (OOP Konstruktor)
    def __init__(self, punkte, x, y, schrift, farbe=pygame.Color('white')):
        self.punkte = punkte
        self.x = x
        self.y = y
        self.schrift = schrift
        self.farbe = farbe

    # Schreibe aktuellen Punktestand an den Bildschirm
    def draw(self, punkte, fensterFlaeche):
        self.punkte = punkte
        result_surf = self.schrift.render('Punkte: %s' %(self.punkte), True, self.farbe)
        rect = result_surf.get_rect()
        rect.topleft = (self.x, self.y)
        fensterFlaeche.blit(result_surf, rect)
