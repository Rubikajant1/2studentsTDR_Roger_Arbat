### styles.py ###

#Importacions
import reflex as rx
from web_2Students.styles.colors import Colors as colors

BASE_STYLE = {
    "background_color":"white",
    "font_family":"",
    rx.button:{
        'backgroud_color': colors.CLAR.value,
        'width':'100%',
        'height':'100%',
        'display':'block',
        'padding':'0.5em',
        'FOSC_color':colors.FOSC.value,
        '_hover':{
            
        }
    },
    rx.link:{
        'text_decoration':'none',
        '_hover':{}
    },
    rx.text:{
        'color': colors.FOSC.value,
        'font_family': 'Geist',
    },
    rx.heading:{
        'color': colors.MIG_FOSC.value,
        'font_familly': 'Geist'
    },
}