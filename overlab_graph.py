def overlap(a, b, min_length=1):
    start = 0
    while True:
        start = a.find(b[:min_length], start)
        if start == -1:
            return 0
        if b.startswith(a[start:]):
            return len(a) - start
        start += 1


def overlap_graph(reads, min_length=1):
    graph = {}
    for a in reads:
        graph[a] = []
        for b in reads:
            if a != b:
                olen = overlap(a, b, min_length)
                if olen > 0:
                    graph[a].append((b, olen))
    return graph
