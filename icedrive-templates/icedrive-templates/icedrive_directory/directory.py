"""Module for servants implementations."""
"""Autor: Daniel Machuca Archidona"""

from typing import List
import os
import Ice
import IceDrive
import IceStorm



class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""
    
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""
        if self.parent:
            return IceDrive.DirectoryPrx.uncheckedCast(self.parent, category="directory")
        else:
            # Si el directorio actual no tiene un padre (nodo raíz), devolver None
            return None

    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""
        try:
            # Obtén la lista de archivos y subdirectorios usando el método existente
            all_files = self.getFiles()

            # Filtro por subdirectorios
            subdirectories = [d for d in all_files if os.path.isdir(os.path.join(os.getcwd(), d))]

            return subdirectories

        # control de  excepciones
        except Exception as e:
            print(f"Error al obtener la lista de subdirectorios: {e}")
            return []

    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""
        try:
            # Verifico el nombre
            if not name:
                raise ValueError("El nombre del directorio no puede estar vacío.")

            # cojo la ruta de hijo
            child_dir_path = os.path.join(os.getcwd(), name)

            # Verifico la existencia del hijo
            if not os.path.isdir(child_dir_path):
                raise FileNotFoundError(f"El directorio {name} no existe en el directorio actual.")

            # devuelvo el proxy del hijo
            child_directory_proxy = IceDrive.DirectoryPrx.uncheckedCast(current.adapter.createProxy(Ice.stringToIdentity(name)))

            return child_directory_proxy

        # control de excepciones valueError y filenotfounderror
        except ValueError as e:
            print(f"Error al obtener el directorio hijo {name}: {e}")
            return None
        except FileNotFoundError as e:
            print(f"Error al obtener el directorio hijo {name}: {e}")
            return None


    def createChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""
        new_child = Directory(name, parent=self)
        self.children.append(new_child)
        proxy = current.adapter.add(new_child, current.id)
        return IceDrive.DirectoryPrx.uncheckedCast(current.adapter.createProxy(Ice.stringToIdentity(name)))


    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""
        child_to_rem = None
        for child in self.children:
            if child.user == name:
                child_to_rem = child
                break

        if child_to_rem:
            self.children.remove(child_to_rem)
            # Elimina el directorio hijo del adaptador
            current.adapter.remove(current.id)
        else:
            raise ValueError(f"No se encontró un directorio hijo con el nombre dado: {name}.")

    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""
        #primera version
        directory = os.getcwd() #con la libreria os obtengo el current directory
        files = [] #creo una lista vacia llamada files
        #recorro los elementos del directorio con os.listdir, utilizo el os.path.join para obtener una ruta de cada elemento 'f' en el directorio y luego
        #compruebo si es un archivo con os.path.isfile, si es un archivo lo añado a la lista files
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        if not files:
            return []
        else:
            return files

    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""
        try:
            # Obtengo los archivos que me devuelve el metodo anterior
            files = self.getFiles()
            # Verifica si el archivo existe
            if filename not in files:
                raise FileNotFoundError(f"El archivo {filename} no existe en el directorio.")
            
            fPath = os.path.join(os.getcwd(), filename)
            # Genera un "blobId" simple utilizando el tamaño del archivo
            blobId = str(os.path.getsize(fPath))

            return blobId

        except FileNotFoundError as e:
            # control de la excepción y realizar acciones adecuadas, como registrar el error
            print(f"Error al obtener el Blob ID para {filename}: {e}")
            return ""

        #cointrol de mas excepciones
        except Exception as e:
            print(f"Error inesperado al obtener el Blob ID: {e}")
            return ""


    def linkFile(self, filename: str, blob_id: str, current: Ice.Current = None) -> None:
        """Link a file to a given blob_id."""
        try:
            # Obtén la ruta completa al nuevo archivo
            new_fPath = os.path.join(os.getcwd(), filename)

            # Crea el nuevo archivo y escribe el blobId en él
            with open(new_fPath, 'w') as file:
                file.write(blob_id)
                
        # control de  excepciones al escribir
        except Exception as e:
            print(f"Error al vincular el archivo {filename} con Blob ID {blob_id}: {e}")

    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""
        try:
            fPath = os.path.join(os.getcwd(), filename)

            # Verifico si el archivo existe antes de eliminarlo
            if os.path.exists(fPath):
                os.remove(fPath)
                print(f"El archivo {filename} ha sido eliminado.")
            else:
                print(f"El archivo {filename} no existe en el directorio.")
        
        except FileNotFoundError as e:
            # control de la excepción y realizar acciones adecuadas, como registrar el error
            print(f"Error al obtener el archivo para {filename}: {e}")
        # control de  excepciones a la hora de eliminar
        except Exception as e:
            print(f"Error al eliminar el archivo {filename}: {e}")

    def listChildren(self, current: Ice.Current = None) -> List[IceDrive.EntryPrx]:
        children_prx = []
        for child in self.children:
            children_prx.append(IceDrive.EntryPrx.uncheckedCast(child, category="directory"))
        return children_prx

"""----------------------------------------------------------------------------------------------------------------------"""

class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""
    def __init__(self):
        # Utiliza un diccionario para almacenar los directorios raíz de los usuarios
        self.root_directory = {}

    def getRoot(self, user: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""
     
        if user in self.root_directory:# Verificar si el usuario ya ha solicitado el directorio root
            return self.root_directory[user] #lo ha solicitado anteriormente, entonces devuelvo el root
        else: 
            #controlo que el nombre no este repetido
            if self.usuarioRepetido(user):
                raise ValueError(f"El usuario {user} ya existe.")
            #y ya creo los directorios
            new_root_directory = self.createRootDirectory(user)
            self.root_directory[user] = new_root_directory
            return new_root_directory

    def usuarioRepetido(self, user: str) -> bool:
        """Comprueba si el usuario ya existe"""
        return user in self.root_directory
       
    def createRootDirectory(self, user: str) -> IceDrive.DirectoryPrx:
        """Create and return a new root directory for the given user."""
        new_directory = IceDrive.DirectoryPrx.uncheckedCast(self.ice_addWithUUID(Directory()))
        return new_directory