#!/usr/bin/env python3
"""Disk scheduling algorithms — FCFS, SSTF, SCAN, C-SCAN, LOOK."""
import sys

def fcfs(requests, head):
    order, total, pos = [], 0, head
    for r in requests:
        total += abs(r - pos); pos = r; order.append(r)
    return order, total

def sstf(requests, head):
    remaining = list(requests); order, total, pos = [], 0, head
    while remaining:
        closest = min(remaining, key=lambda r: abs(r - pos))
        total += abs(closest - pos); pos = closest
        order.append(closest); remaining.remove(closest)
    return order, total

def scan(requests, head, disk_size, direction=1):
    order, total, pos = [], 0, head
    left = sorted(r for r in requests if r < head)
    right = sorted(r for r in requests if r >= head)
    if direction == 1:
        seq = right + [disk_size - 1] + left[::-1]
    else:
        seq = left[::-1] + [0] + right
    for r in seq:
        if r in requests or r in (0, disk_size - 1):
            total += abs(r - pos); pos = r
            if r in requests: order.append(r)
    return order, total

def look(requests, head, direction=1):
    order, total, pos = [], 0, head
    left = sorted(r for r in requests if r < head)
    right = sorted(r for r in requests if r >= head)
    if direction == 1: seq = right + left[::-1]
    else: seq = left[::-1] + right
    for r in seq:
        total += abs(r - pos); pos = r; order.append(r)
    return order, total

def main():
    if len(sys.argv) < 2: print("Usage: disk_sched.py <demo|test>"); return
    if sys.argv[1] == "test":
        reqs = [98, 183, 37, 122, 14, 124, 65, 67]
        _, t_fcfs = fcfs(reqs, 53)
        _, t_sstf = sstf(reqs, 53)
        assert t_sstf <= t_fcfs  # SSTF generally better
        o_sstf, _ = sstf(reqs, 53)
        assert set(o_sstf) == set(reqs)
        o_look, t_look = look(reqs, 53)
        assert set(o_look) == set(reqs)
        # Single request
        o, t = fcfs([100], 50); assert t == 50
        # Empty
        o, t = fcfs([], 50); assert t == 0
        print("All tests passed!")
    else:
        reqs = [98, 183, 37, 122, 14, 124, 65, 67]; head = 53
        for name, fn in [("FCFS", lambda: fcfs(reqs, head)), ("SSTF", lambda: sstf(reqs, head)), ("LOOK", lambda: look(reqs, head))]:
            order, total = fn()
            print(f"{name}: total={total}, order={order}")

if __name__ == "__main__": main()
