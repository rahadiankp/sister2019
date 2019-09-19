import os
from random import randint


class FileManager(object):
    DIRECTORY_PATH = "D:\\sample_files\\"

    def __init__(self):
        pass

    def get_cwd(self) -> str:
        return FileManager.DIRECTORY_PATH

    def get_listdir(self) -> list:
        file_list = []
        for filename in os.listdir(FileManager.DIRECTORY_PATH):
            file_list.append((filename, os.path.getsize(FileManager.DIRECTORY_PATH + filename)))
        return file_list

    def delete_file(self, filename: str) -> (bool, str):
        deleted = False
        try:
            os.remove(FileManager.DIRECTORY_PATH+filename)
            deleted = not deleted
            message = "File " + filename + " successfully deleted"
        except FileNotFoundError:
            message = "Could not find file with name " + filename

        return deleted, message

    def create_file(self, filename: str) -> (bool, str):
        if os.path.isfile(FileManager.DIRECTORY_PATH+filename):
            return False, "File " + filename + " already exists"
        new_file = open(FileManager.DIRECTORY_PATH+filename, "w")
        new_file.close()
        return True, "File " + filename + " successfully created"

    def read_file(self, filename: str) -> (bool, str, int, bytes):
        try:
            size = 0
            content = b""
            with open(FileManager.DIRECTORY_PATH+filename, "rb") as fd:
                buffer = fd.read(1024)
                while buffer != b"":
                    size += len(buffer)
                    content = content + buffer
                    buffer = fd.read(1024)
            return True, FileManager.DIRECTORY_PATH+filename + " OK", size, content
        except FileNotFoundError:
            return False, "File " + filename + " could not be found", -1, b""

    # will overwrite instead of append
    def update_file(self, filename: str, content: str, size: int) -> (bool, str, int):
        try:
            # pseudo-COW
            temp_filename = ".tempfile-"+str(randint(420, 42069))
            with open(FileManager.DIRECTORY_PATH+temp_filename, "wb") as temp_fd:
                write_size = temp_fd.write(content.encode())
            # check if write size doesn't match
            if write_size != size:
                return False, "Error on writing", -1
            # delete original file
            self.delete_file(filename)
            # rename tempfile to filename
            os.rename(FileManager.DIRECTORY_PATH+temp_filename, FileManager.DIRECTORY_PATH+filename)
            return True, "File " + filename + " updated", write_size
        except FileNotFoundError:
            return False, "File " + filename + " could not be found", -1
