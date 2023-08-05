from __future__ import annotations
from codecs import strict_errors
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List

class StringFieldComparison(BaseModel):
  eq: Optional[str]

class LoginInput(BaseModel):
    email: Optional[str]
    password: Optional[str]

class LoginOutput(BaseModel):
    token: Optional[str]
    refreshToken: Optional[str]

class RefreshInput(BaseModel):
    refreshToken: Optional[str]

class PageInfo(BaseModel):
    hasNextPage: Optional[bool]
    hasPreviousPage: Optional[bool]
    startCursor: Optional[str]
    endCursor: Optional[str]

class CursorPaging(BaseModel):
    before: Optional[str]
    after: Optional[str]
    first: Optional[int]
    last: Optional[int]

class ProjectFilter(BaseModel):
    # and, or excluded
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    customerId: Optional[StringFieldComparison]
    conversionStatus: Optional[StringFieldComparison]
    optimizationsCount: Optional[StringFieldComparison]
    lastActivityAt: Optional[StringFieldComparison]
    iname: Optional[StringFieldComparison]

class ProjectSort(BaseModel):
    field: Optional[str]
    direction: Optional[str]
    nulls: Optional[str]

class OptimizationSort(BaseModel):
  field: Optional[str]
  direction: Optional[str]
  nulls: Optional[str]

class ObjectModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    path: Optional[str]
    publicUrl: Optional[str]
    publicUrl2: Optional[str]
    publicUrlExpiresAt: Optional[str]
    fileSizeBytes: Optional[str]
    triangleCount: Optional[int]
    additionals: Optional[List['ObjectModel']]

class Project(BaseModel):
    id: Optional[str]
    name: Optional[str]
    customerId: Optional[str]
    conversionStatus: Optional[str]
    optimizationsCount: Optional[int]
    conversionError: Optional[str]
    lastActivityAt: Optional[str]
    allowsNormalsBaking: Optional[bool]
    allowsVertexMaskPolygonReduction: Optional[bool]
    objectModel: Optional[ObjectModel]

class ProjectEdge(BaseModel):
    node: Project
    cursor: Optional[str]

class ProjectConnection(BaseModel):
    pageInfo: Optional[PageInfo]
    edges: Optional[List[ProjectEdge]]

class RelationId(BaseModel):
    id: Optional[str]

class ProjectCreateDto(BaseModel):
    name: Optional[str]
    objectModel: Optional[RelationId]
    customer: Optional[RelationId]

class OptimizationParams(BaseModel):
    face_reduction: Optional[float]
    feature_importance: Optional[int]
    uv_seam_importance: Optional[int]
    preserve_boundary_edges: Optional[int]
    preserve_hard_edges: Optional[bool]
    preserve_smooth_edges: Optional[bool]
    retexture: Optional[bool]
    merge_duplicated_uv: Optional[bool]
    remove_isolated_vertices: Optional[bool]
    remove_non_manifold_faces: Optional[bool]
    remove_duplicated_faces: Optional[bool]
    remove_duplicated_boundary_vertices: Optional[bool]
    remove_degenerate_faces: Optional[bool]
    project_normals: Optional[bool]
    use_vertex_mask: Optional[bool]
    resize_images: Optional[int]
    normals_weighting: Optional[float]
    contrast: Optional[float]
    joined_simplification: Optional[bool]
    normals_scaling: Optional[int]
    remove_meshes_by_size: Optional[float]
    remove_meshes_by_count: Optional[int]
    minimum_face_number: Optional[int]

class NormalsBakingFormat(str, Enum):
    png = 'png'
    tga = 'tga'
    jpg = 'jpg'

class OptimizationNormalBakingParams(BaseModel):
    opacity: Optional[float]
    width: Optional[int]
    height: Optional[int]
    normal_format: Optional[int]
    image_format: Optional[NormalsBakingFormat]

class OptimizationNormalBakingParamsInput(BaseModel):
    opacity: Optional[float]
    width: Optional[int]
    height: Optional[int]
    normal_format: Optional[int]
    image_format: Optional[NormalsBakingFormat]

class OptimizationFilterProjectFilter(BaseModel):
    # and, or excluded
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    customerId: Optional[StringFieldComparison]
    conversionStatus: Optional[StringFieldComparison]
    optimizationsCount: Optional[StringFieldComparison]
    lastActivityAt: Optional[StringFieldComparison]

