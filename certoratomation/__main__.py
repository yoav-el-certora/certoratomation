import argparse

from certoratomation.cli import run_certora_automation

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Certora Automation Server")
    parser.add_argument("-r", "--run_server", action="store_true", help="Run Certora Automation Server")
    parser.add_argument("-c", "--run_ci", action="store_true", help="Run Certora Automation CI Tests")
    args = parser.parse_args()

    run_certora_automation()

