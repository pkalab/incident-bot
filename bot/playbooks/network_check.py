import subprocess

TARGETS = ["api.github.com", "google.com", "aws.amazon.com"]


def run() -> dict:
    results = []
    failures = 0
    for target in TARGETS:
        try:
            r = subprocess.run(
                ["ping", "-c", "1", "-W", "2", target],
                capture_output=True, text=True, timeout=5,
            )
            if r.returncode == 0:
                results.append(f":white_check_mark: {target} — reachable")
            else:
                results.append(f":x: {target} — unreachable")
                failures += 1
        except Exception:
            results.append(f":x: {target} — error")
            failures += 1
    return {
        "status": "pass" if failures == 0 else "warn",
        "summary": f"Network: {len(TARGETS) - failures}/{len(TARGETS)} targets reachable",
        "details": "\n".join(results),
    }
