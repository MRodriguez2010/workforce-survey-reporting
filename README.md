# Workforce Survey Reporting

**Employee Sentiment Analysis project family:** [Project guide](https://github.com/MRodriguez2010/Revelio/blob/main/docs/employee-sentiment-analysis-projects.md) · [Revelio interactive demo](https://github.com/MRodriguez2010/Revelio)

Harbor’s favorable responses on schedule clarity rose from four of eight to six of eight. The favorable share increased from 50% to 75%, a **25 percentage-point change**. At Juniper, the baseline group was too small to publish a change. Both sites and all responses in this example are fictional.

[Read the sample report](example/results.md) · [Inspect the aggregation SQL](sql/summary.sql) · [Inspect the input](example/responses.csv)

## Reproduce the report

The project uses Python 3.10+ and its standard library.

```sh
python3 report.py example/responses.csv
python3 -m unittest -v
```

The CSV carries the wave, site, question, invented respondent ID and score. The loader rejects duplicate responses, unsupported waves, missing fields and scores outside 1–5. SQL counts favorable responses separately for each wave, site and question. Each published rate needs at least five responses by default. A change requires both waves to qualify.

This is a newly written public example of workforce analytics. The questions, response scale, fictional sites, reporting rule, source code and example output were created for this demonstration. The included fixture generator reproduces the CSV without access to any employer or survey provider.
