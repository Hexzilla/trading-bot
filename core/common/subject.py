from core.common.observer import Observer


class Subject:
    _observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> None:
        self._observers.append(observer)
        print('>>>>>>>>>>>>>>>>>>>>>>>> Observer ' + observer.__str__())

    def unsubscribe(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def clear(self):
        self._observers.clear()

    def notify(self, data: any) -> None:
        for observer in self._observers:
            if observer != self:
                print('>>>>>>>>>>>>>>>>>>>>>>>> Notifying observer ' + observer.__str__())
                observer.update(data)
