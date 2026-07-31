# FileRecoveryVM CRD

## Overview

The FileRecoveryVM CR creates a recovery virtual machine that mounts a backed-up VM disk so files can be browsed and copied without a full VM restore. It is used for granular file-level recovery from OpenShift Virtualization / KubeVirt VM backups stored on a Target.

## Key Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `spec.vmName` | string | Name of the backed-up virtual machine to recover files from | Yes |
| `spec.location` | string | Absolute path on the Target where the VM backup resides | Yes |
| `spec.target` | ObjectReference | Reference to the Target CR that stores the VM backup | Yes |
| `spec.publicKey` | string | SSH public key used to access the FileRecovery VM | Yes |
| `spec.storageClass` | string | StorageClass used when creating the default DataVolume for the recovery VM image | No |
| `spec.externalServiceType` | string | Service type exposing the recovery VM (defaults to `ClusterIP`) | No |
| `spec.encryption.encryptionSecret` | ObjectReference | Secret used to decrypt an encrypted VM backup | No |
| `spec.diskEncryptionSecret` | ObjectReference | Secret with per-disk LUKS unlock material | No |
| `spec.dataVolume` | ObjectReference | Optional existing DataVolume reference | No |
| `spec.persistentVolumeClaim` | ObjectReference | Optional existing PVC reference | No |
| `spec.instancetype` | object | KubeVirt InstancetypeMatcher for the recovery VM | No |
| `spec.preference` | object | KubeVirt PreferenceMatcher for the recovery VM | No |

## Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status.status` | string | Overall FileRecoveryVM status |
| `status.condition` | []Condition | Phase conditions such as `Validation`, `RecoveryDiskProvisioning`, `MountingVMBackup` |
| `status.mountLocations` | []MountLocation | Mounted PVC paths and filesystem details |

## Example

```yaml
apiVersion: triliovault.trilio.io/v1
kind: FileRecoveryVM
metadata:
  name: my-vm-file-recovery
  namespace: my-app
spec:
  vmName: my-vm
  location: /path/to/vm-backup
  publicKey: "ssh-rsa AAAA..."
  target:
    name: s3-target
    namespace: trilio-system
  storageClass: ocs-storagecluster-ceph-rbd
  externalServiceType: ClusterIP
```

## Checking Status

```bash
kubectl get filerecoveryvm my-vm-file-recovery -n my-app
kubectl describe filerecoveryvm my-vm-file-recovery -n my-app
```

## Related Resources

- [Target CRD](target-crd.md)
- [Backup CRD](backup-crd.md)
- [Restore CRD](restore-crd.md)
