from bpkio_cli.api.crudeApi import BroadpeakIoCrudeApi
from bpkio_cli.core.resources import ResourcesContext
from bpkio_cli.utils.tenant_profile_provider import TenantProfileProvider


class AppContext:
    def __init__(
        self, api: BroadpeakIoCrudeApi, tenant_provider: TenantProfileProvider
    ):
        self.api = api
        self.tenant_provider = tenant_provider
        self.tenant = None

        self.settings = dict()
        self.resources = ResourcesContext()
