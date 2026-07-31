# Backup CRD

## Overview

The Backup custom resource triggers a point-in-time backup of an application defined by a BackupPlan. Each Backup references a BackupPlan and can be Full, Incremental, or Mixed. Backups capture application metadata, Kubernetes resources, and persistent volume data to a configured Target.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.type` | string | Backup type: `Full`, `Incremental`, or `Mixed`. Full captures everything; Incremental captures only changes since the last backup. | No (defaults to Full) |
| `spec.backupPlan.name` | string | Name of the BackupPlan CR to back up. | Yes |
| `spec.backupPlan.namespace` | string | Namespace of the BackupPlan CR (optional when in the same namespace). | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | Overall status: `Queued`, `InProgress`, `Pending`, `Error`, `Completed`, `Failed`, `Available`, `Coalescing`, `Canceling`, `Canceled`, `Degraded` |
| `status.phase` | string | Current operation phase (see Backup Phases below) |
| `status.phaseStatus` | string | Status of the current phase: `InProgress`, `Pending`, `Error`, `Completed`, `Failed` |
| `status.type` | string | Resolved backup type (`Full`, `Incremental`, `Mixed`) |
| `status.size` | Quantity | Total size of backup (metadata + data) |
| `status.startTimestamp` | Time | When the backup started |
| `status.completionTimestamp` | Time | When the backup completed |
| `status.percentageCompletion` | int | Progress percentage (0-100) |
| `status.expirationTimestamp` | Time | When the backup expires per retention policy |
| `status.duration` | Duration | Total duration of the backup process |
| `status.encryptionEnabled` | bool | Whether encryption was applied |
| `status.location` | string | Location of the backup on the Target |
| `status.tvkVersion` | string | TVK version that created the backup |

## Backup Phases

Backups progress through these phases sequentially:

1. **PreBackupValidation** - Validates backup prerequisites
2. **MetaSnapshot** - Captures application metadata
3. **HookTargetIdentification** - Identifies hook targets
4. **Quiesce** - Runs pre-backup hooks
5. **ImageBackup** - Backs up container images
6. **DataSnapshot** / **Snapshot** - Creates CSI volume snapshots
7. **Unquiesce** - Runs post-backup hooks
8. **DataUpload** / **Upload** - Uploads data to the target
9. **MetadataUpload** - Uploads metadata to the target
10. **Retention** - Enforces retention policy
11. **Cleanup** - Removes temporary resources
12. **Cancel** - Cancel path when a backup is canceled

## Status Conditions

Each condition entry contains:

| Field | Description |
|-------|-------------|
| `phase` | The operation phase |
| `status` | `InProgress`, `Error`, `Completed`, `Failed`, `Skipped`, `Canceled` |
| `reason` | Human-readable message |
| `timestamp` | When the condition was recorded |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Backup
metadata:
  name: my-app-backup
  namespace: my-app
spec:
  type: Full
  backupPlan:
    name: my-app-backupplan
    namespace: my-app
```

### Incremental Backup

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Backup
metadata:
  name: my-app-incremental
  namespace: my-app
spec:
  type: Incremental
  backupPlan:
    name: my-app-backupplan
    namespace: my-app
```

## Checking Backup Status

```bash
kubectl get backup my-app-backup -n my-app
kubectl describe backup my-app-backup -n my-app
```

Look at `status.condition` to identify failure phase and reason.

## Related Resources

- [BackupPlan CRD](backupplan-crd.md)
- [Restore CRD](restore-crd.md)
- [Target CRD](target-crd.md)
- [Policy CRD](policy-crd.md)
- [Troubleshooting Guide](../operators/triliovault-for-kubernetes/troubleshooting.md)
