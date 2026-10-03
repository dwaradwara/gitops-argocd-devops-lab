# INC001 - Configuration Drift and ArgoCD Self-Healing

## Scenario

The Git repository defined the application Deployment with 2 replicas.

A manual change was introduced directly into the Kubernetes cluster:

```bash
kubectl scale deployment tbc-gitops-api \
  -n tbc-gitops \
  --replicas=5
