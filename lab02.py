"""Lab 2 - Linear and binary search: best / worst / average case (reference solution)."""
import math, random


def linear_search(A, x):
    comparisons = 0
    for i, value in enumerate(A):
        comparisons += 1
        if value == x:
            return i, comparisons
    return -1, comparisons


def binary_search(A, x):
    lo, hi = 0, len(A) - 1
    comparisons = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if A[mid] == x:
            return mid, comparisons
        if A[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, comparisons


def cases_table(n):
    """Exact comparison counts for the special cases (A = [0..n-1])."""
    A = list(range(n))
    out = {}
    out["lin best (x=A[0])"] = linear_search(A, 0)[1]
    out["lin worst (x=A[n-1])"] = linear_search(A, n - 1)[1]
    out["lin worst (absent)"] = linear_search(A, -5)[1]
    out["bin best (x=A[mid])"] = binary_search(A, A[(n - 1) // 2])[1]
    # worst case for binary search: maximum over ALL targets (present or absent)
    worst = max(binary_search(A, x)[1] for x in range(-1, n + 1))
    out["bin worst (max over targets)"] = worst
    out["floor(log2 n)+1"] = int(math.floor(math.log2(n))) + 1
    return out


def average_linear(n, q, trials=20000, seed=1):
    """Monte-Carlo estimate of E[C]: absent with prob. q, else uniform position."""
    rnd = random.Random(seed)
    A = list(range(n))
    total = 0
    for _ in range(trials):
        x = -1 if rnd.random() < q else rnd.randrange(n)
        total += linear_search(A, x)[1]
    return total / trials


def theory_average(n, q):
    return (1 - q) * (n + 1) / 2 + q * n


def average_binary(n, trials=20000, seed=2):
    rnd = random.Random(seed)
    A = list(range(n))
    return sum(binary_search(A, rnd.randrange(n))[1] for _ in range(trials)) / trials


def break_even(n):
    """Smallest number k of searches for which sort-once + binary beats k linear searches.
    Cost model (comparisons): sort ~ n*log2(n); linear search ~ (n+1)/2 on average;
    binary search ~ log2(n)."""
    sort_cost = n * math.log2(n)
    lin, binr = (n + 1) / 2, math.log2(n)
    k = 1
    while k * lin <= sort_cost + k * binr:
        k += 1
    return k


def report():
    from display import banner, section, note, table, ci, figure, save, show_all
    banner("LAB 2 — Linear vs Binary search : best / worst / average")
    section("A. Nombre de comparaisons dans les cas particuliers")
    t16, t1k = cases_table(16), cases_table(1024)
    table(["Cas", "n = 16", "n = 1024"], [[k, t16[k], t1k[k]] for k in t16])
    note("Linear: best = 1, worst = n (dernier élément OU absent). Binary: best = 1, worst = ⌊log2 n⌋ + 1.")
    section("B. Cas moyen de linear search (n = 1000, 20 000 essais)")
    qs = (0, 0.25, 0.5, 0.75, 1.0)
    rows, th, sim = [], [], []
    for q in qs:
        a, b = theory_average(1000, q), average_linear(1000, q)
        th.append(a); sim.append(b)
        rows.append([q, f"{a:.1f}", f"{b:.1f}", f"{abs(a-b):.1f}"])
    table(["q = P(absent)", "théorie (1-q)(n+1)/2 + qn", "simulé", "écart"], rows)
    note("Ki q = 0: E[C] = (n+1)/2 ≈ 500. Ki q yzid, E[C] yetqarreb l n (khatt mostaqim f q), lakin classe tebqa Θ(n).")
    section("C. Linear vs Binary selon n")
    ns = [16, 256, 4096, 65536, 10**6]
    bavg = [average_binary(n, 3000) for n in ns]
    table(["n", "linear moyen", "linear worst", "binary moyen", "binary worst"],
          [[ci(n), f"{(n+1)/2:,.1f}".replace(",", " "), ci(n), f"{b:.2f}", int(math.log2(n)) + 1] for n, b in zip(ns, bavg)])
    section("D. Faut-il trier avant de chercher ? (break-even)")
    table(["n", "nb de recherches k à partir duquel trier+binary gagne"], [[ci(n), break_even(n)] for n in (1000, 10**4, 10**5, 10**6)])
    note("Ida 3andek recherche wahda: linear. Ida 3andek bezzaf recherches (> ~2·log2 n): retb mra wahda w use binary.")
    fig, ax = figure(1, 2, figsize=(11, 4))
    if fig:
        ax[0].plot(qs, sim, "o-", label="simulé"); ax[0].plot(qs, th, "k--", label="théorie")
        ax[0].set_xlabel("q = P(target absent)"); ax[0].set_ylabel("comparaisons moyennes (n = 1000)"); ax[0].set_title("Linear search : cas moyen"); ax[0].legend()
        ax[1].plot(ns, [(n + 1) / 2 for n in ns], "o-", label="linear (moyen)"); ax[1].plot(ns, bavg, "s-", label="binary (moyen)")
        ax[1].set_xscale("log"); ax[1].set_yscale("log"); ax[1].set_xlabel("n"); ax[1].set_ylabel("comparaisons"); ax[1].set_title("Linear vs Binary"); ax[1].legend()
        save(fig, "lab02_search")
    show_all()


if __name__ == "__main__":
    report()
