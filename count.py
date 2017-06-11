class Count:
    """A simple class that acts as a counter which is incremented upon usage."""
    def __init__(self, begin = 1):
        self.count = begin

    def use(self):
        old = self.count
        self.count += 1
        return old
