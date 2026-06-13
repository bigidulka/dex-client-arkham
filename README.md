# Arkham Reverse Client

Python client for endpoints used by [https://arkm.com](https://arkm.com). The implementation is browser/reverse-engineered and mirrors the internal clients used in local DEX modules.

## Educational Use

This project is published as part of an educational process for studying web/API clients and data access patterns. It is unofficial, not affiliated with or endorsed by the upstream service, and should be used responsibly according to the target site's terms and applicable law.


## Install

```bash
pip install git+https://github.com/bigidulka/dex-client-arkham.git
```

For local development:

```bash
pip install -e '.[dev]'
pytest
```

## Quick start

```python
from dex_client_arkham import ArkhamClient

client = ArkhamClient()
# call any method below; all methods return decoded JSON dict/list payloads
```

## Methods

- `tag`
- `tag_top`
- `tag_count_entities`
- `tag_count_addresses`
- `tag_params`
- `cex_tag`
- `cex_top`
- `entity`
- `entity_summary`
- `address`
- `entity_balances`
- `entity_top_address`
- `entity_history`
- `entity_loans`
- `entity_flow`
- `entity_volume`
- `entity_portfolio`
- `entity_portfolio_time_series`
- `entity_for_exchange`
- `search`
- `search_exchange`
- `transfers`
- `insights`
- `translate_languages`
- `translate_dict`
- `exchange_tokens`
- `user`
- `user_alert_methods`
- `user_alerts_tier`
- `user_announcements`
- `user_recent_searches`
- `user_saved_filters`
- `user_entity_is_not_viewable`
- `user_entity_is_shareable`
- `auth_login_need_captcha`
- `login_with_password`
- `login_mfa_challenge`
- `google_login_continue`
- `apple_login_continue`
- `authenticator_app_exists`
- `verify_authenticator_app_code`
- `create_authenticator_app_secret`
- `confirm_authenticator_app_secret`
- `delete_authenticator_app_secret`
- `request_email_change`
- `update_password`
- `update_username`
- `delete_user`
- `account_sessions`
- `account_delete_session`
- `account_terminate_all_sessions`
- `user_email_request_verification`
- `user_email_verify`
- `user_exchange_auth`
- `subscription_info`
- `api_keys`
- `create_api_key`
- `rename_api_key`
- `delete_api_key`
- `api_usage_alerts`
- `update_api_usage_alerts`
- `send_test_api_usage_alert`
- `ws_session_info`
- `ws_sessions`
- `create_ws_session`
- `delete_ws_session`
- `turnkey_wallet`
- `create_turnkey_wallet`
- `turnkey_session`

## Endpoint inventory

Extracted from existing Local clients and rechecked with browser-harness network capture where the site allowed capture.

- `['GET', '/search', 'search']`
- `['GET', '/intelligence/entity/{entity_id}', 'entity']`
- `['GET', '/intelligence/entity/{entity_id}/summary', 'summary']`
- `['GET', '/balances/entity/{entity_id}', 'balances']`
- `['GET', '/intelligence/address/{address}', 'address']`
- `['GET', '/intelligence/entity/{entity_id}/top-address', 'top address']`
- `['GET', '/intelligence/entity/{entity_id}/history', 'history']`
- `['GET', '/intelligence/entity/{entity_id}/loans', 'loans']`
- `['GET', '/intelligence/entity/{entity_id}/flow', 'flow']`
- `['GET', '/intelligence/entity/{entity_id}/volume', 'volume']`
- `['GET', '/portfolio/entity/{entity_id}', 'portfolio']`
- `['GET', '/portfolio/entity/{entity_id}/time-series', 'portfolio time series']`
- `['GET', '/transfers', 'transfers']`
- `['GET', '/tag/{tag}', 'tag']`
- `['GET', '/tag/{tag}/top', 'tag top']`
- `['GET', '/tag/{tag}/count/entities', 'tag count entities']`
- `['GET', '/tag/{tag}/count/addresses', 'tag count addresses']`
- `['GET', '/tag/{tag}/params', 'tag params']`
- `['GET', '/cex/top', 'cex top']`
- `['GET', '/translate/languages', 'languages']`
- `['GET', '/translate/dict', 'dict']`
- `['GET', '/token/arkham_exchange_tokens', 'exchange tokens']`
- `['GET', '/auth/login/need-captcha', 'need captcha']`
- `['POST', '/auth/login', 'login']`
- `['POST', '/auth/mfa/challenge', 'mfa challenge']`
- `['GET', '/user', 'user']`
- `['GET', '/user/recent-searches', 'recent searches']`
- `['GET', '/user/saved-filters', 'saved filters']`
- `['GET', '/account/sessions', 'sessions']`

Full details: [`endpoint_inventory.json`](endpoint_inventory.json).

## Notes

- No official SDK is used.
- Some endpoints require Cloudflare/browser behavior; pass `use_curl_cffi=True` where available.
- Auth/session-only methods need your own cookies/tokens. Do not commit secrets.
- These clients are thin transport wrappers; normalize data in your application layer.
