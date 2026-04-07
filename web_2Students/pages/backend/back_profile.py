
import reflex as rx
from bson import ObjectId
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


class CoachState(rx.State):
    # Variables que se llenarán desde MongoDB
    email: str = ""
    password: str = ""
    nombre: str = ""
    ubicacion: str = "Barcelonès" # Valor por defecto o de DB
    precio: str = ""
    sobre_mi: str = ""
    especialidades: List[str] = []
    img_url: str = "/Short_logo.jpeg" # Fallback por si no tiene foto
    es_modo_edicion: bool = False

    def alternar_edicion(self):
        """Cambia entre ver el texto y ver el formulario."""
        self.es_modo_edicion = not self.es_modo_edicion

    def guardar_y_cerrar(self, campo: str, valor: str):
        """Actualiza el campo en la DB y vuelve a modo vista."""
        self.update_field(campo, valor)
        # Opcional: self.es_modo_edicion = False 
        # (Si prefieres que se cierre solo al terminar de editar)

    
    async def handle_upload(self, files: List[rx.UploadFile]):
        """Maneja la subida de la imagen de perfil."""
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Guardamos el archivo en el directorio de assets
            with outfile.open("wb") as f:
                f.write(upload_data)

            # Actualizamos la variable para que la imagen cambie en pantalla
            self.img_url = f"/{file.filename}"
            
            
    
    def login_coach(self):
        """
        Esta es la función que ya tienes vinculada a tu botón.
        Aquí es donde, tras validar la contraseña, traemos los datos.
        """
        # 1. Tu lógica de validación con MongoDB (ejemplo simplificado)
        # user_data = collection.find_one({"email": self.email})
        
        # 2. Si el usuario es correcto, "mapeamos" los datos a las variables del estado
        # self.nombre = user_data.get("nombre", "Usuario")
        # self.precio = str(user_data.get("precio", "0"))
        # self.sobre_mi = user_data.get("descripcion", "")
        # self.especialidades = user_data.get("especialidades", [])
        
        # 3. Redirigimos al panel de edición
        return rx.redirect("/mi-perfil")

    def update_field(self, field_name: str, value: str):
        """
        Función genérica para actualizar en caliente tanto el Estado como MongoDB.
        """
        setattr(self, field_name, value)
        # Aquí disparas el update a MongoDB:
        # collection.update_one({"email": self.email}, {"$set": {field_name: value}})
        print(f"Actualizado {field_name} a {value} en la DB")

