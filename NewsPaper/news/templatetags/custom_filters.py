from django import template


register = template.Library()

CENSURA = ['бля', 'блядь', 'блять', 'xyёв', 'xyй', 'xyя', 'вафел', 'вафлер', 'гавно', 'гавнюк']

@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Применяется только к строковым выражениям!")


    words = value.split()
    censored_words = []

    for word in words:
        if word.lower() in CENSURA:
            censored_word = f"{word[0]}{'*' * (len(word)-1)}"
            censored_words.append(censored_word)
        else:
            censored_words.append(word)

    return ' '.join(censored_words)
