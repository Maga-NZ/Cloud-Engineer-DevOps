variable "network_name" {
  description = "Docker network name"
  type        = string
}

resource "docker_container" "prometheus" {
  name  = "prometheus"
  image = "prom/prometheus:latest"
  
  networks_advanced {
    name = var.network_name
  }
  
  ports {
    internal = 9090
    external = 9090
  }
  
  volumes {
    host_path      = "${path.module}/../../../monitoring/prometheus/prometheus.yml"
    container_path = "/etc/prometheus/prometheus.yml"
  }
}

resource "docker_container" "grafana" {
  name  = "grafana"
  image = "grafana/grafana:latest"
  
  env = [
    "GF_SECURITY_ADMIN_PASSWORD=admin"
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