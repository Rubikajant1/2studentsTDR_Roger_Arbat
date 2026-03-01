import reflex as rx
from typing import List
from bson import ObjectId  # IMPORTANTE para buscar por ID en MongoDB
from web_2Students.db.db_client import db
from web_2Students.styles.colors import Colors as colors
from web_2Students.components.navbar import navbar

# --- 1. MODELO DE DATOS ---
class Coach(rx.Base):
    id: str  # Añadimos el ID al modelo para poder usarlo en los links
    name: str
    mail: str
    comarca: str
    subjects_list: List[str]
    price: int
    image: str
    description: str

# --- 2. ESTADOS ---

class SearchState(rx.State):
    """Estado para la búsqueda general."""
    filter_subject: str = ""
    filter_comarca: str = ""
    results: List[Coach] = []

    def get_coaches(self):
        query = {"type": "student_coach"}
        if self.filter_subject.strip():
            query["subjects_list"] = {"$elemMatch": {"$regex": self.filter_subject.strip(), "$options": "i"}}
        if self.filter_comarca.strip():
            query["comarca"] = {"$regex": self.filter_comarca.strip(), "$options": "i"}

        try:
            cursor = db.find(query)
            loaded_results = []
            for doc in cursor:
                # Guardamos el ID antes de quitarlo o transformarlo
                coach_id = str(doc.get("_id"))
                
                img_value = doc.get("image", "")
                if not img_value:
                    img_render = "https://api.dicebear.com/7.x/initials/svg?seed=SC"
                elif img_value.startswith("http"):
                    img_render = img_value
                else:
                    img_render = f"/uploaded_files/{img_value.split('/')[-1]}"

                loaded_results.append(
                    Coach(
                        id=coach_id, # Pasamos el ID string
                        name=str(doc.get("name", "Sense nom")),
                        mail=str(doc.get("mail", "")),
                        comarca=str(doc.get("comarca", "No especificada")),
                        subjects_list=list(doc.get("subjects_list", [])),
                        price=int(doc.get("price", 0)),
                        image=img_render,
                        description=str(doc.get("description", ""))
                    )
                )
            self.results = loaded_results
        except Exception as e:
            print(f"ERROR: {e}")
            self.results = []

    def on_load(self):
        return SearchState.get_coaches

class CoachDetailState(rx.State):
    """Estado para la página de perfil dinámico por ID."""
    coach: Coach = Coach(id="", name="", mail="", comarca="", subjects_list=[], price=0, image="", description="")

    def get_coach_details(self):
        # Capturamos el ID de la URL
        coach_id = self.router.page.params.get("coach_id", "")
        
        try:
            # Buscamos por ObjectId
            doc = db.find_one({"_id": ObjectId(coach_id)})
            
            if doc:
                img_value = doc.get("image", "")
                img_render = img_value if img_value.startswith("http") else f"/uploaded_files/{img_value.split('/')[-1]}"
                if not img_value: img_render = "https://api.dicebear.com/7.x/initials/svg?seed=SC"

                self.coach = Coach(
                    id=str(doc.get("_id")),
                    name=str(doc.get("name", "Sense nom")),
                    mail=str(doc.get("mail", "")),
                    comarca=str(doc.get("comarca", "No especificada")),
                    subjects_list=list(doc.get("subjects_list", [])),
                    price=int(doc.get("price", 0)),
                    image=img_render,
                    description=str(doc.get("description", "Aquest coach encara no ha afegit una descripció."))
                )
        except Exception as e:
            print(f"Error cargando detalle: {e}")

# --- 3. COMPONENTES ---

def coach_card(coach: Coach):
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.image(src=coach.image, width="100%", height="160px", object_fit="cover", border_radius="8px",max_width="150px"),
                rx.vstack(
                    rx.hstack(
                        rx.heading(coach.name, size="4", weight="bold"),
                        rx.spacer(),
                        rx.badge(f"{coach.price}€/h", color = colors.MIG.value, variant="surface", size='3'),
                        width="100%",
                    ),
                    rx.badge(f"📍 {coach.comarca}", color_scheme="blue", variant="soft"),
                    rx.flex(
                        rx.foreach(coach.subjects_list, lambda s: rx.badge(s, variant="outline", color_scheme="indigo")),
                        wrap="wrap", spacing="1", padding_top="2",
                    ),
                ),
            ),
            rx.button(
                "Veure perfil", 
                on_click=rx.redirect(f"/perfil/{coach.id}"),
                width="100%", 
                bg=colors.MIG_CLAR.value, 
                color="white",
                margin_top="3",
                cursor="pointer",
                is_external=True
            ),
            align_items="start", width="100%", padding="2",
        ),
    )

