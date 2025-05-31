import requests

def get_tallest_hero_by_gender_and_work(gender: str, has_job: bool):
    url = "https://akabab.github.io/superhero-api/api/all.json"
    response = requests.get(url)
    response.raise_for_status()
    heroes = response.json()

    # Фильтрация по полу, работе + добавляем в лист всех таких героев
    filtered_heroes = []
    for hero in heroes:
        hero_gender = hero.get('appearance', {}).get('gender')
        occupation = hero.get('work', {}).get('occupation', '').strip()
        if hero_gender != gender:
            continue
        if has_job and occupation == '':
            continue
        if not has_job and occupation != '':
            continue
        filtered_heroes.append(hero)

    if not filtered_heroes:
        return None

    # Ищем самого высокого героя(через см)
    def get_height_cm(hero):
        heights = hero.get('appearance', {}).get('height', [])
        # проверка на наличие 2х элементов + деф от индекс эррора для обращения heights[1]
        if len(heights) < 2:
            return 0
        height_str = heights[1]
        # правильно извлекаем рост для сравнения или просто 0 + делаем инт, чтобы было проще
        if height_str.endswith("cm"):
            try:
                return int(height_str.replace("cm", "").strip())
            except ValueError:
                return 0
        return 0

    # макс инт из массива героев, получаем самого выского
    tallest_hero = max(filtered_heroes, key=get_height_cm)
    return tallest_hero

# тут пример + ф строчный вывод, чтобы было читаемо
# можно удалить все, что ниже, чтобы не прокало в строке при запуске тестов
hero = get_tallest_hero_by_gender_and_work('Female', True)
if hero:
    print(f"Самый высокий герой: {hero['name']}, рост: {hero['appearance']['height'][1]}, работа: {hero['work']['occupation']}")
else:
    print("Герой не найден")