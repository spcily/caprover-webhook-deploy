# caprover-webhook-deploy

Github actions to deploy to caprover via webhook URL.
Setting webhook inside repo setting would not provide any valuable information when deploying.

## Inputs

### `server`

**Required** Caprover URL. Ex. https://captain.root.domain.com

### `password`

**Required** Caprover password. Use $\{{ secrets.CAPROVER_PASSWORD }} for better security.

### `appname`

**Required** Application name on the Caprover.

### `webhook`

**Required** Webhook URL to send the deploy request to.

## Example usage

```
- name: Caprover Webhook Deploy Action
  uses: spcily/caprover-webhook-deploy@v1.0.0
  with:
    server: 'https://captain.root.domain.com'
    password: '${{ secrets.CAPROVER_PASSWORD }}'
    appname: 'my-app'
    webhook: 'https://captain.root.domain.com/api/v2/user/apps/webhooks/triggerbuild?namespace=captain&token=...'
```
