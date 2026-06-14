import reflex as rx
from datetime import datetime
import calendar
from web_2Students.db.db_client import db

BLOQUES_HORARIOS = [
    "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", "12:00 - 13:00",
    "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00"
]

class ClienteCalendarState(rx.State):
    current_year: int = datetime.now().year
    current_month: int = datetime.now().month
    today_str: str = datetime.now().strftime("%Y-%m-%d")
    
    dias_disponibles_bd: list[str] = []
    dias_reservados_bd: list[str] = []
    
    show_modal: bool = False
    dia_seleccionado: str = ""
    horas_disponibles_dia: list[str] = []
    horas_reservadas_dia: list[str] = []

    # 🟢 IMPORTANTE: Si un estudiante reserva con un coach en concreto, 
    # la búsqueda a la base de datos debe filtrar por ese "coach_id", 
    # tal y como hace tu código de admin. 
    coach_id_actual: str = "" 

    async def cargar_datos_mes(self):
        prefix = f"^{self.current_year}-{self.current_month:02d}-"
        try:
            # Creamos la misma query que usa tu admin. 
            # (Si integras el ID del coach, descomenta la segunda línea)
            query = {"fecha_str": {"$regex": prefix}}
            # if self.coach_id_actual: query["coach_id"] = self.coach_id_actual
            
            resultados = db["calendario"].find(query)
            disponibles, reservados = [], []
            
            for doc in resultados:
                if doc.get("horas_reservadas"): reservados.append(doc["fecha_str"])
                if doc.get("horas_disponibles"): disponibles.append(doc["fecha_str"])
                
            self.dias_disponibles_bd = disponibles
            self.dias_reservados_bd = reservados
        except Exception as e:
            print(f"Error MongoDB (Cliente): {e}")

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
                    # 🟢 Añadimos todas las claves para evitar errores en la vista
                    days_list.append({"day": "", "date_str": "", "is_current": False, "is_past": False, "is_today": False})
                else: 
                    date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
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
        self.dia_seleccionado = date_str
        self.show_modal = True
        
        query = {"fecha_str": date_str}
        # if self.coach_id_actual: query["coach_id"] = self.coach_id_actual
        
        dia = db["calendario"].find_one(query)
        if dia:
            self.horas_disponibles_dia = dia.get("horas_disponibles", [])
            self.horas_reservadas_dia = dia.get("horas_reservadas", [])
        else:
            self.horas_disponibles_dia = []
            self.horas_reservadas_dia = []

    async def cerrar_modal(self):
        self.show_modal = False
        self.dia_seleccionado = ""

    async def reservar_hora(self, hora: str):
        if hora in self.horas_disponibles_dia:
            horas_disp_puras = list(self.horas_disponibles_dia)
            horas_res_puras = list(self.horas_reservadas_dia)
            
            horas_disp_puras.remove(hora)
            horas_res_puras.append(hora)
            
            query = {"fecha_str": self.dia_seleccionado}
            # if self.coach_id_actual: query["coach_id"] = self.coach_id_actual
            
            db["calendario"].update_one(
                query,
                {"$set": {"horas_disponibles": horas_disp_puras, "horas_reservadas": horas_res_puras}}
            )
            self.horas_disponibles_dia = horas_disp_puras
            self.horas_reservadas_dia = horas_res_puras
            await self.cargar_datos_mes()
            return rx.window_alert(f"Cita confirmada per a les {hora}.")
        else:
            return rx.window_alert("Ho sentim, aquesta hora ja no està disponible.")


# --- COMPONENTES VISUALES ---

def celda_cliente(day_data: dict) -> rx.Component:
    # Exactamente la misma lógica del admin
    is_disponible = ClienteCalendarState.dias_disponibles_bd.contains(day_data["date_str"])
    
    color_scheme = rx.cond(
        day_data["is_past"], "gray", 
        rx.cond(is_disponible, "green", "gray")
    )
    variant = rx.cond(
        day_data["is_past"], "ghost", 
        rx.cond(is_disponible, "solid", "ghost")
    )
    borde = rx.cond(day_data["is_today"], "2px solid var(--accent-9)", "none")
    
    return rx.cond(
        day_data["is_current"],
        rx.button(
            day_data["day"],
            on_click=lambda: ClienteCalendarState.abrir_dia(day_data["date_str"]),
            disabled=day_data["is_past"], 
            variant=variant, color_scheme=color_scheme, size="3", width="100%", height="45px", cursor="pointer", border=borde
        ),
        rx.box(width="100%", height="45px")
    )

def fila_hora_cliente(hora: str) -> rx.Component:
    disponible = ClienteCalendarState.horas_disponibles_dia.contains(hora)
    reservada = ClienteCalendarState.horas_reservadas_dia.contains(hora)
    
    return rx.cond(
        disponible,
        rx.button(
            f"{hora} (Disponible)", 
            on_click=lambda: ClienteCalendarState.reservar_hora(hora), 
            color_scheme="green", variant="solid", width="100%", cursor="pointer"
        ),
        rx.button(
            f"{hora} " + rx.cond(reservada, "(Ocupat)", "(No habilitat)"), 
            disabled=True, color_scheme="gray", variant="soft", width="100%"
        )
    )

# --- VISTA ÚNICA (ESTUDIANTE/CLIENTE) ---

@rx.page(route="/reservar", on_load=ClienteCalendarState.cargar_datos_mes)
def vista_cliente_calendario() -> rx.Component:
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    return rx.center(
        rx.vstack(
            rx.heading("Reserva la teva classe", size="7", color_scheme="green"),
            rx.text("Selecciona un dia en verd per veure les hores lliures.", size="2", color_scheme="gray"),
            
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon_button("chevron-left", on_click=ClienteCalendarState.prev_month, variant="soft", color_scheme="green"),
                        rx.text(ClienteCalendarState.month_name, size="4", weight="bold", width="150px", align="center"),
                        rx.icon_button("chevron-right", on_click=ClienteCalendarState.next_month, variant="soft", color_scheme="green"),
                        width="100%", justify="between", align="center", padding_bottom="15px", border_bottom="1px solid var(--gray-4)"
                    ),
                    rx.grid(*[rx.text(d, size="2", weight="bold", align="center", color_scheme="gray") for d in dias], columns="7", width="100%", padding_y="10px"),
                    rx.grid(rx.foreach(ClienteCalendarState.calendar_days, celda_cliente), columns="7", gap="2", width="100%"),
                    width="100%"
                ),
                rx.dialog.root(
                    rx.dialog.content(
                        rx.dialog.title(f"Hores per al {ClienteCalendarState.dia_seleccionado}"),
                        rx.dialog.description("Fes clic sobre una hora disponible:"),
                        rx.vstack(rx.foreach(BLOQUES_HORARIOS, fila_hora_cliente), spacing="2", padding_y="15px", width="100%"),
                        rx.hstack(
                            rx.dialog.close(
                                rx.button("Tancar", on_click=ClienteCalendarState.cerrar_modal, color_scheme="gray", cursor="pointer")
                            ), justify="end"
                        )
                    ),
                    open=ClienteCalendarState.show_modal, 
                ),
                width=["100%", "400px"], padding="20px", box_shadow="lg"
            ),
            spacing="4", padding_y=["20px", "50px"]
        ),
        min_height="100vh", padding="10px"
    )