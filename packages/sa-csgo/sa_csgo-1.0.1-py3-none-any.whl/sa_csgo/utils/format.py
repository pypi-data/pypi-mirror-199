import importlib.metadata
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich import box

def version():
    return importlib.metadata.version('sa-csgo')

def printLogo(): 
    title = ("[bold blue]\n" +
    f"███████╗ █████╗ [bold blue]<{version()}>[/bold blue] ██████╗███████╗    ██████╗  ██████╗\n" +
    "██╔════╝ ██╔══██╗      ██╔════╝██╔════╝██╗██╔════╝ ██╔═══██╗\n" +
    "███████╗•███████║█████╗██║     ███████╗╚═╝██║  ███╗██║   ██║\n" +
    "╚════██║ ██╔══██║╚════╝██║     ╚════██║██╗██║   ██║██║   ██║\n" +
    "███████║ ██║  ██║      ╚██████╗███████║╚═╝╚██████╔╝╚██████╔╝\n" +
    "╚══════╝ ╚═╝  ╚═╝       ╚═════╝╚══════╝    ╚═════╝  ╚═════╝ \n")
    print(Panel(Align(title,align='center'), title="[bold white][MIT Licensed] by STORM Systems    ||   <info@stormsys.io>", title_align='center', box=box.SIMPLE_HEAVY))