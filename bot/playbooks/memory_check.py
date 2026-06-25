def run() -> dict:
    try:
        import psutil
        mem = psutil.virtual_memory()
        pct = mem.percent
        return {
            "status": "pass" if pct < 80 else "warn",
            "summary": f"Memory: {mem.used / 1e9:.1f}GB / {mem.total / 1e9:.1f}GB ({pct}%)",
            "details": f"Available: {mem.available / 1e9:.1f}GB\nUsed: {mem.used / 1e9:.1f}GB\nPercent: {pct}%",
        }
    except ImportError:
        return {"status": "warn", "summary": "psutil not available", "details": "Install psutil for memory checks"}
    except Exception as e:
        return {"status": "fail", "summary": "Memory check failed", "details": str(e)}