class OptimizationSort(BaseModel):
    field: Optional[str]
    direction: Optional[str]
    nulls: Optional[str]

class OptimizationFilter(BaseModel):
    # and, or excluded
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    status: Optional[StringFieldComparison]
    createdAt: Optional[StringFieldComparison]
    updatedAt: Optional[StringFieldComparison]
    lastActivityAt: Optional[StringFieldComparison]
    project: Optional[OptimizationFilterProjectFilter]

class Optimization(BaseModel):
    id: Optional[str]
    name: Optional[str]
    status: Optional[str]
    type: Optional[str]
    status: Optional[str]
    logs: Optional[str]
    outputFormat: Optional[str]
    preset: Optional[str]
    params: Optional[OptimizationParams]
    nbparams: Optional[OptimizationNormalBakingParams]
    objectModelResult: Optional[ObjectModel]
    objectModelResultObj: Optional[ObjectModel]
    objectModelResultConverted: Optional[ObjectModel]
    createdAt: Optional[str]
    updatedAt: Optional[str]
    lastActivityAt: Optional[str]
    project: Optional[Project]

class OptimizationEdge(BaseModel):
    node: Optional[Optimization]
    cursor: Optional[str]

class OptimizationConnection(BaseModel):
    pageInfo: Optional[PageInfo]
    edges: Optional[List[OptimizationEdge]]

class OptimizationParamsInput(BaseModel):
    face_reduction: Optional[float] = 0.5
    feature_importance: Optional[int] = 0
    uv_seam_importance: Optional[int] = 0
    preserve_boundary_edges: Optional[int] = 2
    preserve_hard_edges: Optional[bool] = True
    preserve_smooth_edges: Optional[bool] = True
    retexture: Optional[bool] = True
    merge_duplicated_uv: Optional[bool]
    remove_isolated_vertices: Optional[bool] = True
    remove_non_manifold_faces: Optional[bool] = True
    remove_duplicated_faces: Optional[bool] = True
    remove_duplicated_boundary_vertices: Optional[bool] = True
    remove_degenerate_faces: Optional[bool] = True
    project_normals: Optional[bool] = False
    use_vertex_mask: Optional[bool] = False
    resize_images: Optional[int] = 0
    normals_weighting: Optional[int] = 0
    contrast: Optional[float] = 0.5
    uv_seam_importance: Optional[int] = 0
    resize_images: Optional[int] = 0
    normals_weighting: Optional[int] = 0
    joined_simplification: Optional[bool] = True
    normals_scaling: Optional[int] = 0
    remove_meshes_by_size: Optional[float] = 0
    remove_meshes_by_count: Optional[int] = 0
    minimum_face_number: Optional[int] = 0

class OptimizationOutputFormat(str, Enum):
    format_obj = 'format_obj'
    format_gltf = 'format_gltf'
    format_stl = 'format_stl'
    format_3ds = 'format_3ds'
    format_fbx = 'format_fbx'

class FormatGLTFOptions(BaseModel):
    export_draco_mesh_compression_enable: Optional[bool]

class OptimizationOutputFormatOptions(BaseModel):
    format_glb: Optional[FormatGLTFOptions]
    format_gltf: Optional[FormatGLTFOptions]

