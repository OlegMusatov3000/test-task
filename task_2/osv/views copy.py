# import json
# import zipfile
# from collections import defaultdict

# import psycopg2
# import openpyxl
# from django.http import HttpResponse, JsonResponse
# from django.core.exceptions import PermissionDenied

# from django.shortcuts import render, redirect
# from django.core.serializers.json import DjangoJSONEncoder
# from django.views.generic.edit import BaseCreateView
# from django.utils.translation import gettext
# from openpyxl import Workbook, load_workbook
# from tablib import Dataset


# from ranking.resources import (
#     CompanyResource, MarketResource, SegmentResource, CompanyFounderResource,
#     CompanyConstitutorResource, CompanyRevenueResource, PersonResource,
#     ImportCompanyResource
# )
# from home.models import Analytics
# from ranking.models import *
# from ranking.utils import get_companies_info, calc_growth, calc_score
# from ranking.forms import SiteRequestForm, PositionForm


# @logger.catch
# def singleCompany(request, slug):
#     company = Company.objects.filter(slug=slug).first()
#     if not company:
#         return HttpResponse('Не нашли такую компанию')

#     navDict = {
#         reverse('marketList'): 'Рейтинги',
#         company.segment.market.get_absolute_url: company.segment.market,
#         0: company.title,
#     }

#     analytics = Analytics.objects.filter(publish=True, publication_date__lte = datetime.datetime.now(), market = company.segment.market)
#     get_revenue_y = company.get_revenue_y()
#     chart_data, revenue_dynamik = [], []
#     if company.companyrevenue.all():
#         year,per, pred = '','',''
#         mv = company.segment.market.marketViews.all()
#         if mv:
#             try:
#                 mv_1 = company.companyrevenue.filter(period=mv[mv.count()-1].period, year=mv[mv.count()-1].year, market_size=mv[mv.count()-1].market_size).first()
#                 mv_2 = company.companyrevenue.filter(period=mv[mv.count()-2].period, year=mv[mv.count()-2].year, market_size=mv[mv.count()-2].market_size).first()
#             except Exception as e:
#                 logger.error(e)
#                 mv_1 = 0
#                 mv_2 = 0

#             if mv_1:
#                 mv_1 = mv_1.revenue
#             if mv_2:
#                 mv_2 = mv_2.revenue
#             per = dict(MarketTableViews.PERIOD_CHOICES).get(mv[mv.count()-1].period).lower()
#             if per in ["квартал", "месяц"]:
#                 per += 'е'
#             elif per in ["год"]:
#                 per += 'у'

#             if mv[mv.count()-1].market_size == 2:
#                 pred = 'во'
#             else:
#                 pred = 'в'


#             if mv_1 and mv_2:
#                 revenue_dynamik = [
#                     "",
#                     mv_1-mv_2,
#                     list(get_revenue_y.keys())[-1],
#                     round((mv_1-mv_2)/mv_2*100, 2),
#                     f"{pred} {mv[mv.count()-1].market_size} {per} {mv[mv.count()-1].year}",
#                 ]
#                 revenue_dynamik[0] = "+" if revenue_dynamik[1] > 0 else "-"
#                 revenue_dynamik[1] = str(number_normal(revenue_dynamik[1])).replace('-', '')
#         chart_data_count = -1
#         for key, item in [["год", company.get_revenue_y()],[" полугодие", company.get_revenue_h_y()], ["кв.", company.get_revenue_kv()]]:
#             chart_data_count += 1
#             chart_data.append([[], []])
#             for year, value_list in item.items():
#                 for value in value_list:
#                     if type(value) != list and type(value) != tuple:
#                         if value > 0:
#                             sr = ""
#                             if value_list[1]:
#                                 sr = "*"
#                             chart_data[chart_data_count][0].append(f"{year} {key}{sr}")
#                             chart_data[chart_data_count][1].append(value/1000)
#                         break

#                     if value[0] > 0:
#                         for i in range(len(value_list)):
#                             sr = ""
#                             if value_list[i][1]:
#                                 sr = "*"
#                             chart_data[chart_data_count][0].append(f"{i+1}{key} {year}{sr}")
#                             chart_data[chart_data_count][1].append(value_list[i][0]/1000)
#                         break
    
#     try:
#         market_size = company.segment.market.get_market_size_actual(info=True)
#     except:
#         market_size = 0
#     market_size_info = ""
#     if market_size:
#         per = dict(MarketTableViews.PERIOD_CHOICES).get(market_size.get("info").period).lower()
#         if per in ["квартал", "месяц"]:
#             per += 'е'
#         elif per in ["год"]:
#             per += 'у'

