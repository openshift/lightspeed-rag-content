# ConsistentSet CRD

## Overview

The ConsistentSet CR represents a consistency point in a continuous restore workflow. It is created automatically by TVK when a ContinuousRestorePlan triggers a restore of incremental backup data. ConsistentSets track which backup data has been applied to the restore destination and can be used to trigger point-in-time restores.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.continuousRestorePlan` | ObjectReference | Reference to the ContinuousRestorePlan CR | Yes |
| `spec.location` | string | Target location of the source Backup/ClusterBackup | Yes |
| `spec.transformComponents` | object | Transform configuration for restore (`custom[]` jsonPatches and/or `helm[]`) | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | `Available`, `InProgress`, `Error`, `Failed`, `Unavailable`, `InUse`, `Queued` |
| `status.condition` | []Condition | Phase conditions such as `PreConsistentSet`, `DataRestore`, `DataSnapshot` |

## How It Works

1. A `ContinuousRestorePlan` watches a Target for new backups.
2. When a new backup arrives, TVK creates a `ConsistentSet` representing that point in time.
3. The ConsistentSet triggers a restore of the backup data to the destination.
4. Multiple ConsistentSets are retained based on the ContinuousRestore policy (1-10).

## Example

ConsistentSets are typically created automatically. Manual creation is not recommended. To view existing consistent sets:

```bash
kubectl get consistentset -n <namespace>
kubectl describe consistentset <name> -n <namespace>
```

A ContinuousRestore policy controls how many consistent sets are retained:

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Policy
metadata:
  name: cr-policy
spec:
  type: ContinuousRestore
  continuousRestoreConfig:
    consistentSets: 5
```

## Related Resources

- [ContinuousRestorePlan CRD](continuousrestoreplan-crd.md)
- [Policy CRD](policy-crd.md)
- [Backup CRD](backup-crd.md)
