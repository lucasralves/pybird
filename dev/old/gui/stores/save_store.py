from pybird.geometry.geometry import Geometry
from pybird.gui.components.save_dialog_component import SaveDialogComponent

class SaveStore:

    def __init__(self, geo: Geometry) -> None:
        self.geo = geo

        self.filename = self.geo.filename
        return
    
    def saveFilename(self, value: str) -> None:
        self.filename = value
        return
    
    def save(self) -> None:
        if '.geo' in self.filename: self.geo.save(self.filename)
        return
    
    def file(self) -> None:
        dialog = SaveDialogComponent(
            saveFilename=self.saveFilename,
            save=self.save,
            initialValue=self.filename,
        )
        dialog.exec()
        return