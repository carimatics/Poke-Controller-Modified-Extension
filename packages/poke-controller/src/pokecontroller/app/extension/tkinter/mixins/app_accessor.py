from ..app import PokeControllerExtensionApp as App
from ..info import PokeControllerAppInfo as Info
from ..model import PokeControllerAppModel as Model
from ..state import PokeControllerAppState as State


class AppAccessor:
    @property
    def app(self) -> App:
        return self.winfo_toplevel()

    @property
    def app_info(self) -> Info:
        return self.app.app_info

    @property
    def app_model(self) -> Model:
        return self.app.app_model

    @property
    def app_state(self) -> State:
        return self.app.app_state
