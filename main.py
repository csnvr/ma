import kivy
from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivy.lang import Builder
from kivymd.uix.navigationdrawer import NavigationLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.textfield import MDTextField
from kivy.core.audio import SoundLoader
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import random
import time
###
'''
root.parent.transition.direction = 'left'
root.parent.current = 'main_screen'
'''

#TODO ONLY FOR DEVELOPMENT...REMOVE WHEN DOING APK
from kivy.core.window import Window
k=16/9
x=400
y=x*k
Window.size=(x,y)
###

global Gameboard
Gameboard = {1: '', 2: '', 3: '',
             4: '', 5: '', 6: '',
             7: '', 8: '', 9: '', }

global znak
znak = 'X'

global st_potez
st_potez = 0

##
class ScreenWelcome(Screen):
    def build(self):
        #self.add_widget(MDIconButton(name='welcome_button'))
        #self.add_widget(MDTextField(name='phone_input'))
        #self.phone_number=phone_input.text if len(phone_input) is 13 else ''
        #return ScreenWelcome
        pass
    def welcome_button(self):
        global phoneN
        phoneN=self.ids.phone_input.text
        if len(phoneN) == 13 and phoneN[0]=='0' and phoneN[1]=='0' and phoneN[2]=='3' and phoneN[3]=='8' and phoneN[4]=='6' and phoneN[5]!='0':
            valid=True
            print(phoneN)
        else:
            valid=True#False #TODO pazi da das to nazaj na false da bo preverjal telefonsko stevilko
        if valid:
            MDApp.get_running_app().screen_manager.transition.direction = 'left'
            MDApp.get_running_app().screen_manager.current = 'main_screen'
        else:
            self.ids.info_text.text = f'{self.ids.info_text.text}\nPlease insert valid phone number'

        global gamemode
        gamemode = ''
        # predvajanje zvoka
        '''
        sound = SoundLoader.load('B1TB01 - Sunrise.mp3')
        if sound:
            print('Now playing: B1TB01 - Sunrise')
        sound.play()
        '''

    pass

class ScreenSettings(Screen):
    def back(self):
        MDApp.get_running_app().screen_manager.transition.direction = 'right'
        MDApp.get_running_app().screen_manager.current = 'main_screen'
    pass

