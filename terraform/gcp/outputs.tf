output "gke_cluster_name" {
  description = "GKE Cluster Name"
  value       = google_container_cluster.primary.name
}

output "gke_cluster_endpoint" {
  description = "GKE Cluster Endpoint"
  value       = google_container_cluster.primary.endpoint
}

output "artifact_registry_repo" {
  description = "Docker Repository URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.indibank_repo.repository_id}"
}

output "ingress_static_ip" {
  description = "Static IP allocated for domain ingress"
  value       = google_compute_address.indibank_static_ip.address
}
