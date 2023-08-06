import logging
import os
from dataclasses import dataclass
from time import sleep
from typing import Any, Dict, List, Optional

import httpx
from pydantic import parse_obj_as

from . import __version__, api, exceptions

log = logging.getLogger(__name__)

LATEST_API_VERSION = 2

CLEARNET_ENDPOINT = "https://api.sporestack.com"
TOR_ENDPOINT = (
    "http://api.spore64i5sofqlfz5gq2ju4msgzojjwifls7rok2cti624zyq3fcelad.onion"
)

API_ENDPOINT = CLEARNET_ENDPOINT

GET_TIMEOUT = 60
POST_TIMEOUT = 90
USE_TOR_PROXY = "auto"

HEADERS = {"User-Agent": f"sporestack-python/{__version__}"}


def _get_tor_proxy() -> str:
    """
    This makes testing easier.
    """
    return os.getenv("TOR_PROXY", "socks5://127.0.0.1:9050")


# For requests module
TOR_PROXY_REQUESTS = {"http": _get_tor_proxy(), "https": _get_tor_proxy()}


def _is_onion_url(url: str) -> bool:
    """
    returns True/False depending on if a URL looks like a Tor hidden service
    (.onion) or not.
    This is designed to false as non-onion just to be on the safe-ish side,
    depending on your view point. It requires URLs like: http://domain.tld/,
    not http://domain.tld or domain.tld/.

    This can be optimized a lot.
    """
    try:
        url_parts = url.split("/")
        domain = url_parts[2]
        tld = domain.split(".")[-1]
        if tld == "onion":
            return True
    except Exception:
        pass
    return False


