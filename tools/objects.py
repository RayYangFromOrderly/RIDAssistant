class Tool:
    def __init__(self, assistant):
        self.assistant = assistant

    def get_name(self):
        return self.__class__.__name__

    def setup(self):
        pass

    def get_root_folder(self):
        return "/" + self.get_name()

class ToolManager:
    pass
