# ClusterBackupPlan CRD

## Overview

The ClusterBackupPlan CR defines a multi-namespace backup plan. Unlike the namespace-scoped BackupPlan, ClusterBackupPlan is cluster-scoped and can protect workloads across multiple namespaces in a single plan. It is used with ClusterBackup, ClusterSnapshot, and ClusterRestore CRs.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.backupConfig.target` | ObjectReference | Reference to the Target CR | Yes (when `backupConfig` is set) |
| `spec.backupConfig.retentionPolicy` | ObjectReference | Retention policy reference | No |
| `spec.backupConfig.schedulePolicy.fullBackupPolicy` | ObjectReference | Schedule for full backups | No |
| `spec.backupConfig.schedulePolicy.incrementalBackupPolicy` | ObjectReference | Schedule for incremental backups | No |
| `spec.backupConfig.maxIncrBackupsPerFullBackup` | uint8 | Max incremental backups between full backups (1-15) | No |
| `spec.snapshotConfig` | object | Snapshot target/retention/schedule configuration | No |
| `spec.backupComponents` | []BackupComponent | Explicit list of namespaces to back up | No |
| `spec.backupComponents[].namespace` | string | Namespace to include in the plan | Yes (per item) |
| `spec.namespaceSelector` | []NamespaceSelector | Select namespaces by name/labels | No |
| `spec.namespaceSelector[].name` | string | Namespace name | Yes (per item) |
| `spec.includeResources` | ResourceSelector | Resources to include | No |
| `spec.excludeResources` | ResourceSelector | Resources to exclude | No |
| `spec.encryption.encryptionSecret` | ObjectReference | Encryption configuration | Yes (when `encryption` is set) |
| `spec.clusterBackupPlanFlags.skipImageBackup` | bool | Skip container image backup | No |
| `spec.clusterBackupPlanFlags.pauseSchedule` | bool | Pause scheduled backups | No |
| `spec.clusterBackupPlanFlags.retainHelmApps` | bool | Retain Helm app metadata | No |
| `spec.securityScanConfig` | object | Security scan instance configuration | No |
| `spec.continuousRestoreConfig` | object | Continuous restore instance configuration | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `Available`, `InProgress`, `Unavailable`, `Error` |
| `status.pauseSchedule` | bool | Whether scheduled backups are paused |
| `status.condition` | []Condition | Sync condition details |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: ClusterBackupPlan
metadata:
  name: multi-ns-backupplan
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
  backupComponents:
    - namespace: app-frontend
    - namespace: app-backend
    - namespace: app-database
```

## Related Resources

- [ClusterBackup CRD](clusterbackup-crd.md)
- [ClusterSnapshot CRD](clustersnapshot-crd.md)
- [ClusterRestore CRD](clusterrestore-crd.md)
- [BackupPlan CRD](backupplan-crd.md)
- [Target CRD](target-crd.md)
