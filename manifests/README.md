# k8s manifest

This provides our APF k8s manifests

Manifests are grouped by functional scope:

- `env`: contains the environment definitions
- `secrets`: defines all our secrets
- `backend`: provides our backend
- `db`: defines everything related to the DB (including persistence)
- `public`: implements all elements that are exposed to the public (ingress, certs)

## Deployment

```bash
# Create namespace
kubectl create ns SOME_NS

# Deploy
kubectl apply -n SOME_NS -f .  # or -f ./manifests if called from project root
```

## Troubleshooting

Ingress API changed before 1.18+, so remember to define your IngressClass (and opt mark it as defautl) with something like:

```yaml
apiVersion: networking.k8s.io/v1beta1
kind: IngressClass
metadata:
  name: traefik
  annotations:
    ingressclass.kubernetes.io/is-default-class: 'true'
spec:
  controller: traefik.io/ingress-controller
```

If you don't want to define it as `default-class`, pass `ingressClassName: traefik` to your `Ingress.spec`
