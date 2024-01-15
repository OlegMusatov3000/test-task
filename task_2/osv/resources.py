# from import_export import fields
# from import_export.resources import ModelResource
# from import_export.widgets import ForeignKeyWidget

# from .models import (
#     Company, Market, Segment, CompanyFounder, CompanyConstitutor,
#     CompanyRevenue, YearTop1000
# )
# from users.models import Person


# class CompanyResource(ModelResource):
#     title = fields.Field(attribute='title')
#     segment = fields.Field(
#         column_name='market',
#         attribute='segment__market',
#         widget=ForeignKeyWidget('market', field='name'))
#     median = fields.Field(attribute='get_median')

#     class Meta:
#         model = Company
#         fields = (
#             'id', 'title', 'place_in_top_1000', 'segment', 'growth_percent',
#             'score', 'median', 'last_revenue', 'before_last'
#         )
#         export_order = (
#             'id', 'title', 'place_in_top_1000', 'segment', 'growth_percent',
#             'score', 'median', 'last_revenue', 'before_last'
#         )


# class ImportCompanyResource(ModelResource):
#     title = fields.Field(attribute='title')
#     description = fields.Field(attribute='description')

#     class Meta:
#         model = Company
#         export_order = (
#             'id', 'segment', 'place', 'logo', 'logoSq', 'slug',
#             'create_company_year', 'ceo', 'revenue', 'activate',
#             'see_to_home', 'update', 'create', 'title', 'description',
#         )


# class MarketResource(ModelResource):
#     name = fields.Field(attribute='name')
#     description = fields.Field(attribute='description')

#     class Meta:
#         model = Market


# class SegmentResource(ModelResource):
#     name = fields.Field(attribute='name')
#     description = fields.Field(attribute='description')

#     class Meta:
#         model = Segment


# class CompanyFounderResource(ModelResource):

#     class Meta:
#         model = CompanyFounder


# class CompanyConstitutorResource(ModelResource):

#     class Meta:
#         model = CompanyConstitutor


# class CompanyRevenueResource(ModelResource):

#     class Meta:
#         model = CompanyRevenue


# class PersonResource(ModelResource):
#     last_name = fields.Field(attribute='last_name')
#     first_name = fields.Field(attribute='first_name')

#     class Meta:
#         model = Person
