### navbar.py ###

#Importacions
import reflex as rx
from web_2Students.styles.colors import Colors as colors


def navbar() -> rx.Component:
    return rx.box(
        rx.link(
            "2Students",
            href='/',
            color = colors.FOSC.value,
            _hover = {},
            weight='bold'
        ),
        position = 'fixed',
        bg = colors.CLAR.value,
        width ='100%',
        padding_x ='1%',
        padding_y = '0.4%',
        z_index = '999',
        spacing = '9',
        justify = 'between'
    )