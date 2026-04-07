import reflex as rx
from bson import ObjectId
from web_2Students.pages.backend.back_stuent_coach import AuthState, user_coach
from typing import Dict, List, Any

class ProfileState(rx.State):
    coach_data: Dict[str, Any] = {}

    @rx.var
    def coach_subjects_all(self) -> List[str]:
        lista_principal = self.coach_data.get("subjects_list", [])
        extra = self.coach_data.get("extra_subject", "").strip()
        totes = list(lista_principal)
        if extra:
            totes.append(extra)
        return totes

    @rx.var
    def coach_image_url(self) -> str:
        img = self.coach_data.get("image", "").strip()
        if not img:
            return "/Logo_2Students.jpeg"
        if img.startswith(("http://", "https://")):
            return img
        
        clean_img = img.lstrip("/")
        if "uploaded_files" in clean_img:
            return f"/{clean_img}"
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
                    if "subjects_list" not in user: # Corregido para que coincida con tu Var
                        user["subjects_list"] = []
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
    editing_field: str = ""

    def set_editing(self, field: str):
        self.editing_field = field

    def stop_editing(self, _val=None):
        self.editing_field = ""

    async def _update_db_field(self, field_key: str, value: str):
        """Función interna para actualizar MongoDB y el estado local."""
        profile_state = await self.get_state(ProfileState)
        coach_id = profile_state.coach_data.get("_id")

        if coach_id:
            try:
                user_coach.update_one(
                    {"_id": ObjectId(coach_id)},
                    {"$set": {field_key: value}}
                )
                # Actualizamos el diccionario local para refrescar la UI
                new_data = profile_state.coach_data.copy()
                new_data[field_key] = value
                profile_state.coach_data = new_data
            except Exception as e:
                print(f"Error al actualizar: {e}")

    # --- CORRECCIÓN: Usar await y no hacer return directo ---

    async def set_nombre(self, val: str):
        await self._update_db_field("name", val)

    async def set_comarca(self, val: str):
        await self._update_db_field("comarca", val)

    async def set_precio(self, val: str):
        await self._update_db_field("price", val)

    async def set_descripcion(self, val: str):
        await self._update_db_field("description", val)

    # --- OTROS MÉTODOS ---

    async def handle_upload(self, files: List[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename
            with outfile.open("wb") as f:
                f.write(upload_data)
            
            # Actualizamos la foto en la DB
            await self._update_db_field("image", file.filename)

    def login_coach(self):
        """Redirige tras el login exitoso"""
        return rx.redirect("/mi-perfil")