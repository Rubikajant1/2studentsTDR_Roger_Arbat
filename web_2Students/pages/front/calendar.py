import reflex as rx
from web_2Students.pages.backend.back_stuent_coach import NewCoach as cnd

def calendar_for_desktop() -> rx.Component:
    return rx.box(
        rx.text("Posa l'horari que et va be per donar classe", margin_bottom = "1em"),
        rx.box(
            rx.hstack(
                rx.text("Dilluns -", margin_right = '19.5px' ),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_dilluns, width = "170px"),
                rx.text("Especificacions (opcional) - "),
                rx.input(placeholder="Ex: Excepte les 17:00", width = "200px",on_change=cnd.set_especificacions_dilluns)
            ),
            rx.hstack(
                rx.text("Dimarts - ",margin_right = "15px"),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_dimarts, width = "170px"),
                rx.text("Especificacions (opcional) - "),
                rx.input(placeholder="Ex: Només presencial", width = "200px", on_change=cnd.set_especificacions_dimarts)
            ),
            rx.hstack(
                rx.text("Dimecres - ", margin_right = "5px"),
                rx.input(placeholder="Ex: 16:00 - 18:00" , on_change=cnd.set_dimecres, width = "170px"),
                rx.text("Especificacions (opcional) -", margin_right = "0.5px"),
                rx.input(placeholder="Ex: I de 8:00 a 10:00 online", width = "200px", on_change=cnd.set_especificacions_dimecres)
            ),
            rx.hstack(
                rx.text("Dijous - ",margin_right = "24px"),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_dijous, width = "169.5px"),
                rx.text("Especificacions (opcional) - ", margin_right = "1px"),
                rx.input(placeholder="Ex: No presencial", width = "200px", on_change=cnd.set_especificacions_dijous)
            ),
            rx.hstack(
                rx.text("Divendres - ", margin_right = "1px"),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_divendres, width = "169.5px"),
                rx.text("Especificacions (opcional) -", margin_right = "0.5px"),
                rx.input(placeholder="Ex: I les 20:00", width = "200px", on_change=cnd.set_especificacions_divendres)
            ),
            rx.hstack(
                rx.text("Dissabte - ", margin_right = "11.5px"),
                rx.input(placeholder="Ex: 09:00 - 13:00", on_change=cnd.set_dissabte_mati, width = "170px"),
                rx.text("Especificacions (opcional) -"),
                rx.input(placeholder="Ex: Matins nomes presencial", width = "200px", on_change=cnd.set_especificacions_dissabte_mati)
            ),
            rx.hstack(
                rx.text("Dissabte - ", margin_right = "11.5px"),
                rx.input(placeholder="Ex: 16:00 - 19:00", on_change=cnd.set_dissabte_tarda, width = "170px"),
                rx.text("Especificacions (opcional) -"),
                rx.input(placeholder="Ex: Tardes presencial i online", width = "200px", on_change=cnd.set_especificacions_dissabte_tarda)
            ),
            rx.hstack(
                rx.text("Diumenge - "),
                rx.input(placeholder="Ex: 09:00 - 13:00", on_change=cnd.set_diumenge_mati, width = "170px"),
                rx.text("Especificacions (opcional) -"),
                rx.input(placeholder="Ex: Matins nomes online", width = "200px", on_change=cnd.set_especificacions_diumenge_mati)
            ),
            rx.hstack(
                rx.text("Diumenge - "),
                rx.input(placeholder="Ex: 16:00 - 19:00", on_change=cnd.set_diumenge_tarda, width = "170px"),
                rx.text("Especificacions (opcional) -"),
                rx.input(placeholder="Ex: Tardes presencial", width = "200px", on_change=cnd.set_especificacions_diumenge_tarda)
            ),
        )
    )
    


def calendar_for_mobile() -> rx.Component:
    day_container_style = dict(
        width="100%",
        spacing="2",
        align_items="start",
        padding_bottom="1.5em",
        border_bottom="1px solid #f0f0f0",
        margin_bottom="1em"
    )

    return rx.box(
        rx.text("Posa l'horari que et va be per donar classe", 
                margin_bottom="1.5em", 
                font_weight="bold",
                text_align="center"),
        
        rx.vstack(
            # Dilluns
            rx.vstack(
                rx.text("Dilluns", font_weight="semibold"),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_dilluns, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: Excepte les 17:00", on_change=cnd.set_especificacions_dilluns, width="100%"),
                style=day_container_style
            ),

            # Dimarts
            rx.vstack(
                rx.text("Dimarts", font_weight="semibold"),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_dimarts, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: Només presencial", on_change=cnd.set_especificacions_dimarts, width="100%"),
                style=day_container_style
            ),

            # Dimecres
            rx.vstack(
                rx.text("Dimecres", font_weight="semibold"),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_dimecres, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: I de 8:00 a 10:00 online", on_change=cnd.set_especificacions_dimecres, width="100%"),
                style=day_container_style
            ),

            # Dijous
            rx.vstack(
                rx.text("Dijous", font_weight="semibold"),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_dijous, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: No presencial", on_change=cnd.set_especificacions_dijous, width="100%"),
                style=day_container_style
            ),

            # Divendres
            rx.vstack(
                rx.text("Divendres", font_weight="semibold"),
                rx.input(placeholder="Ex: 16:00 - 18:00", on_change=cnd.set_divendres, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: I les 20:00", on_change=cnd.set_especificacions_divendres, width="100%"),
                style=day_container_style
            ),

            # Dissabte Matí
            rx.vstack(
                rx.text("Dissabte (Matí)", font_weight="semibold"),
                rx.input(placeholder="Ex: 09:00 - 13:00", on_change=cnd.set_dissabte_mati, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: Matins nomes presencial", on_change=cnd.set_especificacions_dissabte_mati, width="100%"),
                style=day_container_style
            ),

            # Dissabte Tarda
            rx.vstack(
                rx.text("Dissabte (Tarda)", font_weight="semibold"),
                rx.input(placeholder="Ex: 16:00 - 19:00", on_change=cnd.set_dissabte_tarda, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: Tardes presencial i online", on_change=cnd.set_especificacions_dissabte_tarda, width="100%"),
                style=day_container_style
            ),

            # Diumenge Matí
            rx.vstack(
                rx.text("Diumenge (Matí)", font_weight="semibold"),
                rx.input(placeholder="Ex: 09:00 - 13:00", on_change=cnd.set_diumenge_mati, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: Matins nomes online", on_change=cnd.set_especificacions_diumenge_mati, width="100%"),
                style=day_container_style
            ),

            # Diumenge Tarda
            rx.vstack(
                rx.text("Diumenge (Tarda)", font_weight="semibold"),
                rx.input(placeholder="Ex: 16:00 - 19:00", on_change=cnd.set_diumenge_tarda, width="100%"),
                rx.text("Especificacions (opcional)", font_size="0.8em", color="gray"),
                rx.input(placeholder="Ex: Tardes presencial", on_change=cnd.set_especificacions_diumenge_tarda, width="100%"),
                style=day_container_style
            ),
            width="100%",
            padding_x="1em"
        ),
        width="100%"
    )