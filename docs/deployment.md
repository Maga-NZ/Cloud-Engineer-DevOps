# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ installed
- Terraform 1.0+ installed
- Ansible 2.9+ installed

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd cloud-engineer-devops
```

2. Start the infrastructure using Docker Compose:
```bash
docker-compose up -d
```

3. Verify the deployment:
```bash
curl http://localhost:8080/health
```

## Infrastructure Deployment

### Using Terraform

1. Navigate to the terraform directory:
```bash
cd terraform
```

2. Initialize Terraform:
```bash
terraform init
```

3. Plan the deployment:
```bash
terraform plan
```

4. Apply the configuration:
```bash
terraform apply
```

### Using Python Deployment Script

1. Run the deployment script:
```bash
python python/deployment/deploy.py --environment dev
```

## Configuration Management

### Using Ansible

1. Navigate to the ansible directory:
```bash
cd ansible
```

2. Run the main playbook:
```bash
ansible-playbook -i inventory/hosts.yml playbooks/main.yml
```

## Monitoring

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Troubleshooting

1. Check container status:
```bash
docker-compose ps
```

2. View logs:
```bash
docker-compose logs <service-name>
```

3. Health check:
```bash
python python/monitoring/health_check.py
``` 