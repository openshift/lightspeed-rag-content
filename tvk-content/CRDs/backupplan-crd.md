# BackupPlan CRD

## Overview

The BackupPlan defines what to back up and how, including the target storage, retention and schedule policies, application components, and optional hooks. A BackupPlan is referenced by Backup and Snapshot CRs to trigger data protection operations.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.backupConfig.target` | ObjectReference | Reference to the Target CR for storage | Yes (when `backupConfig` is set) |
| `spec.backupConfig.retentionPolicy` | ObjectReference | Reference to a Retention Policy CR | No |
| `spec.backupConfig.schedulePolicy.fullBackupPolicy` | ObjectReference | Schedule Policy for full backups | No |
| `spec.backupConfig.schedulePolicy.incrementalBackupPolicy` | ObjectReference | Schedule Policy for incremental backups | No |
| `spec.backupConfig.maxIncrBackupsPerFullBackup` | uint8 | Max incremental backups between full backups (1-15) | No |
| `spec.snapshotConfig.target` | ObjectReference | Target for snapshot operations | Yes (when `snapshotConfig` is set) |
| `spec.snapshotConfig.retentionPolicy` | ObjectReference | Retention policy for snapshots | No |
| `spec.snapshotConfig.schedulePolicy.snapshotPolicy` | ObjectReference | Schedule Policy for snapshots | No |
| `spec.backupPlanComponents.helmReleases` | []string | Helm release names to back up | No |
| `spec.backupPlanComponents.operators` | []object | Operator-managed applications to back up | No |
| `spec.backupPlanComponents.customSelector` | object | Custom resource selectors (`selectResources` / `excludeResources`) | No |
| `spec.hookConfig` | object | Pre/post backup hook references (`hooks` required when set) | No |
| `spec.includeResources` | ResourceSelector | Resources to include (namespace-scope) | No |
| `spec.excludeResources` | ResourceSelector | Resources to exclude | No |
| `spec.encryption.encryptionSecret` | ObjectReference | Encryption key reference for encrypted backups | Yes (when `encryption` is set) |
| `spec.backupPlanFlags.skipImageBackup` | bool | Skip container image backup | No |
| `spec.backupPlanFlags.pauseSchedule` | bool | Pause scheduled backups | No |
| `spec.backupPlanFlags.retainHelmApps` | bool | Retain Helm app metadata | No |
| `spec.securityScanConfig` | object | Security scan instance configuration | No |
| `spec.continuousRestoreConfig` | object | Continuous restore instance configuration | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `Available`, `InProgress`, `Unavailable`, `Error` |
| `status.scope` | string | `App` or `Namespace` |
| `status.applicationType` | string | `Helm`, `Operator`, `Custom`, `Namespace` |
| `status.pauseSchedule` | bool | Whether scheduled backups are paused |
| `status.condition` | []Condition | Sync and validation conditions |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: BackupPlan
metadata:
  name: my-app-backupplan
  namespace: my-app
spec:
  backupConfig:
    target:
      name: s3-target
      namespace: trilio-system
    retentionPolicy:
      name: weekly-retention
      namespace: trilio-system
    schedulePolicy:
      fullBackupPolicy:
        name: daily-schedule
        namespace: trilio-system
  backupPlanComponents:
    helmReleases:
      - my-release
  encryption:
    encryptionSecret:
      name: backup-encryption-key
      namespace: my-app
```

## Related Resources

- [Backup CRD](backup-crd.md)
- [Target CRD](target-crd.md)
- [Policy CRD](policy-crd.md)
- [Hook CRD](hook-crd.md)
