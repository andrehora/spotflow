def metrics(method):
    return \
        ('method_name', method.full_name), \
        ('calls', len(method.calls)), \
        ('exceptions', len(method.exception_states()))