"""Task 1: deterministic candidate problems, with a small public API."""
from .catalog import ProblemFamily, get_family, load_families
from .generator import generate, generate_histories, replace_collision

__all__ = ['ProblemFamily', 'get_family', 'load_families', 'generate',
           'generate_histories', 'replace_collision']
