from transliterate.decorators import transliterate_function


@transliterate_function(language_code='ru', reversed=True)
def translate(surname: str, name: str):
    return f"{name.capitalize()}_{surname.capitalize()}"
