# ClusterRestore CRD

## Overview

The ClusterRestore CR triggers a multi-namespace restore from a ClusterBackup, ClusterSnapshot, Location, ClusterBackupPlan, ConsistentSet, or ContinuousRestorePlan. It supports namespace mapping (restore to different namespaces), global restore flags, per-component configuration, and component exclusion.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.source.type` | string | Source type: `ClusterBackup`, `ClusterSnapshot`, `Location`, `ClusterBackupPlan`, `ConsistentSet`, or `ContinuousRestorePlan` | Yes |
| `spec.source.clusterBackup` | ObjectReference | Name of the ClusterBackup to restore from | Conditional |
| `spec.source.clusterSnapshot` | ObjectReference | Name of the ClusterSnapshot to restore from | Conditional |
| `spec.source.clusterBackupPlan` | ObjectReference | Name of the ClusterBackupPlan | Conditional |
| `spec.source.consistentSet` | ObjectReference | Name of the ConsistentSet | Conditional |
| `spec.source.continuousRestorePlan` | ObjectReference | Name of the ContinuousRestorePlan | Conditional |
| `spec.source.target` / `spec.source.location` | ObjectReference / string | Target and location when `type` is `Location` | Conditional |
| `spec.globalConfig.restoreFlags` | object | Global restore flags applied to all components | No |
| `spec.components` | []ComponentConfig | Per-namespace restore configuration | No |
| `spec.components[].sourceNamespace` | string | Preferred source namespace from the backup | No |
| `spec.components[].backupNamespace` | string | Deprecated; use `sourceNamespace` | No |
| `spec.components[].restoreNamespace` | string | Target namespace for the restore | No |
| `spec.components[].restoreConfig` | object | Per-component restore configuration | No |
| `spec.components[].hookConfig` | object | Per-component hook configuration | No |
| `spec.excludeComponents` | []string | Namespaces to exclude from restore | No |
| `spec.actionFlags.cleanupOnFailure` | bool | Clean up resources if restore fails | No |
| `spec.encryption` | object | Decryption key for encrypted backups | No |
| `spec.imageRegistry` | object | Override container image registry | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `InProgress`, `Completed`, `Failed`, `Error` |
| `status.phase` | string | `PreClusterRestore`, `Restore`, `ClusterRestoreCleanup`, `AddProtection` |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: ClusterRestore
metadata:
  name: multi-ns-restore
spec:
  source:
    type: ClusterBackup
    clusterBackup:
      name: multi-ns-backup
  globalConfig:
    restoreFlags:
      skipIfAlreadyExists: true
  components:
    - sourceNamespace: app-frontend
      restoreNamespace: app-frontend-dr
    - sourceNamespace: app-backend
      restoreNamespace: app-backend-dr
  actionFlags:
    cleanupOnFailure: true
```

## Related Resources

- [ClusterBackup CRD](clusterbackup-crd.md)
- [ClusterSnapshot CRD](clustersnapshot-crd.md)
- [ClusterBackupPlan CRD](clusterbackupplan-crd.md)
- [Restore CRD](restore-crd.md)
