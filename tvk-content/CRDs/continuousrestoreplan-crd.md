# ContinuousRestorePlan CRD

## Overview

The ContinuousRestorePlan CR enables continuous disaster recovery by automatically restoring new backups to a secondary cluster or namespace as they become available. It watches a Target for incoming backups and creates ConsistentSet CRs that trigger point-in-time restores.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.continuousRestorePolicy` | ObjectReference | Reference to a ContinuousRestore type Policy CR | Yes |
| `spec.target` | ObjectReference | Reference to the Target CR to watch for backups | Yes |
| `spec.transformComponents` | object | Transform configuration for restore (`custom[]` jsonPatches and/or `helm[]`) | No |

## How It Works

1. Create a `Policy` of type `ContinuousRestore` defining how many consistent sets to retain.
2. Create a `Target` CR pointing to the same backup storage as the source cluster.
3. Create a `ContinuousRestorePlan` referencing the policy and target.
4. TVK continuously monitors the target for new backups.
5. When a new backup is detected, a `ConsistentSet` is created and restored.
6. Older consistent sets are pruned based on the policy.

## Example

### Step 1: ContinuousRestore Policy

```yaml
apiVersion: triliovault.trilio.io/v1
kind: Policy
metadata:
  name: cr-policy
spec:
  type: ContinuousRestore
  continuousRestoreConfig:
    consistentSets: 3
```

### Step 2: ContinuousRestorePlan

```yaml
apiVersion: triliovault.trilio.io/v1
kind: ContinuousRestorePlan
metadata:
  name: dr-restore-plan
  namespace: dr-namespace
spec:
  continuousRestorePolicy:
    name: cr-policy
    namespace: dr-namespace
  target:
    name: s3-target
    namespace: dr-namespace
```

## Use Cases

- **Cross-cluster DR**: Continuously replicate backups from a primary cluster to a standby cluster
- **Warm standby**: Maintain a near-real-time copy of applications in a secondary namespace
- **RPO reduction**: Minimize recovery point objective by restoring every incremental backup

## Related Resources

- [ConsistentSet CRD](consistentset-crd.md)
- [Policy CRD](policy-crd.md)
- [Target CRD](target-crd.md)
