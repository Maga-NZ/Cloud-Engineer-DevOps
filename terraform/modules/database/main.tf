variable "network_name" {
  description = "Docker network name"
  type        = string
}

resource "docker_volume" "postgres_data" {
  name = "postgres_data"
}

resource "docker_container" "postgres" {
  name  = "database"
  image = "postgres:13-alpine"
  
  env = [
    "POSTGRES_DB=appdb",
    "POSTGRES_USER=user",
    "POSTGRES_PASSWORD=password"
  ]
  
  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }
  
  networks_advanced {
    name = var.network_name
  }
  
  ports {
    internal = 5432
    external = 5432
  }
}

output "connection_string" {
  value = "postgresql://user:password@localhost:5432/appdb"
}

output "container_id" {
  value = docker_container.postgres.id
} 