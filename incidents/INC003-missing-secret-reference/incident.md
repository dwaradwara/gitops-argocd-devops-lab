# INC003 - Missing Kubernetes Secret Reference

## Scenario

A GitOps-managed Kubernetes Deployment was changed to reference a Secret that did not exist.

Valid Secret:

`tbc-gitops-secret`

Broken reference:

`tbc-gitops-secret-missing`

## Symptoms

The new pod failed with:

`CreateContainerConfigError`

Kubernetes events reported:

`secret "tbc-gitops-secret-missing" not found`

ArgoCD reported:

- Sync Status: Synced
- Health Status: Degraded

## Investigation

Commands used:

```bash
kubectl get pods -n tbc-gitops
kubectl describe pod <pod> -n tbc-gitops
kubectl get events -n tbc-gitops
kubectl logs <pod> -n tbc-gitops