#         if market_size.get("info").market_size == 2:
#             pred = 'во'
#         else:
#             pred = 'в'
#         if market_size.get('info').market_size and per not in ["году", "квартале", "месяце"]:
#             market_size_info = f"{pred} {market_size.get('info').market_size} {per} {year}"
#         else:
#             market_size_info = f"{pred} {year} {per}"


#     try:
#         market_size_comp = 0
#         market_size_pct = 0
#         if market_size.get("info"):
#             market_size_comp = company.companyrevenue.filter(year=market_size.get("info").year, period=market_size.get("info").period, market_size=market_size.get("info").market_size).first().revenue
#             market_size_pct = round(market_size_comp * 100 / market_size.get("data"), 2)
#     except Exception as e:
#         logger.error(e)
        
#     context = {
#         'title': f'{company}',
#         'description': 'Рейтинги крупнейших технологических рынков России и мира',
#         'keywords': 'keywords',
#         'analytics_list_home': analytics.filter(homepage=True),
#         'analytics_list': analytics,
#         'company': company,
#         'company_dynamic': company,
#         'navDict': navDict,
#         "chart_data": chart_data,
#         "revenue_dynamik": company.get_revenue_dynamik(),
#         "market_size_comp": market_size_pct,
#         "market_size_comp_val": market_size_comp,
#         "market_size": 100 - market_size_pct,
#         "market_size_val": market_size.get("data") if market_size else '',
#         "market_size_info": market_size_info,
#         "top_company": Company.objects.filter(activate=True, segment__market=company.segment.market).order_by('place')[:3]
#         }

#     return render(request, 'ranking/company.html', context)


# @logger.catch
# def grow(request):
#     segments = defaultdict(int)
#     top_companies = Company.objects.all().exclude(place_in_top_1000=None)
#     for company in top_companies:
#         segments[company.segment] += 1
#     segments = list(segments.items())
#     segments.sort(key=lambda x: x[0].translations.name.lower() if x[0] is not None and x[0].translations.name is not None else "")

#     navDict = {
#         reverse('marketList'): 'Рейтинги',
#         0: 'Топ 1000',
#     }
#     context = {
#         'segments': segments,
#         'title': 'Рейтинг быстрорастущих технологических компаний',
#         'description': 'Рейтинг быстрорастущих технологических компаний',
#         'keywords': 'keywords',
#         'navDict': navDict,
#         'revenue_value': [10000000, 1000000000],
#         'partners': Top1000Partners.objects.all(),
#     }

#     return render(request, 'ranking/grow.html', context)


# @logger.catch
# def singleMarket(request, slug):
#     market = Market.objects.filter(slug=slug).first()
#     if not market:
#         return HttpResponse('Не нашли такую категорию')
        
#     navDict = {
#         reverse('marketList'): 'Рейтинги',
#         0: market.name,
#     }
#     analytics = Analytics.objects.filter(publish=True, publication_date__lte = datetime.datetime.now(), market = market)
#     market_obj_count = market.marketViews.all().count()
#     try:
#         market_obj_1 = market.marketViews.all()[market_obj_count-1]
#     except Exception as e:
#         logger.error(e)
#         market_obj_1 = ''
#     try:
#         market_obj_2 = market.marketViews.all()[market_obj_count-2]
#     except Exception as e:
#         logger.error(e)
#         market_obj_2 = ''
#     context = {
#         'title': f'{market} - Рейтинги крупнейших технологических рынков России и мира ',
#         'description': f'Рейтинги крупнейших технологических рынков России и мира в области {market}',
#         'keywords': 'keywords',
#         'analytics_list_home': analytics.filter(homepage=True),
#         'analytics_list': analytics,
#         'slug':slug,
#         'market': market,
#         'market_obj_1': market_obj_1,
#         'market_obj_2': market_obj_2,
#         'navDict': navDict,
#         'revenue_value': [0, 9000000]

#         }

#     return render(request, 'ranking/singleMarket.html', context)


# @logger.catch
# def marketList(request):
#     navDict = {
#         '': 'Рейтинги',
#     }
#     context = {
#         'title': "Рейтинги",
#         'descriptions': "Рейтинги",
#         'keywords': "Рейтинги",
#         'segment_list': Market.objects.filter(active=True),
#     }
    

#     context.update({
#         'navDict': navDict,
#         })
    
#     return render(request, "ranking/marketList.html", context)


