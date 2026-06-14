import reflex as rx
from datetime import datetime
import calendar
from web_2Students.db.db_client import db # Importamos MongoDB
from web_2Students.styles.colors import Colors as colors
from web_2Students.components.navbar import navbar
from web_2Students.pages.backend.back_stuent_coach import AuthState
from web_2Students.pages.backend.back_profile import CoachState, ProfileState

# --- LÓGICA DEL CALENDARIO (MODO ADMIN-DB) ---
BLOQUES_HORARIOS = [
    "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 13:00",
    "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
]



class ProfileCalendarState(rx.State):
    current_year: int = datetime.now().year
    current_month: int = datetime.now().month
    # 🟢 NUEVO: Guardamos el día actual
    today_str: str = datetime.now().strftime("%Y-%m-%d")
    
    dias_disponibles_bd: list[str] = []
    dias_reservados_bd: list[str] = []
    
    show_modal: bool = False
    dia_seleccionado: str = ""
    horas_disponibles_dia: list[str] = []
    horas_reservadas_dia: list[str] = []

    async def get_coach_id(self) -> str:
        p_state = await self.get_state(ProfileState)
        return str(p_state.coach_data.get("_id", "")) if p_state.coach_data else ""

    async def cargar_datos_mes(self):
        coach_id = await self.get_coach_id()
        if not coach_id: return
        
        prefix = f"^{self.current_year}-{self.current_month:02d}-"
        try:
            resultados = db["calendario"].find({"coach_id": coach_id, "fecha_str": {"$regex": prefix}})
            disponibles, reservados = [], []
            for doc in resultados:
                if doc.get("horas_reservadas"): reservados.append(doc["fecha_str"])
                if doc.get("horas_disponibles"): disponibles.append(doc["fecha_str"])
            self.dias_disponibles_bd = disponibles
            self.dias_reservados_bd = reservados
        except Exception as e:
            print(f"Error MongoDB (Profile): {e}")

    @rx.var
    def month_name(self) -> str:
        meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        return f"{meses[self.current_month]} {self.current_year}"

    @rx.var
    def calendar_days(self) -> list[dict]:
        cal = calendar.Calendar(firstweekday=0)
        days_list = []
        for week in cal.monthdayscalendar(self.current_year, self.current_month):
            for day in week:
                if day == 0: 
                    days_list.append({"day": "", "date_str": "", "is_current": False})
                else: 
                    date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    # 🟢 NUEVO: Añadimos is_past e is_today
                    days_list.append({
                        "day": str(day), 
                        "date_str": date_str, 
                        "is_current": True,
                        "is_past": date_str < self.today_str,
                        "is_today": date_str == self.today_str
                    })
        return days_list

    async def next_month(self):
        if self.current_month == 12: self.current_month = 1; self.current_year += 1
        else: self.current_month += 1
        await self.cargar_datos_mes()

    async def prev_month(self):
        if self.current_month == 1: self.current_month = 12; self.current_year -= 1
        else: self.current_month -= 1
        await self.cargar_datos_mes()

    async def abrir_dia(self, date_str: str):
        if not date_str: return
        coach_id = await self.get_coach_id()
        self.dia_seleccionado = date_str
        self.show_modal = True
        
        dia = db["calendario"].find_one({"coach_id": coach_id, "fecha_str": date_str})
        if dia:
            self.horas_disponibles_dia = dia.get("horas_disponibles", [])
            self.horas_reservadas_dia = dia.get("horas_reservadas", [])
        else:
            self.horas_disponibles_dia = []
            self.horas_reservadas_dia = []

    async def cerrar_modal(self):
        self.show_modal = False
        self.dia_seleccionado = ""

    async def toggle_hora_disponibilidad(self, hora: str):
        coach_id = await self.get_coach_id()
        if not coach_id: return rx.window_alert("Error de autenticación.")
        
        if hora in self.horas_reservadas_dia:
            return rx.window_alert("Esta hora ya está reservada por un estudiante.")
            
        horas_disp_puras = list(self.horas_disponibles_dia)
        horas_res_puras = list(self.horas_reservadas_dia)
        
        if hora in horas_disp_puras:
            horas_disp_puras.remove(hora)
        else:
            horas_disp_puras.append(hora)
            
        db["calendario"].update_one(
            {"coach_id": coach_id, "fecha_str": self.dia_seleccionado},
            {"$set": {"horas_disponibles": horas_disp_puras, "horas_reservadas": horas_res_puras}},
            upsert=True
        )
        self.horas_disponibles_dia = horas_disp_puras
        await self.cargar_datos_mes()

