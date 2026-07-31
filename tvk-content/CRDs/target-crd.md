# Target CRD

## Overview

The Target CR defines the backup storage destination. TVK supports object stores (AWS S3, MinIO, Azure Blob, and other S3-compatible vendors) and NFS. Targets are validated upon creation to ensure connectivity and permissions. A Target must be `Available` before it can be used by a BackupPlan.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.type` | string | `ObjectStore` or `NFS` | Yes |
| `spec.vendor` | string | Storage vendor: `AWS`, `RedhatCeph`, `Ceph`, `IBMCleversafe`, `Cloudian`, `Scality`, `NetApp`, `Cohesity`, `SwiftStack`, `Wasabi`, `Wassabi`, `MinIO`, `DellEMC`, `Azure`, `DigitalOcean`, `OVH`, `Other` | Yes |
| `spec.objectStoreCredentials.bucketName` | string | Bucket name for backups | For ObjectStore |
| `spec.objectStoreCredentials.region` | string | Cloud region (e.g., `us-east-1`) | For ObjectStore |
| `spec.objectStoreCredentials.credentialSecret` | ObjectReference | Secret with access credentials | For ObjectStore |
| `spec.objectStoreCredentials.url` | string | Custom S3-compatible endpoint URL | No |
| `spec.objectStoreCredentials.objectLockingEnabled` | bool | Enable object locking / immutability | No |
| `spec.objectStoreCredentials.enableDedup` | bool | Enable deduplication for the target | No |
| `spec.objectStoreCredentials.skipCertVerification` | bool | Skip TLS certificate verification | No |
| `spec.nfsCredentials.nfsExport` | string | NFS export as `server:/path` (e.g., `192.0.2.1:/export/path`) | For NFS |
| `spec.nfsCredentials.nfsOptions` | string | NFS mount options (e.g., `nfsvers=4`) | No |
| `spec.enableBrowsing` | bool | Enable target browser for backup exploration | No |
| `spec.thresholdCapacity` | Quantity | Max capacity threshold (e.g., `5Gi`) | No |

## Metadata Annotations

Event target is **not** configured in `spec`. Mark a Target as an event target with a metadata annotation:

| Annotation | Value | Description |
|------------|-------|-------------|
| `trilio.io/event-target` | `"true"` | Enables the Target as an event target for continuous restore / event-driven workflows |

When this annotation is present and set to `true`, the controller enables the event-target stack and reports it in `status.eventTargetEnabled`.

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `InProgress`, `Available`, `Unavailable` |
| `status.browsingEnabled` | bool | Whether target browsing is active |
| `status.eventTargetEnabled` | bool | Whether event target is enabled (driven by `metadata.annotations.trilio.io/event-target`) |
| `status.condition` | []TargetCondition | Validation, browsing, event target conditions |
| `status.stats` | object | Target capacity and usage statistics |

## Credential Secret Format

The referenced secret must contain:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: target-secret
type: Opaque
data:
  accessKey: <base64-encoded>
  secretKey: <base64-encoded>
```

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Target
metadata:
  name: s3-target
  namespace: trilio-system
  annotations:
    trilio.io/event-target: "true"
spec:
  type: ObjectStore
  vendor: AWS
  objectStoreCredentials:
    region: us-east-1
    bucketName: my-tvk-backups
    credentialSecret:
      name: target-secret
      namespace: trilio-system
  thresholdCapacity: 100Gi
  enableBrowsing: true
```

### NFS Target

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Target
metadata:
  name: nfs-target
  namespace: trilio-system
  annotations:
    trilio.io/event-target: "true"
spec:
  type: NFS
  vendor: Other
  enableBrowsing: true
  thresholdCapacity: 100Gi
  nfsCredentials:
    nfsExport: 192.0.2.1:/export/kubedata
    nfsOptions: nfsvers=4
```

## Troubleshooting

If the Target stays `Unavailable`, check the validator pod:

```bash
kubectl get pods -A | grep validator
kubectl logs <validator-pod> -n <namespace>
```

## Related Resources

- [BackupPlan CRD](backupplan-crd.md)
- [Troubleshooting](../operators/triliovault-for-kubernetes/troubleshooting.md)