@dataclass
class APIClient:
    api_endpoint: str = API_ENDPOINT

    def __post_init__(self) -> None:
        headers = httpx.Headers(HEADERS)
        proxy = None
        if _is_onion_url(self.api_endpoint):
            proxy = _get_tor_proxy()
        self._httpx_client = httpx.Client(headers=headers, proxies=proxy)

    def _api_request(
        self,
        url: str,
        empty_post: bool = False,
        json_params: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        retry: bool = False,
    ) -> Any:
        try:
            if empty_post is True:
                request = self._httpx_client.post(url, timeout=POST_TIMEOUT)
            elif json_params is None:
                request = self._httpx_client.get(url, timeout=GET_TIMEOUT)
            else:
                request = self._httpx_client.post(
                    url,
                    json=json_params,
                    timeout=POST_TIMEOUT,
                )
        except Exception as e:
            if retry is True:
                log.warning(f"Got an error, but retrying: {e}")
                sleep(5)
                # Try again.
                return self._api_request(
                    url,
                    empty_post=empty_post,
                    json_params=json_params,
                    retry=retry,
                )
            else:
                raise

        status_code_first_digit = request.status_code // 100
        if status_code_first_digit == 2:
            try:
                return request.json()
            except Exception:
                return request.content
        elif status_code_first_digit == 4:
            log.debug("HTTP status code: {request.status_code}")
            raise exceptions.SporeStackUserError(request.content.decode("utf-8"))
        elif status_code_first_digit == 5:
            if retry is True:
                log.warning(request.content.decode("utf-8"))
                log.warning("Got a 500, retrying in 5 seconds...")
                sleep(5)
                # Try again if we get a 500
                return self._api_request(
                    url,
                    empty_post=empty_post,
                    json_params=json_params,
                    retry=retry,
                )
            else:
                raise exceptions.SporeStackServerError(str(request.content))
        else:
            # Not sure why we'd get this.
            request.raise_for_status()
            raise Exception("Stuff broke strangely. Please contact SporeStack support.")

    def server_launch(
        self,
        machine_id: str,
        days: int,
        flavor: str,
        operating_system: str,
        ssh_key: str,
        token: str,
        region: Optional[str] = None,
        hostname: str = "",
        autorenew: bool = False,
    ) -> None:
        """Launch a server."""
        request = api.ServerLaunch.Request(
            days=days,
            token=token,
            flavor=flavor,
            region=region,
            operating_system=operating_system,
            ssh_key=ssh_key,
            hostname=hostname,
            autorenew=autorenew,
        )
        url = self.api_endpoint + api.ServerLaunch.url.format(machine_id=machine_id)
        self._api_request(url=url, json_params=request.dict())

    def server_topup(
        self,
        machine_id: str,
        days: int,
        token: str,
    ) -> None:
        """Topup a server."""
        request = api.ServerTopup.Request(days=days, token=token)
        url = self.api_endpoint + api.ServerTopup.url.format(machine_id=machine_id)
        self._api_request(url=url, json_params=request.dict())

    def server_quote(self, days: int, flavor: str) -> api.ServerQuote.Response:
        """Get a quote for how much a server will cost."""

        url = self.api_endpoint + api.ServerQuote.url
        response = self._httpx_client.get(
            url=url,
            params={"days": days, "flavor": flavor},
        )
        if response.status_code == 422:
            raise exceptions.SporeStackUserError(response.json()["detail"])

        response.raise_for_status()
        return api.ServerQuote.Response.parse_obj(response.json())

    def autorenew_enable(self, machine_id: str) -> None:
        """
        Enable autorenew on a server.
        """
        url = self.api_endpoint + api.ServerEnableAutorenew.url.format(
            machine_id=machine_id
        )
        self._api_request(url, empty_post=True)

    def autorenew_disable(self, machine_id: str) -> None:
        """
        Disable autorenew on a server.
        """
        url = self.api_endpoint + api.ServerDisableAutorenew.url.format(
            machine_id=machine_id
        )
        self._api_request(url, empty_post=True)

    def server_start(self, machine_id: str) -> None:
        """
        Power on the server.
        """
        url = self.api_endpoint + api.ServerStart.url.format(machine_id=machine_id)
        self._api_request(url, empty_post=True)

    def server_stop(self, machine_id: str) -> None:
        """
        Power off the server.
        """
        url = self.api_endpoint + api.ServerStop.url.format(machine_id=machine_id)
        self._api_request(url, empty_post=True)

    def server_delete(self, machine_id: str) -> None:
        """
        Delete the server.
        """
        url = self.api_endpoint + api.ServerDelete.url.format(machine_id=machine_id)
        self._api_request(url, empty_post=True)

    def server_forget(self, machine_id: str) -> None:
        """
        Forget about a destroyed/deleted server.
        """
        url = self.api_endpoint + api.ServerForget.url.format(machine_id=machine_id)
        self._api_request(url, empty_post=True)

    def server_rebuild(self, machine_id: str) -> None:
        """
        Rebuilds the server with the operating system and SSH key set at launch time.

        Deletes all of the data on the server!
        """
        url = self.api_endpoint + api.ServerRebuild.url.format(machine_id=machine_id)
        self._api_request(url, empty_post=True)

    def server_info(self, machine_id: str) -> api.ServerInfo.Response:
        """
        Returns info about the server.
        """
        url = self.api_endpoint + api.ServerInfo.url.format(machine_id=machine_id)
        response = self._api_request(url)
        response_object = api.ServerInfo.Response.parse_obj(response)
        return response_object

    def servers_launched_from_token(
        self, token: str
    ) -> api.ServersLaunchedFromToken.Response:
        """
        Returns info of servers launched from a given token.
        """
        url = self.api_endpoint + api.ServersLaunchedFromToken.url.format(token=token)
        response = self._api_request(url)
        response_object = api.ServersLaunchedFromToken.Response.parse_obj(response)
        return response_object

    def flavors(self) -> api.Flavors.Response:
        """Returns available flavors (server sizes)."""
        url = self.api_endpoint + api.Flavors.url
        response = self._api_request(url)
        response_object = api.Flavors.Response.parse_obj(response)
        return response_object

    def operating_systems(self) -> api.OperatingSystems.Response:
        """Returns available operating systems."""
        url = self.api_endpoint + api.OperatingSystems.url
        response = self._api_request(url)
        response_object = api.OperatingSystems.Response.parse_obj(response)
        return response_object

    def token_add(
        self,
        token: str,
        dollars: int,
        currency: str,
        retry: bool = False,
    ) -> api.TokenAdd.Response:
        """Add balance (money) to a token."""
        request = api.TokenAdd.Request(dollars=dollars, currency=currency)
        url = self.api_endpoint + api.TokenAdd.url.format(token=token)
        response = self._api_request(url=url, json_params=request.dict(), retry=retry)
        response_object = api.TokenAdd.Response.parse_obj(response)
        return response_object

    def token_balance(self, token: str) -> api.TokenBalance.Response:
        """Return a token's balance."""
        url = self.api_endpoint + api.TokenBalance.url.format(token=token)
        response = self._api_request(url=url)
        response_object = api.TokenBalance.Response.parse_obj(response)
        return response_object

    def token_get_messages(self, token: str) -> List[api.TokenMessage]:
        """Get messages for/from the token."""
        url = self.api_endpoint + f"/token/{token}/messages"
        log.debug(f"Token send message URL: {url}")
        response = self._httpx_client.get(url=url)
        if response.status_code == 422:
            raise exceptions.SporeStackUserError(response.json()["detail"])
        response.raise_for_status()

        return parse_obj_as(List[api.TokenMessage], response.json())

    def token_send_message(self, token: str, message: str) -> None:
        """Send a message to SporeStack support."""
        url = self.api_endpoint + f"/token/{token}/messages"
        response = self._httpx_client.post(url=url, json={"message": message})
        if response.status_code == 422:
            raise exceptions.SporeStackUserError(response.json()["detail"])

        response.raise_for_status()
