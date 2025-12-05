### front_subjects.py ###

#Importacions
import reflex as rx
from web_2Students.pages.backend.back_stuent_coach import *
from web_2Students.styles.colors import Colors as colors
from web_2Students.db.subjects import *



def subjects_selector() -> rx.Component:
        return rx.tablet_and_desktop(
            rx.vstack(
            rx.hstack(
                rx.select.root(
                    rx.select.trigger(),
                    rx.select.content(
                        rx.select.group(
                            rx.select.label("ESO",color=colors.MIG_CLAR.value,font_weight="bold",),
                            rx.foreach(
                                subjects_ESO,
                                lambda subject: rx.select.item(subject, value=subject),
                            ),
                        ),
                        rx.select.separator(color=colors.FOSC.value),
                        rx.select.group(
                            rx.select.label("Batxillerat",color=colors.MIG_CLAR.value,font_weight="bold",),
                            rx.foreach(
                                subjects_Batxillerat,
                                lambda subject: rx.select.item(subject, value=subject),
                            ),
                        ),
                        color_scheme='purple',
                    ),
                    value=NewCoach.current_subject,
                    on_change=NewCoach.set_current_subject,
                    flex='1'
                ),
                rx.button(
                    "Afegir assignatura",
                    bg=colors.MIG_CLAR.value,
                    flex='1',
                    on_click=NewCoach.add_subject
                ),
                rx.button(
                    "Treure assignatura",
                    bg=colors.MIG_CLAR.value,
                    flex='1',
                    on_click=NewCoach.remove_subject
                ),
                width = '100%'
            ),
            rx.text(f"Assignatures seleccionades: {NewCoach.current_subject}"),
            rx.text(f"Llista: {NewCoach.subjects_list}")
        )
    )


def mobile_subjects_selector() -> rx.Component:
        return rx.mobile_only(
            rx.vstack(
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.select.group(
                        rx.select.label("ESO",color=colors.MIG_CLAR.value,font_weight="bold",),
                        rx.foreach(
                            subjects_ESO,
                            lambda subject: rx.select.item(subject, value=subject),
                        ),
                    ),
                    rx.select.separator(color=colors.FOSC.value),
                    rx.select.group(
                        rx.select.label("Batxillerat",color=colors.MIG_CLAR.value,font_weight="bold",),
                        rx.foreach(
                            subjects_Batxillerat,
                            lambda subject: rx.select.item(subject, value=subject),
                        ),
                    ),
                    color_scheme='purple',
                ),
                value=NewCoach.current_subject,
                on_change=NewCoach.set_current_subject,
                flex='1',
                width='100%'
            ),
            rx.hstack(
                rx.button(
                    "Afegir",
                    bg=colors.MIG_CLAR.value,
                    flex='1',
                    on_click=NewCoach.add_subject,
                    width='100%'
                ),
                rx.button(
                    "Treure",
                    bg=colors.MIG_CLAR.value,
                    flex='1',
                    on_click=NewCoach.remove_subject,
                    width='100%'
                ),
            ),
            rx.text(f"Assignatures seleccionades: {NewCoach.current_subject}"),
            rx.text(f"Llista: {NewCoach.subjects_list}"),
        )
    )