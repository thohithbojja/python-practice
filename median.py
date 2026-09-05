nums1 = []

while True:

    n = input("enter a no in nums1: ")

    if n == "q":
        break
    nums1.append(int(n))

nums2 = []

while True:

    N = input("enter a no in nums2: ")

    if N == "q":
        break
    nums2.append(int(N))
print(f"nums1 ={nums1}")
print(f"nums2 ={nums2}")

merged = nums1 + nums2
merged.sort()
print(f"{merged}")


def median(merged):
    n = len(merged)

    if n % 2 == 0:
        median = (merged[n // 2] + merged[n // 2 + 1]) / 2
    else:
        median = merged[n // 2]
    return median


print(f"the median is {median(merged)}")