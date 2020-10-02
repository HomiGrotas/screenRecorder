from configparser import ConfigParser


class Settings:
    """
    reads settings ini file
    """
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read(r"settings\\settings.ini")

    def get_setting_value(self, title, setting):
        """
        returns value by title and setting name
        :param title: str (section)
        :param setting: setting key
        :return: setting value
        """
        return self.parser.get(title, setting)

    def set_setting(self, title, setting):
        """
        sets setting value
        :param title: str (section)
        :param setting: setting key
        """
        self.parser.set(title, setting)
