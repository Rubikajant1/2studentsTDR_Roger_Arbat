### navbar.py ###

#Importacions
import reflex as rx
from web_2Students.styles.colors import Colors as colors


def navbar() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.hstack(    
                #Link que et porta a la pàgina principal
                rx.link(
                    "2Students",
                    href='/',
                    color = colors.FOSC.value,
                    _hover = {},
                    weight='bold',
                    align='center',
                    margin_top='0.4em',
                ),
            ),
            #Si està autoritzat mostrar els botons
            rx.hstack(
                #Botons
                rx.link(
                rx.button(
                    'Inicia sessió com a coach',
                    size='2',
                    color=colors.FOSC.value,
                    background_color = 'white',
                    border_radius = 'full',
                    border = f'2px solid {colors.MIG_FOSC.value}',
                ),
                href='/login_coach'
                ),
            ),
            #Parametres estetics
            position = 'fixed',
            bg = colors.CLAR.value,
            width = '100%',
            padding_x = '16px',
            padding_y = '8px',
            z_index = '999',
            spacing='9',
            justify='between'
        )
        
    )