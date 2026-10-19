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
