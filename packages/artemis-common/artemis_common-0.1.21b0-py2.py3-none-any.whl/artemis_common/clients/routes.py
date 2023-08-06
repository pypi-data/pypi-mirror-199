from __future__ import annotations


class DALRoutes:
    API_kEY = '/v1/api_key'
    CATEGORIES_CHILDREN = '/v1/categories/children'
    SERIES_BY_CATEGORY = '/v1/series/by-category'
    SERIES_COUNT_BY_CATEGORY = '/v1/series/by-category/count'
    SERIES_BY_POPULARITY = '/v1/series/by-popularity'
    SERIES_COUNT_BY_POPULARITY = '/v1/series/by-popularity/count'
    SERIES_CATEGORIES_TREE = '/v1/series/categories-tree'


__all__ = [
    DALRoutes.__name__,
]
