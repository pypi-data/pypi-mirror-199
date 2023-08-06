
# allow_as_field decorator copies async methods essentially
# adding _allowed_as_field to their names. This protects models asynchronous
# methods from being accessed via api by their names listed in _fields
# param as only methods with _allowed_as_field suffix will be processed
class allow_as_field:
    def __init__(self, fn):
        self.fn = fn

    def __set_name__(self, owner, name):
        original_name = self.fn.__name__
        allowed_method_name = f"{self.fn.__name__}_allowed_as_field"
        setattr(owner, allowed_method_name, self.fn)
        setattr(owner, original_name, self.fn)
        return self.fn
