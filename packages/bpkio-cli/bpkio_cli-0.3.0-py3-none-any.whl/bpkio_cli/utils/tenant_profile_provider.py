import configparser
from os import environ, path
from pathlib import Path
from typing import Optional

from bpkio_cli.api.crudeApi import BroadpeakIoCrudeApi

DEFAULT_INI_FILE = path.join(path.expanduser("~"), ".bpkio/tenants")


class TenantProfileProvider:
    config = configparser.ConfigParser()

    def __init__(self, filename: Optional[str] = None) -> None:
        f = Path(filename or DEFAULT_INI_FILE)
        if not f.exists():
            f.parent.mkdir(exist_ok=True, parents=True)
            f.touch()

        self._filename = f
        self._read_ini_file()

    @property
    def inifile(self):
        return self._filename

    def get_api_key(self, tenant: Optional[str] = None):
        return self._get_config_value(
            "api_key",
            tenant=tenant,
            env_var="BPKIO_API_KEY",
            must_be_in_section_if_exists=True,
        )

    def get_fqdn(self, tenant: Optional[str] = None):
        return self._get_config_value(
            "fqdn",
            tenant=tenant,
            env_var="BPKIO_API_FQDN",
            allow_null=True,
            default=BroadpeakIoCrudeApi.DEFAULT_FQDN,
        )

    def list_tenants(self):
        tenants = []
        for section in self.config.sections():
            tenants.append(
                dict(
                    tenant=section,
                    id=self.config[section].get("id"),
                    fqdn=self.config[section].get("fqdn"),
                )
            )
        return tenants

    def has_tenant(self, tenant: str):
        return tenant in self.config

    def has_default_tenant(self):
        return self.has_tenant("default")

    def _get_tenant_section(self, tenant: str | None):
        tenant_section = None
        if tenant:
            if tenant in self.config:
                # tenant is the key in a section of the config file
                tenant_section = self.config[tenant]

            elif tenant.isdigit():
                # by tenant ID, in the first section that contains it
                for section in self.config.sections():
                    if (
                        "id" in self.config[section]
                        and self.config[section]["id"] == tenant
                    ):
                        tenant_section = self.config[section]

            if not tenant_section:
                raise InvalidTenantError(
                    f"There is no tenant `{tenant}` in the file at {self._filename}"
                )

        if not tenant_section and "default" in self.config:
            # default section
            tenant_section = self.config["default"]

        if not tenant_section:
            raise NoTenantSectionError()

        return tenant_section

    def _get_config_value(
        self,
        key: str,
        tenant: Optional[str] = None,
        env_var: Optional[str] = None,
        default: Optional[str] = None,
        allow_null: bool = False,
        must_be_in_section_if_exists=False,
    ):
        # first try to get that key from the config section
        try:
            if tenant_config := self._get_tenant_section(tenant):
                return tenant_config[key]
        except InvalidTenantError as e:
            raise e
        except MissingConfigValueError as e:
            if must_be_in_section_if_exists:
                raise e
        except Exception as e:
            pass

        # if not there, try an env var
        if env_var:
            if value := self._from_env(env_var):
                return value

        # otherwise use a default
        if default:
            return default

        if allow_null:
            return False

        raise MissingConfigValueError(
            f"Could not find a config value for '{key}' in config file or '{env_var}' environment variable"
        )

    def _read_ini_file(self):
        # TODO - warning if the file does not exist
        self.config.read(DEFAULT_INI_FILE)

    def _from_config_file_section(self, tenant: str, key: str) -> str:
        return self.config[tenant][key]

    def _from_env(self, var) -> Optional[str]:
        return environ.get(var)

    def add_tenant(self, key: str, entries: dict):
        self.config[key] = entries
        with open(self._filename, "w") as ini:
            self.config.write(ini)


class InvalidTenantError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class NoTenantSectionError(Exception):
    def __init__(self) -> None:
        super().__init__(
            "No valid tenant section could be found in the tenant config file"
        )


class MissingConfigValueError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
