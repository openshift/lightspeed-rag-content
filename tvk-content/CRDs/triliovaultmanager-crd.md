# TrilioVaultManager CRD

## Overview

The TrilioVaultManager (TVM) CR is the primary resource for installing and managing TrilioVault for Kubernetes. The TVK operator watches TVM CRs and reconciles the TVK control plane via Helm. Creating a TVM CR triggers installation; updating it triggers upgrades or config changes.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.tvkInstanceName` | string | Display name for the TVK instance | No |
| `spec.metadataJobResources` | ResourceRequirements | Resources for metadata jobs | No |
| `spec.dataJobResources` | ResourceRequirements | Resources for data mover jobs | No |
| `spec.targetBrowserResources` | ResourceRequirements | Resources for target browser | No |
| `spec.nodeSelector` | map[string]string | Node selector for TVK pods | No |
| `spec.affinity` | Affinity | Pod affinity rules | No |
| `spec.tolerations` | []Toleration | Pod tolerations | No |
| `spec.workerJobsSchedulingConfig` | object | Scheduling config for worker jobs | No |
| `spec.ingressConfig.host` | string | Hostname for the management console | No |
| `spec.ingressConfig.tlsSecretName` | string | TLS secret for HTTPS | No |
| `spec.ingressConfig.ingressClass` | string | Ingress class name | No |
| `spec.ingressConfig.ingressEnabled` | bool | Enable Ingress-based UI access | No |
| `spec.gatewayAPI.enabled` | bool | Enable Gateway API-based UI access | No |
| `spec.gatewayAPI.host` | string | Hostname when using Gateway API | No |
| `spec.gatewayAPI.gatewayConfig` | object | Gateway class / gateway reference / TLS config | No |
| `spec.componentConfiguration` | object | Per-component resources and settings (keys use kebab-case, e.g. `control-plane`, `web-backend`, `ingress-controller`, `admission-webhook`, `gateway-controller`, `web`, `exporter`, `exporter`) | No |
| `spec.logConfig.logLevel` | string | Log level: `Panic`, `Fatal`, `Error`, `Warn`, `Info`, `Debug`, `Trace` | No |
| `spec.logConfig.datamoverLogLevel` | string | Datamover log level (same enum as `logLevel`) | No |
| `spec.csiConfig` | object | CSI driver include/exclude lists | No |
| `spec.pauseSchedule` | bool | Pause all scheduled backups | No |
| `spec.helmValues` | object | Extra Helm values passed to TVK chart | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `Initialized`, `Deployed`, `Updated`, `ReleaseFailed`, `Irreconcilable` |
| `status.releaseVersion` | string | Deployed TVK version |
| `status.dashboard` | string | URL of the management console |
| `status.conditions` | []Condition | Detailed condition history |

## Status Condition Reasons

| Reason | Description |
|--------|-------------|
| `InstallSuccessful` | TVK installed successfully |
| `UpdateSuccessful` | TVK updated successfully |
| `InstallError` | Installation failed |
| `UpdateError` | Upgrade failed |
| `ReconcileError` | Reconciliation failed |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: TrilioVaultManager
metadata:
  name: triliovault-manager
  namespace: trilio-system
spec:
  applicationScope: Cluster
  tvkInstanceName: my-tvk
  logConfig:
    logLevel: Info
    datamoverLogLevel: Info
  dataJobResources:
    limits:
      memory: 4Gi
      cpu: "2"
  ingressConfig:
    host: tvk.example.com
    tlsSecretName: tvk-tls
  componentConfiguration:
    ingress-controller:
      enabled: true
      service:
        type: LoadBalancer
```

## Related Resources

- [Installation Guide](../operators/triliovault-for-kubernetes/installation.md)
- [Configuration Guide](../operators/triliovault-for-kubernetes/configuration.md)
