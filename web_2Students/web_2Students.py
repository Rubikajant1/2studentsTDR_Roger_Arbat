import reflex as rx
from web_2Students.styles.styles import BASE_STYLE
from web_2Students.pages.front.principal_page import principal_page
from web_2Students.pages.front.student_coach import student_coach
from web_2Students.pages.front.search import search_page, SearchState, coach_profile_page

# Configuració de la web
config = rx.Config(
    app_name="2Students",
    frontend_port=3000
)

app = rx.App(
    style=BASE_STYLE,
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="teal",
    )
)

# 1. Página de Inicio
app.add_page(
    principal_page,
    title="2Students",
    route="/",
)

# 2. Registrarse como coach
app.add_page(student_coach, route='/new_student_coach', title='Student coach')

# 3. Página de búsqueda
app.add_page(
    search_page, 
    route='/find_coach', 
    title='Find a coach', 
    on_load=SearchState.get_coaches
)

# 4. Página de perfil dinámico por ID (CAMBIADO A coach_id)
app.add_page(
    coach_profile_page, 
    route="/perfil/[coach_id]", 
    title="Perfil de Coach"
)