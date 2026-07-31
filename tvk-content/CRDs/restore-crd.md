# Restore CRD

## Overview

The Restore CR triggers recovery of an application from a Backup, Snapshot, Location, ConsistentSet, or ContinuousRestorePlan. It supports restoring to the same or different namespace, selective resource restore, transformation of components, and post-restore hooks.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.source.type` | string | Source type: `Backup`, `Snapshot`, `Location`, `ConsistentSet`, or `ContinuousRestorePlan` | Yes |
| `spec.source.backup` | ObjectReference | Reference to the Backup CR to restore from | Conditional |
| `spec.source.snapshot` | ObjectReference | Reference to the Snapshot CR | Conditional |
| `spec.source.consistentSet` | ObjectReference | Reference to the ConsistentSet CR | Conditional |
| `spec.source.continuousRestorePlan` | ObjectReference | Reference to the ContinuousRestorePlan CR | Conditional |
| `spec.source.target` / `spec.source.location` | ObjectReference / string | Target and location path when `type` is `Location` | Conditional |
| `spec.restoreFlags.skipIfAlreadyExists` | bool | Skip resources that already exist | No |
| `spec.restoreFlags.patchIfAlreadyExists` | bool | Patch existing resources with backed-up spec | No |
| `spec.restoreFlags.patchCRD` | bool | Patch existing CRDs during restore | No |
| `spec.restoreFlags.useOCPNamespaceUIDRange` | bool | Use OCP namespace UID range for data dirs | No |
| `spec.restoreFlags.omitMetadata` | bool | Omit metadata during restore | No |
| `spec.restoreFlags.skipOperatorResources` | bool | Skip operator resources | No |
| `spec.restoreFlags.onlyData` / `onlyMetadata` | bool | Restore only data or only metadata | No |
| `spec.restoreFlags.restoreStorageClass` | bool | Restore storage class | No |
| `spec.restoreFlags.retainHelmReleaseName` | bool | Retain original Helm release name | No |
| `spec.actionFlags.protectRestoredApp` | bool | Re-apply TVK protection after restore | No |
| `spec.actionFlags.cleanupOnFailure` | bool | Clean up restored resources if restore fails | No |
| `spec.actionFlags.imageRestore` | bool | Restore container images | No |
| `spec.excludeResourceSelector` | ResourceSelector | Resources to exclude from restore | No |
| `spec.resourceSelector` | ResourceSelector | Specific resources to restore | No |
| `spec.transformComponents` | object | Transform custom/helm components during restore | No |
| `spec.hookConfig` | object | Post-restore hook configuration | No |
| `spec.encryption` | object | Decryption key for encrypted backups | No |
| `spec.resourcesReadyWaitSeconds` | uint16 | Wait time for pods to become ready (0-1200) | No |
| `spec.cleanupConfig.enabled` | bool | Enable cleanup-on-restore workflow | Yes (when `cleanupConfig` is set) |
| `spec.imageRegistry` | object | Override container image registry | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `InProgress`, `Pending`, `Completed`, `Failed`, `Error` |
| `status.phase` | string | Current restore phase |
| `status.percentageCompletion` | int | Progress (0-100) |
| `status.size` | Quantity | Total restored data size |
| `status.duration` | Duration | Total restore duration |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Restore
metadata:
  name: my-app-restore
  namespace: my-app
spec:
  source:
    type: Backup
    backup:
      name: my-app-backup
      namespace: my-app
  restoreFlags:
    skipIfAlreadyExists: true
    patchCRD: true
    useOCPNamespaceUIDRange: true
  actionFlags:
    protectRestoredApp: true
    cleanupOnFailure: true
```

## Related Resources

- [Backup CRD](backup-crd.md)
- [Snapshot CRD](snapshot-crd.md)
- [ClusterRestore CRD](clusterrestore-crd.md)
- [Troubleshooting](../operators/triliovault-for-kubernetes/troubleshooting.md)
