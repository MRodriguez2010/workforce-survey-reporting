-- Each row is one synthetic respondent's answer to one question in one wave.
WITH counts AS (
    SELECT wave, site, question,
           COUNT(*) AS responses,
           SUM(score >= 4) AS favorable
    FROM response
    GROUP BY wave, site, question
),
publishable AS (
    SELECT wave, site, question, responses,
           100.0 * favorable / responses AS favorable_pct
    FROM counts
    WHERE responses >= :minimum
)
SELECT curr.site, curr.question, curr.responses,
       ROUND(curr.favorable_pct, 1) AS favorable_pct,
       ROUND(curr.favorable_pct - prev.favorable_pct, 1) AS change_pp
FROM publishable AS curr
LEFT JOIN publishable AS prev
  ON curr.site = prev.site AND curr.question = prev.question AND prev.wave = :prior
WHERE curr.wave = :current
ORDER BY curr.site, curr.question;
