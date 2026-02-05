from .detector import detect_language_iso639

def describe_detect_language_iso639() -> None:
  def it_works_for_single_language() -> None:
    assert detect_language_iso639("Backend developer, hiker") == "ENG"
    assert detect_language_iso639("Бекенд разработчик, хайкер") == "RUS"
    assert detect_language_iso639("Backend Entwickler, Wanderer und Abenteurer") == "ENG"
    # ^ https://github.com/pemistahl/lingua-py/discussions/240 (no "OTHER" category support from the lib)

  def it_partially_works_for_multiple_languages() -> None:
    assert detect_language_iso639("Backend developer, hiker | Бекенд разработчик, хайкер") == "RUS"

# print(detect("Ein, zwei, drei, vier"))
# print(detect("Один, два, три, четыре"))
# print(detect("Связи между структурами - это легко! Здесь представлен базовый пример работы с псевдо-БД магазина и связями между структурами базы"))
# print(detect("Zadaci_za_vezbanje_C"))
# print(detect("Приложение, позволяющее отображать на странице масштабируемые изображения, используя svg-разметку"))
# print(detect("Слова, часто используемые в CSS-классах"))
# print(detect("HoLiWeb - компанія, яка спеціалізується на комплексній розробці веб-сайтів та веб-додатків під ключ. Просуваємо бізнес у соцмедіа (Facebook, Instagram, YouTube), що допомагає вашому бренду бути видимим і успішним в онлайн-просторі. Від UI/UX дизайну до SEO-оптимізації – ми забезпечимо максимальний результат для вашого бізнесу."))
# print(detect("Добавляет разметку и оформление всех декоративных элементов (иконок) для страниц Студия и Портфолио"))
