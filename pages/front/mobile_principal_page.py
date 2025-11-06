### mobile_principal_page.py ###

#Importacions
import reflex as rx
from web_2Students.components.navbar import navbar
from web_2Students.styles.colors import Colors as colors

def principal_mobile_page() -> rx.Component:
    return rx.box(
        navbar(),
            rx.center(
                rx.vstack(
                    rx.heading("2Students",size='9'),
                    rx.text(
                        "D'estudiants per a estudiants",
                        size='3',
                        
                    ),
                    align='center'
                ),
                padding_top ='5em',
                padding_bottom = '1em'
            ),
            rx.box(
                rx.card(
                    rx.flex(
                        rx.vstack(
                            rx.heading(
                                "La missió de 2Students",
                                size='4'
                            ),
                            rx.text(
                                """
                                Aquesta app ha estat creada amb la finalitat de crear una comunitat d'aprenentatge entre estudiants. D'una banda, permet als alumnes que
                                destaquen en certes assignatures obtenir una compensació econòmica mentre comparteixen els seus coneixements. D'altra banda, ofereix una
                                alternativa valuosa als estudiants que necessiten suport addicional.
                                """,
                                size='1'
                            ),
                            rx.text(
                                """
                                Aprendre d'un student coach té avantatges únics: ells han superat els mateixos reptes recentment, entenen perfectament les dificultats actuals
                                del curs i poden compartir estratègies d'estudi que han funcionat en el seu propi camí d'aprenentatge.
                                """,
                                size='1'
                            ),
                            rx.text(
                                """
                                La nostra plataforma connecta aquests dos mons, creant un espai on el coneixement es comparteix entre iguals d'una manera propera, efectiva i
                                adaptada a les necessitats reals dels estudiants d'avui.
                                """,
                                size='1'
                            ),
                            padding ='1em'
                        ),
                    ),
                    rx.box(    
                        rx.image(
                            src="Logo_2Students.jpeg",
                            width = '60%',
                            height = '60%',
                        ),
                        display = "flex",
                        justify_content = "center"
                    ),
                    bg = colors.CLAR.value,
                    width = '90%'
                ),
                padding = '2em'
            ),
            rx.box(
                rx.card(
                    rx.flex(
                        rx.vstack(
                            rx.heading(
                                "Com funciona 2Students?",
                                size='4'
                            ),
                            rx.text(
                                """
                                2Students connecta de manera senzilla estudiants que necessiten ajuda amb companys que poden oferir-la. El procés és simple i efectiu. 
                                La nostra plataforma permet que et registris indicant les assignatures en què necessites suport o aquelles en què pots ensenyar altres.
                                """,
                                size='1'
                            ),
                            rx.text(
                                """
                                Si busques ajuda, podràs explorar perfils dels student coaches i contactar amb qui millor s'adapti a les teves necessitats.
                                Si ofereixes ajuda, crearàs el teu perfil destacant les teves habilitats i establint la teva disponibilitat. La plataforma facilita la
                                coordinació d'espais i horaris, tant presencials com en línia, i gestiona els pagaments de manera segura.
                                """,
                                size='1'
                            ),
                            rx.text(
                                """
                                A 2Students creiem que l'aprenentatge entre iguals és una de les formes més efectives d'entendre i dominar nous conceptes. La nostra
                                plataforma no només facilita aquest intercanvi, sinó que crea oportunitats perquè tots els estudiants creixin acadèmicament
                                """,
                                size='1'
                            ),
                            padding_top ='1em',
                            padding ='1em'
                        ),
                    ),
                    rx.box(
                        rx.image(
                            src="2_estudiants_img1.jpg",
                            width = '60%',
                            height = '60%',
                        ),
                        display = "flex",
                        justify_content = "center"
                    ),
                    bg = colors.CLAR.value,
                    width = '90%'
                ),
                padding = '2em',
                display = "flex",
                justify_content = "flex-end"
            ),
            rx.box(
                rx.card(
                    rx.flex(
                        rx.vstack(
                            rx.heading(
                                "Comença a buscar el teu student coach!",
                                size='4'
                            ),
                            rx.text(
                                """
                                Estàs trobant dificultats amb alguna assignatura? No esperis a l'últim moment. A 2Students tenim estudiants com tu, que han superat els mateixos
                                reptes i estan preparats per ajudar-te amb un enfocament proper i personalitzat.
                                """,
                                size='1'
                            ),
                            rx.text(
                                """
                                Trobar el suport adequat pot marcar la diferència entre l'estrès i la confiança, entre aprovar amb dificultats i comprendre realment la matèria.
                                La nostra comunitat d'estudiants col·laboradors coneix de primera mà les dificultats específiques del teu curs i pot oferir-te estratègies d'estudi que potser no has considerat.
                                """,
                                size='1'
                            ),
                            padding ='1em'
                        ),
                    ),
                    rx.button(
                        "Vull trobar el meu student coach!",
                        margin_x = '1em',
                        bg = colors.MIG_CLAR.value,
                        width = '90%',
                        radius='full'
                        
                    ),
                    rx.box(
                        rx.image(
                            src="2_estudiants_img2.jpg",
                            width = '65%',
                            height = '65%',
                            padding_top='1em'
                        ),
                        display = "flex",
                        justify_content = "center"
                    ),
                    bg = colors.CLAR.value,
                    width = '90%'
                ),
                padding = '2em'
            ),
            rx.box(
                rx.card(
                    rx.flex(
                        rx.vstack(
                            rx.heading(
                                "Comparteix el teu coneixement, sigues un student coach!",
                                size='4'
                            ),
                            rx.text(
                                """
                                Tens facilitat per alguna assignatura? Els teus companys et demanen ajuda habitualment? Posa el teu talent al servei d'altres estudiants i 
                                converteix-te en un student coach.
                                """,
                                size='1'
                            ),
                            rx.text(
                                """
                                Ensenyar és una de les millors maneres d'aprendre. Quan ajudes a altres explicant el que saps, tu mateix entens millor la matèria, veus les
                                coses des d'altres punts de vista i millores la teva manera de comunicar-te.
                                """,
                                size='1'
                            ),
                            rx.text(
                                """
                                A 2Students, pots definir les teves pròpies condicions: estableix la teva disponibilitat, tria les assignatures en què et sents més segur
                                i fixa la teva tarifa. L'experiència com a docent millorarà el teu perfil.
                                """,
                                size='1'
                            ),
                            padding_top ='1em',
                            padding_x ='1em'
                        ),
                    ),
                     rx.button(
                        "Vull ser un student coach!",
                        margin_x = '1em',
                        bg = colors.MIG_CLAR.value,
                        width = '90%',
                        radius='full',
                        margin_top='1em',
                        on_click=rx.redirect('/new_student_coach')
                    ),
                    rx.box(
                        rx.image(
                            src="2_estudiants_img3.jpg",
                            width = '70%',
                            height = '70%',
                            margin_top='1.5em'
                        ),
                        display="flex",
                        justify_content="center",
                        padding_top="1em",
                    ),
                    bg = colors.CLAR.value,
                    width = '90%',
                    height='10%'
                ),
                padding = '2em',
                display = "flex",
                justify_content = "flex-end"
            ),
    )