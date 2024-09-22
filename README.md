# Sums of two squares in Python

The script `sums_of_two_squares.py` provides - as the name suggest - an implementation of some functions regarding sums of two squares.
It can also be used as a command line program, see [Usage](#usage).

## How it works

There are mainly three mathematical "ingredients".
The first is an algorithm to find a representation of a prime $p \equiv 1 \pmod 4$ as a sum of two squares due to Stan Wagon in [[1]](#1).
The second one is the [Brahmagupta-Fibonacci identity [BF]](https://en.wikipedia.org/wiki/Brahmagupta%E2%80%93Fibonacci_identity) and the third (implicit one) is [Jacobi's two-square theorem [J]](https://en.wikipedia.org/wiki/Sum_of_two_squares_theorem#Jacobi's_two-square_theorem).

With these remarks out of the way, we can describe how the algorithm for finding all representation of $n$ as a sum of two squares works:
- Factorize $n = p_1^{\nu_1} \cdots p_r^{\nu_r}$  with distinct primes $p_j$, $1 \le j \le r$.
- For every $p_j$ proceed as follows:
    - If $p_j \equiv 3 \pmod 4$ and $\nu_j$ is even, store $(0, p_j^{\nu_j/2})$ (which up to order and signs is the only representation by [J]).
        If $\nu_j$ is odd, quit since in this case $n$ cannot be written as a sum of two squares.
    - If $p_j \equiv 1 \pmod 4$, find the representation of $p_j$ as a sum of two squares as described in [[1]](#1).
    - If $p_j = 2$ store $(1,1)$ (which is once again up to signs unique).
- For every prime $p_j \not\equiv 3 \pmod 4$, calculate representations of $p_j^{\nu_j}$ by repeatedly applying [BF].
- Start with $(0, 1)$ and for every $j \in \{0, \dots, r\}$ apply [BF] to $p_1^{\nu_1} \cdots p_{j - 1}^{\nu_j - 1}$ and $p_j^{\nu_j}$ to obtain all representations for $p_1^{\nu_1} \cdots p_j^{\nu_j}$.

That _all_ representations are actually found like this follows from:
1. If $n = p q$ is a sum of two squares and $p$ is a prime which can be written as a sum of two squares, then so can $q$ (this is a proposition by Euler).
    Furthermore, any representation of $n$ can be found from the one of $p$ and a suitable one of $q$ by applying the [BF].
2. [J] implies that any number of the form $q_1^{\mu_1} \cdots q_s^{\mu_s}$ where all $q_j$ are congruent to $3$ modulo $4$ has only one representation (up to order and signs).

Together, this shows that one can, without loss of generality, repeatedly split off $2$ and [Pythagorean primes](https://en.wikipedia.org/wiki/Pythagorean_prime) from the factorization of $n$ until it is of the form in 2. in which case the claim that all representations are found by the above approach immediately follows.

## Usage

You can either import the file for your own purposes or run it directly.
When doing the latter, the program requires a non-negative integer $n$ as its input.
It can either be provided as a command-line argument, i.e. `python sums_of_two_squares.py 25`, or interactively when the program asks for it.
In both cases, $n$ can also be provided as an expression such as `3**2 * 5` or `log(2534)*2*sqrt(4) + exp(4)` (for this, `sympy` is used).
The `-l` flag can be used to parse LaTeX instead of Python syntax.

Of course, there's also `python sums_of_two_squares.py -h` for getting usage information.

### Example

```sh
> python sums_of_two_squares.py 21855625
Input: n = 21,855,625.
r_2(n) = 60. The representations are:
      m_1    m_2  Sums of two squares    Multiplied out             Count
--  -----  -----  ---------------------  -----------------------  -------
 1      0  4,675  0^2 + 4,675^2          0 + 21,855,625                 4
 2    715  4,620  715^2 + 4,620^2        511,225 + 21,344,400           8
 3    957  4,576  957^2 + 4,576^2        915,849 + 20,939,776           8
 4  1,309  4,488  1,309^2 + 4,488^2      1,713,481 + 20,142,144         8
 5  1,980  4,235  1,980^2 + 4,235^2      3,920,400 + 17,935,225         8
 6  2,200  4,125  2,200^2 + 4,125^2      4,840,000 + 17,015,625         8
 7  2,805  3,740  2,805^2 + 3,740^2      7,868,025 + 13,987,600         8
 8  3,267  3,344  3,267^2 + 3,344^2      10,673,289 + 11,182,336        8
```

## Dependencies

Besides modules from Python's standard library, the script uses `sympy` for parsing the input and integer factorization.
Apart from that, the only dependency is `tabulate` for prettier output if run directly.

## References
<a id="1">[1]</a> 
Stan Wagon.
"Editor's Corner: The Euclidean Algorithm Strikes Again."
In: The American Mathematical Monthly, 97.2 (Feb. 1990), pp. 125-129.
ISSN: 1930-0972.
DOI: https://doi.org/10.2307/2323912.
