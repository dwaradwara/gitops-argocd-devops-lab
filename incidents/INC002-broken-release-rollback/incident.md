# INC002 - Broken GitOps Release and Git Rollback

## Scenario

A deliberately broken release was deployed through the GitOps workflow.

Known-good image:

`tbc-gitops-api:v1`

Broken image:

`tbc-gitops-api:v2-broken`

The broken container started Uvicorn on port 9000 while Kubernetes expected the application on port 8000.

## Symptoms

ArgoCD reported:

- Sync Status: Synced
- Health Status: Degraded

The new pod remained unready and eventually entered restart behavior.

Kubernetes events showed readiness and liveness probe failures:

`connect: connection refused` on port `8000`.

## Investigation

Commands used:

```bash
kubectl get pods -n tbc-gitops
kubectl describe pod <pod> -n tbc-gitops
kubectl logs <pod> -n tbc-gitops
kubectl get events -n tbc-gitops
