# Data archive worklist

## SYS-DATA-SCANNER-RESANITIZE-20260717 — done

Revalidate preserved external data after expanding the credential scanner.
Remove any newly detected tracked client credential and prevent recurrence.

Acceptance evidence:

- corrected whole-tree scan reports zero findings;
- the external page retains an explicit removal marker, not a credential value;
- strict exact-head candidate recovery passes;
- exact branch is pushed while the GitHub repository finishes archived;
- independent read-only final review passes.

## DATA-REFRESH-AND-PEER-CHART-20260716 — done

Own the stable SSA/CTHRU refresh outputs and the ten-year Massachusetts peer
comparison. Regression coverage locks schedules, filenames, periods, and peers.

## SYS-SECURITY-ARCHIVE-GATES-20260716 — done

Own the Husky, Gitleaks, Semgrep, and base-ref security gates for this archive.

## DATA-MARKITDOWN-ARCHIVE-20260716 — done

Own the MarkItDown converter and 78 recovered ingestion bundles. Regression
coverage requires metadata, checksums, Markdown, and parseable source hashes.

## DATA-PRR-EVIDENCE-20260716 — done

Own the recovered DDS telework evidence chain and split MassAbility PRR
templates. Regression coverage requires the source chain, templates, and
metadata to remain present and parseable.

## SYS-FLEET-RECOVERY-LEDGER-20260716 — done

Own the exact-SHA regression and worklist ledger that caused these historical
gaps to fail closed instead of disappearing from fleet review.

## SYS-SECURITY-BASE-REF-20260716 — done

Own the security workflow base-ref boundary and its regression gate so untrusted
pull-request input cannot enter shell commands directly.

## SYS-CATALOG-INTEGRITY-20260716 — done

Own catalog validation that excludes ingestion bundles and rejects dangling
metadata references.
