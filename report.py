#!/usr/bin/env python3
"""Create a compact AWS Cost Explorer report by service."""
import argparse
from datetime import date, timedelta
from pathlib import Path

import boto3


def get_costs(days: int):
    end = date.today()
    start = end - timedelta(days=days)
    response = boto3.client("ce").get_cost_and_usage(
        TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )
    rows = response["ResultsByTime"][0]["Groups"]
    return start, end, sorted(
        ((row["Keys"][0], float(row["Metrics"]["UnblendedCost"]["Amount"])) for row in rows),
        key=lambda item: item[1], reverse=True,
    )


def render(start: date, end: date, costs):
    lines = [f"# AWS cost report ({start} to {end})", "", "| Service | Cost (USD) |", "| --- | ---: |"]
    lines.extend(f"| {service} | ${amount:,.2f} |" for service, amount in costs)
    lines.append(f"| **Total** | **${sum(amount for _, amount in costs):,.2f}** |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--output", default="reports/cost-report.md")
    args = parser.parse_args()
    start, end, costs = get_costs(args.days)
    report = render(start, end, costs)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
