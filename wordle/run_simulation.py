# Запуск симуляції з відео 3Blue1Brown "Solving Wordle using information theory"
# Бот грає у Wordle для всіх 2315 можливих відповідей і рахує середню кількість спроб.

from simulations import *

if __name__ == "__main__":
    FIRST_GUESS = "salet"     # перше слово (у відео найкращими виходять salet, crane, slate)
    TEST_WORDS = 20        # None - усі 2315 слів; або число, напр. 50, для швидкої перевірки

    test_set = get_word_list(short=True)
    if TEST_WORDS:
        test_set = test_set[:TEST_WORDS]

    results, decision_map = simulate_games(
        first_guess=FIRST_GUESS,
        priors=get_true_wordle_prior(),
        optimize_for_uniform_distribution=True,
        test_set=test_set,
    )

    print("\n================ РЕЗУЛЬТАТ ================")
    print(f"Перше слово: {FIRST_GUESS}")
    print(f"Зіграно ігор: {len(test_set)}")
    print(f"Середня кількість спроб: {results['average_score']:.3f}")
    print("Розподіл кількості спроб:")
    for n, count in enumerate(results['score_distribution']):
        if count:
            print(f"  {n} спроб: {count} ігор")

    print("\nПриклади ігор:")
    for game in results['game_results'][:5]:
        print(f"  {game['answer']}: {' -> '.join(game['guesses'])} -> {game['answer']} "
              f"({game['score']} спроб)")
