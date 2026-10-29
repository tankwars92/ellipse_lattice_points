import random

from ellipse import by_rows, circle_points, ellipse_points, quarter_points

DATA = [
    1, 2, 5, 9, 12, 19, 27, 33, 42, 54, 66, 77, 91, 105, 120, 138, 156, 175, 197,
    218, 240, 263, 287, 314, 339, 367, 398, 430, 459, 493, 526, 556, 595, 637, 670,
    709, 752, 794, 833, 878, 921, 965, 1018, 1065, 1112, 1163, 1215, 1266, 1317,
    1370, 1433, 1492, 1544,
]


def by_definition(n):
    count = 0
    for x in range(n + 1):
        for y in range(n + 1):
            if x * x + 2 * y * y <= n * n:
                count += 1
    return count


def check_data():
    assert [ellipse_points(n) for n in range(len(DATA))] == DATA
    print("walk agrees with the %d terms of A218706" % len(DATA))


def check_definition():
    for n in range(0, 201):
        assert ellipse_points(n) == by_definition(n), n
    print("walk equals the definition for n = 0..200")


def check_forms():
    random.seed(218706)
    for _ in range(4000):
        wx, wy = random.randint(1, 12), random.randint(1, 12)
        M = random.randint(0, 8000)
        assert quarter_points(M, wx, wy) == by_rows(M, wx, wy), (M, wx, wy)
    print("walk equals the row count for 4000 random forms wx*x^2 + wy*y^2 <= M, M <= 8000")
    for _ in range(600):
        wx, wy = random.randint(1, 30), random.randint(1, 30)
        M = random.randint(10**6, 10**11)
        assert quarter_points(M, wx, wy) == by_rows(M, wx, wy), (M, wx, wy)
    print("walk equals the row count for 600 random forms with M up to 10^11")


def check_rows():
    for n in range(1, 3001):
        assert ellipse_points(n) == by_rows(n * n, 1, 2), n
        assert circle_points(n) == by_rows(n * n, 1, 1), n
    print("ellipse and circle walks equal the row count for n = 1..3000")
    random.seed(7)
    cases = [random.randrange(3000, 10**6) for _ in range(150)] + [10**6, 10**7, 10**7 + 1]
    for n in cases:
        assert ellipse_points(n) == by_rows(n * n, 1, 2), n
    print("ellipse walk equals the row count for %d further n up to 10^7" % len(cases))


if __name__ == "__main__":
    check_data()
    check_definition()
    check_forms()
    check_rows()
    print("all checks passed")
