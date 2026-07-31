# Snapshot CRD

## Overview

The Snapshot CR creates a point-in-time CSI volume snapshot of an application without uploading data to a Target. Snapshots are faster than full Backups but remain on the cluster's storage backend. They are useful for quick rollback scenarios where off-cluster protection is not needed.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.backupPlan.name` | string | Name of the BackupPlan CR | Yes |
| `spec.backupPlan.namespace` | string | Namespace of the BackupPlan CR (optional when in the same namespace) | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `Queued`, `InProgress`, `Pending`, `Error`, `Completed`, `Failed`, `Available`, `Coalescing`, `Canceling`, `Canceled`, `Degraded` |
| `status.phase` | string | Current operation phase |
| `status.phaseStatus` | string | `InProgress`, `Pending`, `Error`, `Completed`, `Failed` |
| `status.size` | Quantity | Total snapshot size |
| `status.startTimestamp` | Time | When the snapshot started |
| `status.completionTimestamp` | Time | When the snapshot completed |
| `status.percentageCompletion` | int | Progress (0-100) |
| `status.expirationTimestamp` | Time | Retention expiry time |
| `status.duration` | Duration | Total snapshot duration |
| `status.encryptionEnabled` | bool | Whether encryption was applied |
| `status.tvkVersion` | string | TVK version that created the snapshot |

## Snapshot vs Backup

| Feature | Snapshot | Backup |
|---------|----------|--------|
| CSI volume snapshots | Yes | Yes |
| Off-cluster data upload | No | Yes |
| Speed | Faster | Slower |
| DR protection | No (cluster-local) | Yes (off-cluster) |
| Restore source | Yes | Yes |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Snapshot
metadata:
  name: my-app-snapshot
  namespace: my-app
spec:
  backupPlan:
    name: my-app-backupplan
    namespace: my-app
```

## Checking Status

```bash
kubectl get snapshot my-app-snapshot -n my-app
kubectl describe snapshot my-app-snapshot -n my-app
```

## Related Resources

- [Backup CRD](backup-crd.md)
- [BackupPlan CRD](backupplan-crd.md)
- [Restore CRD](restore-crd.md)
