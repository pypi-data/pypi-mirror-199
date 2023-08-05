from gql import Client, gql
from amaz3dpy.webapiclients.gqlwebsocketsclient import GQLWebsocketsClient

from amaz3dpy.models import CursorPaging, ObjectModel, Project, ProjectConnection, ProjectCreateDto, ProjectDeleteResponse, ProjectFilter, ProjectSort
from amaz3dpy.webapiclients.gqlhttpclient import GQLHttpClient, GQLHttpClientError
from amaz3dpy.auth import Auth
from amaz3dpy.items import Paging

import os

class Projects(Paging):

    def __init__(self, auth: Auth):
        super().__init__(Project, ProjectFilter, ProjectSort)
        self._auth = auth
        self.clear()

    def delete_project(self, project_id):
        query = gql(
            """
            mutation DeleteProject($id: ID!) {
                deleteOneProject(input: {id: $id}) {
                    id
                }
            }
            """
        )

        params = {
            "id" : project_id
        }

        project_delete_response = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, ProjectDeleteResponse)
        self._remove_item(project_delete_response.id)
        return


    def create_project(self, project_create: ProjectCreateDto = None, name: str = None, file_path: str = None, additional_files_path = {}) -> Project:
        if project_create is None:
            if name is None and file_path is None:
                raise ValueError("BOTH 'name' and 'file_path' OR 'project_create' must be provided")
            om = self.upload_object_model(file_path)
            for additional_file in additional_files_path:
                self.upload_object_model(additional_file, om.id)
            project_create = ProjectCreateDto(name=name, objectModel={"id" : om.id})

        query = gql(
            """
            mutation CreateProject($input: CreateOneProjectInput!) {
                createOneProject(input: $input) {
                    conversionStatus
                    allowsNormalsBaking
                    allowsVertexMaskPolygonReduction
                    lastActivityAt
                    id
                    name
                    objectModel {
                        fileSizeBytes
                        picture {
                            publicUrl
                        }
                        triangleCount
                        name
                    }
                }
            }
            """
        )

        params = {
            "input": {
                "project" : project_create.dict(exclude_unset=True)
            }
        }

        project = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, Project)
        self._store_item(project, id=project.id)
        return project

    def upload_object_model(self, src_path: str, relatedTo: str = None) -> ObjectModel:
        query = gql(
            """
            mutation UploadProjectFile($input: FileUploadInput!) {
                    uploadObjectModel(input: $input) {
                        id
                    }
                }
            """)

        # cd src_path and extracts filename
        if os.name == "posix":
            os.chdir(os.path.expanduser(os.path.dirname(src_path)))
            src_path = os.path.basename(src_path)

        with open(src_path, "rb") as f:
            params = {
                "input": {
                    "relatedTo": relatedTo,
                    "file": f
                }
            }

            object_model = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, ObjectModel, upload_files=True)
            return object_model

    def clear_and_load(self, paging: CursorPaging, filter: ProjectFilter, sorting: ProjectSort) -> dict:
        self.clear()
        self.load(paging, filter, sorting)

    def _load_items(self, paging: CursorPaging, filter: ProjectFilter, sort: ProjectSort) -> dict:
        query = gql(
            """
            query Projects($paging: CursorPaging, $filter: ProjectFilter, $sorting: [ProjectSort!]) {
                items: projects(filter: $filter, paging: $paging, sorting: $sorting) {
                    pageInfo {
                        startCursor
                        endCursor
                        hasNextPage
                        hasPreviousPage
                    }
                    edges {
                        cursor
                        node {
                            conversionStatus
                            optimizationsCount
                            lastActivityAt
                            id
                            name
                            allowsNormalsBaking
                            allowsVertexMaskPolygonReduction
                            objectModel {
                                fileSizeBytes
                                picture {
                                    publicUrl
                                }
                                triangleCount
                                name
                            }
                        }
                    }
                }
            }
            """
        )

        params = {
            "paging": paging.dict(exclude_unset=True),
            "filter": filter.dict(exclude_unset=True),
            "sorting": sort.dict(exclude_unset=True)
        }

        try:
            items = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, ProjectConnection)
            return items
        except GQLHttpClientError as ex:
            return None

    async def _handle_subscription(self):
        subscription = gql(
            """
            subscription ProjectUpdated {
                updatedOneProject {
                    id
                    conversionStatus
                    allowsNormalsBaking
                    allowsVertexMaskPolygonReduction
                    objectModelObj {
                        fileSizeBytes
                        name
                        picture {
                            publicUrl
                        }
                        publicUrl
                        triangleCount
                        id
                        path
                    }
                    objectModel {
                        fileSizeBytes
                        name
                        picture {
                            publicUrl
                        }
                        publicUrl
                        triangleCount
                        id
                        path
                    }
                    name
                }
            }
            """
        )

        async with Client(
            transport=GQLWebsocketsClient(self._auth.token, self._auth.url, self._auth.use_ssl).transport(), fetch_schema_from_transport=True,
        ) as session:
            async for result in session.subscribe(subscription):
                item = Project(**result["updatedOneProject"])
                self._store_item(item, item.id)
                self._on_item_received(item)
