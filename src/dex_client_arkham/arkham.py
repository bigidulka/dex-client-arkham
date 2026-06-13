from __future__ import annotations

import hashlib
import time
from typing import Any
from urllib.parse import quote

from .core import BaseClient, Json, drop_empty

DEFAULT_WEBAPP_CLIENT_KEY = "gh67j345kl6hj5k432"

EXCHANGE_MAPPINGS: dict[str, dict[str, Any]] = {
    "binance": {"exchange_id": "binance", "search_query": "Binance", "entity_id": "binance"},
    "bybit": {"exchange_id": "bybit", "search_query": "Bybit", "entity_id": "bybit"},
    "gateio": {"exchange_id": "gateio", "search_query": "Gate", "entity_id": "gate-io"},
    "mexc": {"exchange_id": "mexc", "search_query": "MEXC", "entity_id": "mexc"},
    "okx": {"exchange_id": "okx", "search_query": "OKX", "entity_id": "okx"},
    "kucoin": {"exchange_id": "kucoin", "search_query": "KuCoin", "entity_id": "kucoin"},
    "bitget": {"exchange_id": "bitget", "search_query": "Bitget", "entity_id": "bitget"},
    "htx": {"exchange_id": "htx", "search_query": "HTX", "entity_id": "huobi"},
    "poloniex": {"exchange_id": "poloniex", "search_query": "Poloniex", "entity_id": "poloniex"},
    "bingx": {"exchange_id": "bingx", "search_query": "BingX", "entity_id": "bingx"},
    "bitmart": {"exchange_id": "bitmart", "search_query": "BitMart", "entity_id": "bitmart"},
    "lbank": {"exchange_id": "lbank", "search_query": "LBank", "entity_id": "lbank"},
    "xt": {"exchange_id": "xt", "search_query": "XT.com", "entity_id": "xt-com"},
    "coinex": {"exchange_id": "coinex", "search_query": "CoinEx", "entity_id": "coinex"},
    "pionex": {"exchange_id": "pionex", "search_query": "Pionex", "entity_id": "pionex"},
    "aster": {"exchange_id": "aster", "search_query": "Aster", "entity_id": "astherus"},
    "hyperliquid": {"exchange_id": "hyperliquid", "search_query": "Hyperliquid", "entity_id": "hyperliquid"},
    "backpack": {"exchange_id": "backpack", "search_query": "Backpack Exchange", "entity_id": "backpack-exchange"},
    "ourbit": {"exchange_id": "ourbit", "search_query": "Ourbit", "entity_id": "ourbit"},
    "kcex": {"exchange_id": "kcex", "search_query": "KCEX", "entity_missing": True},
    "weex": {"exchange_id": "weex", "search_query": "WEEX", "entity_id": "weex"},
    "edgex": {"exchange_id": "edgex", "search_query": "edgeX", "entity_id": "edgex"},
    "phemex": {"exchange_id": "phemex", "search_query": "Phemex", "entity_id": "phemex"},
    "lighter": {"exchange_id": "lighter", "search_query": "Lighter", "entity_id": "lighter"},
    "paradex": {"exchange_id": "paradex", "search_query": "Paradex", "entity_id": "paradex-trade"},
}

EXCHANGE_ALIASES = {
    "astherus": "aster",
    "backpackexchange": "backpack",
    "gate": "gateio",
    "huobi": "htx",
    "paradextrade": "paradex",
    "xtcom": "xt",
}


def generate_payload(path: str, timestamp: int | None = None, webapp_client_key: str = DEFAULT_WEBAPP_CLIENT_KEY) -> str:
    if not path.startswith("/"):
        path = "/" + path
    ts = str(timestamp or int(time.time()))
    first = hashlib.sha256(f"{path}:{ts}:{webapp_client_key}".encode()).hexdigest()
    return hashlib.sha256(f"{webapp_client_key}:{first}".encode()).hexdigest()


def exchange_key(exchange: str) -> str:
    return exchange.lower().strip().replace("-", "").replace("_", "").replace(".", "").replace(" ", "")


