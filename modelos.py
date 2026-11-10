# -*- coding: utf-8 -*-
# Archivo: modelos.py unificado (Aporte colaborativo)

from abc import ABC, abstractmethod
import re
from excepciones import ClienteInvalidoError, ReservaError
from logger import registrar_log


class EntidadBase(ABC):
    """Clase abstracta base general del sistema."""
    _contador = 0

    def __init__(self):
        EntidadBase._contador += 1
        self._id = EntidadBase._contador

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe devolver una descripción en texto."""
        pass


class Servicio(ABC):
    """Clase abstracta para los servicios de Software FJ."""
    def __init__(self, nombre: str, precio_base: float):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, duracion: int) -> float:
        pass


# --- 3 Servicios Especializados (Polimorfismo) ---
class ReservaSala(Servicio):
    def calcular_costo(self, duracion: int) -> float:
        return self.precio_base * duracion

    def describir(self):
        return f"Reserva de Sala: {self.nombre} (Base: ${self.precio_base})"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion: int) -> float:
        # Incluye cargo fijo por seguro del equipo
        return (self.precio_base * duracion) + 15000.0

    def describir(self):
        return f"Alquiler de Equipo: {self.nombre} con seguro"


class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion: int) -> float:
        # Descuento del 10% a partir de 5 horas
        costo = self.precio_base * duracion
        if duracion >= 5:
            costo *= 0.90
        return costo

    def describir(self):
        return f"Asesoría Especializada: {self.nombre}"


class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, correo=None, telefono=None):
        super().__init__()
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ClienteInvalidoError("El nombre debe tener al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if valor and (not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", valor)):
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'.")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor and (not isinstance(valor, str) or not valor.isdigit() or not (7 <= len(valor) <= 10)):
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos.")
        self._telefono = valor

    def describir(self):
        return f"Cliente #{self.id} (ID: {self.id_cliente}): {self._nombre}"


class Reserva:
    def __init__(self, cliente: Cliente, servicio: Servicio, duracion: int):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

    def procesar_reserva(self):
        try:
            if self.duracion <= 0:
                raise ValueError("La duración debe ser mayor a 0 horas.")
            costo = self.servicio.calcular_costo(self.duracion)
        except ValueError as e:
            registrar_log(f"Error de validación en reserva: {e}", nivel="error")
            raise ReservaError("No se pudo procesar la reserva por parámetros inválidos.") from e
        else:
            registrar_log(f"Reserva procesada para {self.cliente.nombre}. Costo: ${costo:.2f}")
            return costo
        finally:
            registrar_log("Intento de procesamiento de reserva finalizado.")
