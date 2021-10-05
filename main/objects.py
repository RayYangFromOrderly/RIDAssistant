from settings.objects import AssistantSettings, StylePreferences


class Assistant:
    def __init__(self):
        self.tools = []
        self.load_tasks = None
        self.settings = AssistantSettings()
        self.tabs = []
        self.style_preferences = StylePreferences()

    def add_tab(self, panel):
        self.tabs.append(panel)