def search_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Explora els nostres Coaches", size="8", margin_y="4", color=colors.MIG_FOSC.value, padding_top="2em"),
                rx.box(
                    rx.hstack(
                        rx.icon(tag="search", size=25, color=colors.MIG_FOSC.value),
                        rx.input(placeholder="Assignatura...", on_change=SearchState.set_filter_subject, variant="soft", flex="2"),
                        rx.icon(tag="map_pin", size=18, color=colors.MIG_FOSC.value),
                        rx.input(placeholder="Comarca...", on_change=SearchState.set_filter_comarca, variant="soft", flex="1.5"),
                        rx.button("Buscar", on_click=SearchState.get_coaches, bg=colors.MIG_CLAR.value, color="white", flex="1"),
                        width="100%", spacing="3", align_items="center",
                    ),
                    padding="4", bg="#F8FAFC", border_radius="xl", width="100%", margin_bottom="6",
                ),
                rx.cond(
                    SearchState.results.length() > 0,
                    rx.grid(rx.foreach(SearchState.results, coach_card), columns={"initial": "1", "md": "3"}, spacing="6", width="100%"),
                    rx.center(rx.spinner(size="3"), padding_top="10")
                ),
                width="100%",
            ),
            size="4"
        )
    )

def coach_profile_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            rx.vstack(
                rx.button("← Tornar a la cerca", on_click=rx.redirect("/find_coach"), variant="ghost", margin_y="4", cursor="pointer"),
                rx.flex(
                    rx.image(src=CoachDetailState.coach.image, width={"initial": "100%", "md": "350px"}, height="400px", object_fit="cover", border_radius="xl", shadow="lg"),
                    rx.vstack(
                        rx.heading(CoachDetailState.coach.name, size="9", color=colors.MIG_FOSC.value),
                        rx.hstack(
                            rx.badge(f"📍 {CoachDetailState.coach.comarca}", size="3", color_scheme="blue"),
                            rx.badge(f"{CoachDetailState.coach.price}€/hora", size="3", color = colors.MIG.value),
                        ),
                        rx.separator(width="100%"),
                        rx.text("Sobre mi", weight="bold", size="5"),
                        rx.text(CoachDetailState.coach.description, size="4", line_height="1.6"),
                        rx.text("Especialitats", weight="bold", size="5", padding_top="2"),
                        rx.flex(
                            rx.foreach(CoachDetailState.coach.subjects_list, lambda s: rx.badge(s, variant="surface", size="3", color=colors.MIG.value)),
                            wrap="wrap", spacing="2"
                        ),
                        rx.spacer(),
                        rx.popover.root(
                            rx.popover.trigger(
                                rx.button(
                                    rx.hstack(
                                        rx.icon(tag="mail"),
                                        rx.text(f"Contactar amb {CoachDetailState.coach.name}",color="white", size="4"),
                                    ),
                                    bg = colors.MIG.value,
                                    size="4",
                                    height="50px",
                                    width="100%",
                                ),
                            ),
                            rx.popover.content(
                                rx.flex(
                                    rx.text(f"Escriu a: {CoachDetailState.coach.mail}",color=colors.FOSC.value),
                                    direction="column",
                                    spacing="3",
                                ),
                            ),
                        ),
                        align_items="start", spacing="4", flex="1"
                    ),
                    spacing="8", direction={"initial": "column", "md": "row"}, width="100%", background="white", padding="6", border_radius="2xl", shadow="sm"
                ),
                padding_top="2em", padding_bottom="4em"
            )
        ),
        bg="#FBFBFE", min_height="100vh",
        on_mount=CoachDetailState.get_coach_details
    )