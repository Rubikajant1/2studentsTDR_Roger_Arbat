### web_2Students.py ###

#Importacions
import reflex as rx
from web_2Students.styles.styles import BASE_STYLE
from web_2Students.pages.front.principal_page import principal_page
from web_2Students.pages.front.student_coach import student_coach
from web_2Students.pages.backend.back_stuent_coach import NewCoach



# Configuració de la web
config = rx.Config(
    app_name="2Students",
    frontend_port=3000
)

#Funció front-end per a la pàgina principal



#Posar estils
app = rx.App(
    style=BASE_STYLE
)


app.add_page(
    principal_page,
    title="2Students",
    route="/",
    description="Pàgina web per alumnes que ajuden a altres alumnes"
)
app.add_page(student_coach,route='/new_student_coach',title='Student coach')