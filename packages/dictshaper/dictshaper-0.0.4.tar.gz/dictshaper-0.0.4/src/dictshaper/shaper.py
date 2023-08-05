class DictShaper(dict):
    """
    This class is for shaping of dictionary in string format
    and writing it to any file (optional) with or without a name.
    It shapes a normal one-row dictionary to a convenient entry with
    the all necessary indents.
    As all the objects of this class are inherit a standard dict class,
    they have all the methods and properties of it.
    """

    @staticmethod
    def __quotes(el):
        """Takes a dictionary key or value and adds quotes if the element type is string"""
        return f"'{el}'" if isinstance(el, str) else el

    @staticmethod
    def __name_check(name):
        """Checks if a dictionary name is correct"""

        # Allowed symbols for the dictionary name
        allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'

        # Raises an error if the name type is not string
        if not isinstance(name, str):
            raise TypeError('Name must be string')

        def good_first(n): return n[0] in allowed[:-10]  # Checker for the first character
        def allow(n): return all(map(lambda x: x in allowed, n))  # Checker for the all other characters

        # Raises an error if the first character and subsequent characters are incorrect
        if not (good_first(name) and allow(name)):
            raise ValueError("The name must meet the requirements of variable's name")

        return True

    def __shaper(self, dictionary, start='', deep=1):
        """
        The main recursive method which goes through the dictionary
        and shapes its string view.
        """
        indent = '    ' * deep  # An indent from start of a row to an element of the dictionary
        start += '{\n' + indent  # The current formed part of the dictionary in the string view

        # The loop for iteration of the dictionary
        for k, v in dictionary.items():
            k, v = self.__quotes(k), self.__quotes(v)  # Add quotes if necessary
            v_dict = isinstance(v, dict)  # Check if the value is a dictionary (True/False)

            # Just join a key-value pair to the 'start' in the string format
            # if the value isn't the dictionary type or empty dictionary
            if not v_dict or (v_dict and not v):
                start += f'{k}: {v},\n{indent}'
            # Else send the dictionary from the value to the recurse
            else:
                start += self.__shaper(v, start=f'{k}: ', deep=deep + 1)

        return start[:-4] + '},\n' + indent[:-4]

    def shape(self, *, name='', write_to=None):
        """The callable method which is called from a dictionary object for shaping"""

        # Add the name if the correspondent param is not empty
        if name:
            self.__name_check(name)
            name = f'{name} = '

        result = name + self.__shaper(self)[:-2]  # A concatenating the name and the string dictionary

        # If the 'write_to' param is not empty
        if write_to:
            # If the 'write_to' param has '1' or 'True' value
            if write_to == 1:
                import inspect
                write_to = inspect.stack()[1].filename  # Gets a path of a current file

            # Else writes the result to the end of the file by the path from the 'write_to' param
            with open(write_to, 'a', encoding='utf-8') as file:
                file.write(f'\n{result}\n')

        return result
