terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  description = "AWS Jakarta Region"
  default     = "ap-southeast-3"
}

variable "cluster_name" {
  type        = string
  description = "EKS Cluster Name"
  default     = "indibank-eks-cluster"
}

# 1. VPC & Networking for EKS
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "indibank-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["ap-southeast-3a", "ap-southeast-3b", "ap-southeast-3c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}

# 2. Amazon Elastic Kubernetes Service (EKS)
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.30"

  cluster_endpoint_public_access = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    indibank_nodes = {
      instance_types = ["m6i.xlarge"] # 4 vCPU, 16 GB RAM for Oracle, Kafka, Redis, Java
      min_size       = 1
      max_size       = 3
      desired_size   = 1
    }
  }
}

# 3. Amazon Elastic Container Registry (ECR)
resource "aws_ecr_repository" "indibank_repo" {
  name                 = "indibank-engine"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.indibank_repo.repository_url
}
