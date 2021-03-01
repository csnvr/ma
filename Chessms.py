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
            valid=False #TODO pazi da das to nazaj na false da bo preverjal telefonsko stevilko
        if valid:
            MDApp.get_running_app().screen_manager.transition.direction = 'left'
            MDApp.get_running_app().screen_manager.current = 'main_screen'
        else:
            self.ids.info_text.text = f'{self.ids.info_text.text}\nPlease insert valid phone number'

        #predvajanje zvoka
        '''
        sound = SoundLoader.load('B1TB01 - Sunrise.mp3')
        if sound:
            print('Now playing: B1TB01 - Sunrise')
        #sound.play()
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