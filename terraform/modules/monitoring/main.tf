variable "network_name" {
  description = "Docker network name"
  type        = string
}

variable "grafana_admin_password" {
  description = "Grafana admin password"
  type        = string
  sensitive   = true
}

resource "docker_image" "prometheus" {
  name = "prom/prometheus:latest"
}

resource "docker_image" "grafana" {
  name = "grafana/grafana:latest"
}

resource "docker_container" "prometheus" {
  name  = "prometheus"
  image = docker_image.prometheus.image_id

  networks_advanced {
    name = var.network_name
  }

  ports {
    internal = 9090
    external = 9090
  }

  volumes {
    host_path      = abspath("${path.module}/../../../monitoring/prometheus/prometheus.yml")
    container_path = "/etc/prometheus/prometheus.yml"
  }
}

resource "docker_container" "grafana" {
  name  = "grafana"
  image = docker_image.grafana.image_id

  env = [
    "GF_SECURITY_ADMIN_PASSWORD=${var.grafana_admin_password}"
  ]

  networks_advanced {
    name = var.network_name
  }

  ports {
    internal = 3000
    external = 3000
  }

  depends_on = [docker_container.prometheus]
}

output "prometheus_container_id" {
  value = docker_container.prometheus.id
}

output "grafana_container_id" {
  value = docker_container.grafana.id
} 