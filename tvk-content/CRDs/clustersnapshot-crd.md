# ClusterSnapshot CRD

## Overview

The ClusterSnapshot CR creates a cluster-scoped point-in-time CSI snapshot across namespaces defined by a ClusterBackupPlan. It is the cluster-scoped equivalent of Snapshot and does not upload data to a Target.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.clusterBackupPlan.name` | string | Name of the ClusterBackupPlan CR | Yes |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `Queued`, `InProgress`, `Pending`, `Error`, `Completed`, `Failed`, `Available`, `Coalescing`, `Canceling`, `Canceled`, `Degraded` |
| `status.type` | string | Resolved snapshot/backup type |
| `status.size` | Quantity | Total snapshot size |
| `status.startTimestamp` | Time | When the snapshot started |
| `status.completionTimestamp` | Time | When the snapshot completed |
| `status.percentageCompletion` | int | Progress (0-100) |
| `status.duration` | Duration | Total snapshot duration |
| `status.location` | string | Location associated with the snapshot |
| `status.tvkVersion` | string | TVK version that created the snapshot |
| `status.encryptionEnabled` | bool | Whether encryption was applied |
| `status.condition` | []Condition | Phase conditions |
| `status.snapshotInfos` | []SnapshotInfo | Per-namespace child Snapshot references and status |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: ClusterSnapshot
metadata:
  name: multi-ns-snapshot
spec:
  clusterBackupPlan:
    name: multi-ns-backupplan
```

## Checking Status

```bash
kubectl get clustersnapshot multi-ns-snapshot
kubectl describe clustersnapshot multi-ns-snapshot
```

## Related Resources

- [ClusterBackupPlan CRD](clusterbackupplan-crd.md)
- [ClusterBackup CRD](clusterbackup-crd.md)
- [ClusterRestore CRD](clusterrestore-crd.md)
- [Snapshot CRD](snapshot-crd.md)
