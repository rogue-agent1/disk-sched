#!/usr/bin/env python3
"""disk_sched: Disk scheduling algorithms (FCFS, SSTF, SCAN, C-SCAN)."""
import sys

def fcfs(requests, head):
    order = list(requests)
    total = 0
    pos = head
    for r in order:
        total += abs(r - pos)
        pos = r
    return order, total

def sstf(requests, head):
    remaining = list(requests)
    order = []
    total = 0
    pos = head
    while remaining:
        nearest = min(remaining, key=lambda r: abs(r - pos))
        total += abs(nearest - pos)
        pos = nearest
        order.append(nearest)
        remaining.remove(nearest)
    return order, total

def scan(requests, head, direction="up", max_cyl=199):
    order = []
    total = 0
    pos = head
    if direction == "up":
        up = sorted(r for r in requests if r >= head)
        down = sorted((r for r in requests if r < head), reverse=True)
        seq = up + [max_cyl] + down if up else down
    else:
        down = sorted((r for r in requests if r <= head), reverse=True)
        up = sorted(r for r in requests if r > head)
        seq = down + [0] + up if down else up
    # Remove boundary if not in requests
    for r in seq:
        if r in requests or r == max_cyl or r == 0:
            total += abs(r - pos)
            pos = r
            if r in requests:
                order.append(r)
    return order, total

def cscan(requests, head, max_cyl=199):
    order = []
    total = 0
    pos = head
    up = sorted(r for r in requests if r >= head)
    down = sorted(r for r in requests if r < head)
    for r in up:
        total += abs(r - pos); pos = r; order.append(r)
    if down:
        total += abs(max_cyl - pos) + max_cyl  # Go to end, wrap to 0
        pos = 0
        for r in down:
            total += abs(r - pos); pos = r; order.append(r)
    return order, total

def test():
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    # FCFS
    order, total = fcfs(requests, head)
    assert order == requests
    assert total == 640
    # SSTF
    order2, total2 = sstf(requests, head)
    assert total2 < total  # SSTF should be better than FCFS
    assert set(order2) == set(requests)
    # SCAN
    order3, total3 = scan(requests, head, "up")
    assert set(order3) == set(requests)
    # C-SCAN
    order4, total4 = cscan(requests, head)
    assert set(order4) == set(requests)
    # Empty
    assert fcfs([], 50) == ([], 0)
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: disk_sched.py test")
