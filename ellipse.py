from math import isqrt


def floor_sum(n, m, a, b):
    total = 0
    while True:
        if a >= m:
            total += (n - 1) * n // 2 * (a // m)
            a %= m
        if b >= m:
            total += n * (b // m)
            b %= m
        y = a * n + b
        if y < m:
            return total
        n, b = divmod(y, m)
        m, a = a, m


def strip(p, q, y, k):
    c = (p - 1) * (q - 1) // 2 + p - 1 + q
    return k * p * y - k * c - p * q * k * (k - 1) // 2


def max_copies(x, y, p, q, M, wx, wy):
    s = wx * p * p + wy * q * q
    c = wx * x * p - wy * y * q
    d = c * c - s * (wx * x * x + wy * y * y - M)
    if d < 0:
        return 0
    return max(0, (isqrt(d) - c) // s)


def first_fit(x, y, fp, fq, gp, gq, M, wx, wy):
    u = x + gp
    v = y - gq
    s = wx * fp * fp + wy * fq * fq

    def excess(k):
        return wx * (u + k * fp) ** 2 + wy * (v - k * fq) ** 2 - M

    k0 = max(1, (wy * v * fq - wx * u * fp) // s)
    if excess(k0) <= 0:
        hi = k0
    elif excess(k0 + 1) <= 0:
        hi = k0 + 1
    else:
        return 0
    lo = 1
    while lo < hi:
        mid = (lo + hi) // 2
        if excess(mid) <= 0:
            hi = mid
        else:
            lo = mid + 1
    return lo


def column_sum(M, wx, wy, stats=None):
    x_end = isqrt(M * wy // (wx * (wx + wy)))
    x, y = 0, isqrt(M // wy)
    total = 0
    stack = [(1, 1), (1, 0)]
    while x < x_end:
        p, q = stack.pop()
        k = max_copies(x, y, p, q, M, wx, wy)
        kx = (x_end - x) // p
        take = min(k, kx)
        if take:
            total += strip(p, q, y, take)
            x += take * p
            y -= take * q
            if stats is not None:
                stats["edges"] += 1
        if k > kx:
            rem = x_end - x
            if rem:
                total += rem * y - floor_sum(rem, p, q, p + q - 1)
            break
        if x >= x_end:
            break
        gp, gq = p, q
        while True:
            p, q = stack.pop()
            if wx * (x + p) ** 2 + wy * (y - q) ** 2 <= M:
                break
            gp, gq = p, q
        fp, fq = p, q
        while True:
            if stats is not None:
                stats["steps"] += 1
            k = first_fit(x, y, fp, fq, gp, gq, M, wx, wy)
            if k == 0:
                break
            stack.append((fp, fq))
            gp += (k - 1) * fp
            gq += (k - 1) * fq
            fp += gp
            fq += gq
        stack.append((fp, fq))
    return total


def quarter_points(M, wx, wy, stats=None):
    if M < 0:
        return 0
    x0 = isqrt(M * wy // (wx * (wx + wy)))
    y0 = isqrt(M * wx // (wy * (wx + wy)))
    inner = column_sum(M, wx, wy, stats) + column_sum(M, wy, wx, stats) - x0 * y0
    return 1 + isqrt(M // wx) + isqrt(M // wy) + inner


def ellipse_points(n, stats=None):
    return quarter_points(n * n, 1, 2, stats)


def circle_points(n, stats=None):
    return quarter_points(n * n, 1, 1, stats)


def by_rows(M, wx, wy):
    return sum(1 + isqrt((M - wy * y * y) // wx) for y in range(isqrt(M // wy) + 1))
