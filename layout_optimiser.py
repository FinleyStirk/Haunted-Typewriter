from collections import defaultdict
from random import shuffle
from itertools import combinations


def generate_corpus_bigrams(corpus: str):
    bigrams = defaultdict(int)
    for i in range(len(corpus) - 1):
        cur_char, nxt_char = corpus[i], corpus[i + 1]
        bigrams[(cur_char, nxt_char)] += 1

    return bigrams

def generate_layout_distances(layout: list[str]) -> dict[tuple[str, str], int]:
    distances = {(char, char) : 0 for char in layout}
    for i in range(len(layout)):
        cur_char = layout[i]
        for j in range(i + 1, len(layout)):
            nxt_char = layout[j]
            distances[(cur_char, nxt_char)] = j - i
            distances[(nxt_char, cur_char)] = len(layout) - j + i
    return distances

def derive_layout(layout_distances: dict[tuple[str, str], int], anchor: str):
    return sorted(list(KEYS), key=lambda key: layout_distances[(anchor, key)])

def layout_score(layout_distances: dict[tuple[str, str], int], corpus_bigrams: dict[tuple[str, str], int]) -> float:
    total_distance = 0
    num_pairs = 0
    for bigram, occurences in corpus_bigrams.items():
        if bigram not in layout_distances:
            continue

        total_distance += layout_distances[bigram] * occurences
        num_pairs += occurences
    return total_distance / num_pairs


def swap_keys(key_one: str, key_two: str, prev_layout_distances: dict[tuple[str, str], int]) -> dict[tuple[str, str], int]:
    def f(char: str) -> str:
        if char == key_one:
            return key_two
        if char == key_two:
            return key_one
        else:
            return char

    return {(f(a), f(b)): distance for (a, b), distance in prev_layout_distances.items()}


def optimise(layout_distances: dict[tuple[str, str], int], corpus_bigrams: dict[tuple[str, str], int]) -> tuple[list[str], float]:
    best_score = layout_score(layout_distances, corpus_bigrams)

    improved = True
    while improved:
        improved = False
        best_swap = None
        for key_one, key_two in combinations(KEYS, 2):
            swapped = swap_keys(key_one, key_two, layout_distances)
            swapped_score = layout_score(swapped, corpus_bigrams)
            if swapped_score < best_score:
                best_score = swapped_score
                best_swap = swapped
                improved = True

        if best_swap is not None:
            layout_distances = best_swap

    return layout_distances, best_score

def random_optimise(letters: list[str], corpus_bigrams: dict[tuple[str, str], int], num_iterations: int = 10) -> tuple[list[str], float]:
    best_score = float('inf')
    best_layout = None
    for _ in range(num_iterations):
        shuffle(letters)
        layout_distances, score = optimise(generate_layout_distances(letters), corpus_bigrams)
        print(score, derive_layout(layout_distances, ANCHOR))
        if score < best_score:
            best_score = score
            best_layout = derive_layout(layout_distances, ANCHOR)
    return best_layout, best_score


KEYS = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
ANCHOR = "t"

with open("corpus.txt", "r") as corpus_file:
    corpus = "".join(c for c in corpus_file.read().lower() if c in KEYS)
    corpus_bigrams = generate_corpus_bigrams(corpus)

if __name__ == "__main__":
    layout, score = random_optimise(list(KEYS), corpus_bigrams)