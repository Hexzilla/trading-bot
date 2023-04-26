from abc import ABC

from core.common.observer import Observer
from core.common.subject import Subject


class Algo(Subject, Observer, ABC):
    pass
