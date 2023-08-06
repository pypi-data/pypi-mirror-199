def modifier_factory(*modifiers):
    """
    return a subclass of EngineTypeModifier
    @param modifiers (list of str):
    """
    if len(modifiers) != 1:
        raise NotImplementedError("Current supports a single engine type modifier")
