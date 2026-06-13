import inspect
from dex_client_arkham import ArkhamClient


def test_client_imports_and_instantiates():
    client = ArkhamClient()
    assert client is not None


def test_public_methods_present():
    methods = [name for name, value in inspect.getmembers(ArkhamClient, inspect.isfunction) if not name.startswith('_')]
    assert set(['tag', 'tag_top', 'tag_count_entities', 'tag_count_addresses', 'tag_params', 'cex_tag', 'cex_top', 'entity', 'entity_summary', 'address', 'entity_balances', 'entity_top_address', 'entity_history', 'entity_loans', 'entity_flow', 'entity_volume', 'entity_portfolio', 'entity_portfolio_time_series', 'entity_for_exchange', 'search', 'search_exchange', 'transfers', 'insights', 'translate_languages', 'translate_dict', 'exchange_tokens', 'user', 'user_alert_methods', 'user_alerts_tier', 'user_announcements', 'user_recent_searches', 'user_saved_filters', 'user_entity_is_not_viewable', 'user_entity_is_shareable', 'auth_login_need_captcha', 'login_with_password', 'login_mfa_challenge', 'google_login_continue', 'apple_login_continue', 'authenticator_app_exists', 'verify_authenticator_app_code', 'create_authenticator_app_secret', 'confirm_authenticator_app_secret', 'delete_authenticator_app_secret', 'request_email_change', 'update_password', 'update_username', 'delete_user', 'account_sessions', 'account_delete_session', 'account_terminate_all_sessions', 'user_email_request_verification', 'user_email_verify', 'user_exchange_auth', 'subscription_info', 'api_keys', 'create_api_key', 'rename_api_key', 'delete_api_key', 'api_usage_alerts', 'update_api_usage_alerts', 'send_test_api_usage_alert', 'ws_session_info', 'ws_sessions', 'create_ws_session', 'delete_ws_session', 'turnkey_wallet', 'create_turnkey_wallet', 'turnkey_session']) <= set(methods)
