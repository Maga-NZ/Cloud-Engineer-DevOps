# Kubernetes Deployment

Manifests to run the application stack on Kubernetes.

## Contents

- `namespace.yaml` — dedicated `cloud-devops` namespace
- `secret.example.yaml` — example secret (do **not** apply as-is; create the real one out-of-band)
- `postgres.yaml` — PostgreSQL Deployment, headless Service and PVC
- `app.yaml` — application Deployment (liveness/readiness probes, resource limits) and Service
- `ingress.yaml` — Ingress (requires an ingress controller such as ingress-nginx)
- `hpa.yaml` — HorizontalPodAutoscaler (requires metrics-server)
- `kustomization.yaml` — bundles the resources (except the secret)

## Usage

1. Create the namespace and secret:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl -n cloud-devops create secret generic app-secrets \
  --from-literal=POSTGRES_DB=appdb \
  --from-literal=POSTGRES_USER=user \
  --from-literal=POSTGRES_PASSWORD='change-me' \
  --from-literal=DATABASE_URL='postgresql://user:change-me@postgres:5432/appdb'
```

2. Set the application image in `app.yaml` (replace `ghcr.io/OWNER/REPO/app:latest`).

3. Deploy everything:

```bash
kubectl apply -k k8s/
```

4. Add a hosts entry for the ingress host (local clusters):

```bash
echo "127.0.0.1 app.local" | sudo tee -a /etc/hosts
```
