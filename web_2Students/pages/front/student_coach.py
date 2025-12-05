### student_coach.py ###

#Importacions
import reflex as rx
from web_2Students.styles.colors import Colors as colors
from web_2Students.components.navbar import navbar
from web_2Students.pages.backend.back_stuent_coach import NewCoach
from web_2Students.pages.front.front_subjects import subjects_selector
from web_2Students.pages.front.calendar import calendar_for_desktop
from web_2Students.pages.front.mobile_student_coach import mobile_student_coach



def front_insertar_coach() -> rx.Component:
    return rx.tablet_and_desktop(
        rx.card(
            rx.vstack(
                # Título
                rx.text.strong(
                    "Tots els paràmetres s'han omplert correctament!",
                    margin_top='1em',
                    size='4'
                ),
                
                rx.text(
                    "Establiu contrassenya per finalitzar el registre com a StudentCoach.",
                    margin_y='0.5em',
                    weight="bold"
                ),
                
                # Información de seguridad
                rx.hstack(
                    rx.icon(tag='info', color=colors.FOSC.value),
                    rx.text(
                        """
                        La contrassenya que trieu serà la que fareu servir per entrar al
                        vostre compte, es important que sigui segura i que no la compartiu amb ningú més.""",
                        margin_bottom='1em',
                    ),
                    align="start",
                    width="100%",
                ),
                
                # Requisitos de contraseña
                rx.box(
                    rx.text(
                        f"Requisits: mínim {NewCoach.MIN_PASSWORD_LENGTH} caràcters, màxim {NewCoach.MAX_PASSWORD_LENGTH}",
                        size="2",
                        color=colors.FOSC.value,
                        opacity="0.7",
                    ),
                    margin_bottom="0.5em",
                ),
                
                # Input per la primera contrasenya
                rx.input(
                    placeholder="Posa la teva contrassenya",
                    on_change=NewCoach.set_first_password,
                    on_blur=NewCoach.validate_on_blur,  # ✨ Validar al sortir del camp
                    type='password',
                    width="100%",
                    px="4",
                    py="2",
                    border="1px solid",
                    border_color=colors.MIG_CLAR.value,
                    border_radius="md",
                    bg='white',
                    font_size="md",
                    color=colors.FOSC.value,
                    text_color=colors.FOSC.value,
                    _placeholder={"color": colors.FOSC.value},
                    _hover={
                        "border_color": colors.FOSC.value,
                    },
                    _focus={
                        "border_color": colors.FOSC.value,
                        "outline": "none"
                    },
                    required=True,
                    disabled=NewCoach.is_rate_limited,
                ),
                
                # Input per la segona contrassenya
                rx.input(
                    placeholder="Repetir contrassenya",
                    on_change=NewCoach.set_second_password,
                    on_blur=NewCoach.validate_on_blur,  # ✨ Validar al salir del campo
                    type='password',
                    width="100%",
                    px="4",
                    py="2",
                    border="1px solid",
                    border_color=rx.cond(
                        NewCoach.same_passwords & (NewCoach.error_message == ""),
                        "green",
                        colors.MIG_CLAR.value
                    ),
                    border_radius="md",
                    bg='white',
                    font_size="md",
                    color=colors.FOSC.value,
                    text_color=colors.FOSC.value,
                    _placeholder={"color": colors.FOSC.value},
                    _hover={
                        "border_color": colors.FOSC.value,
                    },
                    _focus={
                        "border_color": colors.FOSC.value,
                        "outline": "none"
                    },
                    required=True,
                    disabled=NewCoach.is_rate_limited,
                ),
                
                # Missatge d'error
                rx.cond(
                    NewCoach.error_message != "",
                    rx.hstack(
                        rx.icon(tag='circle-x', color='red', size=16),
                        rx.text(
                            NewCoach.error_message,
                            color='red',
                            size='2',
                            weight='medium',
                        ),
                        align="center",
                        spacing="2",
                        width="100%",
                        margin_top="0.5em",
                    ),
                ),
                
                # Indicador de contrassenyes coincidents
                rx.cond(
                    NewCoach.same_passwords & (NewCoach.error_message == ""),
                    rx.hstack(
                        rx.icon('circle-check-big', color='green', size=16),
                        rx.text(
                            "Les contrasenyes coincideixen!",
                            color='green',
                            size='2',
                            weight='medium',
                        ),
                        align="center",
                        spacing="2",
                        width="100%",
                        margin_top="0.5em",
                    ),
                ),
                rx.cond(
                    NewCoach.same_passwords & (NewCoach.error_message == ""),
                    rx.button(
                        "Finalitzar registre",
                        bg=colors.MIG.value,
                        width="100%",
                        margin_top="1em",
                        on_click=NewCoach.insert_student_coach()
                    ),
                ),
                # Botón de reset si está bloqueado
                rx.cond(
                    NewCoach.is_rate_limited,
                    rx.button(
                        "Reiniciar",
                        on_click=NewCoach.reset_rate_limit,
                        size="2",
                        margin_top="1em",
                        bg=colors.FOSC.value,
                        color="white",
                    ),
                ),
                
                width="100%",
                spacing="3",
            ),
            bg=colors.MIG.value,
            margin_top='1em',
            padding="1.5em",
        )
    )


