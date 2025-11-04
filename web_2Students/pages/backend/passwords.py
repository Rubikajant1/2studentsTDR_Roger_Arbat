import reflex as rx
import secrets
from typing import Optional
import hashlib


class Passwords(rx.State):
    # Constantes de configuración
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