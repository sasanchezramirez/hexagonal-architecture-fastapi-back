import os
from types import ModuleType
from typing import Iterator, Final, List, Set


class Handlers:
    """
    Clase responsable de cargar y gestionar los handlers de la aplicación.
    
    Esta clase implementa un cargador dinámico de handlers que se encuentran
    en el directorio de entry points.
    """
    
    HANDLERS_BASE_PATH: Final[tuple] = ('app', 'infrastructure', 'entry_point', 'handler')
    IGNORED_FILES: Final[Set[str]] = {'__init__.py', '__pycache__'}

    @classmethod
    def _get_all_module_names(cls) -> List[str]:
        """
        Obtiene la lista de nombres de módulos de handlers disponibles.
        
        Returns:
            List[str]: Lista de nombres de módulos
        """
        return [
            module for module in os.listdir('/'.join(cls.HANDLERS_BASE_PATH))
            if module not in cls.IGNORED_FILES
        ]
    
    @classmethod
    def _get_module_namespace(cls, handler_name: str) -> str:
        """
        Construye el namespace completo para un módulo handler.
        
        Args:
            handler_name: Nombre del archivo handler
            
        Returns:
            str: Namespace completo del módulo
        """
        return '.'.join([*cls.HANDLERS_BASE_PATH, handler_name[:-3]])
    
    @classmethod
    def iterator(cls) -> Iterator[ModuleType]:
        """
        Itera sobre todos los módulos de handlers disponibles.
        
        Returns:
            Iterator[ModuleType]: Iterador de módulos de handlers
        """
        import importlib
        
        for module in cls._get_all_module_names():
            handler = importlib.import_module(cls._get_module_namespace(module))
            yield handler
    
    @classmethod
    def get_module_namespaces(cls) -> Iterator[str]:
        """
        Obtiene los namespaces de todos los módulos de handlers.
        
        Returns:
            Iterator[str]: Iterador de namespaces de módulos
        """
        return (
            cls._get_module_namespace(module)
            for module in cls._get_all_module_names()
        )
