# GitOps ArgoCD DevOps Lab

Hands-on GitOps delivery lab demonstrating Docker, Kubernetes, ArgoCD, CI/CD, configuration drift detection, automated self-healing, deployment troubleshooting, Git-based rollback, and safe rolling releases.

## Architecture

```text
Developer
   |
   v
GitHub Repository
   |
   +---- GitHub Actions CI
   |        |
   |        +-- Python validation
   |        +-- Kubernetes YAML validation
   |        +-- Docker build
   |        +-- application health test
   |
   v
ArgoCD
   |
   | watches k8s/base
   v
Kubernetes / kind
   |
   +-- FastAPI Deployment (2 replicas)
   +-- ClusterIP Service
   +-- ConfigMap
   +-- Secret
   +-- readiness probe
   +-- liveness probe
```

## Technology Stack

- Linux / WSL2
- Docker
- Kubernetes
- kind
- ArgoCD
- Git / GitHub
- GitHub Actions
- FastAPI / Python
- ConfigMaps and Secrets
- readiness and liveness probes

## GitOps Workflow

```text
Git change
   |
   v
GitHub
   |
   v
ArgoCD detects desired-state change
   |
   v
Kubernetes reconciliation
   |
   v
Rolling deployment
   |
   v
Health validation
```

Git is the source of truth for the Kubernetes application configuration.

## Successful v2 Release

The application was upgraded from:

`tbc-gitops-api:v1`

to:

`tbc-gitops-api:v2`

through Git rather than a direct cluster modification.

Final validation:

```text
Deployment:    2/2 Ready
ArgoCD Sync:   Synced
ArgoCD Health: Healthy
Application:   version v2
```

The application returned:

```json
{
  "application": "tbc-gitops-api",
  "version": "v2",
  "message": "Successful v2 release through ArgoCD"
}
```

## Controlled Incident Summary

| Incident | Failure | Diagnosis | Recovery |
|---|---|---|---|
| INC001 | Manual replica drift from 2 to 5 | Git desired state differed from live Kubernetes state | ArgoCD self-healed back to 2 |
| INC002 | Broken image listened on port 9000 while probes expected 8000 | Readiness/liveness failures and container logs | Git rollback to v1 |
| INC003 | Deployment referenced a nonexistent Kubernetes Secret | `CreateContainerConfigError` and Kubernetes events | `git revert` restored valid configuration |

## INC001 - Configuration Drift and Self-Healing

Git defined:

```yaml
replicas: 2
```

A manual change modified the live Deployment:

```bash
kubectl scale deployment tbc-gitops-api \
  -n tbc-gitops \
  --replicas=5
```

ArgoCD detected that the live state no longer matched Git.

Because automated synchronization and self-healing were enabled, ArgoCD restored the Deployment from 5 replicas back to the Git-defined value of 2.

Final state:

```text
Deployment:    2/2 Ready
ArgoCD Sync:   Synced
ArgoCD Health: Healthy
```

## INC002 - Broken Release

A deliberately broken image was deployed:

`tbc-gitops-api:v2-broken`

The container started Uvicorn on port 9000 while Kubernetes readiness and liveness probes expected port 8000.

ArgoCD reported:

```text
Sync Status:   Synced
Health Status: Degraded
```

This demonstrates an important GitOps distinction:

- **Synced** means Kubernetes matches the desired configuration in Git.
- **Healthy** means the deployed resources are functioning successfully.

Investigation used:

```bash
kubectl get pods
kubectl describe pod
kubectl logs
kubectl get events
```

Container logs revealed:

```text
Uvicorn running on http://0.0.0.0:9000
```

The failed release never became Ready.

The existing v1 replicas remained healthy, so the Kubernetes Service continued routing traffic only to working pods.

The deployment was recovered by returning Git to the known-good v1 image and allowing ArgoCD to reconcile the cluster.

## INC003 - Missing Kubernetes Secret

The Deployment was intentionally changed to reference:

`tbc-gitops-secret-missing`

The Secret did not exist.

The new pod entered:

```text
CreateContainerConfigError
```

Kubernetes events identified the root cause:

```text
secret "tbc-gitops-secret-missing" not found
```

Application logs were unavailable because the container never reached startup.

The faulty Git commit was reverted with Git, pushed to the repository, and ArgoCD reconciled Kubernetes automatically.

Final state:

```text
Deployment:    2/2 Ready
ArgoCD Sync:   Synced
ArgoCD Health: Healthy
```

## CI Validation

GitHub Actions validates changes on pushes and pull requests.

The workflow performs:

- Python syntax validation
- Kubernetes YAML validation
- Docker image build
- container startup
- FastAPI health-endpoint validation

## Repository Structure

```text
gitops-argocd-devops-lab/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── Dockerfile
│   ├── Dockerfile.v2-broken
│   ├── main.py
│   └── requirements.txt
├── incidents/
│   ├── INC001-config-drift-self-heal/
│   ├── INC002-broken-release-rollback/
│   └── INC003-missing-secret-reference/
├── k8s/
│   ├── argocd/
│   │   └── application.yaml
│   └── base/
│       ├── configmap.yaml
│       ├── deployment.yaml
│       ├── secret.yaml
│       └── service.yaml
└── README.md
```

## Security Note

The Kubernetes Secret stored in this repository contains only a non-sensitive lab demonstration value.

Real production secrets should not be stored as plaintext in Git. Production GitOps environments should use an appropriate secrets-management approach such as Vault, External Secrets, or encrypted/sealed secrets.

## Skills Demonstrated

- ArgoCD GitOps
- Kubernetes operations
- Docker containerization
- GitHub Actions CI/CD
- Git as source of truth
- configuration drift detection
- automated reconciliation and self-healing
- Kubernetes rolling deployments
- readiness and liveness probes
- ConfigMaps and Secrets
- incident troubleshooting
- Git-based rollback
- root-cause analysis

## Portfolio Scope

This is an isolated hands-on technical lab. All failures were deliberately introduced for training and demonstration purposes and do not represent production incidents or customer systems.