class ScreenMain(Screen):
    def welcome(self):
        MDApp.get_running_app().screen_manager.transition.direction = 'right'
        MDApp.get_running_app().screen_manager.current= 'welcome_screen'
    def settings(self):
        MDApp.get_running_app().screen_manager.transition.direction = 'left'
        MDApp.get_running_app().screen_manager.current = 'settings_screen'
    pass

    def prepare_for_game(self):
            # zamenja tab na igro
        self.ids.bottom_navigation.switch_tab('game_tab')

            #resetira ploščo
        self.ids.image_1.source = 'blackpixel.jpg'
        self.ids.image_2.source = 'blackpixel.jpg'
        self.ids.image_3.source = 'blackpixel.jpg'
        self.ids.image_4.source = 'blackpixel.jpg'
        self.ids.image_5.source = 'blackpixel.jpg'
        self.ids.image_6.source = 'blackpixel.jpg'
        self.ids.image_7.source = 'blackpixel.jpg'
        self.ids.image_8.source = 'blackpixel.jpg'
        self.ids.image_9.source = 'blackpixel.jpg'

            # resetira Gameboard
        global Gameboard
        Gameboard = {1: '', 2: '', 3: '',
                     4: '', 5: '', 6: '',
                     7: '', 8: '', 9: '', }

            # resetira tip konca igre
        global end_type
        end_type = ''

            # resetira stevilo potez
        global st_potez
        st_potez = 0

            # resetira znak na X
        global znak
        znak = 'X'

            # globalno spremenljivko za popup
        global popup
        popup = False

    def start_multiplayer(self):
        sound = SoundLoader.load('bloody.mp3')
        if sound:
            print('FU')
        sound.play()

    def start_bot(self):
            # funkcija ki pripravi na igro
        self.prepare_for_game()
            # doloci vrsto igre na coop
        global gamemode
        gamemode = 'bot'
        nakl=random.randint(0,1)
        if nakl==1:
            self.iai()

    def start_coop(self):
            # pripravi gameboard na igro
        self.prepare_for_game()
            # doloci vrsto igre na coop
        global znak
        znak = 'X'
        global gamemode
        gamemode = 'coop'

    def check(self):
            # preverjanje ce je kdo zmagal
        global Gameboard
        global end_type
        global znak
        global gamemode
        global popup

        ''' najprej preveri ce je vec ali enako kot 5 potez, nato pa vsako mozno zmago in preveri tudi da ta polja vsebujejo x ali o, da ne vrne zamago ce so tri prazna polja v zmagovalni kombinaciji'''


        if (Gameboard[1] == Gameboard[2] == Gameboard[3] and Gameboard[1] in ['X', 'O']) or (Gameboard[4] == Gameboard[5] == Gameboard[6] and Gameboard[4] in ['X', 'O']) or (Gameboard[7] == Gameboard[8] == Gameboard[9] and Gameboard[7] in ['X', 'O']):
            end_type = znak
            print('check1')

        elif (Gameboard[1] == Gameboard[4] == Gameboard[7] and Gameboard[1] in ['X', 'O']) or (Gameboard[2] == Gameboard[5] == Gameboard[8] and Gameboard[2] in ['X', 'O']) or (Gameboard[3] == Gameboard[6] == Gameboard[9] and Gameboard[3] in ['X', 'O']):
            end_type = znak
            print('check2')

        elif (Gameboard[1] == Gameboard[5] == Gameboard[9] or Gameboard[3] == Gameboard[5] == Gameboard[7]) and Gameboard[5] in ['X', 'O']:
            end_type = znak
            print('check3')

            # ce je konec igre zakljuci igro
        if end_type == 'X' and not popup:
            popup = True
            ok_button = MDFlatButton(text='OK', on_release =self.ok_button)
            playagain_button = MDFlatButton(text='Play Again', on_release=self.playagain_button)
            self.dialog = MDDialog(title='Congrats X!' if gamemode == 'coop' else 'Congrats!', text='You are the winner!', size_hint=(0.5, 1),
                                   buttons=[playagain_button, ok_button])
            self.dialog.open()
            #time.sleep(2)
            #self.dialog.dismiss()
            # self.ids.bottom_navigation.switch_tab('play_tab') ----to bom dal ko bo pritisnil na gumb ok

        elif end_type == 'O' and not popup:
            popup =True
            ok_button = MDFlatButton(text='OK', on_release=self.ok_button)
            playagain_button = MDFlatButton(text='Play Again', on_release=self.playagain_button)
            self.dialog = MDDialog(title='Congrats O!' if gamemode == 'coop' else 'You Lost! :(', text='You are the winner!' if gamemode == 'coop' else 'Better luck next time!', size_hint=(0.5, 1),
                                   buttons=[playagain_button, ok_button])
            self.dialog.open()
            #time.sleep(2)
            #self.dialog.dismiss()

        elif st_potez == 9 and end_type == '' and not popup:
            popup = True
            ok_button = MDFlatButton(text='OK', on_release=self.ok_button)
            playagain_button = MDFlatButton(text='Play Again', on_release=self.playagain_button)
            self.dialog = MDDialog(title="It's a Tie!", text='Better luck next time!', size_hint=(0.5, 1),
                                   buttons=[playagain_button, ok_button])
            self.dialog.open()
            print('izenaceno')
            #time.sleep(2)
            #self.dialog.dismiss()

# A. K. A. IMPRESSIVE ARTIFICIAL INTELlIGENCE
    def iai(self):
        #print('ai activated')
        global Gameboard
        global znak
        global st_potez

#Doloci znak za ai O
        znak = 'O'
        st_potez += 1

        already = False
# preverja za vse možne vodoravne
        for x in [1, 4, 7]:
            if Gameboard[x] == Gameboard[x + 1] and Gameboard[x + 2] not in ['X', 'O'] and Gameboard[x] != '':
                Gameboard[x + 2] = znak
                already = True
                break
            elif Gameboard[x] == Gameboard[x + 2] and Gameboard[x + 1] not in ['X', 'O'] and Gameboard[x] != '':
                Gameboard[x + 1] = znak
                already = True
                break
            elif Gameboard[x + 1] == Gameboard[x + 2] and Gameboard[x] not in ['X', 'O'] and Gameboard[x+1] != '':
                Gameboard[x] = znak
                already = True
                break

