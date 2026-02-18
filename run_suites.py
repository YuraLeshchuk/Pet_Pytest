import configparser
import subprocess
from concurrent.futures import ThreadPoolExecutor

CONFIG_FILE = "test_suites.conf"


def parse_tests(raw: str) -> list[str]:
    return [line.strip() for line in raw.splitlines() if line.strip()]


def run_suite(name: str, tests: list[str]):
    cmd = [
        "pytest",
        *tests,
        f"--suite-name={name}",
    ]

    print(f"RUN SUITE: {name}")
    for t in tests:
        print(f"    - {t}")

    return subprocess.run(cmd).returncode


def main():
    cfg = configparser.ConfigParser()
    cfg.optionxform = str
    cfg.read(CONFIG_FILE)

    max_parallel = int(cfg["Configuration"].get("max-parallel-suites", 1))

    suites = []
    for suite, action in cfg["TestSuites"].items():
        if action.strip().lower() == "run":
            tests = parse_tests(cfg[suite]["tests"])
            suites.append((suite, tests))

    with ThreadPoolExecutor(max_workers=max_parallel) as pool:
        results = pool.map(lambda s: run_suite(*s), suites)

    exit(max(results, default=0))


if __name__ == "__main__":
    main()
