# Data template codebook

Files in this folder:

- `data_template.csv` — header row only. Paste your 220 rows underneath.
- `data_template_with_examples.csv` — same header plus three illustrative rows. The three example
  rows are fabricated for format demonstration only and must be deleted before use.

One row per respondent. 220 rows expected. 43 columns.

---

## Column specification

| Column | Type | Permitted values | Required |
|---|---|---|---|
| `respondent_id` | integer | 1 to 220, unique | Yes |
| `group` | text | `developing` or `emerging` (lowercase) | Yes |
| `country` | text | Country name, or `NA` | Preferred |
| `role` | text | `logistics_manager`, `sc_director`, `ops_sustainability`, `other_senior` | Yes |
| `firm_size` | text | `small`, `medium`, `large` | Yes |
| `employees` | integer | Headcount, or `NA` | Preferred |
| `experience` | text | `lt5`, `5to10`, `gt10` | Yes |
| `sector` | text | `manufacturing`, `distribution_retail`, `3pl_logistics`, `other`, or `NA` | If collected |
| `ems` | integer | `1` certified EMS/ISO 14001, `0` none, `NA` not collected | If collected |
| `GSCI1`–`GSCI5` | integer | 1 to 5 | Yes |
| `RP1`–`RP4` | integer | 1 to 5 | Yes |
| `DI1`–`DI5` | integer | 1 to 5 | Yes |
| `TMC1`–`TMC4` | integer | 1 to 5 | Yes |
| `SP1`–`SP4` | integer | 1 to 5 | Yes |
| `CBI1`–`CBI4` | integer | 1 to 5 | Yes |
| `KSR1`–`KSR4` | integer | 1 to 5 | Yes |
| `GLP1`–`GLP4` | integer | 1 to 5 | Yes |

34 indicator columns in total, matching Table 1 of the manuscript.

---

## Coding rules

**Likert values.** Integers 1 to 5 only, where 1 = strongly disagree and 5 = strongly agree. No
decimals, no zeros, no blanks.

**Item direction.** All 34 items must run in the direction printed in Table 1, so that a higher score
means more of the construct. No item in Table 1 is reverse worded, so no recoding should be needed.
Confirm this before exporting, because a single reversed item will distort loadings, AVE, and every
downstream test.

**Missing values.** Enter `-99`. Do not leave cells empty and do not substitute the mean. State how
many missing values exist and I will apply and report a consistent treatment.

**Row order.** Irrelevant. Do not sort by group.

**Encoding.** UTF-8, comma separated. Excel exports are fine.

---

## Optional columns and why they matter

`country` is not needed for the statistics, but it resolves a separate weakness. The manuscript
classifies firms as developing or emerging without stating a criterion or listing countries, and the
comparative contribution rests entirely on that split. With country data the classification can be
anchored to a published standard such as the IMF World Economic Outlook grouping or the World Bank
income bands, and a country table can be added to Section 3.2.

`ems` supports the control that answers the reverse-causality comment most directly. Without it, that
control has to be dropped and the omitted common cause named openly in Section 6 instead.

`employees` allows firm size to enter as a log-transformed continuous control, which is preferable to
three bands. If unavailable, the bands will be used.

`sector` is described in Section 4.1 but does not appear in Table 3, which suggests it may not have
been recorded as a variable. If it was not collected, enter `NA` throughout and say so. Sector will
then be omitted from the controls rather than approximated.

---

## Validation before sending

The file should reproduce the published descriptives. Please check these, since a mismatch usually
means a wrong export, a reversed item, or a different working file.

**Group sizes.** developing = 100, emerging = 120.

**Table 3 marginals.**

| Variable | Expected counts |
|---|---|
| `role` | logistics_manager 84, sc_director 61, ops_sustainability 52, other_senior 23 |
| `firm_size` | small 47, medium 96, large 77 |
| `experience` | lt5 38, 5to10 92, gt10 90 |

**Table 8 construct means and standard deviations**, computed as the unweighted average of each
construct's items.

| Construct | Developing M (SD) | Emerging M (SD) | Pooled M (SD) |
|---|---|---|---|
| GSCI | 3.05 (0.62) | 3.98 (0.55) | 3.56 (0.74) |
| RP | 3.62 (0.58) | 4.18 (0.51) | 3.93 (0.61) |
| DI | 2.58 (0.66) | 4.07 (0.57) | 3.39 (0.92) |
| TMC | 3.01 (0.69) | 4.31 (0.52) | 3.72 (0.88) |
| SP | 2.88 (0.64) | 3.92 (0.59) | 3.45 (0.78) |
| CBI | 3.00 (0.67) | 3.79 (0.62) | 3.43 (0.74) |
| KSR | 2.79 (0.63) | 4.02 (0.56) | 3.46 (0.86) |
| GLP | 3.04 (0.65) | 4.21 (0.53) | 3.68 (0.86) |

Small rounding differences are expected. Differences beyond roughly 0.05 are not, and should be
investigated before the file is used.

---

## What will be produced from the file

1. Measurement model reproduction, checked against Tables 4 and 5, including loadings, CR, AVE,
   Fornell-Larcker, and HTMT.
2. Structural model reproduction, checked against Table 6, with bootstrapping at 5,000 subsamples.
3. Exact R-squared values for TMC, GSCI, DI, and GLP, replacing the vague "0.54 to 0.62 range across
   specifications" phrasing in Section 4.3.
4. Controls model, giving the largest change in any standardised coefficient.
5. Kolmogorov-Smirnov normality tests for all seven construct scores.
6. Gaussian copula terms, individually and jointly specified, with adjusted path estimates. Completes
   Table 14.
7. Models 2 and 3 estimated, with CVPAT contrasts against Model 1. Completes Table 15.
8. MICOM measurement invariance testing for the developing and emerging groups, which the multi-group
   analysis in Section 4.4 currently omits and which is a prerequisite for interpreting group
   differences in path coefficients.
9. Any divergence between these estimates and the published tables reported plainly rather than
   smoothed over.
