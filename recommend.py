"""Offline resource recommendation from synthetic CPU samples; never changes infrastructure."""
import argparse
import json
import math
from pathlib import Path


def recommend(samples, current_replicas, target_cpu=0.65, max_replicas=10):
    if not isinstance(samples, list) or len(samples) < 3 or any(type(x) not in (int, float) or not 0 <= x <= 1 or not math.isfinite(x) for x in samples):
        raise ValueError("provide at least three normalized CPU samples in [0,1]")
    if type(current_replicas) is not int or type(max_replicas) is not int or not 1 <= current_replicas <= max_replicas or not 0 < target_cpu <= 1:
        raise ValueError("invalid replica budget or target CPU")
    n = len(samples)
    mean_x = (n - 1) / 2
    mean_y = sum(samples) / n
    slope = sum((i-mean_x)*(v-mean_y) for i, v in enumerate(samples)) / sum((i-mean_x)**2 for i in range(n))
    forecast = max(0, min(1, mean_y + slope*(n-mean_x)))
    desired = min(max_replicas, max(1, math.ceil(current_replicas * forecast / target_cpu)))
    # Never recommend cutting more than one replica in a single interval.
    desired = max(current_replicas - 1, desired)
    return {"forecast_cpu_fraction": round(forecast, 4), "current_replicas": current_replicas, "recommended_replicas": desired, "max_replicas": max_replicas, "mode": "advisory-only", "requires_operator_review": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.fixture.read_text(encoding="utf-8"))
        print(json.dumps(recommend(data["samples"], data["current_replicas"], max_replicas=data["max_replicas"]), indent=2))
    except (OSError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
