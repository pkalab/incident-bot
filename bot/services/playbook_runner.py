import importlib
from datetime import datetime
from typing import Optional

from bot.models.incident import PlaybookResult

PLAYBOOKS = {
    "cpu-check": "bot.playbooks.cpu_check",
    "memory-check": "bot.playbooks.memory_check",
    "network-check": "bot.playbooks.network_check",
}


def list_playbooks() -> list[str]:
    return list(PLAYBOOKS.keys())


def run_playbook(name: str) -> Optional[PlaybookResult]:
    module_path = PLAYBOOKS.get(name)
    if not module_path:
        return None
    try:
        module = importlib.import_module(module_path)
        result = module.run()
        return PlaybookResult(
            playbook_name=name,
            status=result["status"],
            summary=result["summary"],
            details=result["details"],
            ran_at=datetime.now(),
        )
    except Exception as e:
        return PlaybookResult(
            playbook_name=name,
            status="fail",
            summary=f"Playbook execution error: {e}",
            details=str(e),
            ran_at=datetime.now(),
        )
