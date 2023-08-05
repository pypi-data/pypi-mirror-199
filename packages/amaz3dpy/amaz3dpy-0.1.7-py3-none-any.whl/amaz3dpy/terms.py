from gql import Client, gql
from amaz3dpy.webapiclients.gqlhttpclient import GQLHttpClient, GQLHttpClientError
from amaz3dpy.auth import Auth

from amaz3dpy.models import UserInfoForATACOutput

class Terms:
    def __init__(self, auth: Auth):
        self._auth = auth

    def user_info_related_to_terms_and_conditions(self) -> dict:
        query = gql(
            """
            query UserInfoRelatedToTermsAndConditions {
                UserInfoRelatedToTermsAndConditions {
                    fullName
                    accepted
                    marketing
                    shareData
                }
            }
            """
        )

        params = {

        }

        try:
            terms = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, UserInfoForATACOutput)
            return terms
        except GQLHttpClientError as ex:
            return None

    
