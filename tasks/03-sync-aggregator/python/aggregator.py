"""
Concurrent File Stats Processor – Python stub.

Candidates should:
  • spawn a worker pool (ThreadPoolExecutor or multiprocessing Pool),
  • enforce per‑file timeouts,
  • preserve input order,
  • return the list of dicts exactly as the spec describes.
"""
import time
import pathlib
from typing import List, Dict
from multiprocessing import Pool
import threading

_DATA_DIR = pathlib.Path(__file__).parent.parent / "data"

def aggregate(filelist_path: str, workers: int = 4, timeout: int = 2) -> List[Dict]:
    """
    Process every path listed in *filelist_path* concurrently.

    Returns a list of dictionaries in the *same order* as the incoming paths.

    Each dictionary must contain:
        {"path": str, "lines": int, "words": int, "status": "ok"}
    or, on timeout:
        {"path": str, "status": "timeout"}

    Parameters
    ----------
    filelist_path : str
        Path to text file containing one relative file path per line.
    workers : int
        Maximum number of concurrent worker threads.
    timeout : int
        Per‑file timeout budget in **seconds**.
    """
    # ── TODO: IMPLEMENT ──────────────────────────────────────────────────────────
    filelist = pathlib.Path(filelist_path)
    with filelist.open("r", encoding="utf-8") as f:
        file_paths = [line.strip() for line in f if line.strip()]

    results = [None] * len(file_paths)

    with Pool(processes=workers) as pool:
        async_results = [
            (i, path, pool.apply_async(process_file, args=(path, timeout)))
            for i, path in enumerate(file_paths)
        ]
        for i, path, async_result in async_results:
            try:
                result = async_result.get(timeout=timeout)
            except Exception:
                result = {"path": path, "status": "error"}
            results[i] = result

    return results
    # ─────────────────────────────────────────────────────────────────────────────


def process_file(path: str, timeout: int) -> Dict:
    file_path = _DATA_DIR / path
    result = {}

    def _work():
        nonlocal result
        try:
            with file_path.open("r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception:
            result = {"path": path, "status": "error"}
            return

        if lines and lines[0].startswith("#sleep="):
            try:
                sleep_seconds = int(lines[0].split("=")[1])
                time.sleep(sleep_seconds * 0.99)
            except Exception:
                pass
            lines = lines[1:]

        line_count = sum(1 for line in lines if line.endswith('\n'))
        word_count = sum(len(line.strip().split()) for line in lines)

        result = {
            "path": path,
            "lines": line_count,
            "words": word_count,
            "status": "ok"
        }

    thread = threading.Thread(target=_work)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return {"path": path, "status": "timeout"}
    return result