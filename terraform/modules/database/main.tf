variable "network_name" {
  description = "Docker network name"
  type        = string
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

resource "docker_image" "postgres" {
  name = "postgres:13-alpine"
}

resource "docker_volume" "postgres_data" {
  name = "postgres_data"
}

resource "docker_container" "postgres" {
  name  = "database"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}"
  ]

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

  networks_advanced {
    name = var.network_name
  }
}

output "connection_string" {
  value     = "postgresql://${var.postgres_user}:${var.postgres_password}@${docker_container.postgres.name}:5432/${var.postgres_db}"
  sensitive = true
}

output "container_id" {
  value = docker_container.postgres.id
} 