from objectron import Objectron
from objectron_decorators.decorators import proxy_class

custom_objectron = Objectron()


@proxy_class(objectron=custom_objectron)
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

    def reset(self):
        self.count = 0


counter = Counter()
print(counter.increment())  # 1
print(counter.increment())  # 2
counter.reset()
