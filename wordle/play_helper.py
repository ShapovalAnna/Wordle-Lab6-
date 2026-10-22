
# Ти граєш у справжній Wordle, а програма підказує, яке слово ввести наступним.

from simulations import *


def ask_pattern():
    """Зчитує кольори від користувача: g - зелена, y - жовта, b - сіра."""
    while True:
        s = input("Кольори (5 літер: g - зелена, y - жовта, b - сіра), напр. bygbb: ").strip().lower()
        if len(s) == 5 and all(c in "gyb" for c in s):
            return pattern_from_string(s.replace("b", "0").replace("y", "1").replace("g", "2"))
        print("Неправильний формат, спробуй ще раз.")


def main():
    allowed = get_word_list()                 # усі слова, які можна вводити
    possible = get_word_list(short=True)      # слова, які можуть бути відповіддю
    priors = get_true_wordle_prior()

    print("Готуємо дані (перший запуск може тривати кілька хвилин)...")
    get_pattern_matrix(allowed[:1], allowed[:1])

    step = 1
    while True:
        weights = get_weights(possible, priors)
        ents = get_entropies(allowed, possible, weights)
        top = np.argsort(ents)[::-1][:5]

        print(f"\n--- Спроба {step} --- Можливих відповідей: {len(possible)} "
              f"(невизначеність {math.log2(len(possible)):.2f} біт)")
        if len(possible) <= 10:
            print("Можливі відповіді:", ", ".join(possible))
        print("Найкращі слова за ентропією (скільки біт інформації в середньому дасть слово):")
        for i in top:
            mark = " (може бути відповіддю)" if allowed[i] in possible else ""
            print(f"  {allowed[i]}: {ents[i]:.2f} біт{mark}")

        if len(possible) == 1:
            print(f"\nВідповідь: {possible[0].upper()}")
            break

        guess = input("\nЯке слово ти ввела? ").strip().lower()
        if guess not in allowed:
            print("Такого слова немає у словнику Wordle.")
            continue
        pattern = ask_pattern()
        if pattern == 3 ** 5 - 1:
            print("Вітаю, слово відгадано! 🎉")
            break

        possible = get_possible_words(guess, pattern, possible)
        if not possible:
            print("Немає слів з такими кольорами - перевір введення.")
            break
        step += 1


if __name__ == "__main__":
    main()
