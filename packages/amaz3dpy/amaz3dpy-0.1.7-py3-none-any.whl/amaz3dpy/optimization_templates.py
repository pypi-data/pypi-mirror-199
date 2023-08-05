from gql import Client, gql
from amaz3dpy.webapiclients.gqlwebsocketsclient import GQLWebsocketsClient

from amaz3dpy.webapiclients.gqlhttpclient import GQLHttpClient, GQLHttpClientError
from amaz3dpy.auth import Auth
from amaz3dpy.models import CursorPaging, CreateOneOptimizationTemplateInput, OptimizationTemplate, OptimizationTemplateFilter, OptimizationTemplateSort
from amaz3dpy.items import Paging

class OptimizationTemplates(Paging):

    def __init__(self, auth: Auth):
        super().__init__(CreateOneOptimizationTemplateInput, OptimizationTemplateFilter, OptimizationTemplateSort)
        self._auth = auth
        self.clear()

    def list(self):
        with self._lock:
            return Paging.get_list(self._items)

    def clear_and_load(self, paging: CursorPaging, filter: OptimizationTemplateFilter, sorting: OptimizationTemplateSort) -> dict:
        self.clear()
        self.load(paging, filter, sorting)

    def load_next(self) -> int:
        return super().load_next()

    def create_optimizations_from_template(self, name_optimizations: str = None, project_id: str = None, optimization_template_id: str = None):
        query = gql(
            """
            mutation createOptimizationsFromTemplate($input: OptimizationFromTemplateInput!) {
                createOptimizationsFromTemplate(input: $input) {
                    id
                    name
                    status
                    outputFormat
                    outputFormatOptions {
                        format_glb {
                            export_draco_mesh_compression_enable
                        }
                        format_gltf {
                            export_draco_mesh_compression_enable
                        }
                    }
                    type
                    params {
                        face_reduction
                        feature_importance
                        uv_seam_importance
                        preserve_boundary_edges
                        preserve_hard_edges
                        preserve_smooth_edges
                        retexture
                        merge_duplicated_uv
                        remove_isolated_vertices
                        remove_non_manifold_faces
                        remove_duplicated_faces
                        remove_duplicated_boundary_vertices
                        remove_degenerate_faces
                        project_normals
                        use_vertex_mask
                        resize_images
                        normals_weighting
                        contrast
                        joined_simplification
                        normals_scaling
                        minimum_face_number
                        remove_meshes_by_size
                        remove_meshes_by_count
                    }
                    preset
                    objectModelResult {
                        id
                        name
                        path
                        picture {
                            publicUrl
                        }
                        publicUrl
                        triangleCount
                        fileSizeBytes
                        additionals {
                            name
                            publicUrl2
                            publicUrl
                            id
                            path
                        }
                    }
                    objectModelResultConverted {
                        id
                        name
                        path
                        picture {
                            publicUrl
                        }
                        publicUrl2
                        publicUrl
                        triangleCount
                        fileSizeBytes
                        additionals {
                            name
                            publicUrl2
                            publicUrl
                            id
                            path
                        }
                    }
                    lastActivityAt
                    objectModelResultObj {
                        id
                        name
                        path
                        picture {
                            publicUrl
                        }
                        publicUrl
                        triangleCount
                        fileSizeBytes
                    }
                    project {
                        id
                    }
                }
            }
            """
        )

        params = {
            "input": {
                "name": name_optimizations,
                "projectId": project_id,
                "templateId": optimization_template_id
            }
        }

        try:
            return GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params)
        except GQLHttpClientError:
            return GQLHttpClientError("Unable to retrive create the optimization")

    def _load_items(self, paging: CursorPaging, filter: OptimizationTemplateFilter, sort: OptimizationTemplateSort) -> dict:
        query = gql(
            """
            query OptimizationTemplates($paging: CursorPaging, $filter: OptimizationTemplateFilter, $sort: [OptimizationTemplateSort!]) {
                items: optimizationTemplates(paging: $paging, filter: $filter, sorting: $sort) {
                    pageInfo {
                        startCursor
                        endCursor
                        hasNextPage
                        hasPreviousPage
                    }
                    edges {
                        cursor
                        node {
                            id
                            name
                            description
                            lastActivityAt
                            optimizationTemplateItems {
                                id
                                name
                                preset
                                outputFormat
                                outputFormatOptions {
                                    format_glb {
                                        export_draco_mesh_compression_enable
                                    }
                                    format_gltf {
                                        export_draco_mesh_compression_enable
                                    }
                                }
                            }
                            customer {
                                id
                                user {
                                    fullName
                                }
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
            return GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, OptimizationTemplate)
        except GQLHttpClientError as ex:
            return 0

    async def _handle_subscription(self):
        pass