def exchange_mapping(exchange: str) -> dict[str, Any] | None:
    key = EXCHANGE_ALIASES.get(exchange_key(exchange), exchange_key(exchange))
    return EXCHANGE_MAPPINGS.get(key)


class ArkhamClient(BaseClient):
    def __init__(
        self,
        *,
        base_url: str = "https://api.arkm.com",
        web_url: str = "https://arkm.com/",
        webapp_client_key: str = DEFAULT_WEBAPP_CLIENT_KEY,
        cookie: str = "",
        timeout: float = 10.0,
        use_curl_cffi: bool = True,
    ):
        super().__init__(base_url, timeout=timeout, use_curl_cffi=use_curl_cffi, headers={"Accept": "application/json, text/plain, */*"})
        self.web_url = web_url
        self.webapp_client_key = webapp_client_key
        self.cookie = cookie

    def _headers_for(self, path: str) -> dict[str, str]:
        ts = int(time.time())
        headers = {
            "Origin": self.web_url.rstrip("/"),
            "Referer": self.web_url,
            "X-Timestamp": str(ts),
            "X-Payload": generate_payload(path, ts, self.webapp_client_key),
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }
        if self.cookie:
            headers["Cookie"] = self.cookie
        return headers

    def _get(self, path: str, **params: Any) -> Json:
        return self.get(path, params=drop_empty(params), headers=self._headers_for(path), curl_cffi=True)

    def _post(self, path: str, body: Any | None = None) -> Json:
        return self.post(path, json_body=body or {}, headers=self._headers_for(path), curl_cffi=True)

    def tag(self, tag: str) -> Json: return self._get(f"/tag/{quote(tag)}")
    def tag_top(self, tag: str, page: int = 1) -> Json: return self._get("/tag/top", tag=tag, page=max(page, 1))
    def tag_count_entities(self, tag: str) -> Json: return self._get(f"/tag/{quote(tag)}/count_entities")
    def tag_count_addresses(self, tag: str) -> Json: return self._get(f"/tag/{quote(tag)}/count_addresses")
    def tag_params(self, tag: str) -> Json: return self._get(f"/tag/{quote(tag)}/params")
    def cex_tag(self) -> Json: return self.tag("cex")
    def cex_top(self, page: int = 1) -> Json: return self.tag_top("cex", page)
    def entity(self, entity_id: str) -> Json: return self._get(f"/intelligence/entity/{quote(entity_id)}")
    def entity_summary(self, entity_id: str) -> Json: return self._get(f"/intelligence/entity/{quote(entity_id)}/summary")
    def address(self, address: str) -> Json: return self._get(f"/intelligence/address/{quote(address)}")
    def entity_balances(self, entity_id: str, cheap: bool | None = None) -> Json: return self._get(f"/balances/entity/{quote(entity_id)}", cheap=str(cheap).lower() if cheap is not None else None)
    def entity_top_address(self, entity_id: str, custom_entity: bool = False) -> Json: return self._get(f"/balances/entity_top_address/{quote(entity_id)}", customEntity=str(custom_entity).lower())
    def entity_history(self, entity_id: str) -> Json: return self._get(f"/history/entity/{quote(entity_id)}")
    def entity_loans(self, entity_id: str) -> Json: return self._get(f"/loans/entity/{quote(entity_id)}")
    def entity_flow(self, entity_id: str) -> Json: return self._get(f"/flow/entity/{quote(entity_id)}")
    def entity_volume(self, entity_id: str) -> Json: return self._get(f"/volume/entity/{quote(entity_id)}")
    def entity_portfolio(self, entity_id: str, time_ms: int) -> Json: return self._get(f"/portfolio/entity/{quote(entity_id)}", time=time_ms)
    def entity_portfolio_time_series(self, entity_id: str, pricing_id: str = "bitcoin") -> Json: return self._get(f"/portfolio/timeSeries/entity/{quote(entity_id)}", pricingId=pricing_id)

    def entity_for_exchange(self, exchange: str) -> Json:
        mapping = exchange_mapping(exchange)
        if not mapping or not mapping.get("entity_id"):
            raise ValueError(f"Arkham entity mapping not found for {exchange!r}")
        return self.entity(str(mapping["entity_id"]))

    def search(self, query: str, limit: int = 15) -> Json:
        return self._get("/intelligence/search", query=query, arkhamEntities=limit, arkhamAddresses=limit, userEntities=limit, userAddresses=limit, ens=limit, types=limit, services=limit, twitter=limit, opensea=limit, tokens=limit, pools=limit, tags=limit)

    def search_exchange(self, exchange: str) -> Json:
        mapping = exchange_mapping(exchange)
        if not mapping or not mapping.get("search_query"):
            raise ValueError(f"Arkham search mapping not found for {exchange!r}")
        return self.search(str(mapping["search_query"]))

    def transfers(self, *, base: str = "", flow: str = "all", usd_gte: str = "1", usd_lte: str = "", tokens: str = "", time_gte: str = "", time_lte: str = "", sort_key: str = "time", sort_dir: str = "desc", limit: int = 16, offset: int = 0) -> Json:
        return self._get("/transfers", base=base, flow=flow, usdGte=usd_gte, usdLte=usd_lte, tokens=tokens, timeGte=time_gte, timeLte=time_lte, sortKey=sort_key, sortDir=sort_dir, limit=limit, offset=offset)

    def insights(self, *, page_from: int = 0, page_to: int | None = None, time_last: str = "24h", search_query: str = "", entity_ids: str = "", token_ids: str = "", misc_tags: str = "", insight_ids: str = "", ai_importance: str = "", from_time: str = "", to_time: str = "") -> Json:
        return self._get("/insights/insights", pageFrom=page_from, pageTo=page_to or page_from + 4, timeLast=time_last, searchQuery=search_query, entityIds=entity_ids, tokenIds=token_ids, miscTags=misc_tags, insightIds=insight_ids, aiImportance=ai_importance, fromTime=from_time, toTime=to_time)

    def translate_languages(self) -> Json: return self._get("/translate/languages")
    def translate_dict(self, token: str = "", known_language: bool | None = None) -> Json: return self._get("/translate/dict", token=token, knownLanguage=str(known_language).lower() if known_language is not None else None)
    def exchange_tokens(self) -> Json: return self._get("/token/arkham_exchange_tokens")
    def user(self) -> Json: return self._get("/user")
    def user_alert_methods(self) -> Json: return self._get("/user/alertmethods")
    def user_alerts_tier(self) -> Json: return self._get("/user/alerts/tier")
    def user_announcements(self) -> Json: return self._get("/user/announcements")
    def user_recent_searches(self) -> Json: return self._get("/user/recent_searches")
    def user_saved_filters(self) -> Json: return self._get("/user/saved-filters")
    def user_entity_is_not_viewable(self, entity_id: str) -> Json: return self._get(f"/user/entities/{quote(entity_id)}/is_not_viewable")
    def user_entity_is_shareable(self, entity_id: str) -> Json: return self._get(f"/user/entities/{quote(entity_id)}/is_shareable")

    def auth_login_need_captcha(self) -> Json: return self._get("/auth/login/need-captcha")
    def login_with_password(self, email: str, password: str, *, redirect_domain: str = "https://arkm.com", redirect_path: str = "/", turnstile: str = "", invisible_turnstile: str = "") -> Json:
        return self._post("/auth/login", {"email": email, "password": password, "redirectDomain": redirect_domain, "redirectPath": redirect_path, "turnstile": turnstile, "invisibleTurnstile": invisible_turnstile})
    def login_mfa_challenge(self, code: str, *, redirect_domain: str = "https://arkm.com", redirect_path: str = "/") -> Json: return self._post("/auth/login/challenge", {"code": code, "redirectDomain": redirect_domain, "redirectPath": redirect_path})
    def google_login_continue(self, token: str, *, redirect_domain: str = "https://arkm.com", redirect_path: str = "/") -> Json: return self._post("/auth/google/continue", {"token": token, "redirectDomain": redirect_domain, "redirectPath": redirect_path, "referralSlug": None})
    def apple_login_continue(self, token: str, *, redirect_domain: str = "https://arkm.com", redirect_path: str = "/") -> Json: return self._post("/auth/apple/continue", {"token": token, "redirectDomain": redirect_domain, "redirectPath": redirect_path, "referralSlug": None})
    def authenticator_app_exists(self) -> Json: return self._get("/auth/authenticator-app/exists")
    def verify_authenticator_app_code(self, code: str) -> Json: return self._post("/auth/authenticator-app/verify", {"code": code})
    def create_authenticator_app_secret(self) -> Json: return self._post("/auth/authenticator-app/create")
    def confirm_authenticator_app_secret(self, code: str) -> Json: return self._post("/auth/authenticator-app/confirm", {"code": code})
    def delete_authenticator_app_secret(self) -> Json: return self.request("DELETE", "/auth/authenticator-app", headers=self._headers_for("/auth/authenticator-app"), curl_cffi=True)
    def request_email_change(self, new_email: str) -> Json: return self._post("/auth/email/change", {"newEmail": new_email})
    def update_password(self, old_password: str, new_password: str) -> Json: return self.request("PUT", "/auth/password", json_body={"oldPassword": old_password, "newPassword": new_password}, headers=self._headers_for("/auth/password"), curl_cffi=True)
    def update_username(self, new_username: str) -> Json: return self.request("PUT", "/auth/username", json_body={"newUsername": new_username}, headers=self._headers_for("/auth/username"), curl_cffi=True)
    def delete_user(self) -> Json: return self.request("DELETE", "/auth/user", headers=self._headers_for("/auth/user"), curl_cffi=True)

    def account_sessions(self) -> Json: return self._get("/account/sessions")
    def account_delete_session(self, session_id: str) -> Json: return self._post("/account/sessions/delete", {"sessionId": session_id})
    def account_terminate_all_sessions(self) -> Json: return self._post("/account/sessions/terminate-all")
    def user_email_request_verification(self) -> Json: return self._post("/user/email/request_verification")
    def user_email_verify(self, code: str) -> Json: return self._post("/user/email/verify", {"code": code})
    def user_exchange_auth(self) -> Json: return self._get("/user/exchangeauth")
    def subscription_info(self) -> Json: return self._get("/subscription/info")
    def api_keys(self) -> Json: return self._get("/api_keys/keys")
    def create_api_key(self, name: str) -> Json: return self._post("/api_keys/create", {"name": name})
    def rename_api_key(self, key_id: str, name: str) -> Json: return self._post("/api_keys/rename", {"id": key_id, "name": name})
    def delete_api_key(self, key_id: str) -> Json: return self.request("DELETE", f"/api_keys/key/{quote(key_id)}", headers=self._headers_for(f"/api_keys/key/{quote(key_id)}"), curl_cffi=True)
    def api_usage_alerts(self) -> Json: return self._get("/settings/api-usage-alerts")
    def update_api_usage_alerts(self, config: Any) -> Json: return self.request("PUT", "/settings/api-usage-alerts", json_body=config, headers=self._headers_for("/settings/api-usage-alerts"), curl_cffi=True)
    def send_test_api_usage_alert(self, config: Any) -> Json: return self._post("/settings/api-usage-alerts/test", config)
    def ws_session_info(self) -> Json: return self._get("/ws/session-info")
    def ws_sessions(self) -> Json: return self._get("/ws/sessions")
    def create_ws_session(self) -> Json: return self._post("/ws/sessions")
    def delete_ws_session(self, session_id: str) -> Json: return self.request("DELETE", f"/ws/sessions/{quote(session_id)}", headers=self._headers_for(f"/ws/sessions/{quote(session_id)}"), curl_cffi=True)
    def turnkey_wallet(self) -> Json: return self._get("/turnkey/wallet")
    def create_turnkey_wallet(self) -> Json: return self._post("/turnkey/wallet")
    def turnkey_session(self, public_key: str) -> Json: return self._post("/turnkey/session", {"publicKey": public_key})
