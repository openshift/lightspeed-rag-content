# Configuring TrilioVault for Kubernetes

## Overview

TVK is configured primarily through the `TrilioVaultManager` (TVM) CR and Helm values. This guide covers key configuration areas including resources, logging, scheduling, ingress, and security.

## Resource Configuration

### Job Resources

Control resource limits for backup/restore data-plane jobs:

```yaml
apiVersion: triliovault.trilio.io/v1
kind: TrilioVaultManager
metadata:
  name: triliovault-manager
spec:
  metadataJobResources:
    limits:
      memory: 800Mi
      cpu: 200m
  dataJobResources:
    limits:
      memory: 2Gi
      cpu: "1"
  targetBrowserResources:
    limits:
      memory: 2Gi
      cpu: "1"
```

### Control Plane Resources

Configure via `componentConfiguration`:

```yaml
spec:
  componentConfiguration:
    controlPlane:
      resources:
        requests:
          cpu: 400m
          memory: 512Mi
```

## Logging

```yaml
spec:
  logConfig:
    logLevel: Info          # Trace, Debug, Info, Warning, Error
    datamoverLogLevel: Info
```

## Scheduling and Node Placement

```yaml
spec:
  nodeSelector:
    node-role.kubernetes.io/infra: ""
  tolerations:
    - key: "dedicated"
      operator: "Equal"
      value: "backup"
      effect: "NoSchedule"
```

For worker jobs (datamover pods):

```yaml
spec:
  workerJobsSchedulingConfig:
    nodeSelector:
      backup-node: "true"
    tolerations:
      - key: "backup"
        operator: "Exists"
```

## Ingress and Management Console

| Option | Description | Default |
|--------|-------------|---------|
| `ingressConfig.host` | Hostname for the UI | "" |
| `ingressConfig.tlsSecretName` | TLS secret name | "" |
| `ingressConfig.ingressClass` | Ingress class | "" |
| `ingressConfig.annotations` | Extra annotations | {} |
| `componentConfiguration.ingress-controller.service.type` | Service type | NodePort |

### Access Methods

- **NodePort**: `http://<node-ip>:<nodeport>`
- **LoadBalancer**: Set service type to `LoadBalancer`
- **Port-forward**: `kubectl port-forward svc/k8s-triliovault-ingress-gateway 8080:80 -n <ns>`

## RBAC Roles

| Role | Permissions |
|------|-------------|
| `triliovault-admin` | Full access to all TVK resources |
| `triliovault-reader` | Read-only access to TVK resources |
| `triliovault-login-only` | UI login only, no resource access |

## Encryption

Configure master encryption key for encrypted backups:

```yaml
spec:
  helmValues:
    masterEncryptionKeyConfig:
      namespace: trilio-system
      name: master-key-secret
```

## CSI Configuration

Include or exclude specific CSI drivers:

```yaml
spec:
  csiConfig:
    include:
      - driverName: ebs.csi.aws.com
    exclude:
      - driverName: efs.csi.aws.com
```

## Schedule and Job Deadlines

| Option | Default | Description |
|--------|---------|-------------|
| `pauseSchedule` | false | Pause all scheduled backups |
| `helmValues.jobSpec.activeDeadlineSeconds` | 43200 | Max job runtime (12h) |
| `helmValues.jobSpec.pendingDeadlineSeconds` | 43200 | Max pending time |
| `helmValues.schedulePolicyTimezone` | Etc/UTC | Cron schedule timezone |

## Related Resources

- [Installation Guide](installation.md)
- [TrilioVaultManager CRD](../CRDs/triliovaultmanager-crd.md)
- [Policy CRD](../CRDs/policy-crd.md)
