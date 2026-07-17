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
