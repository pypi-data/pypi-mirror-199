import base64
import json
import logging
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests


class BroadpeakIoCrudeApi:
    DEFAULT_FQDN = "api.broadpeak.io"
    API_VERSION = "v1"

    def __init__(self, api_key: str, fqdn: Optional[str]) -> None:
        self.logger = logging.getLogger("bpkio.sdk")

        self._api_key = api_key
        # TODO - validate the FQDN
        if fqdn:
            self._fqdn = fqdn
            self.logger.debug("FQDN: " + self._fqdn)

    @property
    def base_url(self):
        return "https://" + (self._fqdn or self.DEFAULT_FQDN) + "/" + self.API_VERSION

    def uses_default_fqdn(self) -> bool:
        return self._fqdn == self.DEFAULT_FQDN

    @staticmethod
    def is_valid_api_key_format(string: str):
        try:
            BroadpeakIoCrudeApi._parse_api_key(string)
            return True
        except:
            return False

    @staticmethod
    def _parse_api_key(candidate: str) -> dict:
        parts = candidate.split(".")
        # Padding is required. Length doesn't matter provided it's long enough
        base64_bytes = parts[1] + "========"
        s = base64.b64decode(base64_bytes).decode("utf-8")
        payload = json.loads(s)
        return payload

    def parse_api_key(self) -> dict:
        try:
            payload = self._parse_api_key(self._api_key)
            self.logger.debug("API Key payload: " + str(payload))
            return payload
        except Exception as e:
            raise InvalidApiKeyFormat()

    @staticmethod
    def extract_fqdn(full_url: str) -> str:
        url = "https://www.example.com/path/to/page.html"
        parsed_url = urlparse(url)
        fqdn = parsed_url.netloc
        return fqdn

    def _make_url(self, path: str) -> str:
        if path.startswith("/"):
            path = path[1:]
        return f"{self.base_url}/{path}"

    def _get_std_headers(self) -> object:
        return {
            "accept": "application/json",
            "authorization": f"Bearer {self._api_key}",
        }

    def get(self, path: str, params: Optional[Dict] = None) -> Any:
        url = self._make_url(path)
        headers = self._get_std_headers()

        self.logger.debug(f"GET {url}")

        response = requests.get(url, headers=headers, params=params)
        response_json = response.json()

        self.logger.debug(f" -> ({response.status_code}) {str(response_json)}")

        if "error" in response_json:
            raise ApiClientError(
                "{c} - {m}".format(
                    c=response_json.get("statusCode"),
                    m=response_json.get("message"),
                )
            )

        self.decorate_resource_with_url(response_json, url)

        return response.json()

    def post(self, path: str, payload: object) -> Dict:
        url = self._make_url(path)
        headers = self._get_std_headers()

        self.logger.debug(f"POST {url} with {str(payload)}")

        response = requests.post(url, headers=headers, json=payload)

        self.logger.debug(f" -> ({response.status_code}) {str(response.json())}")

        if response.status_code == 201:
            return response.json()
        if response.status_code == 403:
            raise ObjectExistsError(response.json()["message"])
        raise OtherApiError(response.json()["message"])

    def delete(self, path: str) -> object:
        url = self._make_url(path)
        headers = self._get_std_headers()

        self.logger.debug(f"DELETE {url}")

        response = requests.delete(url, headers=headers)

        self.logger.debug(f" -> ({response.status_code})")

        return None

    # Status Endpoint
    def get_status(self):
        response = self.get(path="status")
        return response

    @staticmethod
    def is_correct_entrypoint(url: str, api_key: str) -> bool:
        """Checks that the URL is a valid Broadpeak.io entrypoint"""
        try:
            api = BroadpeakIoCrudeApi(api_key=api_key, fqdn=url)
            api.get_my_tenant()
            return True
        except:
            return False

    # Sources Endpoints

    def list_sources(self) -> List:
        response = self.get(path=f"sources")
        self.decorate_resource_with_title(response, "Source")
        return response

    def get_source(self, id) -> Any:
        """Retrieve a type-specific source, by its ID only"""
        source = self.retrieve_source_by("id", id)
        if source:
            payload = self.get(f"sources/{source['type']}/{id}")
            payload["type"] = source["type"]

            self.decorate_resource_with_title(payload, "Source")
            return payload

    def retrieve_source_by(self, field, value) -> Optional[Dict]:
        sources = self.list_sources()
        for source in sources:
            if source.get(field) == value:
                self.logger.info(
                    f"Retrieved {source.get('type')} source [{source.get('id')}]"
                )
                return source

    def check_source(self, id) -> Any:
        source = self.retrieve_source_by("id", id)
        if source:
            return self.get(
                f"sources/{source['type']}/check", params={"url": source["url"]}
            )

    @lru_cache
    def create_or_retrieve_source(
        self, mode: str, name: str, url: str, description: str = ""
    ) -> object:
        try:
            return self.create_source(mode, name, url, description)
        except ObjectExistsError as e:
            return self.retrieve_source_by("url", url)

    def create_source(self, mode: str, name: str, url: str, **kwargs) -> object:
        payload = {"name": name, "url": url}
        payload.update(kwargs)

        response = self.post(path=f"sources/{mode}", payload=payload)
        self.logger.info(f"Created {mode} source [{response['id']}]: {url}")
        return response

    def create_source_live(self, name: str, url: str):
        return self.create_source("live", name, url)

    def create_source_asset(self, name: str, url: str):
        return self.create_source("asset", name, url)

    def create_source_slate(self, name: str, url: str):
        return self.create_source("slate", name, url)

    def create_source_adserver(self, name: str, url: str, queries: str):
        return self.create_source("ad-server", name, url, queries=queries)

    def delete_source(self, mode: str, id: int):
        response = self.delete(path=f"sources/{mode}/{id}")
        self.logger.info(f"Deleted {mode} source [{id}]")
        return response

    # Virtual Channel Endpoints

    def list_services(self) -> List:
        response = self.get(path="/services")
        self.decorate_resource_with_title(response, "Service")
        return response

    def get_service(self, id) -> Any:
        """Retrieve a type-specific source, by its ID only"""
        service = self.retrieve_service_by("id", id)
        if service:
            payload = self.get(f"services/{service['type']}/{id}")
            payload["type"] = service["type"]
            self.decorate_resource_with_title(payload, "Service")
            return payload

    def retrieve_service_by(self, field, value) -> Optional[Dict]:
        services = self.list_services()
        for service in services:
            if service.get(field) == value:
                self.logger.info(
                    f"Retrieved {service.get('type')} source [{service.get('id')}]"
                )
                return service

    @lru_cache
    def create_or_retrieve_virtualchannel(self, name: str, live_source_id: int):
        try:
            return self.create_virtualchannel(name, live_source_id)
        except ObjectExistsError as e:
            return self.retrieve_virtualchannel_by_name(name)

    def create_virtualchannel(self, name: str, live_source_id: int):
        payload = {
            "source": {"id": live_source_id},
            "replacement": {"id": live_source_id},
            "name": name,
        }

        response = self.post(path=f"/services/virtual-channel", payload=payload)
        self.logger.info(f"Created virtual channel [{response['id']}]: {name}")
        return response

    def delete_virtualchannel(self, id: int):
        response = self.delete(path=f"/services/virtual-channel/{id}")
        self.logger.info(f"Deleted virtual source [{id}]")
        return response

    def retrieve_virtualchannel_by_name(self, name: str) -> object:
        services = self.list_services()
        for service in services:
            if service.get("type") == "virtual-channel":
                if service.get("name") == name:
                    self.logger.info(f"Retrieved virtual channel [{service.get('id')}]")
                    return service

    # Scheduling

    def create_slot(
        self,
        virtual_channel_id: int,
        source_id: int,
        name: str,
        start_time: datetime,
        duration: int,
    ):
        payload = {
            "replacement": {"id": source_id},
            "name": name,
            "startTime": str(start_time),
            "duration": duration,
        }

        return self.post(
            path=f"/services/virtual-channel/{virtual_channel_id}/slots",
            payload=payload,
        )

    def list_transcoding_profiles(self, tenant_id: Optional[int] = None):
        params = {}
        if tenant_id:
            params["tenantId"] = tenant_id

        response = self.get(path="/transcoding-profiles", params=params)
        self.decorate_resource_with_title(response, "TranscodingProfile")
        return response

    def get_transcoding_profile(self, profile_id: int, tenant_id: Optional[int] = None):
        params = {}
        if tenant_id:
            params["tenantId"] = tenant_id

        response = self.get(path=f"/transcoding-profiles/{profile_id}", params=params)
        self.decorate_resource_with_title(response, "TranscodingProfile")
        return response

    def list_tenants(self):
        response = self.get(path="/tenants")
        self.decorate_resource_with_title(response, "Tenant")
        return response

    def get_tenant(self, tenant_id: int):
        response = self.get(path=f"/tenants/{tenant_id}")
        self.decorate_resource_with_title(response, "Tenant")
        return response

    def get_my_tenant(self):
        tenant_id = self._parse_api_key(self._api_key)["tenantId"]
        return self.get_tenant(tenant_id)

    def list_users(self):
        response = self.get(path="/users")
        self.decorate_resource_with_title(response, "User")
        return response

    def retrieve_user_by(self, field, value) -> Optional[Dict]:
        users = self.list_users()
        for user in users:
            if user.get(field) == value:
                return user

    def get_consumption(
        self, from_time: datetime, to_time: datetime, tenant_id: int = None
    ):
        params = {
            "start-time": from_time.isoformat(),
            "end-time": to_time.isoformat(),
        }
        if tenant_id:
            params["tenantId"] = tenant_id

        return self.get(path="/consumption", params=params)

    @staticmethod
    def extract_service_id(url):
        return url.split("/")[3]

    @staticmethod
    def decorate_resource_with_title(resource, value):
        BroadpeakIoCrudeApi.decorate_resource_with_key(
            resource, "__resourceTitle", value
        )

    @staticmethod
    def decorate_resource_with_url(resource, value):
        BroadpeakIoCrudeApi.decorate_resource_with_key(resource, "__urlPath", value)

    @staticmethod
    def decorate_resource_with_key(resource, key, value):
        if isinstance(resource, dict):
            resource[key] = value
        if isinstance(resource, list):
            for el in resource:
                BroadpeakIoCrudeApi.decorate_resource_with_key(el, key, value)

    @staticmethod
    def strip_resource_decorations(d):
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [BroadpeakIoCrudeApi.strip_resource_decorations(v) for v in d]

        return {
            k: BroadpeakIoCrudeApi.strip_resource_decorations(v)
            for k, v in d.items()
            if not k.startswith("__")
        }


class ApiClientError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ObjectExistsError(ApiClientError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class OtherApiError(ApiClientError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidApiKeyFormat(ApiClientError):
    def __init__(self, *args) -> None:
        super().__init__("The API Key provided has an invalid format")
