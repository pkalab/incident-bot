import os
import subprocess


def run() -> dict:
    try:
        result = subprocess.run(
            ["python3", "-c", "import os; print(os.cpu_count() or 'unknown')"],
            capture_output=True, text=True, timeout=10,
        )
        cpu_count_str = result.stdout.strip()
        cpu_count = int(cpu_count_str) if cpu_count_str.isdigit() else 1
        load_avg = os.getloadavg() if hasattr(os, "getloadavg") else (0, 0, 0)
        return {
            "status": "pass" if load_avg[0] < cpu_count else "warn",
            "summary": f"CPU cores: {cpu_count}, Load avg: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}",
            "details": f"1min: {load_avg[0]:.2f}\n5min: {load_avg[1]:.2f}\n15min: {load_avg[2]:.2f}",
        }
    except Exception as e:
        return {"status": "fail", "summary": "CPU check failed", "details": str(e)}
