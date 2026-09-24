# IndiBank Multi-Platform Deployment Guide

This guide details how to deploy the **IndiBank Core Transaction & Ledger Engine** across multiple platforms:
1. [Local Development (Minikube & Kind)](#1-local-development-minikube--kind)
2. [On-Premise Red Hat OpenShift (OCP)](#2-on-premise-red-hat-openshift-ocp)
3. [Amazon Web Services (AWS EKS)](#3-amazon-web-services-aws-eks)
4. [Microsoft Azure (Azure AKS)](#4-microsoft-azure-azure-aks)
5. [Google Cloud Platform (GCP GKE - Live)](#5-google-cloud-platform-gcp-gke)

---

## 1. Local Development (Minikube & Kind)

### Prerequisites
* Docker installed and running
* `minikube` or `kind`
* `kubectl` and `helm`

### Option A: Using Minikube
```bash
# 1. Start Minikube with sufficient resources (min 4 vCPUs, 8GB RAM)
minikube start --cpus=4 --memory=8192 --disk-size=30g

# 2. Build image inside Minikube's Docker daemon
eval $(minikube docker-env)
docker build -t indibank-engine:latest .

# 3. Deploy using Helm
helm install indibank ./helm/indibank -f ./helm/indibank/values-local.yaml --namespace indibank --create-namespace

# 4. Access the Banking Dashboard & Swagger UI
minikube service indibank-core -n indibank
```

### Option B: Using Kind
```bash
# 1. Create a Kind cluster with port mapping
cat <<EOF | kind create cluster --name indibank --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8080
    protocol: TCP
EOF

# 2. Build & load image into Kind
docker build -t indibank-engine:latest .
kind load docker-image indibank-engine:latest --name indibank

# 3. Deploy via Helm
helm install indibank ./helm/indibank -f ./helm/indibank/values-local.yaml --namespace indibank --create-namespace

# 4. Open http://localhost:8080
```

---

## 2. On-Premise Red Hat OpenShift (OCP)

Indonesian enterprise banks (e.g. Bank Mandiri, BCA, BRI) frequently run on-premise OpenShift clusters.

### Security Context Constraints (SCC)
Oracle DB containers require specific file permissions and privileges:

```bash
# 1. Login to OpenShift cluster
oc login https://api.ocp-cluster.bank.local:6443

# 2. Create project / namespace
oc new-project indibank

# 3. Grant 'anyuid' SCC to service account for Oracle storage mounts
oc adm policy add-scc-to-user anyuid -z default -n indibank

# 4. Deploy using Helm with OpenShift values (Creates OpenShift Route automatically)
helm install indibank ./helm/indibank \
  -f ./helm/indibank/values-openshift.yaml \
  --namespace indibank

# 5. Get the generated OpenShift Route URL
oc get route indibank-route -n indibank
```

---

## 3. Amazon Web Services (AWS EKS)

### 1. Provision AWS EKS with Terraform
```bash
cd terraform/aws
terraform init
terraform apply -auto-approve
```

### 2. Push Image to Amazon ECR
```bash
# Login to ECR
aws ecr get-login-password --region ap-southeast-3 | \
  docker login --username AWS --password-stdin $(terraform output -raw ecr_repository_url)

# Tag and push image
docker tag indibank-engine:latest $(terraform output -raw ecr_repository_url):latest
docker push $(terraform output -raw ecr_repository_url):latest
```

### 3. Deploy via Helm
```bash
# Connect kubectl to EKS
aws eks update-kubeconfig --region ap-southeast-3 --name indibank-eks-cluster

# Deploy with AWS ALB Ingress values
helm install indibank ./helm/indibank \
  -f ./helm/indibank/values-aws.yaml \
  --set app.image.repository=$(terraform output -raw ecr_repository_url) \
  --namespace indibank --create-namespace
```

---

## 4. Microsoft Azure (Azure AKS)

### 1. Provision AKS with Terraform
```bash
cd terraform/azure
terraform init
terraform apply -auto-approve
```

### 2. Push Image to Azure ACR
```bash
az acr login --name indibankacr
docker tag indibank-engine:latest indibankacr.azurecr.io/indibank-engine:latest
docker push indibankacr.azurecr.io/indibank-engine:latest
```

### 3. Deploy via Helm
```bash
# Connect kubectl to AKS
az aks get-credentials --resource-group rg-indibank-prod --name indibank-aks-cluster

# Deploy with Azure AGIC values
helm install indibank ./helm/indibank \
  -f ./helm/indibank/values-azure.yaml \
  --namespace indibank --create-namespace
```

---

## 5. Google Cloud Platform (GCP GKE) - Live Reference

The current live deployment is hosted on GKE in Jakarta (`asia-southeast2`):
* **Live Dashboard:** [https://indibank.aldianapps.com](https://indibank.aldianapps.com)
* **Provisioned with:** `terraform/` (Google Provider)
* **Continuous Deployment:** Handled automatically via `.github/workflows/ci-cd.yml` on push to `main`.
