from kivymd.app import MDApp

from app.bases.base import AppBase
from app.bases.meta import NoInheritMeta


class AppBaseABCLike(AppBase, metaclass=NoInheritMeta):
	...


class MDAppABCLike(MDApp, metaclass=NoInheritMeta):
	...
