import reflex as rx
from bson import ObjectId
from web_2Students.styles.colors import Colors as colors
from web_2Students.components.navbar import navbar
from web_2Students.pages.backend.back_stuent_coach import AuthState, user_coach
from typing import Dict, List, Any



class ProfileState(rx.State):
    coach_data: Dict[str, Any] = {}

    @rx.var
    def coach_subjects_all(self) -> List[str]:
        # 1. Obtenemos la lista principal del DICCIONARIO coach_data
        # Usamos .get() porque coach_data es un dict en ProfileState
        lista_principal = self.coach_data.get("subjects_list", [])
        
        # 2. Obtenemos el subject extra
        extra = self.coach_data.get("extra_subject", "").strip()
        
        # 3. Combinamos
        totes = list(lista_principal)
        if extra:
            totes.append(extra)
            
        return totes
    
    
    @rx.var
    def coach_image_url(self) -> str:
        # Obtenemos el campo "image" del diccionario de datos del coach
        img = self.coach_data.get("image", "").strip()
        
        # 1. Si no hay imagen, ponemos el logo por defecto
        if not img:
            return "/Logo_2Students.jpeg"
        
        # 2. Si es una URL externa (http), la devolvemos tal cual
        if img.startswith(("http://", "https://")):
            return img
        
        # 3. SI LA RUTA ES LOCAL (Subida por el usuario):
        # Si la base de datos devuelve solo "Professor.jpg", 
        # debemos transformarlo en "/uploaded_files/Professor.jpg"
        
        # Primero limpiamos posibles barras iniciales para no duplicarlas
        clean_img = img.lstrip("/")
        
        # Si el nombre del archivo ya contiene 'uploaded_files', solo aseguramos la barra inicial
        if "uploaded_files" in clean_img:
            return f"/{clean_img}"
        
        # Si es solo el nombre del archivo, le ponemos la ruta completa
        return f"/uploaded_files/{clean_img}"
    
    
    
    @rx.event
    def get_coach_info(self):
        """Busca los datos del coach usando el ID de la URL"""
        c_id = self.router.page.params.get("coach_id")
        
        try:
            if c_id:
                user = user_coach.find_one({"_id": ObjectId(c_id)})
                if user:
                    user["_id"] = str(user["_id"])
                    if "password" in user: 
                        del user["password"]
                    # Aseguramos que subjects exista para evitar errores en el frontend
                    if "subjects" not in user:
                        user["subjects"] = []
                    
                    self.coach_data = user
                else:
                    self.coach_data = {}
        except Exception as e:
            print(f"Error en get_coach_info: {e}")
            self.coach_data = {}

    @rx.event
    async def init_profile_page(self):
        auth_state = await self.get_state(AuthState)
        result = auth_state.check_login()
        
        if result is not None:
            return result

        return self.get_coach_info()




### Funció personalitzada per cada coach on es pot veure les seves característiques i editar el seu perfil (aquesta funció es pot reutilitzar per altres pàgines de perfil) ###
### Perfil del coach (página protegida, només pel coach loguejat) ###
def profile_page_coach() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(
            ProfileState.coach_data,
            rx.container(
                rx.vstack(
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
                    # Sección de perfil principal
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
                            rx.heading(ProfileState.coach_data['name'], size="9", color=colors.MIG_FOSC.value),
                            rx.hstack(
                                rx.badge(f"📍 {ProfileState.coach_data['comarca']}", size="3", color_scheme="blue"),
                                rx.badge(f"{ProfileState.coach_data['price']}€/hora", size="3", color=colors.MIG.value),
                            ),
                            rx.separator(width="100%"),
                            rx.text("Especialitats", weight="bold", size="5", padding_top="2"),
                            
                            # Uso de la Var computada para evitar el ForeachVarError
                            rx.flex(
                                rx.foreach(
                                    ProfileState.coach_subjects_all, # <--- IMPORTANTE: Usar la nueva Var
                                    lambda s: rx.badge(s, variant="surface", size="3", color=colors.MIG.value)
                                ),
                                wrap="wrap", 
                                spacing="2"
                            ),
                            
                            rx.spacer(),
                            
                            # Botón de contacto
                            
                            
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
                    rx.text("Sobre mi", weight="bold", size="5"),
                    rx.text(ProfileState.coach_data['description'], size="4", line_height="1.6"),
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
                    padding_bottom="4em"
                )
            ),
            # Mientras carga o si no hay datos
            rx.center(rx.spinner(), height="80vh")
        ),
        bg="#FBFBFE", 
        min_height="100vh",
        # CORRECCIÓN: on_mount debe llamar a un EVENTO (función), no a un texto
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
