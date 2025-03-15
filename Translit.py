translit_dict = {
    'а': 'a', 'А': 'A', 'б': 'b', 'Б': 'B', 'в': 'v', 'В': 'V', 'г': 'g', 'Г': 'G',
    'д': 'd', 'Д': 'D', 'е': 'e', 'Е': 'E', 'ё': 'yo', 'Ё': 'Yo', 'ж': 'zh', 'Ж': 'Zh',
    'з': 'z', 'З': 'Z', 'и': 'i', 'И': 'I', 'й': 'y', 'Й': 'Y', 'к': 'k', 'К': 'K',
    'л': 'l', 'Л': 'L', 'м': 'm', 'М': 'M', 'н': 'n', 'Н': 'N', 'о': 'o', 'О': 'O',
    'п': 'p', 'П': 'P', 'р': 'r', 'Р': 'R', 'с': 's', 'С': 'S', 'т': 't', 'Т': 'T',
    'у': 'u', 'У': 'U', 'ф': 'f', 'Ф': 'F', 'х': 'kh', 'Х': 'Kh', 'ц': 'ts', 'Ц': 'Ts',
    'ч': 'ch', 'Ч': 'Ch', 'ш': 'sh', 'Ш': 'Sh', 'щ': 'sch', 'Щ': 'Sch', 'ъ': '', 'Ъ': '',
    'ы': 'y', 'Ы': 'Y', 'ь': '', 'Ь': '', 'э': 'e', 'Э': 'E', 'ю': 'yu', 'Ю': 'Yu',
    'я': 'ya', 'Я': 'Ya'
}

def transliterate(text):
    result = ''
    for char in text:
        result += translit_dict.get(char, char)
    return result

if __name__ == "__main__":
    word = input().replace('.', '')
    translit_word = transliterate(word)
    print(f"{translit_word.replace(' ', '_')}")