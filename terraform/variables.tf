variable "project_id" {
  type        = string
  description = "GCP Project ID"
  default     = "aldianfazrihady"
}

variable "region" {
  type        = string
  description = "GCP Region (Jakarta, Indonesia)"
  default     = "asia-southeast2"
}

variable "zone" {
  type        = string
  description = "GCP Zone"
  default     = "asia-southeast2-a"
}

variable "cluster_name" {
  type        = string
  description = "GKE Cluster Name"
  default     = "indibank-gke-cluster"
}

variable "node_machine_type" {
  type        = string
  description = "Compute instance machine type for GKE node (4 vCPU, 16GB RAM for Oracle, Kafka, Redis, Java)"
  default     = "e2-standard-4"
}
