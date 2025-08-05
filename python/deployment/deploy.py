#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeploymentManager:
    def __init__(self, environment):
        self.environment = environment
        self.project_root = Path(__file__).parent.parent.parent
        
    def run_command(self, command, cwd=None):
        """Execute shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"Command executed successfully: {command}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {command}")
            logger.error(f"Error: {e.stderr}")
            sys.exit(1)
    
    def deploy_infrastructure(self):
        """Deploy infrastructure using Terraform"""
        logger.info("Deploying infrastructure...")
        terraform_dir = self.project_root / "terraform"
        
        self.run_command("terraform init", cwd=terraform_dir)
        self.run_command("terraform plan", cwd=terraform_dir)
        self.run_command("terraform apply -auto-approve", cwd=terraform_dir)
        
    def deploy_application(self):
        """Deploy application using Docker Compose"""
        logger.info("Deploying application...")
        
        self.run_command("docker-compose down")
        self.run_command("docker-compose build")
        self.run_command("docker-compose up -d")
        
    def run_ansible(self):
        """Run Ansible playbooks"""
        logger.info("Running Ansible playbooks...")
        ansible_dir = self.project_root / "ansible"
        
        self.run_command("ansible-playbook playbooks/main.yml", cwd=ansible_dir)
        
    def health_check(self):
        """Perform health checks"""
        logger.info("Performing health checks...")
        
        import requests
        import time
        
        max_retries = 30
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = requests.get("http://localhost:8080/health", timeout=5)
                if response.status_code == 200:
                    logger.info("Application is healthy")
                    return True
            except requests.RequestException:
                pass
            
            retry_count += 1
            time.sleep(2)
            
        logger.error("Health check failed")
        return False

def main():
    parser = argparse.ArgumentParser(description="Deployment script")
    parser.add_argument("--environment", default="dev", choices=["dev", "staging", "prod"])
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