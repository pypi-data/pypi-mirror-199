import uuid

import contexts
import providers


provider = providers.DictProvider({
    'locale': 'ru',
    'correlation_id': str(uuid.uuid4()),
    'auth_token': 'token',
})

pfm = contexts.PlatformContext(provider)

resp, exc = pfm.services['ecommerce'].get('api/v1/products/')

print(resp.json() if not exc else None)
