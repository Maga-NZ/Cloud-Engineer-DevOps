#!/usr/bin/env python3

import argparse
import logging
import sys
import time

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        
    def check_application_health(self):
        """Check application health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Application health: {data}")
                return True
            else:
                logger.error(f"Health check failed with status: {response.status_code}")
                return False
        except requests.RequestException as e:
            logger.error(f"Health check error: {e}")
            return False
    
    def check_metrics_endpoint(self):
        """Check Prometheus metrics endpoint"""
        try:
            response = requests.get(f"{self.base_url}/metrics", timeout=5)
            if response.status_code == 200:
                logger.info("Metrics endpoint is accessible")
                return True
            else:
                logger.error(f"Metrics check failed with status: {response.status_code}")
                return False
        except requests.RequestException as e:
            logger.error(f"Metrics check error: {e}")
            return False
    
    def check_database_connection(self):
        """Check database connection through API"""
        try:
            response = requests.get(f"{self.base_url}/api/data", timeout=5)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Database connection: {data}")
                return True
            else:
                logger.error(f"Database check failed with status: {response.status_code}")
                return False
        except requests.RequestException as e:
            logger.error(f"Database check error: {e}")
            return False
    
    def run_all_checks(self):
        """Run all health checks"""
        logger.info("Starting health checks...")
        
        checks = {
            "application": self.check_application_health(),
            "metrics": self.check_metrics_endpoint(),
            "database": self.check_database_connection()
        }
        
        all_passed = all(checks.values())
        
        if all_passed:
            logger.info("All health checks passed")
        else:
            logger.error("Some health checks failed")
            
        return checks

def main():
    parser = argparse.ArgumentParser(description="Application health checker")
    parser.add_argument(
        "--url",
        default="http://localhost:8080",
        help="Base URL of the application (default: http://localhost:8080)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run the checks a single time and exit with a status code",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Seconds between checks in continuous mode (default: 60)",
    )
    args = parser.parse_args()

    checker = HealthChecker(base_url=args.url)

    if args.once:
        checks = checker.run_all_checks()
        sys.exit(0 if all(checks.values()) else 1)

    try:
        while True:
            checker.run_all_checks()
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logger.info("Stopping health checker")


if __name__ == "__main__":
    main() 