"""Module for servants implementations."""
"""Autor: Daniel Machuca Archidona"""

from typing import List

import Ice

import IceDrive
import IceStorm



class Directory(IceDrive.Directory):
    """Implementation of the IceDrive.Directory interface."""

    def getParent(self, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to the parent directory, if it exists. None in other case."""

    def getChilds(self, current: Ice.Current = None) -> List[str]:
        """Return a list of names of the directories contained in the directory."""

    def getChild(self, name: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy to one specific directory inside the current one."""

    def createChild(
        self, name: str, current: Ice.Current = None
    ) -> IceDrive.DirectoryPrx:
        """Create a new child directory and returns its proxy."""

    def removeChild(self, name: str, current: Ice.Current = None) -> None:
        """Remove the child directory with the given name if exists."""

    def getFiles(self, current: Ice.Current = None) -> List[str]:
        """Return a list of the files linked inside the current directory."""

    def getBlobId(self, filename: str, current: Ice.Current = None) -> str:
        """Return the "blob id" for a given file name inside the directory."""

    def linkFile(
        self, filename: str, blob_id: str, current: Ice.Current = None
    ) -> None:
        """Link a file to a given blob_id."""

    def unlinkFile(self, filename: str, current: Ice.Current = None) -> None:
        """Unlink (remove) a filename from the current directory."""


class DirectoryService(IceDrive.DirectoryService):
    """Implementation of the IceDrive.Directory interface."""

    def getRoot(self, user: str, current: Ice.Current = None) -> IceDrive.DirectoryPrx:
        """Return the proxy for the root directory of the given user."""
        root_directories = []
        
        if user in self.root_directories:# Verificar si el usuario ya ha solicitado el directorio raíz anteriormente.
            # Caso 2: El usuario ya solicitó el directorio raíz anteriormente.
            return self.root_directories[user]
        else:
            # Caso 1: El usuario nunca ha solicitado el directorio raíz.
            new_root_directory = self.createRootDirectory(user)
            self.root_directories[user] = new_root_directory
            return new_root_directory

    def createRootDirectory(self, user: str) -> IceDrive.DirectoryPrx:
        """Create and return a new root directory for the given user."""
        new_directory = IceDrive.DirectoryPrx.uncheckedCast(self.ice_addWithUUID(Directory()))
        return new_directory