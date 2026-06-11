# Infrastructure (IaC)

Bicep / Terraform definitions for deploying the agent service to Azure.

The course builds this out in **Week 9 (Hosting & Scale)**. The default target is
**Azure Container Apps** (KEDA autoscale, scale-to-zero); graduate to **AKS** only
when you need cluster-level control.

## Planned modules
- `main.bicep` — resource group composition
- `container-app.bicep` — Container Apps environment + app
- `acr.bicep` — Azure Container Registry
- `observability.bicep` — Application Insights + Log Analytics

> TODO (Week 9): implement Bicep modules and wire them into the GitHub Actions
> deploy job using OIDC federated credentials (no secrets in pipeline).
