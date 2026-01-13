import ast
from utils.logger import Logger


def read_dict_from_text_file(file_location):
    """
    Read dictionary from text file.

    .. function:: read_dict_from_text_file
        :param file_location: source file absloute path
        :type file_location: string

    Returns:
        :param dict_data: dictonary data
        :type dict_data: dict

    Examples:

        >>> textfile_utils.read_dict_from_text_file(file_location)

    |
    |
    """
    Logger.checkpoint(f"Read dictionary from text file {file_location}")
    src_file = open(file_location, "r")
    contents = src_file.read()
    dictionary = ast.literal_eval(contents)
    src_file.close()
    return dictionary


def save_dict_to_text_file(file_location, dict_data):
    """
    Save dictionary data to text file.

    .. function:: save_dict_to_text_file
        :param file_location: source file absloute path
        :type file_location: string
        :param dict_data: dictonary data
        :type dict_data: dict

    Returns:
        None

    Examples:
        >>> textfile_utils.save_dict_to_text_file(file_location, dict_data)

    |
    |
    """
    Logger.checkpoint(
        f"Save dictionary {dict_data} to text file {file_location}")
    f = open(file_location, "w")
    f.write(str(dict_data) + "\n")
    f.close()