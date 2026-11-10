"""Generate a fictional two-wave fixture without external data."""
import csv
import sys

writer = csv.writer(sys.stdout, lineterminator="\n")
writer.writerow(("wave", "site", "question", "response_id", "score"))
# Each pair specifies group size and the number of favorable responses.
groups = {
    "Harbor": {"Schedule clarity": [(8, 4), (8, 6)], "Tool availability": [(8, 6), (8, 5)]},
    "Juniper": {"Schedule clarity": [(3, 2), (6, 4)], "Tool availability": [(6, 3), (4, 3)]},
}
for site, questions in groups.items():
    for question, waves in questions.items():
        for wave, (count, favorable) in zip(("Baseline", "Follow-up"), waves):
            for i in range(count):
                score = (4 + i % 2) if i < favorable else (1 + i % 3)
                writer.writerow((wave, site, question, f"sample-{i + 1:02}", score))
