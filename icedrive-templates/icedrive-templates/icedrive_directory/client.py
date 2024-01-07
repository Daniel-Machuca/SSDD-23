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

        while True: 
            print("Option menu:")
            option = input("1. getFiles \n2. getBlobId \n 3. linkFile \n4. unlinkFile \n5. getChilds  \n6.getChild \ n7. createChild \n8. removeChild \n9. getParent \n10. Exit\n")
            if option == 1:
                files_list = directory_proxy.getFiles()
            elif option == 2:
                blob_name = input("Ingrese el nombre del blob: ")
                directory_proxy.getBlobId(blob_name)
            elif option == 3:
                files_link = input("Ingrese el nombre del blob a linkear: ")
                files_id = input("Ingrese el id del blob a linkear: ")
                directory_proxy.linkFile(files_link, files_id)
        

        return 0 

def main():

    app= ClientApp()
    app.main(sys.argv)