# Secret Rotation Runbook

If gitleaks failed to catch a secret before it landed in git history, follow this runbook **in order**. Do not skip steps — the rotation must happen before history rewrite, or attackers race the cleanup window.

## 1. Revoke at provider FIRST

Find the secret's provider and revoke the credential immediately:

| Provider | Console URL | Action |
|---|---|---|
| Supabase | supabase.com/dashboard → project → Settings → API | Rotate `service_role` and/or `anon` keys |
| Vercel | vercel.com/dashboard → project → Settings → Environment Variables | Remove + replace |
| Resend | resend.com/api-keys | Delete + re-create |
| Google Cloud (OAuth) | console.cloud.google.com → APIs & Services → Credentials | Delete client + create new |
| GitHub (PAT) | github.com/settings/tokens | Revoke + create new |
| AWS | console.aws.amazon.com → IAM → Users → Security credentials | Disable + delete key |

After revocation, audit the provider's access logs for misuse during the exposure window.

## 2. Audit access logs

Window: from the commit that introduced the secret to now. Look for:
- IP addresses outside expected ranges
- API calls that don't match normal app traffic patterns
- Spikes in usage

If misuse is detected, escalate immediately (do not continue with rotation in silence).

## 3. Rewrite git history

The secret is in the repo's git objects. Removing the file in a new commit is NOT enough — the blob is still reachable via the old commit SHA.

```bash
# Install git-filter-repo if missing:
# pip install git-filter-repo

# Replace <path-to-file> with the file containing the leaked secret:
git filter-repo --invert-paths --path <path-to-file> --force

# Force-push to origin (REQUIRES coordination with all collaborators):
git push --force-with-lease origin Main
```

Notify all collaborators: they must `git reset --hard origin/Main` after the force-push. Any branch or worktree based on the rewritten history must be reset.

## 4. Re-issue the credential

Create a new credential at the provider. Add it to:
- **Vercel:** `vercel env add` for each environment (Production, Preview, Development)
- **GitHub Actions:** Settings → Secrets and variables → Actions → New repository secret
- **Local `.env.local`** (developer machines): update via the team's normal channel (1Password, etc.)

Never commit the new credential. Trigger a new deploy after env vars are updated.

## 5. Add a gitleaks allowlist entry (if false positive)

If after triage you determined the "leak" was actually a fixture / known-safe value: add to `.gitleaks.toml`:

```toml
[[allowlist.commits]]
sha = "<the-commit-sha>"
# why: <one-line reason>
```

Commit the allowlist entry on Main. Future scans will skip it.

## 6. Post-mortem

Open a worklist item or issue capturing:
- How the secret got committed (no pre-commit? bypassed with `--no-verify`?)
- Detection timing (when committed → when caught)
- Rotation time (from detection → revoke)
- Process fix (e.g. "add provider X's secret pattern to .gitleaks.toml regexes")

Triage in the next review cycle.
