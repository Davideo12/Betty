from rich.console import Console
from rich.theme import Theme
from rich.table import Table
import config.config as config
import rich.box as box
from datetime import datetime
from pyfiglet import Figlet

class LogerFucker:
    _instance = None
    debug_enabled = config.DEBUG  # Variable de clase para activar/desactivar debug

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Configuración inicial de rich."""
        custom_theme = Theme({
            "success": "bold green",
            "error": "bold red",
            "info": "bold cyan",
            "warning": "bold yellow",
            "debug": "dim white"
        })
        self.console = Console(theme=custom_theme)

    @classmethod
    def set_debug(cls, value: bool):
        """Permite activar o desactivar debug desde cualquier parte."""
        cls.debug_enabled = value

    def print_banner(self):
        f = Figlet(font="slant")
        print("\n")
        self.console.print(f'[bold cyan]{f.renderText("Betty")}')
        self.console.print(f'[italic magenta] Version: 1.0\n')

    # --- Métodos de logging ---
    def _log_format(self, state:str, message:str, style:str):
        """ Formato general del texto que se imprime """
        self.console.print(f": [dim white]{datetime.now()}[/dim white] | [{style}]{state}[/{style}] | {message}", )

    def success(self, message: str):
        #self.console.print(f":[SUCCESS] [ {message} ]", style="success")
        self._log_format(state="SUCCESS", message=message, style="success")

    def info(self, message: str):
        #self.console.print(f":[INFO] [ {message} ]", style="info")
        self._log_format(state="INFO", message=message, style="info")

    def warning(self, message: str):
        #self.console.print(f":[WARNING] [ {message} ]", style="warning")
        self._log_format(state="WARNING", message=message, style="warning")

    def error(self, message: str):
        #self.console.print(f":[ERROR] [ {message} ]", style="error")
        self._log_format(state="ERROR", message=message, style="error")

    def debug(self, message: str):
        """Solo imprime si debug_enabled es True"""
        if self.debug_enabled:
            #self.console.print(f":[DEBUG] [ {message} ]", style="debug")
            self._log_format(state="DEBUG", message=message, style="debug")

    def json(self, json_data: dict):
        """Imprime un JSON formateado"""
        #self.console.print(":[JSON] ->")
        self._log_format(state="JSON", message=":", style="info")
        self.console.print_json(data=json_data)

    def table(self, data: dict, title: str = "Tabla de datos"):
        """Imprime un diccionario como tabla usando rich"""
        table = Table(
            title=title, 
            show_header=True, 
            header_style="bold white", 
            expand=False, 
            box=box.MARKDOWN, 
            title_style="bold yellow"
        )

        table.add_column("Clave", style="bold blue", justify="left")
        table.add_column("Valor", style="cyan", justify="left")

        for key, value in data.items():
            table.add_row(str(key), str(value))

        self.console.print(table)

    def separator(self, char: str = "─", style: str = "dim"):
        """Imprime una línea separadora del ancho actual de la ventana."""
        width = self.console.size.width
        line = char * width
        self.console.print(line, style=style)
