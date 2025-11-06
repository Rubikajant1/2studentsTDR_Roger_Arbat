#Importacions
import reflex as rx
from web_2Students.db.db_client import db
from web_2Students.pages.backend.passwords import Passwords as pw


user_coach = db['student_coach']

class NewCoach(rx.State):
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
            "description": self.description,
            "image": self.img if self.img else "Logo_2Students.jpeg",
            "password": pw._password_hash
        }
        try:
            db.insert_one(new_coach)
            return rx.toast.success('Registre completat amb èxit!')
        except Exception as e:
            print(e)
            return rx.toast.error('S\'ha produït un error en completar el registre.')