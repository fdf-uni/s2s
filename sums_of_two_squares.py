import itertools
from math import prod

from sympy import divisors, factorint, primerange, sqrt


def r_2(n):
    """
    Number of representations of n >= 0 as a sum of two squares.

    If one is also interested in finding those representations, use
    sums_of_two_squares instead.
    """
    d4 = [0] * 4
    for d in divisors(n):
        d4[d % 4] += 1
    return 4 * (d4[1] - d4[3]) if n != 0 else 1


def find_quadratic_nonresidue(p, candidates):
    """
    Find quadratic non-residue of a prime p = 4k + 1.
    This approach is the one described in [1].
    """
    if p % 8 == 5:
        return 2
    elif p % 3 == 2:
        return 3
    elif p % 8 == 1:
        if candidates is None:
            # 2 and 3 are handled above
            # also, the least quadratic non-residue is < sqrt(p) + 1
            candidates = primerange(5, sqrt(p) + 1)
        for q in candidates:
            # Euler's criterion with mod q reduction of p
            if pow(p % q, (q - 1) // 2) % q == q - 1:
                return q


def rep_prod(a, b, c, d):
    """
    Get representations of (a^2 + b^2)*(c^2 + b^2) as a sum of two squares.
    Applies the Brahmagupta-Fibonacci (BF) formula.
    """
    s = [
        tuple(sorted([abs(a * c + b * d), abs(a * d - b * c)])),
        tuple(sorted([abs(a * c - b * d), abs(a * d + b * c)])),
    ]
    # Remove possible duplicates
    return s if s[0] != s[1] else [s[0]]


def rep_prime_power(representation_of_p, n):
    """
    Get representations of p^n as a sum of two squares, given that of p.
    Assumes that p is a prime which is equal to 2 or of the form 4 k + 1.
    """
    r0 = representation_of_p
    rep_p = [r0]
    for i in range(n - 1):
        new_rep = []
        for r in rep_p:
            new_rep += rep_prod(r[0], r[1], *r0)
            rep_p = new_rep
    return rep_p


def sum_of_two_squares(n):
    """
    Finds all representations of n as a sum of two squares m_1^2 + m_2^2.
    Returns a list whose first element is the number of representations r_2(n)
    and whose second element is itself a list containing all representations
    where 0 <= m_1 <= m_2.
    """
    # Handle edge cases
    if n < 0:
        raise ValueError("n has to be a non-negative integer.")
    elif n == 0:
        return [1, [(0, 0)]]
    elif n == 1:
        return [4, [(0, 1)]]

    # Get prime factors and corresponding exponents
    fac = factorint(n)
    # Assuming that there exist representations, this gives their number
    r_2 = 4 * prod(fac[p] + 1 if p % 4 == 1 else 1 for p in fac)

    # Same motivation as in find_quadratic_nonresidue
    # Assigning candidates here allows single use of primerange
    candidates = primerange(
        5, max([sqrt(x) + 1 if x % 8 == 1 else 0 for x in fac])
    )

    # Representations for primes, starting with 2 = 1^2 + 1^2
    prime_reps = {2: (1, 1)}
    for p in fac:
        if p % 4 == 3:
            # Check whether representations even exist
            if fac[p] & 1:
                return [0, []]  # No representations exist
            else:
                prime_reps[p] = (0, pow(p, fac[p] // 2))
        elif p % 4 == 1:
            # Based on [1], is mostly Euclidean algorithm
            x = pow(find_quadratic_nonresidue(p, candidates), (p - 1) // 4) % p
            a, b = p, x
            while a >= sqrt(p):
                a, b = b, a % b
            prime_reps[p] = (a, b)

    # Start with 1 and use BF to iteratively multiply with prime factors
    reps = [(0, 1)]
    for p in fac:
        if p % 4 == 3:
            new_reps = []
            for r in reps:
                new_reps += rep_prod(r[0], r[1], *prime_reps[p])
            reps = new_reps
        elif p == 2 or p % 4 == 1:
            # Calculate representations for correct power of p first
            reps_p = rep_prime_power(prime_reps[p], fac[p])
            # Now essentially the same as before
            new_reps = []
            for r1, r2 in itertools.product(reps, reps_p):
                new_reps += rep_prod(r1[0], r1[1], r2[0], r2[1])
            reps = new_reps

    # Remove duplicates and sort lexicographically, then return result
    return [r_2, sorted(list(set(reps)))]


def print_representations(n):
    # Get result
    res = sum_of_two_squares(n)

    # Output result
    if res[0] == 0:
        print(
            f"Input: n = {n:,}.",
            "No representations exist, r_2(n) = 0.",
            sep="\n",
        )
    else:
        print(
            f"Input: n = {n:,}.",
            f"r_2(n) = {res[0]:,}. The representations are:",
            tabulate(
                [
                    [
                        r[0],
                        r[1],
                        f"{r[0]:,}^2 + {r[1]:,}^2",
                        f"{r[0]**2:,} + {r[1]**2:,}",
                        8 / pow(2, (r[0] == r[1]) + (r[0] == 0) + (r[1] == 0)),
                    ]
                    for r in res[1]
                ],
                headers=[
                    "m_1",
                    "m_2",
                    "Sums of two squares",
                    "Multiplied out",
                    "Count",
                ],
                showindex=list(range(1, len(res[1]) + 1)),
                tablefmt="simple",  # Adjust this for different formats
                intfmt=",",
            ),
            sep="\n",
        )


if __name__ == "__main__":
    import argparse

    from sympy import parse_expr
    from sympy.parsing.latex import parse_latex
    from tabulate import tabulate

    desc = "Find all representations of an integer as a sum of two squares."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-l",
        "--latex",
        action="store_true",
        help="Whether to parse the input as a LaTeX string.",
    )
    parser.add_argument(
        "n",
        nargs="?",
        default=None,
        help="""
        The non-negative integer to be represented as a sum of two squares.
        Can be a mathematical expression such as '3**2*5'.
        """,
    )
    # Get user input interactively if not given as command line argument
    args = parser.parse_args()

    n_in = input("n: ") if args.n is None else args.n
    n = int(parse_latex(n_in) if args.latex else parse_expr(n_in))

    print_representations(n)

"""
References
[1] Stan Wagon. "Editor's Corner: The Euclidean Algorithm Strikes Again." In: The American Mathematical Monthly, 97.2 (Feb. 1990), pp. 125-129. ISSN: 1930-0972. DOI: https://doi.org/10.2307/2323912.
"""
