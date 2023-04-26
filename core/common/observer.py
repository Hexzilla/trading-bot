from abc import abstractmethod


class Observer:
    @abstractmethod
    def update(self, data: any) -> None:
        pass
