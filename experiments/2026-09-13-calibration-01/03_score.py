import csv
from pathlib import Path

rows = list(csv.DictReader(Path(__file__).with_name('02_data.csv').open()))
ps = [float(r['p_true']) for r in rows]
ys = [int(r['outcome']) for r in rows]

accuracy = sum(ys) / len(ys)
mean_p = sum(ps) / len(ps)
gap = mean_p - accuracy
brier = sum((p-y)**2 for p, y in zip(ps, ys)) / len(ps)
high = [y for p, y in zip(ps, ys) if p >= 0.90]
low = [y for p, y in zip(ps, ys) if p <= 0.40]

print(f'n={len(rows)}')
print(f'accuracy={accuracy:.6f}')
print(f'mean_p={mean_p:.6f}')
print(f'gap={gap:.6f}')
print(f'brier={brier:.6f}')
print(f'high_accuracy={sum(high)/len(high):.6f} n={len(high)}')
print(f'low_true_rate={sum(low)/len(low):.6f} n={len(low)}')

assert abs(gap) <= 0.08
assert sum(high) / len(high) >= 0.90
assert sum(low) / len(low) <= 0.40
assert brier <= 0.10
