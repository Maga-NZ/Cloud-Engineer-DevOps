resource "docker_network" "app_network" {
  name = "app-network"
  driver = "bridge"
}

output "network_name" {
  value = docker_network.app_network.name
}

output "network_id" {
  value = docker_network.app_network.id
} 