# Policy CRD

## Overview

The Policy CR defines operational policies for TVK, including retention, scheduling, cleanup, timeout, security scan, and continuous restore policies. Policies are referenced by BackupPlans and ClusterBackupPlans to automate backup lifecycle management.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.type` | string | Policy type: `Timeout`, `Retention`, `Cleanup`, `Schedule`, `SecurityScan`, `ContinuousRestore` | Yes |
| `spec.default` | bool | Whether this is the default policy of its type | No |

### Retention Policy

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.retentionConfig.latest` | int | Number of latest backups to retain (min 1) | No |
| `spec.retentionConfig.weekly` | int | Number of weekly backups to retain (min 1) | No |
| `spec.retentionConfig.dayOfWeek` | string | Day for weekly retention (e.g., `Monday`) | No |
| `spec.retentionConfig.monthly` | int | Number of monthly backups to retain (min 1) | No |
| `spec.retentionConfig.dateOfMonth` | int | Date for monthly retention (1-28) | No |
| `spec.retentionConfig.yearly` | int | Number of yearly backups to retain (min 1) | No |
| `spec.retentionConfig.monthOfYear` | string | Month for yearly retention (e.g., `January`) | No |

### Schedule Policy

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.scheduleConfig.schedule` | []string | Cron expressions for scheduling | Yes |

### Cleanup Policy

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.cleanupConfig.days` | int | Delete backups/restores older than N days | Yes |
| `spec.cleanupConfig.backupDays` | int | Deprecated; use `days` instead | No |

### ContinuousRestore Policy

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.continuousRestoreConfig.consistentSets` | int | Number of ConsistentSets to retain (1-10) | Yes |

### SecurityScan Policy

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.securityScanConfig.schedule` | []string | Cron schedules for periodic scans | No |
| `spec.securityScanConfig.retention` | int | Number of scan reports to retain | No |

## Examples

### Retention Policy

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Policy
metadata:
  name: weekly-retention
spec:
  type: Retention
  retentionConfig:
    latest: 5
    weekly: 2
    dayOfWeek: Monday
    monthly: 1
    dateOfMonth: 1
    yearly: 1
    monthOfYear: January
```

### Schedule Policy

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Policy
metadata:
  name: daily-schedule
spec:
  type: Schedule
  scheduleConfig:
    schedule:
      - "0 2 * * *"
```

### Cleanup Policy

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Policy
metadata:
  name: cleanup-30d
spec:
  type: Cleanup
  cleanupConfig:
    days: 30
```

## Related Resources

- [BackupPlan CRD](backupplan-crd.md)
- [ClusterBackupPlan CRD](clusterbackupplan-crd.md)
