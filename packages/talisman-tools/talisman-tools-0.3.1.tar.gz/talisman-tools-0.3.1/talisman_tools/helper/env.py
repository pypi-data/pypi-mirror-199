import os


def get_max_concurrent_threads(*, default: int = 20) -> int:
    max_threads = os.getenv("MAX_CONCURRENT_THREADS")
    return int(max_threads) if max_threads else default


def get_max_spawned_processes() -> int:
    max_spawned_processes = os.environ.get('MAX_SPAWNED_PROCESSES')
    return int(max_spawned_processes) if max_spawned_processes is not None else min(os.cpu_count(), 8)


def get_max_treated_jobs() -> int:
    max_treated_jobs = os.environ.get('MAX_TREATED_JOBS')
    return int(max_treated_jobs) if max_treated_jobs is not None else 5