# @logger.catch
# def singleMarketAjax(request, slug):
#     market = Market.objects.get(slug = slug)
#     all_objects = Company.objects.filter(segment__market = market)
#     all_objects_list = []
#     for object in all_objects:
#         try:
#             all_objects_list.append({
#                 'pk': object.pk,
#                 'segment': str(object.segment.name),
#                 'place': object.place,
#                 'logo': str(object.get_logoSq()),
#                 'title': object.title,
#                 'slug': object.get_absolute_url(),
#                 'description': object.description,
#                 'create_company_year': object.create_company_year,
#                 'ceo': object.ceo.natural_key() if object.ceo else '',
#                 'revenue': object.revenue,
#                 'revenue_period': object.get_revenue_period()
#             })
#         except Exception as e:
#             logger.error(f'Не смогли включить компанию {object.pk} {object.title} в рейтинг. Ошибка: {e}')


#     return HttpResponse(json.dumps(all_objects_list, cls=DjangoJSONEncoder, ensure_ascii=False), content_type='application/json')


# def grow_data(request):
#     all_objects_list = []
#     top_companies = Company.objects.all().exclude(place_in_top_1000=None)
#     for company in top_companies:
#         all_objects_list.append({
#             'pk': company.pk,
#             'segment': str(company.segment.name),
#             'place': company.place_in_top_1000,
#             'logo': str(company.get_logoSq()),
#             'title': company.title,
#             'slug': company.get_absolute_url(),
#             'description': company.description,
#             'create_company_year': company.create_company_year,
#             'ceo': company.ceo.natural_key() if company.ceo else '',
#             'revenue': number_normal(company.last_revenue),
#             'growth': round(company.growth_percent, 2),
#             'score': company.score,
#         })
#     return JsonResponse(all_objects_list, safe=False, json_dumps_params={'ensure_ascii': False})


# class SiteRequestView(BaseCreateView):
#     form_class = SiteRequestForm

#     def get(self, *args, **kwargs):
#         raise PermissionDenied

#     def form_invalid(self, form):
#         return JsonResponse(form.errors, status=400)

#     def form_valid(self, form):
#         form.save()
#         return JsonResponse({'status': 'ok'})


# def grow_position(request):
#     form = PositionForm(request.GET)
#     if form.is_valid():
#         last_year = form.cleaned_data['last_year'] * 1000000
#         year_before_last = form.cleaned_data['year_before_last'] * 1000000

#         growth = calc_growth(last_year, year_before_last)
#         if growth <= 0:
#             return JsonResponse({'text': gettext('У вас отрицательный рост, вы не можете участвовать в рейтинге')})

#         companies = get_companies_info()
#         if not companies:
#             return JsonResponse({'text': gettext('Невозможно определить рейтинг')})

#         median = companies[0][1]['median']
#         score = calc_score(last_year, growth, median)

#         for number, (company, info) in enumerate(companies, start=1):
#             if score > info['score']:
#                 return JsonResponse({'text': gettext(f'Ваша позиция в рейтинге {number}')})

#         return JsonResponse({'text': gettext(f'Ваша позиция в рейтинге {len(companies)}')})

#     return JsonResponse(form.errors, status=400)


# def import_data_from_excel(request):
#     all_tables = [
#         MarketResource, SegmentResource,
#         PersonResource, CompanyFounderResource,
#         CompanyConstitutorResource, CompanyRevenueResource
#     ]
#     if request.method == 'POST':
#         try:
#             new_companies = request.FILES['myfile']
#         except KeyError:
#             return HttpResponse("произошла ошибка, проверьте файл")
#         file_name = new_companies.name[:-5]
#         for company in all_tables:
#             if file_name == 'CompanyResource':
#                 company = ImportCompanyResource
#                 break
#             elif company.__name__ == file_name:
#                 break
#         company_resource = company()
#         dataset = Dataset()

#         dataset.load(new_companies, format='xlsx')

#         result = company_resource.import_data(dataset, dry_run=True)

#         if not result.has_errors():
#             company_resource.import_data(dataset, dry_run=False)
#             return HttpResponse("Данные успешно импортированы")

#     return HttpResponse('произошла ошибка, проверьте файл')


# def export_data_to_excel(request):
#     all_tables = [
#         CompanyResource, MarketResource, SegmentResource,
#         PersonResource, CompanyFounderResource,
#         CompanyConstitutorResource, CompanyRevenueResource
#     ]

#     response = HttpResponse(content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename="exported_data.zip"'

#     with zipfile.ZipFile(response, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for company in all_tables:
#             company_resource = company()
#             dataset = company_resource.export()
#             excel_data = dataset.xlsx
#             file_name = f"{company.__name__}.xlsx"

#             zipf.writestr(file_name, excel_data)

#     return response