# preverja za vse možne navpične
        if not already:
            for x in [1, 2, 3]:
                if Gameboard[x] == Gameboard[x + 3] and Gameboard[x + 6] not in ['X', 'O'] and Gameboard[x] != '':
                    Gameboard[x + 6] = znak
                    already = True
                    break
                elif Gameboard[x] == Gameboard[x + 6] and Gameboard[x + 3] not in ['X', 'O'] and Gameboard[x] != '':
                    Gameboard[x + 3] = znak
                    already = True
                    break
                elif Gameboard[x + 3] == Gameboard[x + 6] and Gameboard[x] not in ['X', 'O'] and Gameboard[x+3] != '':
                    Gameboard[x] = znak
                    already = True
                    break

# preverja za 1. diagonalo
        if not already:
            if Gameboard[1] == Gameboard[5] and Gameboard[9] not in ['X', 'O'] and Gameboard[1] != '':
                Gameboard[9] = znak
                already = True
            elif Gameboard[1] == Gameboard[9] and Gameboard[5] not in ['X', 'O'] and Gameboard[1] != '':
                Gameboard[5] = znak
                already = True
            elif Gameboard[5] == Gameboard[9] and Gameboard[1] not in ['X', 'O'] and Gameboard[5] != '':
                Gameboard[1] = znak
                already = True

# preverja za 2. diagonalo
        if not already:
            if Gameboard[3] == Gameboard[5] and Gameboard[7] not in ['X', 'O'] and Gameboard[3] != '':
                Gameboard[7] = znak
                already = True
            elif Gameboard[3] == Gameboard[7] and Gameboard[5] not in ['X', 'O'] and Gameboard[3] != '':
                Gameboard[5] = znak
                already = True
            elif Gameboard[5] == Gameboard[7] and Gameboard[3] not in ['X', 'O'] and Gameboard[5] != '':
                Gameboard[3] = znak
                already = True

# če ni nič izbere naključno
        if not already:
            while True:
                nakljucno = random.randint(1, 9)
                if Gameboard[nakljucno] not in ['X', 'O']:
                    Gameboard[nakljucno] = znak
                    #print(Gameboard[nakljucno],znak)
                    #print(nakljucno,'to je nakljucna ki si ga ai izbere')
                    break

# posodobi igralno plosco
        for i in range(1,10):
            if Gameboard[i] =='O':
                #print(i,'se posodablja')
                if i == 1:
                    self.ids.image_1.source = 'O.jpg'
                elif i == 2:
                    self.ids.image_2.source = 'O.jpg'
                elif i == 3:
                    self.ids.image_3.source = 'O.jpg'
                elif i == 4:
                    self.ids.image_4.source = 'O.jpg'
                elif i == 5:
                    self.ids.image_5.source = 'O.jpg'
                elif i == 6:
                    self.ids.image_6.source = 'O.jpg'
                elif i == 7:
                    self.ids.image_7.source = 'O.jpg'
                elif i == 8:
                    self.ids.image_8.source = 'O.jpg'
                elif i == 9:
                    self.ids.image_9.source = 'O.jpg'




    def gamebutton(self,polje):
        global st_potez # spremenljivka ki steje stevilo potez
        global znak # spremenljivka ki je zadolzena za menjavo znaka x in o
        global Gameboard # slovar v katerem je zapisan gameboard
        global end_type # tip konca, sepravi da zmaga x('X'), zmaga o('O'), ali pa je neodločeno('' in poteze = 9)
        global gamemode
        valid_move=True

