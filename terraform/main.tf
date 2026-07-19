terraform {
  required_version = ">= 1.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

variable "postgres_db" {
  description = "PostgreSQL database name"
  type        = string
  default     = "appdb"
}

variable "postgres_user" {
  description = "PostgreSQL user"
  type        = string
  default     = "user"
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "grafana_admin_password" {
  description = "Grafana admin password"
  type        = string
  sensitive   = true
}

module "network" {
  source = "./modules/network"
}

module "database" {
  source            = "./modules/database"
  network_name      = module.network.network_name
  postgres_db       = var.postgres_db
  postgres_user     = var.postgres_user
  postgres_password = var.postgres_password
}

module "application" {
  source       = "./modules/application"
  network_name = module.network.network_name
  database_url = module.database.connection_string
}

module "monitoring" {
  source                 = "./modules/monitoring"
  network_name           = module.network.network_name
  grafana_admin_password = var.grafana_admin_password
} 