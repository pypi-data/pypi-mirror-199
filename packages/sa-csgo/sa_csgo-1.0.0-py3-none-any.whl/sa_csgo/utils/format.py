from rich import print
from rich.panel import Panel
from rich.align import Align
from rich import box

def printLogo(): 
    title = ("[bold blue]\n" +
    "███████╗ █████╗        ██████╗███████╗    ██████╗  ██████╗\n" +
    "██╔════╝ ██╔══██╗      ██╔════╝██╔════╝██╗██╔════╝ ██╔═══██╗\n" +
    "███████╗•███████║█████╗██║     ███████╗╚═╝██║  ███╗██║   ██║\n" +
    "╚════██║ ██╔══██║╚════╝██║     ╚════██║██╗██║   ██║██║   ██║\n" +
    "███████║ ██║  ██║      ╚██████╗███████║╚═╝╚██████╔╝╚██████╔╝\n" +
    "╚══════╝ ╚═╝  ╚═╝ [bold white]v1.00 [/bold white]╚═════╝╚══════╝    ╚═════╝  ╚═════╝ \n")
    print(Panel(Align(title,align='center'), title="[bold white][MIT Licensed] by STORM Systems    ||   <info@stormsys.io>", title_align='center', box=box.SIMPLE_HEAVY))