# COOP GAMEMODE
        if gamemode == 'coop':

            # pretvorba znaka v sliko
            if znak == 'X':
                slika = 'X.png'
            else:
                slika = 'O.jpg'

            # doda sliko v polje v aplikaciji
            if polje == 1 and Gameboard[polje] not in ['X', 'O']: # prvi pogoj je da uprasa v katero polje da sliko, drugi pa da v tem polju ze ni kateri od znakov da ga ne povozi
                self.ids.image_1.source = slika
            elif polje == 2 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_2.source = slika
            elif polje == 3 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_3.source = slika
            elif polje == 4 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_4.source = slika
            elif polje == 5 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_5.source = slika
            elif polje == 6 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_6.source = slika
            elif polje == 7 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_7.source = slika
            elif polje == 8 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_8.source = slika
            elif polje == 9 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_9.source = slika
            else:
                valid_move=False

            if valid_move:
                    # steje pravilne poteze
                st_potez += 1
                    # doda x ali o v gameboard
                Gameboard[polje] = znak

                # precekira ce je kdo zmagal
            if st_potez >= 5:
                self.check()

                #menjava znake x in o
            if valid_move:
                if znak == 'O':
                    znak = 'X'
                else:
                    znak = 'O'

# to mam samo za referenco da vidim če se isto dogaja v programu kot na zaslonu
            #print(f'{Gameboard[1]}|{Gameboard[2]}|{Gameboard[3]}\n-----\n{Gameboard[4]}|{Gameboard[5]}|{Gameboard[6]}\n-----\n{Gameboard[7]}|{Gameboard[8]}|{Gameboard[9]}')
            #print(valid_move)
            #print(st_potez)
            #print(end_type)

#BOT GAMEMODE
        elif gamemode == 'bot':
# precekira
            if st_potez >= 5:
                self.check()

# znak za cloveka spremeni v x
            znak = 'X'
            # doda sliko v polje v aplikaciji
            if polje == 1 and Gameboard[polje] not in ['X', 'O']:  # prvi pogoj je da uprasa v katero polje da sliko, drugi pa da v tem polju ze ni kateri od znakov da ga ne povozi
                self.ids.image_1.source = 'X.png'
            elif polje == 2 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_2.source = 'X.png'
            elif polje == 3 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_3.source = 'X.png'
            elif polje == 4 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_4.source = 'X.png'
            elif polje == 5 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_5.source = 'X.png'
            elif polje == 6 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_6.source = 'X.png'
            elif polje == 7 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_7.source = 'X.png'
            elif polje == 8 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_8.source = 'X.png'
            elif polje == 9 and Gameboard[polje] not in ['X', 'O']:
                self.ids.image_9.source = 'X.png'
            else:
                valid_move = False

            if valid_move:
                # steje pravilne poteze
                st_potez += 1
                # doda x ali o v gameboard
                Gameboard[polje] = znak

# precekira
            if st_potez >= 5:
                self.check()
                #time.sleep(0.1)
            #time.sleep(0.5)
# AI doda en znak
            if st_potez!=9 and end_type == '' and valid_move:
                self.iai()
                #time.sleep(0.1)

# precekira
            if st_potez >= 5:
                self.check()
                #time.sleep(0.1)

# gumb na popup-u ki zapre dialog in gre na play tab
    def ok_button(self,obj):
        global gamemode
        gamemode = ''
        self.dialog.dismiss()
        print('dialog zaprt')
        self.ids.bottom_navigation.switch_tab('play_tab')

# gumb na popup-u ki zapre dialog in ponovno zacne igro
    def playagain_button(self, obj):
        self.dialog.dismiss()
        print('dialog zaprt')
        time.thread_time_ns()
        global gamemode
        if gamemode == 'coop':
            self.start_coop()
        elif gamemode == 'bot':
            self.start_bot()
        else:
            pass



class ScreenManager1(ScreenManager):
    pass



class MDBoxLayout(MDBoxLayout):
    pass



class chessms(MDApp):

    def build(self):
        self.theme_cls.primary_palette = 'Orange'
        self.theme_cls.primary_hue = '200'
        self.screen_manager = ScreenManager1()
        self.screen_manager.add_widget(ScreenWelcome(name='welcome_screen'))
        self.screen_manager.add_widget(ScreenMain(name='main_screen'))
        self.screen_manager.add_widget(ScreenSettings(name='settings_screen'))
        return self.screen_manager


######
if __name__=='__main__':
    chessms().run()