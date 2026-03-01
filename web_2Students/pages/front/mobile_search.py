   
    
import reflex as rx
from typing import List
from web_2Students.styles.colors import Colors as colors

# 1. IMPORTA L'ESTAT (Ajusta la ruta segons on tinguis el SearchState principal)
# Si el SearchState està al fitxer d'ordinador (ex: search.py), importa'l així:
# from web_2Students.pages.front.search import SearchState, Coach 
# (Si prefereixes tenir-lo aquí, t'he deixat el model Coach a sota)

class Coach(rx.Base):
    name: str
    mail: str
    comarca: str
    subjects_list: List[str]
    price: int
    image: str
    description: str

# 2. COMPONENT CARD PER A MÒBIL
def mobile_coach_card(coach: Coach):
    """Renderitza una card optimitzada per a l'amplada del mòbil."""
    return rx.card(
        rx.vstack(
            rx.image(
                src=coach.image, 
                width="100%", 
                height="180px", 
                object_fit="cover", 
                border_radius="8px"
            ),
            rx.vstack(
                rx.hstack(
                    rx.heading(coach.name, size="3", weight="bold"),
                    rx.spacer(),
                    rx.badge(f"{coach.price}€/h", color = colors.MIG.value, variant="surface", size="2"),
                    width="100%",
                    align_items="center",
                ),
                rx.badge(
                    f"📍 {coach.comarca}",
                    color_scheme="blue",
                    variant="soft"
                ),
                rx.flex(
                    rx.foreach(coach.subjects_list, lambda s: rx.badge(s, variant="outline", color_scheme="indigo")),
                    wrap="wrap", 
                    spacing="1",
                ),
                align_items="start", 
                width="100%", 
                padding_top="2",
            ),
            width="100%",
        ),
        width="100%",
    )

# 3. PÀGINA DE CERCA MÒBIL
def front_search_page() -> rx.Component:
    from .search import SearchState # Import local per evitar importacions circulars
    
    return rx.container(
        rx.vstack(
            rx.heading(
                "Explora els nostres Coaches",
                size="6", margin_y="4", 
                color=colors.MIG_FOSC.value, 
                padding_top="2em",
                padding_bottom="0.5em"
            ),
            rx.box(
                rx.hstack(
                    rx.icon(tag="search", size=25, padding_left="0.4em",color=colors.MIG_FOSC.value),
                        rx.hstack(
                            rx.input(
                                placeholder="Assignatura",
                                on_change=SearchState.set_filter_subject,
                                width="100%",
                                color=colors.MIG_FOSC.value,
                                bg=colors.CLAR.value,
                                placeholder_color=colors.MIG_FOSC.value,
                            ),
                            bg="white",
                            border="1px solid #E2E8F0",
                            padding_x="3",
                            border_radius="lg",
                            flex="2",
                            align_items="center",
                        ),
                        rx.icon(
                            tag="map_pin",
                            size=18, 
                            color=colors.MIG_FOSC.value
                        ),
                        rx.hstack(
                            rx.input(
                                placeholder="Comarca",
                                on_change=SearchState.set_filter_comarca,
                                width="100%",
                                color=colors.MIG_FOSC.value,
                                bg=colors.CLAR.value,
                                placeholder_color=colors.MIG_FOSC.value,
                            ),
                            bg="white",
                            border="1px solid #E2E8F0",
                            padding_x="3",
                            border_radius="lg",
                            flex="1.5", 
                            align_items="center",
                        ),
                        rx.button(
                            "Buscar",
                            on_click=SearchState.get_coaches,
                            bg=colors.MIG.value, 
                            color="white", 
                            flex="1"
                        ),
                        width="100%", spacing="3", align_items="center",
                    ),
                    padding="4",
                    bg="#F8FAFC",
                    border_radius="xl", 
                    width="100%",
                    margin_bottom="6",
                ),

            # RESULTATS
            rx.cond(
                SearchState.results, # Comprova si hi ha dades
                rx.vstack(
                    rx.foreach(
                        SearchState.results, 
                        mobile_coach_card
                    ),
                    width="100%",
                    spacing="4",
                    padding_bottom="4em"
                ),
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3"),
                        rx.text("Carregant o sense resultats...", color="gray", size="2"),
                        align_items="center",
                        padding_top="10"
                    ),
                    width="100%"
                )
            ),
            width="100%",
        ),
        size="1", # Mida estreta per a mòbils
    )