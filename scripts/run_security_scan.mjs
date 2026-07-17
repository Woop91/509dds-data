import { spawnSync } from "node:child_process";

const mode = process.argv[2];
const cwd = process.cwd();

const scans = {
  gitleaks: [
    "run", "--rm", "-v", `${cwd}:/repo`, "-w", "/repo",
    "zricethezav/gitleaks:v8.21.2",
    "detect", "--no-banner", "--source=/repo",
    "--config=/repo/.gitleaks.toml",
    "--baseline-path=/repo/.security/gitleaks-baseline.json",
  ],
  semgrep: [
    "run", "--rm", "-v", `${cwd}:/src`, "-w", "/src",
    "semgrep/semgrep:1.91.0", "semgrep",
    "--config=p/security-audit", "--config=p/javascript", "--config=p/python",
    "--config=/src/.semgrep.yml", "/src",
  ],
};

if (!(mode in scans)) {
  process.stderr.write("Usage: node scripts/run_security_scan.mjs <gitleaks|semgrep>\n");
  process.exit(2);
}

const result = spawnSync("docker", scans[mode], {
  cwd,
  stdio: "inherit",
  windowsHide: true,
});

if (result.error) {
  process.stderr.write(`Security scan launcher failed: ${result.error.message}\n`);
  process.exit(1);
}
process.exit(result.status ?? 1);
