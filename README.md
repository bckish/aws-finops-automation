# AWS FinOps Automation

An original Python utility that reads AWS Cost Explorer data and creates a simple Markdown cost
report, grouped by AWS service. It is designed for a scheduled GitHub Actions workflow or a
local run using least-privilege AWS credentials.

## Local use

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
AWS_PROFILE=finops-readonly .venv/bin/python report.py --days 30
```

The AWS identity needs `ce:GetCostAndUsage`. Cost Explorer must be enabled in the AWS billing
account. No credentials are stored in this repository.

## Automation

The included workflow runs weekly. Before enabling it, configure GitHub OpenID Connect or add
the required AWS authentication approach in the workflow for your own account.

## Output

The script prints a Markdown summary and can write it to `reports/cost-report.md`, which is
ignored by Git because reports may reveal billing data.
Automated AWS cost reporting and EBS snapshot lifecycle automation.

## Offline resource recommendation lab

The independent local forecasting baseline fits a linear trend to normalized synthetic CPU samples, estimates the next interval and recommends a bounded replica count. It keeps at least one replica, never recommends more than the configured maximum, and limits downscaling to one replica per interval. It only produces recommendations; it does not call AWS or Kubernetes APIs.

```bash
python3 -W error -m unittest -v test_recommend
python3 recommend.py fixtures/synthetic-cpu.json
```

Verified 26 November 2026: all three strict tests passed, and the synthetic rising-demand example forecast 89.8% CPU and recommended three replicas from an initial two. It is not a claim of savings, predictive autoscaling in production, or a substitute for HPA/Karpenter capacity controls. Production integration and cost measurement require approved real telemetry and separate validation.
