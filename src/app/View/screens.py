# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.

# TODO: Do it better..

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Type, TypedDict  # noqa: UP035

    class ScreenParams(TypedDict):
        model: Type[MainScreenModel]
        controller: Type[MainScreenController]

from app.Model.main_screen import MainScreenModel  # noqa: I001
from app.Controller.main_screen import MainScreenController

from app.Model.settings_screen import MainScreenModel as SettingsScreenModel
from app.Controller.settings_screen import MainScreenController as SettingsScreenController

screens: Dict[str, ScreenParams] = {  # noqa: UP006
    'main_screen': {
        'model': MainScreenModel,
        'controller': MainScreenController,
    },
    'settings_screen': {
        'model': SettingsScreenModel,
        'controller': SettingsScreenController,
    },
}
