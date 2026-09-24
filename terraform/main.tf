provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Artifact Registry for IndiBank Microservice Images
resource "google_artifact_registry_repository" "indibank_repo" {
  location      = var.region
  repository_id = "indibank-repo"
  description   = "Docker repository for IndiBank Core Engine"
  format        = "DOCKER"
}

# 2. Static External IP for Domain Ingress (indibank.aldianapps.com)
resource "google_compute_address" "indibank_static_ip" {
  name   = "indibank-static-ip"
  region = var.region
}

# 3. GKE Cluster Definition (Standard Zonal Cluster in Jakarta)
resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.zone

  # Remove default node pool and create a customized one
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = "default"
  subnetwork = "default"

  deletion_protection = false

  ip_allocation_policy {}

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }
}

# 4. GKE Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "indibank-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    machine_type = var.node_machine_type
    disk_size_gb = 50
    disk_type    = "pd-balanced"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      app = "indibank"
    }

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }
}
