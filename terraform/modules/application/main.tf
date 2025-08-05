variable "network_name" {
  description = "Docker network name"
  type        = string
}

variable "database_url" {
  description = "Database connection string"
  type        = string
}

resource "docker_image" "app" {
  name = "app:latest"
  build {
    context = "../../../docker/app"
  }
}

resource "docker_container" "app" {
  name  = "python-app"
  image = docker_image.app.latest
  
  env = [
    "DATABASE_URL=${var.database_url}"
  ]
  
  networks_advanced {
    name = var.network_name
  }
  
  ports {
    internal = 5000
    external = 5000
  }
}

output "app_container_id" {
  value = docker_container.app.id
}

output "app_container_name" {
  value = docker_container.app.name
} 