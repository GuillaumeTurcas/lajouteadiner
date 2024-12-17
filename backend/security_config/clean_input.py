import re

# Fonction de nettoyage pour prévenir XSS (nettoyage des entrées)
def clean_input(value):
    return re.sub(r"[<>\"';]", "", value)