def celda_admin_prof(day_data: dict) -> rx.Component:
    is_disponible = ProfileCalendarState.dias_disponibles_bd.contains(day_data["date_str"])
    is_reservado = ProfileCalendarState.dias_reservados_bd.contains(day_data["date_str"])
    
    # 🟢 NUEVO: Lógica de colores y estados de la celda
    color_scheme = rx.cond(
        day_data["is_past"], "gray", 
        rx.cond(is_reservado, "crimson", rx.cond(is_disponible, "indigo", "gray"))
    )
    variant = rx.cond(
        day_data["is_past"], "ghost", 
        rx.cond(is_reservado, "solid", rx.cond(is_disponible, "solid", "ghost"))
    )
    borde = rx.cond(day_data["is_today"], "2px solid var(--accent-9)", "none")
    
    return rx.cond(
        day_data["is_current"],
        rx.button(
            day_data["day"],
            on_click=lambda: ProfileCalendarState.abrir_dia(day_data["date_str"]),
            disabled=day_data["is_past"], # Bloquea días pasados
            variant=variant, color_scheme=color_scheme, size="3", width="100%", height="45px", cursor="pointer", border=borde
        ),
        rx.box(width="100%", height="45px")
    )

def fila_hora_admin_prof(hora: str) -> rx.Component:
    activa = ProfileCalendarState.horas_disponibles_dia.contains(hora)
    reservada = ProfileCalendarState.horas_reservadas_dia.contains(hora)
    return rx.button(
        hora,
        on_click=lambda: ProfileCalendarState.toggle_hora_disponibilidad(hora),
        width="100%", color_scheme=rx.cond(reservada, "crimson", rx.cond(activa, "indigo", "gray")),
        variant=rx.cond(reservada, "solid", rx.cond(activa, "solid", "outline")), cursor="pointer"
    )

def admin_calendar_profile() -> rx.Component:
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    return rx.vstack(
        rx.text("Gestiona tu Disponibilidad", weight="bold", size="5", margin_top="1.5em"),
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon_button("chevron-left", on_click=ProfileCalendarState.prev_month, variant="soft", color_scheme="indigo"),
                    rx.text(ProfileCalendarState.month_name, size="4", weight="bold", width="150px", align="center"),
                    rx.icon_button("chevron-right", on_click=ProfileCalendarState.next_month, variant="soft", color_scheme="indigo"),
                    width="100%", justify="between", align="center", padding_bottom="15px", border_bottom="1px solid var(--gray-4)"
                ),
                rx.grid(*[rx.text(d, size="2", weight="bold", align="center", color_scheme="gray") for d in dias], columns="7", width="100%", padding_y="10px"),
                rx.grid(rx.foreach(ProfileCalendarState.calendar_days, celda_admin_prof), columns="7", gap="2", width="100%"),
                width="100%"
            ),
            rx.dialog.root(
                rx.dialog.content(
                    rx.dialog.title(f"Horarios para el {ProfileCalendarState.dia_seleccionado}"),
                    rx.dialog.description("Selecciona las horas que tienes disponibles:"),
                    rx.vstack(rx.foreach(BLOQUES_HORARIOS, fila_hora_admin_prof), spacing="2", padding_y="15px", width="100%"),
                    rx.hstack(rx.dialog.close(rx.button("Listo", on_click=ProfileCalendarState.cerrar_modal, color_scheme="indigo", cursor="pointer")), justify="end")
                ),
                open=ProfileCalendarState.show_modal,
            ),
            width="100%", padding="20px", box_shadow="sm", border_radius="lg"
        ),
        width="100%"
    )
# --- FIN LÓGICA DEL CALENDARIO ---

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
                                    
                                    # Remove input-like appearance
                                    border="none",
                                    background="transparent",
                                    outline="none",
                                    _focus={"box_shadow": "none", "border": "none"},
                                    # Add header-like typography
                                    font_size="3rem",
                                    font_weight="bold",
                                    width="100%",
                                    text_align="left",
                                    height="auto",
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
                                rx.cond(
                                    CoachState.editing_field == "localitzacio",
                                    rx.input(
                                        value=ProfileState.coach_data['localitzacio'],
                                        on_change=CoachState.set_localitzacio,
                                        on_blur=CoachState.stop_editing,
                                        auto_focus=True,
                                    ),
                                    rx.badge(
                                        f"🏡 {ProfileState.coach_data['localitzacio']}",
                                        on_click=lambda: CoachState.set_editing("localitzacio"),
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
                                        f"💵 {ProfileState.coach_data['price']}€/hora",
                                        #color=colors.MIG.value,
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
                    admin_calendar_profile(),
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
                                margin_top="0.5em",
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
