from utils.tabs_management import tabManager


class MainScreen(tabManager.TabmanagerScreen):
    def __init__(self):
        tabManager.TabmanagerScreen.__init__(self, file_path='modules\development\screens.yaml')