import requests
import json
from difflib import SequenceMatcher

import pprint


class CompaniesSearchApi:
    url = 'https://zachestnyibiznesapi.ru/paid/data/'

    def __init__(self):
        try:
            self.token = open('CompaniesSearchApi.token').read()
        except:
            print('ERROR: CompaniesSearch: __init__: file CompaniesSearchApi.token not found')

    """Возвращает список словарей информацией о компаниях, найденных по запросу query (произвольная строка)"""
    def search(self, query):
        try:
            params = {'string': query, 'api_key': self.token}
            resp = requests.get(self.url + 'search', params=params)
            data = json.loads(resp.content, encoding='utf-8')
            if data['status'] != '200':
                print('ERROR: CompaniesSearchApi: search: request.status != 200')
            return data['body']['total'], data['body']['docs']
        except Exception as e:
            print('ERROR: CompaniesSearchApi: search: something went wrong')
            print(e)
            return 0, []

    """Принимает ОГРН или ИНН или ОГРНИП или ИННФЛ компании (сторка или число), 
    возвращает словарь с подробной информацией"""
    def company_info(self, company_id):
        company_id = str(company_id)
        try:
            params = {'id': company_id, 'api_key': self.token}
            resp = requests.get(self.url + 'card', params=params)
            data = json.loads(resp.content, encoding='utf-8')
            if data['status'] != '200':
                print('ERROR: CompaniesSearchApi: company_info: request.status != 200')
            if 'docs' in data['body']:  # был запрос по ИНН
                if len(data['body']) != 1:
                    print('WARNING: CompaniesSearchApi: company_info: items != 1, company_id = ' + str(company_id))
                return data['body']['docs'][0]
            else:   # был другой запрос
                return data['body']
        except Exception as e:
            print('ERROR: CompaniesSearchApi: company_info: something went wrong')
            print(e)
            return {}

def _name(info):
    if 'fl_aff' in info:
        return info['fl_aff']
    if 'fl' in info:
        return info['fl']
    if 'name' in info:
        return info['name']
    return ''

class CompaniesSearch:
    fast_search_limit = 100
    deep_search_limit = 10
    sequence_matched = 0.9

    def __init__(self):
        self.csa = CompaniesSearchApi()

    def post_processing(self, search_result):
        full_comp_info = search_result
        affilated = set()
        short_companies = []
        for c in full_comp_info:
            try:
                for x in c['Руководители'] + c['СвУчредит']['all']:
                    affilated.add(_name(x))
            except:
                pass
            try:
                short_companies.append((c['ИНН'], c['НаимЮЛСокр'], c['КодРегион']))
            except:
                pass
        return [affilated, short_companies]

    """Ищет компании по ФИО, возвращает те, где совпадает ФИО главного руководителя"""
    def find_companies_by_person_name_fast(self, person_name):
        count, companies = self.csa.search(person_name)
        if count > self.fast_search_limit:
            print('INFO: CompaniesSearch: find_companies_by_person_name_fast: too many companies: '
                  + str(count) + ', person_name="' + person_name + '"')
            return [set(), set(), []]
        affilated = set()
        for c in companies:
            for x in c['Руководитель']:
                affilated.add(x)
        if person_name in affilated:
            affilated.remove(person_name)
        suggested_companies = [self.csa.company_info(x['id']) for x in companies if person_name in x['Руководитель']]
        suggested_inns = set()
        try:
            for c in suggested_companies:
                for x in c['Руководители']:
                    if _name(x).upper() == person_name.upper():
                        suggested_inns.add(x['inn'])
        except:
            pass
        return [suggested_inns, ] + self.post_processing(suggested_companies)

    """Ищет компании по ФИО, выбирает те, для которых pfilter(company_info) == True,
    для каждой запрашивает подробную инфу, в ней ищет совпадения ФИО,
    возвращает тройку ([предпологаемые инн чиновника], [предполагаемые аффелированные], [список с инфой о компаниях])"""
    def find_companies_by_person_name_deep(self, person_name, use_seq_matcher=False, pfilter=lambda x: True):
        count, _companies = self.csa.search(person_name)
        _companies = [x for x in _companies if pfilter(x)]
        if count > self.fast_search_limit or len(_companies) > self.deep_search_limit:
            print('INFO: CompaniesSearch: find_companies_by_person_name_deep: too many companies: '
                  + str(count) + ', ' + str(len(_companies)) + ', person_name="' + person_name + '"')
            return [set(), set(), []]
        companies = [self.csa.company_info(c['id']) for c in _companies]
        suggested_inns = set()
        suggested_companies = dict()

        def strcmp(x, y):
            x = x.upper()
            y = y.upper()
            if use_seq_matcher:
                return SequenceMatcher(None, x, y).ratio() >= self.sequence_matched
            else:
                return x == y

        for c in companies:
            try:
                for x in c['Руководители'] + c['СвУчредит']['all']:
                    if strcmp(person_name, _name(x)):
                        try:
                            suggested_inns.add(x['inn'])
                            suggested_companies[c['ИНН']] = c
                        except:
                            pass
            except Exception as e:
                print('WARNING: CompaniesSearch: find_companies_by_person_name_deep: incomplete data, person_name = '
                      + person_name + ', company_id = ' + c['ИНН'])
                print(e)

        return [suggested_inns, ] + self.post_processing([suggested_companies[x] for x in suggested_companies])




