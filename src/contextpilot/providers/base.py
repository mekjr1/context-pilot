class Provider:
    def complete(self, model, messages, **kwargs):
        raise NotImplementedError

    def stream(self, model, messages, **kwargs):
        raise NotImplementedError
