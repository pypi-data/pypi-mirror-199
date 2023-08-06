"""Karrio Canada post client settings."""

from base64 import b64encode
from karrio.core.settings import Settings as BaseSettings


class Settings(BaseSettings):
    """Canada post connection settings."""

    username: str
    password: str
    customer_number: str
    contract_id: str = None
    language: str = "en"

    id: str = None
    account_country_code: str = "CA"
    metadata: dict = {}

    @property
    def carrier_name(self):
        return "canadapost"

    @property
    def server_url(self):
        return (
            "https://ct.soa-gw.canadapost.ca"
            if self.test_mode
            else "https://soa-gw.canadapost.ca"
        )

    @property
    def tracking_url(self):
        return "https://www.canadapost-postescanada.ca/track-reperage/" + self.language + "#/resultList?searchFor={}"

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return b64encode(pair.encode("utf-8")).decode("ascii")


def format_ca_postal_code(code: str = None) -> str:
    """Format canadian postal code."""
    return (code or "").replace(" ", "").upper()
