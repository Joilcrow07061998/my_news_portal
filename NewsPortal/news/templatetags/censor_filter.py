from django import template

register = template.Library()

BAD_WORDS = ['редиска']

@register.filter()
def censor(value):
    """
    Фильтр заменяет нецензурные слова на звездочки
    """
    if not isinstance(value, str):
        raise TypeError('Фильтр применяется только к строкам')

    for word in BAD_WORDS:
        replacement = '*' * len(word)
        value = value.replace(word, replacement)
        value = value.replace(word.capitalize(), replacement)

    return value
