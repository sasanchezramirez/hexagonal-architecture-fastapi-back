import os
from types import ModuleType
from typing import Iterator, Final, List, Set


class Handlers:
    """
    Class responsible for loading and managing application handlers.
    
    This class implements a dynamic handler loader that finds handlers
    in the entry point directory.
    """
    
    HANDLERS_BASE_PATH: Final[tuple] = ('app', 'infrastructure', 'entry_point', 'controller')
    IGNORED_FILES: Final[Set[str]] = {'__init__.py', '__pycache__'}

    @classmethod
    def _get_all_module_names(cls) -> List[str]:
        """
        Gets the list of available handler module names.
        
        Returns:
            List[str]: List of module names
        """
        return [
            module for module in os.listdir('/'.join(cls.HANDLERS_BASE_PATH))
            if module not in cls.IGNORED_FILES
        ]
    
    @classmethod
    def _get_module_namespace(cls, handler_name: str) -> str:
        """
        Builds the full namespace for a handler module.
        
        Args:
            handler_name: Handler file name
            
        Returns:
            str: Full module namespace
        """
        return '.'.join([*cls.HANDLERS_BASE_PATH, handler_name[:-3]])
    
    @classmethod
    def iterator(cls) -> Iterator[ModuleType]:
        """
        Iterates over all available handler modules.
        
        Returns:
            Iterator[ModuleType]: Iterator of handler modules
        """
        import importlib
        
        for module in cls._get_all_module_names():
            handler = importlib.import_module(cls._get_module_namespace(module))
            yield handler
    
    @classmethod
    def get_module_namespaces(cls) -> Iterator[str]:
        """
        Gets the namespaces of all handler modules.
        
        Returns:
            Iterator[str]: Iterator of module namespaces
        """
        return (
            cls._get_module_namespace(module)
            for module in cls._get_all_module_names()
        )
