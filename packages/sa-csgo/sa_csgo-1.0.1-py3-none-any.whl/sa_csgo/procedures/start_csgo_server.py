import typer
from sa_csgo.addons.gui import Procedure
from rich.prompt import Prompt
from sa_csgo.utils.os_commands import startCSGOServer, verifyCSGOServerInstallation


class CustomProcedure(Procedure):
    id=4
    name= "Start [orange4]CS:GO[/orange4] Server"
    description = ""

    def run():
        if not verifyCSGOServerInstallation():
            print('CSGO is not installed, please install it first.')
            return
        
        port = Prompt.ask('Server port (default: 27015)')
        wan = typer.confirm('Make server available through the internet (default: no)')
        token= None
        if wan:
            token = Prompt.ask('GSLT Token (required)')

        process = startCSGOServer(port,wan,token)
        print('CS:GO Server started.. Please visit console to see updates.')

        pass