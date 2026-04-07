import reflex as rx
from web_2Students.styles.colors import Colors as colors
from web_2Students.components.navbar import navbar
from web_2Students.pages.backend.back_stuent_coach import AuthState
from web_2Students.pages.backend.back_profile import CoachState, ProfileState




### Funció personalitzada per cada coach on es pot veure les seves característiques i editar el seu perfil (aquesta funció es pot reutilitzar per altres pàgines de perfil) ###
### Perfil del coach (página protegida, només pel coach loguejat) ###
def profile_page_coach() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(
            ProfileState.coach_data,
            rx.container(
                rx.vstack(
                    # --- SALUDO ---
                    rx.heading(f"Hola, {ProfileState.coach_data['name']}", margin_top='2em'),
                    
                    rx.button(
                        "Tancar Sessió",
                        on_click=AuthState.logout,
                        bg=colors.MIG_FOSC.value,
                        color='white',
                        variant="soft",
                        cursor="pointer",
                        margin_top="1.5em",
                        margin_bottom="3em"
                    ),

                    # --- SECCIÓN DE PERFIL PRINCIPAL ---
                    rx.flex(
                        rx.image(
                            src=ProfileState.coach_image_url, 
                            width={"initial": "100%", "md": "150px"}, 
                            height="220px", 
                            object_fit="cover", 
                            border_radius="xl", 
                            shadow="lg"
                        ),
                        rx.vstack(
                            # NOMBRE: Click para editar
                            rx.cond(
                                CoachState.editing_field == "name",
                                rx.input(
                                    value=ProfileState.coach_data['name'],
                                    on_change=CoachState.set_nombre,
                                    on_blur=CoachState.stop_editing, # Solo limpia el estado
                                    auto_focus=True,
                                ),
                                rx.heading(
                                    ProfileState.coach_data['name'], 
                                    on_click=lambda: CoachState.set_editing("name"), # Especificamos qué abrimos
                                    cursor="pointer",
                                    size="9"
                                ),
                            ),
                            
                            rx.hstack(
                                # COMARCA: Click para editar
                                rx.cond(
                                    CoachState.editing_field == "comarca",
                                    rx.input(
                                        value=ProfileState.coach_data['comarca'],
                                        on_change=CoachState.set_comarca,
                                        on_blur=CoachState.stop_editing,
                                        auto_focus=True,
                                    ),
                                    rx.badge(
                                        f"📍 {ProfileState.coach_data['comarca']}",
                                        on_click=lambda: CoachState.set_editing("comarca"),
                                        cursor="pointer",
                                        size="3"
                                    ),
                                ),
                                # PRECIO: Click para editar
                                rx.cond(
                                    CoachState.editing_field == "price",
                                    rx.input(
                                        value=ProfileState.coach_data['price'],
                                        on_change=CoachState.set_precio,
                                        on_blur=CoachState.stop_editing,
                                        auto_focus=True,
                                    ),
                                    rx.badge(
                                        f"€ {ProfileState.coach_data['price']}€/hora",
                                        color=colors.MIG.value,
                                        on_click=lambda: CoachState.set_editing("price"),
                                        cursor="pointer",
                                        size="3"
                                    ),
                                )
                            ),
                            
                            rx.separator(width="100%"),
                            rx.text("Especialitats", weight="bold", size="5", padding_top="2"),
                            
                            rx.flex(
                                rx.foreach(
                                    ProfileState.coach_subjects_all,
                                    lambda s: rx.badge(s, variant="surface", size="3", color=colors.MIG.value)
                                ),
                                wrap="wrap", 
                                spacing="2"
                            ),
                            
                            align_items="start", 
                            spacing="4", 
                            flex="1"
                        ),
                        spacing="8", 
                        direction={"initial": "column", "md": "row"}, 
                        width="100%", 
                        background="white", 
                        padding="6", 
                        border_radius="2xl", 
                        shadow="sm"
                    ),

                    # --- SOBRE MI (DESCRIPCIÓN) ---
                    # --- SOBRE MI (DESCRIPCIÓN) ---
                    rx.text("Sobre mi", weight="bold", size="5", margin_top="1em"),
                    rx.cond(
                        CoachState.editing_field == "description",
                        rx.text_area(
                            value=ProfileState.coach_data['description'],
                            on_change=CoachState.set_descripcion, # Llama a la función que actualiza DB
                            on_blur=CoachState.stop_editing,      # Cierra el modo edición al salir
                            auto_focus=True,
                            width="100%",
                            height="200px", # Altura fija para que sea cómodo escribir
                            size="3",
                        ),
                        rx.text(
                            ProfileState.coach_data['description'], 
                            on_click=lambda: CoachState.set_editing("description"),
                            size="4", 
                            line_height="1.6",
                            cursor="pointer",
                            padding="10px",
                            border="1px solid transparent",
                            _hover={"border": "1px dashed #ccc", "border_radius": "md"} # Efecto visual al pasar el ratón
                        ),
                    ),
                    # --- BOTÓN DE CONTACTO (POPOVER) ---
                    rx.popover.root(
                        rx.popover.trigger(
                            rx.button(
                                rx.hstack(
                                    rx.icon(tag="mail"),
                                    rx.text(f"Contactar amb {ProfileState.coach_data['name']}", color="white", size="4"),
                                ),
                                bg=colors.MIG.value,
                                size="4",
                                height="50px",
                                width="100%",
                                margin_top="2em",
                            ),
                        ),
                        rx.popover.content(
                            rx.text(f"Escriu a: {ProfileState.coach_data['mail']}", color=colors.FOSC.value),
                        ),
                    ),
                    padding_top="2em", 
                    padding_bottom="4em",
                    align_items="start",
                    width="100%"
                )
            ),
            # Mientras carga
            rx.center(rx.spinner(), height="80vh")
        ),
        bg="#FBFBFE", 
        min_height="100vh",
        on_mount=ProfileState.init_profile_page 
    )




