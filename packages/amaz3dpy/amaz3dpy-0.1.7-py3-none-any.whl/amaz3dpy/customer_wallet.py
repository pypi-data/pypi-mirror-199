from gql import Client, gql
from amaz3dpy.webapiclients.gqlwebsocketsclient import GQLWebsocketsClient

from amaz3dpy.webapiclients.gqlhttpclient import GQLHttpClient, GQLHttpClientError
from amaz3dpy.auth import Auth
from amaz3dpy.models import CustomerWalletDto

class CustomerWalletError(Exception):
    pass

class CustomerWallet():
    def __init__(self, auth: Auth):
        self._auth = auth

    def retrive(self) -> CustomerWalletDto:
        query = gql(
            """
            query Wallet {
                wallet: getWallet {
                    value
                    type
                    customer_id
                    expires
                    bytes_limit
                }
            }
            """
        )

        params = {
        }

        try:
            result = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, CustomerWalletDto)
            return result
        except GQLHttpClientError as ex:
            raise GQLHttpClientError("Unable to retrive wallet: " + str(ex))