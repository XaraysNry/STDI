class VectorClock:
    def __init__(self, num_processes, process_id):
        self.clocks = [0] * num_processes
        self.process_id = process_id

    def increment(self):
        self.clocks[self.process_id] += 1

    def send_message(self):
        self.increment()
        return list(self.clocks)

    def receive_message(self, received_clocks):
        for i in range(len(self.clocks)):
            self.clocks[i] = max(self.clocks[i], received_clocks[i])
        self.increment()

    def happens_before(self, other):
        if self.clocks == other.clocks:
            return False

        any_lt = False
        for i in range(len(self.clocks)):
            if self.clocks[i] > other.clocks[i]:
                return False
            if self.clocks[i] < other.clocks[i]:
                any_lt = True

        return any_lt

    def is_concurrent(self, other):
        return not (self.happens_before(other) or other.happens_before(self))

    def __str__(self):
        return f"P{self.process_id}: {self.clocks}"