from os.path import join

from cfinterface.data.registerdata import RegisterData
from cfinterface.adapters.writing.repository import (
    Repository,
    factory,
)


class RegisterWriting:
    """
    Class for writing custom files based on a RegisterData structure.
    """

    def __init__(self, data: RegisterData, storage: str = "") -> None:
        self.__data = data
        self.__storage = storage
        self.__repository: Repository = None  # type: ignore

    def __write_file(self):
        """
        Writes all the registers from the given RegisterData structure
        to the specified file.

        """
        for r in self.__data:
            r.write(self.__repository.file, self.__storage)

    def write(self, filename: str, directory: str, encoding: str):
        """
        Writes a file with a given name in a given directory with
        the data from the RegisterData structure.

        :param filename: The name of the file
        :type filename: str
        :param directory: The directory where the file will be
        :type directory: str
        :param encoding: The encoding for reading the file
        :type encoding: str
        """
        filepath = join(directory, filename)
        self.__repository = factory(self.__storage)(filepath, encoding)
        with self.__repository:
            return self.__write_file()

    @property
    def data(self) -> RegisterData:
        return self.__data