# Funció predeterminada per als inputs
def chakra_input(placeholder, on_change) -> rx.Component:
    return rx.input(
        placeholder=placeholder,
        on_change=on_change,
        width="100%",
        px="4",
        py="2",
        border="1px solid",
        border_color=colors.MIG_CLAR.value,
        border_radius="md",
        bg='white',
        font_size="md",
        color=colors.FOSC.value,
        text_color=colors.FOSC.value,
        _placeholder={"color": colors.FOSC.value},
        _hover={
            "border_color": colors.FOSC.value,
        },
        _focus={
            "border_color": colors.FOSC.value,
            "outline": "none"
        },
        required=True
    )


# Funció front-end
def student_coach() -> rx.Component:
    return rx.box(
        navbar(),
        rx.tablet_and_desktop(
            rx.center(
                rx.vstack(
                    rx.heading("2Students", size='9'),
                    rx.text(
                        "D'estudiants per a estudiants",
                        size='5',
                    ),
                    align='center'
                ),
                padding_top='5em',
                padding_bottom='1em'
            ),
            rx.box(
                rx.card(
                    rx.box(
                        rx.heading(
                            "Registrar-me com a student coach",
                            size='5',
                            padding_bottom='0.6em'
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text("Nom i cognoms", padding_bottom = '0.4em',),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Posa el teu nom complet amb els dos cognoms",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        chakra_input(
                            placeholder="Posa el teu nom complet",
                            on_change=NewCoach.set_name
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Correu electrònic",
                                    padding_bottom='0.4em',
                                    padding_top='0.5em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Posa un correu electronic que facis servir on et puguin contactar",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        chakra_input(
                            placeholder="Posa el correu electrònic",
                            on_change=NewCoach.set_mail
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Comarca",
                                    padding_bottom='0.4em',
                                    padding_top='0.5em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Selecciona la comarca de Catalunya on vols donar classe",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        rx.select(
                            [
                                "Alt Camp","Alt Empordà","Alt Penedès","Alt Urgell","Alta Ribagorça","Anoia","Bages","Baix Camp","Baix Ebre","Baix Empordà","Baix Llobregat","Baix Penedès","Barcelonès",
                                "Berguedà","Cerdanya","Conca de Barberà","Garraf","Garrigues","Garrotxa","Gironès","La Selva","La Vall d'Aran","Maresme","Montsià","Noguera","Osona","Pallars Jussà","Pallars Sobirà",
                                "Pla de l'Estany","Pla d'Urgell","Priorat","Ribera d'Ebre","Ripollès","Segarra","Segrià","Solsonès","Tarragonès","Terra Alta","Urgell","Vallès Occidental","Vallès Oriental",
                            ],
                            variant='classic',
                            color_scheme='purple',
                            on_change=NewCoach.set_comarca,
                            default_value='Alt Camp',
                            radius="large",
                            position='item-aligned',
                            required=True,
                            width='100%',
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Poble o ciutat",
                                    padding_bottom='0.4em',
                                    padding_top='0.5em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    """Posa el nom complet del poble o ciutat, no s'accepten abreviatures com "Sanpe" per referir-se a Sant Pere o qualsevol altre
                                    abreviatura""",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        chakra_input(
                            placeholder="Posa el nom del teu poble o ciutat",
                            on_change=NewCoach.set_localitzacio
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "DNI o NIE",
                                    padding_bottom='0.4em',
                                    padding_top='0.5em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Posa el teu DNI o NIE amb la lletra corresponent",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        chakra_input(
                            placeholder='DNI/NIE',
                            on_change=NewCoach.set_dni
                        ),
                        rx.cond(
                            ~NewCoach.is_dni,
                            rx.text(
                                "El DNI/NIE introduït no és vàlid",
                                color='red',
                                font_size='sm',
                                padding_bottom='0.5em'
                            ),
                        ),
                        rx.cond(
                            NewCoach.is_dni,
                            rx.text(
                                "El DNI/NIE introduït és vàlid",
                                color='green',
                                font_size='sm',
                                padding_bottom='0.5em'
                            ),
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Data de naixement",
                                    padding_bottom='0.4em',
                                    padding_top='0.5em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Posa la teva data de naixement seguint aquest format: dia/mes/any",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        rx.hstack(
                            rx.input(
                                placeholder="Dia",
                                on_change=NewCoach.set_dia_neixament,
                                max_length=2,
                                width="100%",
                                px="4",
                                py="2",
                                border="1px solid",
                                border_color=colors.MIG_CLAR.value,
                                border_radius="md",
                                bg='white',
                                font_size="md",
                                color=colors.FOSC.value,
                                text_color=colors.FOSC.value,
                                _placeholder={"color": colors.FOSC.value},
                                _hover={
                                    "border_color": colors.FOSC.value,
                                },
                                _focus={
                                    "border_color": colors.FOSC.value,
                                    "outline": "none"
                                },
                                required=True
                            ),
                            rx.text("/"),
                            rx.input(
                                placeholder="Mes",
                                on_change=NewCoach.set_mes_neixament,
                                max_length=2,
                                width="100%",
                                px="4",
                                py="2",
                                border="1px solid",
                                border_color=colors.MIG_CLAR.value,
                                border_radius="md",
                                bg='white',
                                font_size="md",
                                color=colors.FOSC.value,
                                text_color=colors.FOSC.value,
                                _placeholder={"color": colors.FOSC.value},
                                _hover={
                                    "border_color": colors.FOSC.value,
                                },
                                _focus={
                                    "border_color": colors.FOSC.value,
                                    "outline": "none"
                                },
                                required=True
                            ),
                            rx.text("/"),
                            rx.input(
                                placeholder="Any",
                                on_change=NewCoach.set_any_neixament,
                                max_length=4,
                                width="100%",
                                px="4",
                                py="2",
                                border="1px solid",
                                border_color=colors.MIG_CLAR.value,
                                border_radius="md",
                                bg='white',
                                font_size="md",
                                color=colors.FOSC.value,
                                text_color=colors.FOSC.value,
                                _placeholder={"color": colors.FOSC.value},
                                _hover={
                                    "border_color": colors.FOSC.value,
                                },
                                _focus={
                                    "border_color": colors.FOSC.value,
                                    "outline": "none"
                                },
                                required=True
                            ),
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Assignatures que vols donar",
                                    padding_bottom='0.4em',
                                    padding_top='1em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Selecciona totes les assignatures en les que vulguis compartir coneixaments",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        subjects_selector(),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Mes assignatures",
                                    padding_bottom='0.4em',
                                    padding_top='0.5em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    """Si hi ha alguna assignatura mes que vulguis donar i que no surti als botons que hi ha a sobre el pots escriure
                                    en aquest input""",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        chakra_input(
                            placeholder='Assignatures extra',
                            on_change=NewCoach.set_extra_subject
                        ),
                        rx.hstack(
                            rx.menu.root(
                                rx.menu.trigger(
                                    rx.text("Preu per classe", padding_bottom = '1em',font_weight="bold",),
                                ),
                                rx.menu.content(
                                    rx.menu.item(
                                        "El preu recomanat per classe es d'uns 10€ aproximadament tot i que pots posar el preu que creguis adequat",
                                        color=colors.FOSC.value,
                                        bg=colors.CLAR.value
                                    )
                                )
                            ),
                            padding_bottom='0.2em', 
                            padding_top='1.5em'
                        ),
                        rx.hstack(
                            rx.input(placeholder='10', max_length=2, required=True, width='5%',on_change=NewCoach.set_price),
                            rx.heading("€"),
                            padding_bottom ='1em'
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Horaris disponibles:",
                                    font_weight="bold",
                                    padding_y='0.4em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Selecciona els horaris que estiguis disponible per donar classe",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        calendar_for_desktop(),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Foto",
                                    font_weight="bold",
                                    padding_top='1em'
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Puja una imatge teva que vulguis que veigin les persones que busquen un StudentCoach",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        rx.vstack(
                            rx.cond(
                                ~NewCoach.has_image,
                                rx.vstack(
                                    rx.upload(
                                        rx.vstack(
                                            rx.button(
                                                "Selecciona una imatge",
                                                color=colors.MIG_FOSC.value,
                                                bg="white",
                                                border=f"1px solid {colors.MIG_FOSC.value}",
                                            ),
                                            rx.text(
                                                "Tria una imatge teva que vulguis que es veigi com a foto de perfil d'usuari"
                                            ),
                                        ),
                                        id="upload1",
                                        border=f"1px dotted {colors.MIG_FOSC.value}",
                                        padding="5em",
                                        multiple=False,  # Nomes prermet un arxiu
                                    ),
                                    rx.hstack(
                                        rx.foreach(
                                            rx.selected_files("upload1"), rx.text
                                        )
                                    ),
                                    rx.button(
                                        "Puja",
                                        on_click=NewCoach.handle_upload(
                                            rx.upload_files(upload_id="upload1")
                                        ),
                                        bg = colors.MIG.value
                                    ),
                                    rx.button(
                                        "Borra",
                                        on_click=rx.clear_selected_files("upload1"),
                                        bg=colors.MIG.value
                                    ),
                                ),
                                rx.vstack(
                                    rx.image(
                                        src=rx.get_upload_url(NewCoach.img),
                                        width="100%",
                                        height="auto",
                                        border_radius="8px",
                                        border=f"2px solid {colors.MIG.value}",
                                    ),
                                    rx.button(
                                        "Substituir",
                                        on_click=NewCoach.clear_image,
                                        color="white",
                                        bg=colors.MIG.value,
                                    ),
                                    rx.button(
                                        "Borrar imatge",
                                        on_click=NewCoach.clear_image,
                                        color=colors.MIG.value,
                                        bg="white",
                                        border=f"1px solid {colors.MIG.value}",
                                    ),
                                    spacing="2",
                                    align="center",
                                    justify='center'
                                ),
                            ),
                            padding_y="1em",
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.text(
                                    "Descripció",
                                    font_weight="bold",
                                    padding_y='0.4em',
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    "Escriu la descripció o coses que creguis que et diferencien de la resta de StudentCoaches",
                                    color=colors.FOSC.value,
                                    bg=colors.CLAR.value
                                )
                            )
                        ),
                        rx.text_area(
                            placeholder='Escriu una descripció que et descrigui i explica les teves qualitats com a professor',
                            height = "200px",
                            width = "100%",
                            resize="none",
                            on_change=NewCoach.set_description,
                            color_scheme='purple'
                        ),
                        rx.button(
                            "Crear nou StudentCoach",
                            margin_top='5em',
                            width = "100%",
                            bg=colors.MIG.value,
                            on_click=NewCoach.check_all_parameters
                        ),
                        rx.cond(
                            NewCoach.tots_els_parametres==True,
                            front_insertar_coach()
                        ),
                        margin_x='6em'
                    ),
                    margin_x='20em',
                    padding_y='2em',
                    margin_top='1em',
                    margin_bottom='4em',
                    bg=colors.CLAR.value
                )
            )
        ),
        rx.mobile_only(
            mobile_student_coach()
        )
    )