class OptimizationPreset(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class CreateOptimizationDto(BaseModel):
    name: Optional[str]
    outputFormat: Optional[OptimizationOutputFormat]
    preset: Optional[OptimizationPreset]
    project: Optional[RelationId]
    relatedTo: Optional[RelationId]
    params: Optional[OptimizationParamsInput]
    nbparams: Optional[OptimizationNormalBakingParamsInput]

class CreateOneOptimizationInput(BaseModel):
    optimization: Optional[CreateOptimizationDto]

class ProjectDeleteResponse(BaseModel):
    id: Optional[str]
    name: Optional[str]
    customerId: Optional[str]
    conversionStatus: Optional[str]
    optimizationsCount: Optional[int]
    conversionError: Optional[str]
    lastActivityAt: Optional[str]

class CustomerWalletDto(BaseModel):
    value: Optional[int]
    type: Optional[str]
    customer_id: Optional[str]
    expires: Optional[str]
    bytes_limit: Optional[int]

class OptimizationTemplateCreateDto(BaseModel):
  name: Optional[str]
  description: Optional[str]
  customer: Optional[RelationId]

class CreateOneOptimizationTemplateInput(BaseModel):
  optimizationTemplate: Optional[OptimizationTemplateCreateDto]

class OptimizationTemplateFilter(BaseModel):
    # and, or excluded
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    customerId: Optional[StringFieldComparison]
    conversionStatus: Optional[StringFieldComparison]
    optimizationsCount: Optional[StringFieldComparison]
    lastActivityAt: Optional[StringFieldComparison]
    iname: Optional[StringFieldComparison]

class OptimizationTemplateSort(BaseModel):
    field: Optional[str]
    direction: Optional[str]
    nulls: Optional[str]

class OptimizationTemplateItemFilterOptimizationTemplateFilter(BaseModel):
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    description: Optional[StringFieldComparison]
    customerId: Optional[StringFieldComparison]
    lastActivityAt: Optional[StringFieldComparison]
    createdAt: Optional[StringFieldComparison]
    iname: Optional[StringFieldComparison]

class OptimizationTemplateItemFilter(BaseModel):
    id: Optional[StringFieldComparison]
    name: Optional[StringFieldComparison]
    createdAt: Optional[StringFieldComparison]
    updatedAt: Optional[StringFieldComparison]
    optimizationTemplate: Optional[OptimizationTemplateItemFilterOptimizationTemplateFilter]

class OptimizationTemplateItemSortFields(str, Enum):
    id = 'id'
    name = 'name'
    createdAt = 'createdAt'
    updatedAt = 'updatedAt'

class SortDirection(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'

class SortNulls(str, Enum):
    NULLS_FIRST = 'NULLS_FIRST'
    NULLS_LAST = 'NULLS_LAST'

class OptimizationTemplateItemSort(BaseModel):
    field: Optional[OptimizationTemplateItemSortFields]
    direction: Optional[SortDirection]
    nulls: Optional[SortNulls]

class OptimizationTemplateItems(BaseModel):
    id: Optional[str]
    name: Optional[str]

class OptimizationTemplateDto(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    lastActivityAt: Optional[str]
    optimizationTemplateItems: Optional[List[OptimizationTemplateItems]]

class OptimizationTemplateEdge(BaseModel):
    node: Optional[OptimizationTemplateDto]
    cursor: Optional[str]

class OptimizationTemplate(BaseModel):
    pageInfo: Optional[PageInfo]
    edges: Optional[List[OptimizationTemplateEdge]]

class OptimizationOutputFormat(str, Enum):
    format_obj = 'format_obj'
    format_gltf = 'format_gltf'
    format_glb = 'format_glb'
    format_stl = 'format_stl'
    format_3ds = 'format_3ds'
    format_fbx = 'format_fbx'
    format_orig = 'format_orig'

class FormatGLTFOptionsInput(BaseModel):
    export_draco_mesh_compression_enable: Optional[bool]

class OptimizationOutputFormatOptionsInput(BaseModel):
    format_glb: Optional[FormatGLTFOptionsInput]
    format_gltf: Optional[FormatGLTFOptionsInput]

class CreateOptimizationTemplateItemDto(BaseModel):
    name: Optional[str]
    outputFormat: Optional[OptimizationOutputFormat]
    outputFormatOptions: Optional[OptimizationOutputFormatOptionsInput]
    preset: Optional[OptimizationPreset]
    optimizationTemplate: Optional[RelationId]
    params: Optional[OptimizationParamsInput]

class CreateOneOptimizationTemplateItemInput(BaseModel):
    optimizationTemplateItem: Optional[CreateOptimizationTemplateItemDto]

class UpdateOneOptimizationTemplateItemInput(BaseModel):
    id: Optional[str]
    update: Optional[CreateOptimizationTemplateItemDto]

class OptimizationTemplateDeleteResponse(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    customerId: Optional[str]
    lastActivityAt: Optional[str]
    createdAt: Optional[str]

class UserInfoForATACOutput(BaseModel):
  fullName: Optional[str]
  accepted: Optional[str] #DateTime
  marketing: Optional[bool]
  shareData: Optional[bool]