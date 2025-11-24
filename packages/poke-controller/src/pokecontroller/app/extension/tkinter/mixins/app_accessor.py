from ..app import PokeControllerExtensionApp as App
from ..info import PokeControllerAppInfo as AppInfo
from ..model import PokeControllerAppModel as AppModel
from ..state import PokeControllerAppState as AppState


class AppAccessor:
    @property
    def app(self) -> App:
        return self.winfo_toplevel()

    @property
    def app_info(self) -> AppInfo:
        return self.app.app_info

    @property
    def app_model(self) -> AppModel:
        return self.app.app_model

    @property
    def app_state(self) -> AppState:
        return self.app.app_state
