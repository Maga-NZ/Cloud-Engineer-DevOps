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

module "network" {
  source = "./modules/network"
}

module "database" {
  source = "./modules/database"
  network_name = module.network.network_name
}

module "application" {
  source = "./modules/application"
  network_name = module.network.network_name
  database_url = module.database.connection_string
}

module "monitoring" {
  source = "./modules/monitoring"
  network_name = module.network.network_name
} 