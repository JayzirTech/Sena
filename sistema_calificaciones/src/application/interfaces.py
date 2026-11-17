"""
Capa de Aplicación: Contratos (Puertos) de Repositorios.
Define las interfaces abstractas que la capa de infraestructura debe cumplir.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import Estudiante, Calificacion


class EstudianteRepositoryInterface(ABC):

    @abstractmethod
    def obtener_todos(self) -> List[Estudiante]:
        pass

    @abstractmethod
    def obtener_activos(self) -> List[Estudiante]:
        pass

    @abstractmethod
    def buscar_por_id(self, id_estudiante: str, solo_activos: bool = True) -> Optional[Estudiante]:
        pass

    @abstractmethod
    def buscar_por_documento(self, documento: str, solo_activos: bool = False) -> Optional[Estudiante]:
        pass

    @abstractmethod
    def guardar(self, estudiante: Estudiante) -> None:
        pass

    @abstractmethod
    def desactivar(self, id_estudiante: str) -> bool:
        """Aplica borrado lógico (estado = INACTIVO)."""
        pass


class CalificacionRepositoryInterface(ABC):

    @abstractmethod
    def obtener_todas(self) -> List[Calificacion]:
        pass

    @abstractmethod
    def obtener_por_estudiante(self, id_estudiante: str) -> List[Calificacion]:
        pass

    @abstractmethod
    def obtener_por_materia(self, id_materia: str) -> List[Calificacion]:
        pass

    @abstractmethod
    def guardar(self, calificacion: Calificacion) -> None:
        pass

    @abstractmethod
    def actualizar(self, calificacion: Calificacion) -> bool:
        pass

    @abstractmethod
    def eliminar(self, id_calificacion: int) -> bool:
        pass

    @abstractmethod
    def obtener_siguiente_id(self) -> int:
        pass
