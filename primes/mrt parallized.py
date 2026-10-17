import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import gmpy2

# Remove Python's 4,300-digit conversion limit
sys.set_int_max_str_digits(0)


def get_d_and_r(n: int) -> tuple[int, int]:
    """Factors n - 1 into m * 2^count using fast bitwise operations."""
    m = n - 1
    # Isolate the lowest set bit to find the number of trailing zeros in O(1) steps
    count = (m & -m).bit_length() - 1
    return count, m >> count


def mrt_worker(args: tuple[int, int, int, int]) -> bool:
    """Runs a single Miller-Rabin witness test using gmpy2. Returns True if composite."""
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

    if n < 2**32:
        raw_bases = [2, 3, 5, 7, 11]
    elif n < 3317044064679887385961981:
        raw_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    else:
        raw_bases = [2] + [random.randrange(3, n - 1) for _ in range(k - 1)]

    # Filter out bases >= n so small numbers (like 5, 7, 11) don't fail
    bases = [a for a in raw_bases if a < n]

    if n.bit_length() < 512:
        return not any(mrt_worker((n, m, count, a)) for a in bases)

    # Test base 2 first before spawning worker processes
    if mrt_worker((n, m, count, bases[0])):
        return False

    tasks = [(n, m, count, a) for a in bases[1:]]
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(mrt_worker, task) for task in tasks]
        for future in as_completed(futures):
            if future.result():
                for f in futures:
                    f.cancel()
                return False

    return True


if __name__ == "__main__":
    user_input = input(
        "Enter a number, a .txt filename, or press Enter for 'number.txt': "
    ).strip()

    # Check if the user pressed Enter or typed a filename
    is_file_request = (
        not user_input
        or user_input.lower().endswith(".txt")
        or Path(user_input).is_file()
        or Path(__file__).with_name(user_input).is_file()
    )

    if is_file_request:
        filename = user_input if user_input else "number.txt"
        file_path = Path(filename)
        if not file_path.is_file():
            file_path = Path(__file__).with_name(filename)

        # Auto-create number.txt with a 10,000-digit number if it doesn't exist yet
        if not file_path.exists():
            if filename == "number.txt":
                random_10k = str(random.randint(10**9999, 10**10000 - 1) | 1)
                file_path.write_text(random_10k, encoding="utf-8")
                print(f"Created '{file_path.name}' with a random 10,000-digit odd number.")
            else:
                print(f"Error: File '{filename}' not found!")
                sys.exit(1)

        raw_text = file_path.read_text(encoding="utf-8")
        print(f"Loaded number from file: {file_path.name}")
    else:
        # User typed a number directly into the console
        raw_text = user_input

    # Keep only digits (ignores spaces, newlines, or accidental letter typos)
    clean_digits = "".join(ch for ch in raw_text if ch.isdigit())

    if not clean_digits:
        print("Error: No valid digits found!")
        sys.exit(1)

    n = int(clean_digits)
    print(f"Testing {len(clean_digits):,}-digit number ({n.bit_length():,} bits)...")

    start_time = time.perf_counter()
    if is_prime_parallel(n):
        status = "prime" if n < 3317044064679887385961981 else "probably prime"
    else:
        status = "composite"
    elapsed = time.perf_counter() - start_time

    print(f"{status} (completed in {elapsed:.3f} seconds)")
