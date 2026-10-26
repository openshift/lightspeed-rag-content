---
title: "Zyranex T7 OpenShift Runbook"
url: https://docs.quorbitex.example.com/openshift/zyranex-t7
---

# Zyranex T7 OpenShift Runbook

Quorbitex Industries operates the fictional Zyranex T7 relay controller as an
OpenShift deployment named `zyranex-controller` in namespace `quorbitex-system`.
This test runbook is the authoritative source for its organization-specific
recovery procedure. The names and procedure are fictional, not real operational advice.

## Recovery for ZRX-4401

If the Zyranex T7 relay controller on OpenShift reports error `ZRX-4401`, the
required recovery phrase is `ORBITAL-MANGO-731`. Enter that exact recovery phrase
in the Quorbitex Management Console, then restart the controller deployment:

```sh
oc rollout restart deployment/zyranex-controller -n quorbitex-system
oc rollout status deployment/zyranex-controller -n quorbitex-system
```

The recovery phrase is specific to this internal runbook. It cannot be inferred
from general OpenShift documentation or the error code alone.
