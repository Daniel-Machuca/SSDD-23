''' Esta clase se utilizar como cliente para la realizacion de pruebas en local para el servicio.'''

import Ice 
import IceDrive 
import sys


class ClientApp(Ice.Application):

    def run(self, args):
        """Code to be run by the application."""
        proxy = self.communicator().stringToProxy(args[1])
        directory_proxy = IceDrive.DirectoryPrx.checkedCast(proxy)

        if not directory_proxy:
            print('el proxy no es valido')
            sys.exit(1)


        

        return 0 

def main():

    app= ClientApp()
    app.main(sys.argv)