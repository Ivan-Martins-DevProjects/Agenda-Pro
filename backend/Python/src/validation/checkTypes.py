# Validação para tipo string
def isStr(value) -> bool:
    if isinstance(value, str):
        return True
    else:
        return False

# Validação para tipo int
def isInt(value) -> bool:
    if isinstance(value, int):
        return True
    else:
        return False

# Validação para tipo boolean
def isBool(value) -> bool:
    if isinstance(value, bool):
        return True
    else:
        return False
