import re

# Validação para nomes em geral
def isName(value: str) -> bool:
    # Verifica se é um valor do tipo string
    if not isinstance(value, str):
        return False

    # Elimina espaços adjascentes nas extremidades
    name = value.strip()

    # Divide o nome entre espaços e verifica se tem no mínimo 2 elementos, exemplo: "Ana Maria"
    parts = name.split()
    if len(parts) < 2:
        return False

    # Só letras Unicode e Espaços
    if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ\s]+", value):
        return False

    # Cada elemento do nome deve ter ao menos 2 letras
    if any(len(p) < 2 for p in parts):
        return False

    # O nome não deve estar completamente em caixa alta ou baixa
    if value.islower() or value.isupper():
        return False

    return True

# Validação para Emails
def isEmail(value: str) -> bool:
    EmailRegex = re.compile(
    r"(^[-!#$%&'*+/=?^_`{|}~0-9A-Z]+"
    r"(\.[-!#$%&'*+/=?^_`{|}~0-9A-Z]+)*"
    r"@"
    r"[A-Z0-9]([A-Z0-9-]{0,61}[A-Z0-9])?"
    r"(\.[A-Z0-9]([A-Z0-9-]{0,61}[A-Z0-9])?)+$)",
    re.IGNORECASE
)
    if not isinstance(value, str):
        return False

    email = value.strip()

    return EmailRegex.match(email) is not None

# Validação para números de telefones nacionais
def isNumber(value: str) -> bool:
    DDDS_VALIDOS = {
    11,12,13,14,15,16,17,18,19,
    21,22,24,27,28,
    31,32,33,34,35,37,38,
    41,42,43,44,45,46,
    47,48,49,
    51,53,54,55,
    61,62,63,64,
    65,66,67,
    68,69,
    71,73,74,75,77,
    79,
    81,82,83,84,85,86,87,88,89,
    91,92,93,94,95,96,97,98,99
}

    if not isinstance(value, str):
        return False

    # Remove caracteres que não forem número
    digits = re.sub(r"\D", "", value)

    # Remove prefixo internacional (+55 ou 55)
    if digits.startswith("55"):
        digits = digits[2:]

    # Verifica tamanho: fixo (10) ou celular (11)
    if len(digits) not in (10, 11):
        return False

    ddd = int(digits[:2])

    # Verifica DDD válido
    if ddd not in DDDS_VALIDOS:
        return False

    # Se for celular (11 dígitos): terceiro dígito deve ser 9
    if len(digits) == 11 and digits[2] != "9":
        return False

    # Se for fixo (10 dígitos): terceiro dígito entre 2 e 5
    if len(digits) == 10 and digits[2] not in "2345":
        return False

    return True
