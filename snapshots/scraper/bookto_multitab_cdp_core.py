"""Small, pure-CDP primitives for the Bookto/Newtoki multi-tab lane."""  # noqa: SIZE_OK — one cohesive CDP protocol adapter

from __future__ import annotations

import base64
import http.client
import json
import time
from typing import Any, Final

import websocket


AUTOMATIC_CHALLENGE_WAIT_SECONDS: Final = 180.0
AUTOMATIC_CHALLENGE_POLL_SECONDS: Final = 1.0


class CdpError(RuntimeError):
    """A browser or page failure that must not be converted into a skip."""


class CloudflareChallenge(CdpError):
    """The current page still requires the user's checkbox action."""


class RetryableCloudflareChallenge(CdpError):
    """Cloudflare is auto-verifying without a visible user control."""


class ImageRouteUnavailable(CdpError):
    """The page names an image route that Chrome cannot actually render."""


def _targets(port: int) -> list[dict[str, Any]]:
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=4)
    conn.request("GET", "/json/list")
    response = conn.getresponse()
    payload = json.loads(response.read().decode("utf-8"))
    conn.close()
    return [row for row in payload if row.get("type") == "page"]


def open_target(port: int) -> dict[str, Any]:
    pages = _targets(port)
    if not pages:
        raise CdpError(f"CDP_PAGE_MISSING:{port}")
    return pages[0]


def new_target(port: int) -> dict[str, Any]:
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=4)
    conn.request("GET", "/json/version")
    response = conn.getresponse()
    version = json.loads(response.read().decode("utf-8"))
    conn.close()
    browser_url = version.get("webSocketDebuggerUrl")
    if response.status != 200 or not isinstance(browser_url, str):
        raise CdpError(f"CDP_BROWSER_ENDPOINT_FAILED:{response.status}")
    ws = websocket.create_connection(browser_url, timeout=20, suppress_origin=True)
    try:
        ws.send(json.dumps({
            "id": 1,
            "method": "Target.createTarget",
            "params": {"url": "about:blank", "background": True},
        }))
        result = json.loads(ws.recv()).get("result", {})
    finally:
        ws.close()
    target_id = result.get("targetId")
    targets = [target for target in _targets(port) if target.get("id") == target_id]
    if not targets:
        raise CdpError("CDP_BACKGROUND_TARGET_MISSING")
    return targets[0]


