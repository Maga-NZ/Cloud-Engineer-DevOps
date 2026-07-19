#!/usr/bin/env python3

import argparse
import logging
import shutil
import subprocess
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def detect_compose_command():
    """Return the available Docker Compose command as a list of args."""
    if shutil.which("docker"):
        try:
            subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                check=True,
            )
            return ["docker", "compose"]
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    logger.error("Neither 'docker compose' nor 'docker-compose' is available")
    sys.exit(1)


class DeploymentManager:
    def __init__(self, environment):
        self.environment = environment
        self.project_root = Path(__file__).parent.parent.parent
        self.compose_cmd = detect_compose_command()

    def run_command(self, command, cwd=None):
        """Execute a command given as a list of arguments (no shell)."""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                check=True,
            )
            logger.info("Command executed successfully: %s", " ".join(command))
            return result.returncode
        except FileNotFoundError:
            logger.error("Executable not found: %s", command[0])
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            logger.error("Command failed (%s): %s", e.returncode, " ".join(command))
            sys.exit(1)

    def deploy_infrastructure(self):
        """Deploy infrastructure using Terraform."""
        logger.info("Deploying infrastructure...")
        terraform_dir = self.project_root / "terraform"

        self.run_command(["terraform", "init"], cwd=terraform_dir)
        self.run_command(["terraform", "plan"], cwd=terraform_dir)
        self.run_command(
            ["terraform", "apply", "-auto-approve"], cwd=terraform_dir
        )

    def deploy_application(self):
        """Deploy application using Docker Compose."""
        logger.info("Deploying application...")

        self.run_command(self.compose_cmd + ["down"])
        self.run_command(self.compose_cmd + ["build"])
        self.run_command(self.compose_cmd + ["up", "-d"])

    def run_ansible(self):
        """Run Ansible playbooks."""
        logger.info("Running Ansible playbooks...")
        ansible_dir = self.project_root / "ansible"

        self.run_command(
            [
                "ansible-playbook",
                "-i",
                "inventory/hosts.yml",
                "playbooks/main.yml",
            ],
            cwd=ansible_dir,
        )

    def health_check(self, url="http://localhost:8080/health", max_retries=30):
        """Perform health checks."""
        logger.info("Performing health checks...")

        import requests

        for _ in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    logger.info("Application is healthy")
                    return True
            except requests.RequestException:
                pass
            time.sleep(2)

        logger.error("Health check failed")
        return False


def main():
    parser = argparse.ArgumentParser(description="Deployment script")
    parser.add_argument(
        "--environment", default="dev", choices=["dev", "staging", "prod"]
    )
    parser.add_argument("--skip-infrastructure", action="store_true")
    parser.add_argument("--skip-ansible", action="store_true")

    args = parser.parse_args()

    deployer = DeploymentManager(args.environment)

    if not args.skip_infrastructure:
        deployer.deploy_infrastructure()

    deployer.deploy_application()

    if not args.skip_ansible:
        deployer.run_ansible()

    if deployer.health_check():
        logger.info("Deployment completed successfully")
    else:
        logger.error("Deployment failed health checks")
        sys.exit(1)


if __name__ == "__main__":
    main()