### Página de login del coach (página pública) ###
def oauth_coach_page():
    return rx.box(
        navbar(),
        rx.tablet_and_desktop(
            rx.center(
                rx.hstack(    
                    rx.image(src="/Short_logo.jpeg", width="100%", height="102px"),
                    rx.vstack(
                        rx.heading("2Students", size='9'),
                        rx.text(
                            "D'estudiants per a estudiants",
                            size='5',
                        ),
                        align='center'
                    ),
                ),
                padding_top='6em',
                padding_bottom='1em'
            ),
            rx.box(
                rx.card(
                    rx.vstack(  
                        rx.heading(
                            "Inicia la sessió al teu perfil de coach",
                            margin_bottom='0.7em',
                            size='5',
                        ),
                        rx.text("Correu electrònic"),
                        # CONECTADO AL ESTADO
                        rx.input(
                            type="email", 
                            placeholder="Correu electrònic", 
                            width="300px",
                            text_align="center",
                            on_change=AuthState.set_email 
                        ),
                        rx.text("Contrasenya"),
                        # CONECTADO AL ESTADO
                        rx.input(
                            type="password", 
                            placeholder="Contrasenya", 
                            on_change=AuthState.set_password, # Captura el text
                            width="300px",
                            text_align="center"
                        ),
                        rx.button(
                            "Iniciar sessió", 
                            on_click=AuthState.login_coach, # Executa la validació encriptada
                            bg=colors.MIG_FOSC.value, 
                            width="300px",
                            margin_top="1em"
                        ),
                        align="center",
                        spacing="3",
                        width="100%",
                    ),
                    margin_x='34em',
                    padding_y='2em',
                    margin_top='3em',
                    margin_bottom='4em',
                    bg=colors.CLAR.value,
                )
            )
        ),
        rx.mobile_only(
            rx.center(
                rx.hstack(    
                    rx.image(src="/Short_logo.jpeg", width="150px", height="102px"),
                    rx.vstack(
                        rx.heading("2Students", size='8'),
                        rx.text(
                            "D'estudiants per a estudiants",
                            size='5',
                        ),
                    ),
    
                ),
                margin_left='2em',
                padding_top='7em',
                padding_bottom='1em'
            ),
            rx.box(
                rx.card(
                    rx.vstack(  
                        rx.heading(
                            "Inicia la sessió al teu perfil de coach",
                            margin_bottom='0.7em',
                            size='5',
                        ),
                        rx.text("Correu electrònic"),
                        # CONECTADO AL ESTADO
                        rx.input(
                            type="email", 
                            placeholder="Correu electrònic", 
                            width="300px",
                            text_align="center",
                            on_change=AuthState.set_email 
                        ),
                        rx.text("Contrasenya"),
                        # CONECTADO AL ESTADO
                        rx.input(
                            type="password", 
                            placeholder="Contrasenya", 
                            on_change=AuthState.set_password, # Captura el text
                            width="300px",
                            text_align="center"
                        ),
                        rx.button(
                            "Iniciar sessió", 
                            on_click=AuthState.login_coach, # Executa la validació encriptada
                            bg=colors.MIG_FOSC.value, 
                            width="300px",
                            margin_top="1em"
                        ),
                        align="center",
                        spacing="3",
                        width="100%",
                    ),
                    margin_x='1em',
                    padding_y='2em',
                    margin_top='1em',
                    margin_bottom='4em',
                    bg=colors.CLAR.value,
                )
            )
        )
    )
