import time

from ellipse import by_rows, ellipse_points


def timed(f, *args):
    t = time.perf_counter()
    v = f(*args)
    return time.perf_counter() - t, v


def by_pairs(n):
    return sum(1 for x in range(n + 1) for y in range(n + 1) if x * x + 2 * y * y <= n * n)


def bench_pairs():
    print("table 1: pair enumeration O(n^2) against the walk")
    print("n, pairs, walk")
    for n in (100, 200, 400, 800):
        tp, vp = timed(by_pairs, n)
        tw, vw = timed(ellipse_points, n)
        assert vp == vw
        print(n, "%.4f" % tp, "%.6f" % tw)


def bench_main():
    print("table 2: a(n) by rows O(n) and by the walk")
    print("n, rows, walk, edges, steps, steps/n^(2/3), a(n), a(n)/n^2")
    for e in range(2, 11):
        n = 10**e
        stats = {"edges": 0, "steps": 0}
        tw, vw = timed(ellipse_points, n, stats)
        if e <= 7:
            tr, vr = timed(by_rows, n * n, 1, 2)
            assert vr == vw
            col = "%.4f" % tr
        else:
            col = "---"
        print(n, col, "%.4f" % tw, stats["edges"], stats["steps"], "%.3f" % (stats["steps"] / n ** (2 / 3)), vw, "%.7f" % (vw / n**2), flush=True)


if __name__ == "__main__":
    bench_pairs()
    bench_main()
