#Importacions
import reflex as rx
from web_2Students.db.db_client import db
import secrets
from typing import Optional
import hashlib


user_coach = db['student_coach']


class NewCoach(rx.State):
    
    dilluns: str = ""
    dimarts: str = ""
    dimecres: str = ""
    dijous: str = ""
    divendres: str = ""
    dissabte_mati: str = ""
    dissabte_tarda: str = ""
    diumenge_mati: str = ""
    diumenge_tarda: str = ""
    especificacions_dilluns: str = ""
    especificacions_dimarts: str = ""
    especificacions_dimecres: str = ""
    especificacions_dijous: str = ""
    especificacions_divendres: str = ""
    especificacions_dissabte_mati: str = ""
    especificacions_dissabte_tarda: str = ""
    especificacions_diumenge_mati: str = ""
    especificacions_diumenge_tarda: str = ""
    
    
    ### Contrassenya ###
    
    MAX_PASSWORD_LENGTH: int = 128
    MIN_PASSWORD_LENGTH: int = 8
    MAX_VALIDATION_ATTEMPTS: int = 5
    
    # Variables privadas
    _first_password: str = ""
    _second_password: str = ""
    _password_hash: Optional[bytes] = None
    _validation_attempts: int = 0
    _last_validation_state: tuple = ("", "")  # Guarda ultim
    
    # Variables públicas
    same_passwords: bool = False
    error_message: str = ""
    is_rate_limited: bool = False

    
    @rx.event()
    def set_first_password(self, first_password: str):
        """Establir la primera contrasenya amb validació de longitud"""
        if self.is_rate_limited:
            self.error_message = "Demasiats intents. Espera un moment."
            return
            
        if len(first_password) > self.MAX_PASSWORD_LENGTH:
            self.error_message = f"Contrassenya massa llarga (màx. {self.MAX_PASSWORD_LENGTH} caràcters)"
            return
            
        self._first_password = first_password
        self.error_message = ""
        # NO validar aquí, només guardar
        
        
    @rx.event()
    def set_second_password(self, second_password: str):
        """Establir la segona contrasenya amb validació de longitud"""
        if self.is_rate_limited:
            self.error_message = "Demasiats intents. Espera un moment."
            return
            
        if len(second_password) > self.MAX_PASSWORD_LENGTH:
            self.error_message = f"Contrassenya massa llarga (màx. {self.MAX_PASSWORD_LENGTH} caràcters)"
            return
            
        self._second_password = second_password
        self.error_message = ""
        # NO validar aquí, només guardar

    
    @rx.event()
    def validate_on_blur(self):
        """Validar només quan l'usuari canvia de camp (onBlur)"""
        current_state = (self._first_password, self._second_password)
        if current_state == self._last_validation_state:
            return  # No validar si no hi ha canvis
            
        self._last_validation_state = current_state
        
        # Incrementar el contador només en validacions reales
        self._validation_attempts += 1
        
        # Rate limiting bàsic
        if self._validation_attempts > self.MAX_VALIDATION_ATTEMPTS:
            self.is_rate_limited = True
            self.same_passwords = False
            self.error_message = "Demasiats intents de validació"
            return
        
        # Validar que les dues coincideixin
        if not self._first_password or not self._second_password:
            self.same_passwords = False
            return
            
        if len(self._first_password) < self.MIN_PASSWORD_LENGTH:
            self.same_passwords = False
            self.error_message = f"La contrassenya ha de tenir almenys {self.MIN_PASSWORD_LENGTH} caràcters"
            return
        
        try:
            # Normalizar strings abans de compararles (evitar atacs Unicode)
            first_normalized = self._first_password.encode('utf-8', errors='strict')
            second_normalized = self._second_password.encode('utf-8', errors='strict')
            
            # Comparació segura de contrasenyes
            self.same_passwords = secrets.compare_digest(
                first_normalized,
                second_normalized
            )
            
            # Generar hash si coinciden
            if self.same_passwords:
                self._password_hash = hashlib.sha256(first_normalized).digest()
                self.error_message = ""
            else:
                self.error_message = "Les contrasenyes no coincideixen"
                
        except UnicodeEncodeError:
            self.same_passwords = False
            self.error_message = "Caràcters invàlids a la contrassenya"
        except Exception as e:
            self.same_passwords = False
            self.error_message = "Error al validar contrasenyes"
            print(f"Error intern: {type(e).__name__}")
    
    
    def clear_passwords(self):
        """Neteja les les contrassenyes de memoria (limitat en Python)"""
        self._first_password = ""
        self._second_password = ""
        
        
    @rx.event()
    def reset_rate_limit(self):
        """Permet resetear el rate limit"""
        self._validation_attempts = 0
        self.is_rate_limited = False
        self.error_message = ""
        self._last_validation_state = ("", "")
        
    @rx.var
    def password_hash(self) -> str:
        """Return a hex-encoded password hash if exists"""
        if self._password_hash:
            return self._password_hash.hex()
        return ""
    
    name: str = ""
    mail: str = ""
    comarca: str = "Alt Camp"
    localitzacio: str = ""
    dni:str = ''
    dia_neixament:str = ''
    mes_neixament:str = ''
    any_neixament:str = ''
    subjects_list:list = []
    current_subject:str = ''
    extra_subject:str = ''
    price:int = 10
    description:str = ''
    uploaded_image: str = "Logo_2Students.jpeg"
    img= str = ""
    
    is_dni:bool = False
    tots_els_parametres:bool = False
    
    rx.var()
    def set_dilluns(self,dilluns ):
        self.dilluns=dilluns

        
    rx.var()
    def set_dimarts(self,dimarts ):
        self.dimarts=dimarts
        
    rx.var()
    def set_dimecres(self,dimecres ):
        self.dimecres=dimecres
        
    rx.var()
    def set_dijous(self,dijous ):
        self.dijous=dijous
        
    rx.var()
    def set_divendres(self,divendres ):
        self.divendres=divendres
        
    rx.var()
    def set_dissabte_mati(self,dissabte_mati ):
        self.dissabte_mati=dissabte_mati
        
    rx.var()
    def set_dissabte_tarda(self,dissabte_tarda ):
        self.dissabte_tarda=dissabte_tarda
        
    rx.var()
    def set_diumenge_mati(self,diumenge_mati ):
        self.diumenge_mati=diumenge_mati
        
    rx.var()
    def set_diumenge_tarda(self,diumenge_tarda ):
        self.diumenge_tarda=diumenge_tarda
        
    rx.var()
    def set_especificacions_dilluns(self,especificacions_dilluns ):
        self.especificacions_dilluns=especificacions_dilluns
        
    rx.var()
    def set_especificacions_dimarts(self,especificacions_dimarts ):
        self.especificacions_dimarts=especificacions_dimarts
        
    rx.var()
    def set_especificacions_dimecres(self,especificacions_dimecres ):
        self.especificacions_dimecres=especificacions_dimecres
        
    rx.var()
    def set_especificacions_dijous(self,especificacions_dijous ):
        self.especificacions_dijous=especificacions_dijous
        
    rx.var()
    def set_especificacions_divendres(self,especificacions_divendres ):
        self.especificacions_divendres=especificacions_divendres
        
    rx.var()
    def set_especificacions_dissabte_mati(self,especificacions_dissabte_mati ):
        self.especificacions_dissabte_mati=especificacions_dissabte_mati
        
    rx.var()
    def set_especificacions_dissabte_tarda(self,especificacions_dissabte_tarda ):
        self.especificacions_dissabte_tarda=especificacions_dissabte_tarda 
        
    rx.var()
    def set_especificacions_diumenge_mati(self,especificacions_diumenge_mati ):
        self.especificacions_diumenge_mati=especificacions_diumenge_mati
        
    rx.var()
    def set_especificacions_diumenge_tarda(self,especificacions_diumenge_tarda ):
        self.especificacions_diumenge_tarda=especificacions_diumenge_tarda

    
    @rx.event()
    def set_name(self, new_name):
        self.name = new_name
    
    @rx.event()
    def set_mail(self, new_mail):
        self.mail = new_mail
    
    @rx.event()
    def set_comarca(self, new_comarca):
        self.comarca = new_comarca
    
    @rx.event()
    def set_localitzacio(self, new_location):
        self.localitzacio = new_location
    
    @rx.event()
    def set_dni(self, new_dni):
        self.dni = new_dni
        self.validar_dni_nie()
        
    @rx.event()
    def set_dia_neixament(self, new_dia):
        self.dia_neixament = new_dia
        
    @rx.event()
    def set_mes_neixament(self, new_mes):
        self.mes_neixament = new_mes
        
    @rx.event()
    def set_any_neixament(self, new_any):
        self.any_neixament = new_any
        
        
    """Subjects functions"""
    """----------------------------------------------------------------------"""
    @rx.event()
    def set_current_subject(self, subject):
        self.current_subject=subject
        
    @rx.event()
    def add_subject(self):
        self.subjects_list.append(self.current_subject)
        
    @rx.event()
    def remove_subject(self):
        if self.current_subject in self.subjects_list:
            self.subjects_list.remove(self.current_subject)
        else:
            return rx.toast.error(f"Aquesta assignatura no està dintre de la llista de assignatures seleccionades ({self.current_subject})")
    """----------------------------------------------------------------------"""
    
    @rx.event()
    def set_extra_subject(self, new_extra_subject):
        self.extra_subject = new_extra_subject
    
    @rx.event()
    def set_price(self, new_price):
        self.price = int(new_price)
    
    
    """Upload Image functions"""
    """----------------------------------------------------------------------"""
    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        try:
            if files:  #Nomes procesa si hi ha algun arxiu
                #Agafa el primer arxiu
                file = files[0]
                upload_data = await file.read()
                outfile = rx.get_upload_dir() / file.name

                # Save the file.
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)

                # Update the img var (reemplaza la imagen anterior)
                self.img = file.name
            else:
                return rx.toast.error('No hi ha cap fitxer seleccionat')
        except Exception as e:
            return rx.toast.error('S\'ha produït un error durant la càrrega del fitxer.')

    @rx.event
    def clear_image(self):
        """Limpia la imagen actual"""
        self.img = ""

    @rx.var
    def has_image(self) -> bool:
        """Verifica si ya hay una imagen cargada"""
        return bool(self.img)
    """----------------------------------------------------------------------"""
    
    @rx.event()
    def set_description(self, new_description):
        self.description = new_description


    """DNI/NIE validation function"""
    """----------------------------------------------------------------------"""
    def validar_dni_nie(self):
        try:
            """Funció per validar el DNI o NIE introduït per l'usuari"""
            documento = self.dni.upper()
            lletres_valides = "TRWAGMYFPDXBNJZSQVHLCKE"
            
            # Validació bàsica de longitud
            if len(documento) != 9:
                self.is_dni = False
                return
            
            lletra_final = documento[-1]
            
            # Verificar que la lletra final sigui vàlida
            if lletra_final not in lletres_valides:
                self.is_dni = False
                return
            
            primer_caracter = documento[0]
            
            # Processar segons si és DNI o NIE
            if primer_caracter in "XYZ":
                # És un NIE
                numeros_centrals = documento[1:-1]
                
                # Verificar que els 7 dígits centrals siguin numèrics
                if not numeros_centrals.isdigit() or len(numeros_centrals) != 7:
                    self.is_dni = False
                    return
                
                # Substituir X/Y/Z per 0/1/2
                conversio = {'X': '0', 'Y': '1', 'Z': '2'}
                numeros_complet = conversio[primer_caracter] + numeros_centrals
            else:
                # És un DNI
                numeros_complet = documento[:-1]
                
                # Verificar que els 8 primers caràcters siguin numèrics
                if not numeros_complet.isdigit() or len(numeros_complet) != 8:
                    self.is_dni = False
                    return
            
            # Calcular la lletra correcta
            index = int(numeros_complet) % 23
            lletra_correcta = lletres_valides[index]
            
            # Comprovar si coincideix
            if lletra_final == lletra_correcta:
                self.is_dni = True
            else:
                self.is_dni = False
                
        except Exception:
            self.is_dni = False
    """----------------------------------------------------------------------"""
    
    
    """All parameters filled function"""
    """----------------------------------------------------------------------"""
    
    def check_all_parameters(self):
        """Funció per comprovar que tots els paràmetres estan omplerts"""
        if (self.name and self.mail and self.comarca and self.localitzacio and self.dni and
            self.dia_neixament and self.mes_neixament and self.any_neixament and
            self.subjects_list and self.price and self.description and self.is_dni):
            self.tots_els_parametres = True
        else:
            self.tots_els_parametres = False
            return rx.toast.error('Cal omplir tots els camps correctament abans de continuar.')


    """----------------------------------------------------------------------"""
    def insert_student_coach(self):
        """Funció per inserir el nou student coach a la base de dades"""
        if db.find_one({"dni": self.dni}):
            return rx.toast.error('Ja existeix un usuari registrat amb aquest DNI/NIE.')
        new_coach = {
            "name": self.name,
            "mail": self.mail,
            "comarca": self.comarca,
            "localitzacio": self.localitzacio,
            "dni": self.dni,
            "data_neixament": f"{self.dia_neixament}/{self.mes_neixament}/{self.any_neixament}",
            "subjects_list": list(self.subjects_list),
            "extra_subject": self.extra_subject,
            "price": self.price,
            "Horari": [
                {"dilluns": self.dilluns},  # Quita str() y accede directamente
                {"dilluns excepcions":self.especificacions_dilluns},
                {"dimarts": self.dimarts},
                {"dimarts excepcions":self.especificacions_dimarts},
                {"dimecres": self.dimecres},
                {"dimecres excepcions":self.especificacions_dimecres},
                {"dijous": self.dijous},
                {"dijous excepcions":self.especificacions_dijous},
                {"divendres": self.divendres},
                {"divendres excepcions":self.especificacions_divendres},
                {"dissabte_mati": self.dissabte_mati},
                {"dissabte_mati excepcions":self.especificacions_dissabte_mati},
                {"dissabte_tarda": self.dissabte_tarda},
                {"dissabte_tarda excepcions":self.especificacions_dissabte_tarda},
                {"diumenge_mati": self.diumenge_mati},
                {"diumenge_mati excepcions":self.especificacions_diumenge_mati},
                {"diumenge_tarda": self.diumenge_tarda},
                {"diumenge_tarda excepcions":self.especificacions_diumenge_tarda}
            ],
            "description": self.description,
            "image": self.img if self.img else "Logo_2Students.jpeg",
            "password": self._password_hash
        }
        try:
            db.insert_one(new_coach)
            return rx.toast.success('Registre completat amb èxit!')
        except Exception as e:
            print(e)
            return rx.toast.error('S\'ha produït un error en completar el registre.')
        
