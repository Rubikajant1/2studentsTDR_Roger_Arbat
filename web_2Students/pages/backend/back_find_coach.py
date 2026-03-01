import reflex as rx
from web_2Students.db.db_client import db_coaches


class Find(rx.State):
    # Definimos la lista que almacenará los datos
    coaches_list: list[dict] = []

    
    #Load inicial que es crida al add_page()
    def load_alumnes(self):
        #Convertir ObjectId a string per la compatibilitat
        #Només dels alumnes de 2n d'ESO
        raw_alumnes = [
            {**coach, '_id': str(coach['_id'])}
            for coach in db_coaches
        ]
        
        #Crear variables de la llista a string i deixar la normal per que sigui compatible
        #Per a la llista on es veuen les hores que s'han posat els retards ha de ser un str si no no és compatible
        self.alumnes = [
            {
                **alumno,
                "retards_list": str(alumno.get('Llista de retards', [])),
                "Llista de retards": alumno.get('Llista de retards', []),
                "faltesnj_list": str(alumno.get('Llista de faltes no justificades', [])),
                "Llista de faltes no justificades": alumno.get('Llista de faltes no justificades', []),
                "faltesj_list": str(alumno.get('Llista de faltes justificades', [])),
                "Llista de faltes justificades": alumno.get('Llista de faltes justificades', []), 
            }
            # Cicle for per a cada alumne de la variable row alumnes creada anteriorment
            for alumno in raw_alumnes
        ]
    
    @rx.event()
    def get_coaches(self):
        print(db_coaches)
            
        