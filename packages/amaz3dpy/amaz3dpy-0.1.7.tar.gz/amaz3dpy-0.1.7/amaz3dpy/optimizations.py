import requests
import os
from gql import Client, gql
from amaz3dpy.webapiclients.gqlhttpclient import GQLHttpClient, GQLHttpClientError
from amaz3dpy.webapiclients.gqlwebsocketsclient import GQLWebsocketsClient

from amaz3dpy.auth import Auth
from amaz3dpy.models import CreateOptimizationDto, CursorPaging, ObjectModel, Optimization, OptimizationConnection, OptimizationFilter, OptimizationFilterProjectFilter, OptimizationOutputFormat, OptimizationNormalBakingParamsInput, OptimizationParams, OptimizationPreset, OptimizationSort, RelationId, StringFieldComparison
from amaz3dpy.items import Paging

class OptimizationError(Exception):
    pass

class ProjectOptimizations(Paging):

    def __init__(self, auth: Auth, project = None):
        super().__init__(Optimization, OptimizationFilter, OptimizationSort)
        self._auth = auth
        self._project = project
        if self._project:
            self._project_id = project.id
        self.clear()

    @property
    def project_id(self):
        return self._project_id

    def clear_and_load(self, paging: CursorPaging, filter: OptimizationFilter, sorting: OptimizationSort) -> dict:
        self.clear()
        self.load(paging, filter, sorting)

    def load_next(self) -> int:
        if self._project_id:
            self._filter.project = OptimizationFilterProjectFilter()
            self._filter.project.id = StringFieldComparison()
            self._filter.project.id.eq = self._project_id

        return super().load_next()

    def view_downloads(self, optimization: Optimization):
        tmp = {}
        additional_number = 0

        tmp["original_file"] = optimization.objectModelResult.name
        for opt in optimization.objectModelResult.additionals:
            tmp["original_file_additionals_"+str(additional_number)] = opt.name
            additional_number += 1
    
        additional_number = 0
        if optimization.objectModelResultConverted is not None:
            tmp ["converted_file"] = optimization.objectModelResultConverted.name
            for opt in optimization.objectModelResultConverted.additionals:
                tmp["converted_file_additionals_"+str(additional_number)] = opt.name
                additional_number += 1

        return tmp

    def __download_item(self, objectModel: ObjectModel, dst_file_path = None, dst_path = None):
        if objectModel is None:
            raise ValueError("optimization doesn't have a result")

        r = requests.get(objectModel.publicUrl, allow_redirects=True)
        path = dst_file_path
        
        if dst_file_path is None:
            if dst_path is None:
                raise ValueError("EITHER dst_file_path OR dst_path have to be provided")
            
            #if dst_file_path is None but dst_path exists
            path = os.path.join(dst_path, objectModel.name)

        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'wb').write(r.content)

    def download_result(self, optimization: Optimization, dst_file_path = None, dst_path = None, results_files = False, converted_files = True, additionals=True):
        if optimization.objectModelResult is None:
            raise ValueError("optimization doesn't have a result")

        if dst_file_path is None:
            if dst_path is None:
                raise ValueError("EITHER dst_file_path OR dst_path have to be provided")

        if results_files:
            self.__download_item(optimization.objectModelResult, dst_file_path, dst_path)

            if additionals:
                for opt in optimization.objectModelResult.additionals:
                    self.__download_item(opt, dst_file_path, dst_path)

        if converted_files and optimization.objectModelResultConverted is not None:
            self.__download_item(optimization.objectModelResultConverted, dst_file_path, dst_path)

            if additionals:
                for opt in optimization.objectModelResultConverted.additionals:
                    self.__download_item(opt, dst_file_path, dst_path)
            
        return True
    def create_optimization(
        self, create_optimization: CreateOptimizationDto = None, 
        name: str = None, outputFormat: OptimizationOutputFormat = None, 
        params: OptimizationParams = None,
        nbparams: OptimizationNormalBakingParamsInput = None,
        preset: OptimizationPreset = None,
        project_id: str = None,
        relatedTo_id: str = None
    ) -> Optimization:

        if create_optimization is None:
            if name is None and outputFormat is None and (params is None or preset is None or nbparams is None):
                raise ValueError("EITHER 'name', 'outputFormat', and one of 'params', 'preset' and 'nbparams' OR 'create_optimization' must be provided")
            
            if project_id is None and self._project is None:
                raise ValueError("Project must be provided when calling this method. Please provide project_id or a project")

            create_optimization = CreateOptimizationDto()
            create_optimization.name = name
            create_optimization.outputFormat = outputFormat

            if nbparams:
                if relatedTo_id is None:
                    raise ValueError("Optimization must be provided when calling this method. Please provide relatedTo_id")

                create_optimization.nbparams = nbparams
                create_optimization.relatedTo = RelationId()
                create_optimization.relatedTo.id = relatedTo_id

            if params:
                create_optimization.params = params
            else:
                create_optimization.preset = preset

            create_optimization.project = RelationId()
            create_optimization.project.id = project_id or self._project_id


        query = gql(
            """
            mutation CreateOptimization($input: CreateOneOptimizationInput!) {
                createOneOptimization(input: $input) {
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
                    relatedTo {
                        id
                        name
                    }
                    nbparams {
                        opacity
                        width
                        height
                        image_format
                        normal_format
                    }
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
                    feedback
                    objectModelResultObj {
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
                "optimization": create_optimization.dict(exclude_unset=True)
            }
        }

        try:
            optimization = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, Optimization)
            self._store_item(optimization, id=optimization.id)
            return optimization
        except GQLHttpClientError as ex:
            raise OptimizationError(ex)
        

    def _load_items(self, paging: CursorPaging, filter: OptimizationFilter, sort: OptimizationSort) -> dict:
        query = gql(
            """
            query Optimizations ($paging: CursorPaging, $filter: OptimizationFilter, $sorting: [OptimizationSort!]) {
                items: optimizations(filter: $filter, paging: $paging, sorting: $sorting) {
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
                            relatedTo {
                                id
                                name
                            }
                            nbparams {
                                opacity
                                width
                                height
                                image_format
                                normal_format
                            }
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
                            feedback
                            objectModelResultObj {
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
                            }
                            project {
                                id
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
            items = GQLHttpClient(self._auth.token, self._auth.url, self._auth.use_ssl).execute(query, params, OptimizationConnection)
            return items
        except GQLHttpClientError as ex:
            return 0

    async def _handle_subscription(self):
        subscription = gql(
            """
            subscription OptimizationUpdated {
                updatedOneOptimization {
                    id
                    name
                    status
                    outputFormat
                    type
                    relatedTo {
                        id
                        name
                    }
                    nbparams {
                        opacity
                        width
                        height
                        image_format
                        normal_format
                    }
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
                    feedback
                    objectModelResultObj {
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
                    }
                    project {
                        id
                        allowsNormalsBaking
                        allowsVertexMaskPolygonReduction
                    }
                }
            }
            """
        )

        async with Client(
            transport=GQLWebsocketsClient(self._auth.token, self._auth.url, self._auth.use_ssl).transport(), fetch_schema_from_transport=True,
        ) as session:
            async for result in session.subscribe(subscription):
                item = Optimization(**result["updatedOneOptimization"])
                self._store_item(item, item.id)
                self._on_item_received(item)