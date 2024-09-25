from cx_Freeze import setup, Executable

setup(
    name="Sistema de Gestion de Empleados",
    version="1.0",
    description="Sistema para gestionar empleados, sueldos, y búsqueda de perfiles.",
    executables=[Executable("Empleados.py")]
)