class CdpPage:
    def __init__(self, port: int, target: dict[str, Any] | None = None) -> None:
        self.port = port
        self.target = target or open_target(port)
        self.ws = websocket.create_connection(
            self.target["webSocketDebuggerUrl"], timeout=20, suppress_origin=True
        )
        self._next_id = 0
        self._network_by_url: dict[str, list[str]] = {}
        self.request("Page.enable")

    def _record_message(self, message: dict[str, Any]) -> None:
        method = message.get("method")
        params = message.get("params", {})
        if method == "Network.requestWillBeSent":
            request = params.get("request", {})
            url = request.get("url")
            request_id = params.get("requestId")
            if isinstance(url, str) and isinstance(request_id, str):
                self._network_by_url.setdefault(url, []).append(request_id)

    def _drain_events(self) -> None:
        original_timeout = self.ws.gettimeout()
        self.ws.settimeout(0.05)
        try:
            while True:
                try:
                    message = self.ws.recv()
                except (TimeoutError, websocket.WebSocketTimeoutException):
                    break
                if not message:
                    break
                self._record_message(json.loads(message))
        finally:
            self.ws.settimeout(original_timeout)

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._next_id += 1
        message_id = self._next_id
        self.ws.send(json.dumps({"id": message_id, "method": method, "params": params or {}}))
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            try:
                response = json.loads(self.ws.recv())
            except (TimeoutError, websocket.WebSocketTimeoutException) as error:
                raise CdpError(f"CDP_TIMEOUT:{method}") from error
            except websocket.WebSocketConnectionClosedException as error:
                raise CdpError(f"CDP_CONNECTION_CLOSED:{method}") from error
            self._record_message(response)
            if response.get("id") == message_id:
                if response.get("error"):
                    raise CdpError(f"CDP_{method}:{response['error']}")
                return response
        raise CdpError(f"CDP_TIMEOUT:{method}")

    def enable_network_capture(self) -> None:
        self.request("Network.enable")

    def network_body(self, url_prefix: str) -> tuple[str, bytes]:
        candidates = [
            (url, request_id)
            for url, request_ids in self._network_by_url.items()
            if url.startswith(url_prefix)
            for request_id in reversed(request_ids)
        ]
        for url, request_id in candidates:
            try:
                result = self.request("Network.getResponseBody", {"requestId": request_id}).get("result", {})
            except CdpError:
                continue
            body = result.get("body")
            if not isinstance(body, str) or not body:
                continue
            if result.get("base64Encoded"):
                return url, base64.b64decode(body)
            return url, body.encode("utf-8")
        raise CdpError(f"CDP_NETWORK_BODY_MISSING:{url_prefix}")

    def evaluate(self, expression: str, await_promise: bool = False) -> Any:
        result = self.request(
            "Runtime.evaluate",
            {
                "expression": expression,
                "returnByValue": True,
                "awaitPromise": await_promise,
            },
        )
        value = result.get("result", {}).get("result", {})
        if value.get("subtype") == "error":
            raise CdpError(f"JS_ERROR:{value.get('description', '')}")
        return value.get("value")

    def navigate(
        self, url: str, settle_seconds: float = 1.5,
        automatic_challenge_wait_seconds: float = 0.0,
    ) -> dict[str, Any]:
        self.request("Page.navigate", {"url": url})
        time.sleep(settle_seconds)
        automatic_deadline = time.monotonic() + max(0.0, automatic_challenge_wait_seconds)
        while True:
            self._drain_events()
            state = self.evaluate(
                """({href:location.href,title:document.title,ready:document.readyState,
                body:(document.body?.innerText||'').slice(0,500),
                challenge:[...document.querySelectorAll('#challenge-running,#challenge-form,.cf-turnstile,iframe[src*="turnstile"]')]
                  .some(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);
                    return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'&&s.opacity!=='0';})})"""
            )
            self._drain_events()
            if not isinstance(state, dict):
                raise RetryableCloudflareChallenge(
                    f"CLOUDFLARE_AUTO_CHALLENGE_RETRYABLE:{url}"
                )
            challenge_text = f"{state.get('title', '')}\n{state.get('body', '')}".casefold()
            semantic_challenge = any(
                marker in challenge_text
                for marker in (
                    "잠시만 기다리십시오",
                    "보안 확인 수행 중",
                    "just a moment",
                    "performing security verification",
                    "verify you are human",
                )
            )
            if state.get("challenge"):
                raise CloudflareChallenge(f"CLOUDFLARE_CHECK_REQUIRED:{url}")
            if state.get("href") == "chrome-error://chromewebdata/":
                raise CdpError(f"SITE_ROUTE_UNAVAILABLE:{url}")
            page_loading = state.get("ready") not in {"interactive", "complete"}
            if semantic_challenge or page_loading:
                remaining = automatic_deadline - time.monotonic()
                if remaining > 0:
                    time.sleep(min(AUTOMATIC_CHALLENGE_POLL_SECONDS, remaining))
                    continue
                if semantic_challenge:
                    raise RetryableCloudflareChallenge(
                        f"CLOUDFLARE_AUTO_CHALLENGE_RETRYABLE:{url}"
                    )
                raise CdpError(f"PAGE_NOT_READY:{url}")
            return state

    def load_resource(self, url_prefix: str) -> tuple[str, bytes]:
        self.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.35)
        self._drain_events()
        tree = self.request("Page.getResourceTree").get("result", {}).get("frameTree", {})
        frame = tree.get("frame", {}).get("id")
        resources = tree.get("resources", [])
        matches = [row for row in resources if row.get("url", "").startswith(url_prefix)]
        if not matches or not frame:
            raise CdpError(f"CDP_RESOURCE_MISSING:{url_prefix}")
        self.request("Page.enable")
        for resource in reversed(matches):
            try:
                content = self.request(
                    "Page.getResourceContent",
                    {"frameId": frame, "url": resource["url"]},
                ).get("result", {})
            except CdpError:
                continue
            if content.get("base64Encoded") and content.get("content"):
                return resource["url"], base64.b64decode(content["content"])
        return self.network_body(url_prefix)

    def close(self) -> None:
        self.ws.close()


def load_resource_with_retries(client: CdpPage, url_prefix: str, attempts: int = 3) -> tuple[str, bytes]:
    last_error: CdpError | None = None
    for attempt in range(attempts):
        try:
            return client.load_resource(url_prefix)
        except CdpError as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(0.5 * (attempt + 1))
    expression = f"""(() => {{
      const prefix={json.dumps(url_prefix)};
      const image=[...document.images].find(i=>(i.currentSrc||i.src).startsWith(prefix));
      return image ? {{found:true,complete:image.complete,naturalWidth:image.naturalWidth,
        naturalHeight:image.naturalHeight}} : {{found:false}};
    }})()"""
    try:
        render_state = client.evaluate(expression)
    except CdpError:
        render_state = None
    if (
        isinstance(render_state, dict)
        and render_state.get("found")
        and render_state.get("complete")
        and int(render_state.get("naturalWidth", 0)) == 0
    ):
        raise ImageRouteUnavailable(f"IMAGE_ROUTE_UNAVAILABLE:{url_prefix}")
    if last_error is not None:
        raise last_error
    raise CdpError(f"CDP_RESOURCE_RETRY_EXHAUSTED:{url_prefix}")


def close_target(port: int, target_id: str, attempts: int = 3) -> bool:
    last_status = 0
    for attempt in range(attempts):
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=4)
        conn.request("GET", f"/json/close/{target_id}")
        response = conn.getresponse()
        response.read()
        last_status = response.status
        conn.close()
        if last_status == 200:
            return True
        if last_status == 404:
            return False
        if attempt + 1 < attempts:
            time.sleep(0.2 * (attempt + 1))
    raise CdpError(f"CDP_TARGET_CLOSE_FAILED:{target_id}:{last_status}")
