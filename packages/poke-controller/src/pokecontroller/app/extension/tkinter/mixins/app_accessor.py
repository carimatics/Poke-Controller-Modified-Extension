class AppAccessor:
    @property
    def app(self):
        return self.winfo_toplevel()

    @property
    def app_info(self):
        return self.app.app_info

    @property
    def app_model(self):
        return self.app.app_model

    @property
    def app_state(self):
        return self.app.app_state
