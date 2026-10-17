n = int(input("enter a number: "))

if n == 2:
    print("prime")
elif n < 2 or n % 2 == 0:
    print("composite")
else:

    def mrt1(n):
        count = 0
        m = n - 1
        while m % 2 == 0:
            m = m // 2
            count += 1
        return count, m

    count, m = mrt1(n)

    def mrt2(n, m, count, a):
        b = pow(a, m, n)

        if b == 1 or b == n - 1:
            return a, None

        for i in range(2, count + 1):
            b = pow(b, 2, n)

            if b == n - 1:
                return a, None
            elif b == 1:
                return a, "composite"

        return a, "composite"

    if n < 2**32:
        bases = [2, 3, 5, 7, 11]

    elif n < 3317044064679887385961981:
        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    else:
        import random
        bases = []

        for _ in range(20):
            bases.append(random.randrange(2, n - 1))

    for a in bases:
        if a >= n:
            continue
        a, result = mrt2(n, m, count, a)

        if result == "composite":
            print("composite")
            break
    else:
        if n < 3317044064679887385961981:
            print("prime")
        else:
            print("probably prime")