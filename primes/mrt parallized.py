import random
from concurrent.futures import ProcessPoolExecutor, as_completed


def get_d_and_r(n: int) -> tuple[int, int]:
    """Factors n - 1 into m * 2^count using fast bitwise operations."""
    m = n - 1
    # Isolate the lowest set bit to find the number of trailing zeros in O(1) steps
    count = (m & -m).bit_length() - 1
    return count, m >> count

import gmpy2

def mrt_worker(args: tuple[int, int, int, int]) -> bool:
    """Runs a single Miller-Rabin witness test. Returns True if composite."""
    n, m, count, a = args
    n, m, a = gmpy2.mpz(n), gmpy2.mpz(m), gmpy2.mpz(a)

    b = gmpy2.powmod(a, m, n)

    if b == 1 or b == n - 1:
        return False  # Probably prime for this base

    for _ in range(count - 1):
        b = gmpy2.powmod(b, 2, n)
        if b == n - 1:
            return False  # Probably prime for this base
        if b == 1:
            return True  # Definitely composite

    return True  # Definitely composite


def is_prime_parallel(n: int, k: int = 20) -> bool:
    if n in (2, 3):
        return True
    if n < 2 or n % 2 == 0 or n % 3 == 0:
        return False

    count, m = get_d_and_r(n)

    # Select deterministic bases or generate random bases
    if n < 2 ** 32:
        raw_bases = [2, 3, 5, 7, 11]
    elif n < 3317044064679887385961981:
        raw_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    else:
        raw_bases = [random.randrange(2, n - 1) for _ in range(k)]

        # Filter out bases >= n to prevent small primes (like 3, 5, 7, 11) from failing
    bases = [a for a in raw_bases if a < n]

    # Note: Multiprocessing has startup overhead (~10-50ms).
    # For numbers under 512 bits, sequential execution is faster than spawning processes.
    if n.bit_length() < 512:
        return not any(mrt_worker((n, m, count, a)) for a in bases)

        # Parallel execution with early exit for large numbers
    tasks = [(n, m, count, a) for a in bases]
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(mrt_worker, task) for task in tasks]
        for future in as_completed(futures):
            if future.result():  # If any worker finds it is composite
                # Cancel remaining pending tasks and exit immediately
                for f in futures:
                    f.cancel()
                return False

    return True


if __name__ == "__main__":
    n = int(input("enter a number: "))
    if is_prime_parallel(n):
        print("prime" if n < 3317044064679887385961981 else "probably prime")
    else:
        print("composite")
