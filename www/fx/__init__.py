# -*- coding: utf-8 -*-
from core.errors import MoneypitException
from django.contrib.gis.utils import GeoIP
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from fx.models import Currency
from fx.models import CurrencyRate
from fx.tasks import fetch_rate
from logging import getLogger
from settings import DEBUG

logger = getLogger('fx')


COUNTRY_CURRENCY_MAP = {
    'BELIZE': 'BZD',
    'YEMEN': 'YER',
    'SIERRA LEONE': 'SLL',
    'ERITREA': 'ERN',
    'NIGERIA': 'NGN',
    'COSTA RICA': 'CRC',
    'VENEZUELA': 'VEF',
    'LAO PEOPLES DEMOCRATIC REPUBLIC': 'LAK',
    'ALGERIA': 'DZD',
    'SWAZILAND': 'SZL',
    'MACAO': 'MOP',
    'BELARUS': 'BYR',
    'MAURITIUS': 'MUR',
    'SAMOA': 'WST',
    'LIBERIA': 'LRD',
    'MYANMAR': 'MMK',
    'KYRGYZSTAN': 'KGS',
    'PARAGUAY': 'PYG',
    'INDONESIA': 'IDR',
    'GUATEMALA': 'GTQ',
    'CANADA': 'CAD',
    'ARUBA': 'AWG',
    'TRINIDAD AND TOBAGO': 'TTD',
    'PAKISTAN': 'PKR',
    'UZBEKISTAN': 'UZS',
    'ANGUILLA': 'XCD',
    'ANTIGUA AND BARBUDA': 'XCD',
    'DOMINICA': 'XCD',
    'GRENADA': 'XCD',
    'MONTSERRAT': 'XCD',
    'SAINT KITTS AND NEVIS': 'XCD',
    'SAINT LUCIA': 'XCD',
    'SAINT VINCENT AND THE GRENADINES': 'XCD',
    'VANUATU': 'VUV',
    'COMOROS': 'KMF',
    'AZERBAIJAN': 'AZN',
    'MONGOLIA': 'MNT',
    'NETHERLANDS ANTILLES': 'ANG',
    'LEBANON': 'LBP',
    'KENYA': 'KES',
    'UNITED KINGDOM': 'GBP',
    'SWEDEN': 'SEK',
    'AFGHANISTAN': 'AFN',
    'KAZAKHSTAN': 'KZT',
    'ZAMBIA': 'ZMK',
    'SLOVAKIA': 'SKK',
    'DENMARK': 'DKK',
    'GREENLAND': 'DKK',
    'FAROE ISLANDS': 'DKK',
    'TURKMENISTAN': 'TMM',
    'ARMENIA': 'AMD',
    'SEYCHELLES': 'SCR',
    'FIJI': 'FJD',
    'SAINT HELENA': 'SHP',
    'ALBANIA': 'ALL',
    'TONGA': 'TOP',
    'UGANDA': 'UGX',
    'OMAN': 'OMR',
    'DJIBOUTI': 'DJF',
    'BRUNEI DARUSSALAM': 'BND',
    'TUNISIA': 'TND',
    'SOLOMON ISLANDS': 'SBD',
    'GHANA': 'GHS',
    'GUINEA': 'GNF',
    'CAPE VERDE': 'CVE',
    'ARGENTINA': 'ARS',
    'GAMBIA': 'GMD',
    'ZIMBABWE': 'ZWD',
    'MALAWI': 'MWK',
    'BANGLADESH': 'BDT',
    'KUWAIT': 'KWD',
    'ANDORRA': 'EUR',
    'AUSTRIA': 'EUR',
    'BELGIUM': 'EUR',
    'FINLAND': 'EUR',
    'FRANCE': 'EUR',
    'FRENCH GUIANA': 'EUR',
    'FRENCH SOUTHERN TERRITORIES': 'EUR',
    'GERMANY': 'EUR',
    'GREECE': 'EUR',
    'GUADELOUPE': 'EUR',
    'IRELAND': 'EUR',
    'ITALY': 'EUR',
    'LUXEMBOURG': 'EUR',
    'MARTINIQUE': 'EUR',
    'MAYOTTE': 'EUR',
    'MONACO': 'EUR',
    'MONTENEGRO': 'EUR',
    'NETHERLANDS': 'EUR',
    'PORTUGAL': 'EUR',
    'R.UNION': 'EUR',
    'SAINT PIERRE AND MIQUELON': 'EUR',
    'SAN MARINO': 'EUR',
    'SLOVENIA': 'EUR',
    'SPAIN': 'EUR',
    'LIECHTENSTEIN': 'CHF',
    'SWITZERLAND': 'CHF',
    'SURINAME': 'SRD',
    'DOMINICAN REPUBLIC': 'DOP',
    'PERU': 'PEN',
    'KOREA': 'KPW',
    'SINGAPORE': 'SGD',
    'TAIWAN': 'TWD',
    'AMERICAN SAMOA': 'USD',
    'BRITISH INDIAN OCEAN TERRITORY': 'USD',
    'ECUADOR': 'USD',
    'GUAM': 'USD',
    'MARSHALL ISLANDS': 'USD',
    'MICRONESIA': 'USD',
    'NORTHERN MARIANA ISLANDS': 'USD',
    'PALAU': 'USD',
    'PUERTO RICO': 'USD',
    'TIMOR-LESTE': 'USD',
    'TURKS AND CAICOS ISLANDS': 'USD',
    'UNITED STATES MINOR OUTLYING ISLANDS': 'USD',
    'VIRGIN ISLANDS (BRITISH)': 'USD',
    'VIRGIN ISLANDS (U.S.)': 'USD',
    'UNITED STATES': 'USD',
    'BULGARIA': 'BGN',
    'MOROCCO': 'MAD',
    'WESTERN SAHARA': 'MAD',
    'SAUDI ARABIA': 'SAR',
    'AUSTRALIA': 'AUD',
    'CHRISTMAS ISLAND': 'AUD',
    'COCOS (KEELING) ISLANDS': 'AUD',
    'HEARD ISLAND AND MCDONALD ISLANDS': 'AUD',
    'KIRIBATI': 'AUD',
    'NAURU': 'AUD',
    'NORFOLK ISLAND': 'AUD',
    'TUVALU': 'AUD',
    'CAYMAN ISLANDS': 'KYD',
    'KOREA': 'KRW',
    'GIBRALTAR': 'GIP',
    'TURKEY': 'TRY',
    'CZECH REPUBLIC': 'CZK',
    'JAMAICA': 'JMD',
    'BAHAMAS': 'BSD',
    'BOTSWANA': 'BWP',
    'GUYANA': 'GYD',
    'LIBYAN ARAB JAMAHIRIYA': 'LYD',
    'EGYPT': 'EGP',
    'THAILAND': 'THB',
    'MACEDONIA': 'MKD',
    'SUDAN': 'SDG',
    'UNITED ARAB EMIRATES': 'AED',
    'JORDAN': 'JOD',
    'JAPAN': 'JPY',
    'SOUTH AFRICA': 'ZAR',
    'CROATIA': 'HRK',
    'ANGOLA': 'AOA',
    'RWANDA': 'RWF',
    'CUBA': 'CUP',
    'BARBADOS': 'BBD',
    'PAPUA NEW GUINEA': 'PGK',
    'SRI LANKA': 'LKR',
    'ROMANIA': 'RON',
    'POLAND': 'PLN',
    'IRAQ': 'IQD',
    'TAJIKISTAN': 'TJS',
    'MOLDOVA': 'MDL',
    'MALAYSIA': 'MYR',
    'CHINA': 'CNY',
    'LATVIA': 'LVL',
    'INDIA': 'INR',
    'FALKLAND ISLANDS (MALVINAS)': 'FKP',
    'NICARAGUA': 'NIO',
    'PHILIPPINES': 'PHP',
    'HONDURAS': 'HNL',
    'HONG KONG': 'HKD',
    'COOK ISLANDS': 'NZD',
    'NEW ZEALAND': 'NZD',
    'NIUE': 'NZD',
    'PITCAIRN': 'NZD',
    'TOKELAU': 'NZD',
    'BRAZIL': 'BRL',
    'SERBIA': 'RSD',
    'ESTONIA': 'EEK',
    'SOMALIA': 'SOS',
    'MOZAMBIQUE': 'MZN',
    'BOUVET ISLAND': 'NOK',
    'NORWAY': 'NOK',
    'SVALBARD AND JAN MAYEN': 'NOK',
    'ICELAND': 'ISK',
    'GEORGIA': 'GEL',
    'ISRAEL': 'ILS',
    'HUNGARY': 'HUF',
    'UKRAINE': 'UAH',
    'RUSSIAN FEDERATION': 'RUB',
    'IRAN': 'IRR',
    'BERMUDA': 'BMD',
    'MADAGASCAR': 'MGA',
    'MALDIVES': 'MVR',
    'QATAR': 'QAR',
    'VIETNAM': 'VND',
    'MAURITANIA': 'MRO',
    'NEPAL': 'NPR',
    'TANZANIA': 'TZS',
    'BURUNDI': 'BIF',
    'CAMBODIA': 'KHR',
    'SYRIAN ARAB REPUBLIC': 'SYP',
    'BAHRAIN': 'BHD',
    'SAO TOME AND PRINCIPE': 'STD',
    'BOSNIA AND HERZEGOVINA': 'BAM',
    'LITHUANIA': 'LTL',
    'ETHIOPIA': 'ETB',
    'FRENCH POLYNESIA': 'XPF',
    'WALLIS AND FUTUNA': 'XPF',
    'NEW CALEDONIA': 'XPF' }


def refresh_rates(currencies):
  if DEBUG:
    return

  if len(currencies) < 2:
    return

  for pair in permutations(currencies, 2):
    pair_str = '%s%s' % pair
    if not pair_str in cache:
      fetch_rate.delay(pair[0], pair[1])


def detect_currency(request):
  country = GeoIP().country(request.META['REMOTE_ADDR'])
  currency_id = Currency.objects.get(symbol='EUR').id
  if country['country_name']:
    country_up = country['country_name'].upper()
    if country_up in COUNTRY_CURRENCY_MAP:
      symbol = COUNTRY_CURRENCY_MAP[country_up]
      try:
        currency = Currency.objects.get(symbol=symbol)
        currency_id = currency.id
      except ObjectDoesNotExist:
        pass
  return currency_id


def get_rate(symbol_from, symbol_to):
  pair = '%s%s' % (symbol_from, symbol_to)

  if DEBUG:
    return 1

  if pair in cache:
    return cache.get(pair)
  else:
    fetch_rate.delay(symbol_from, symbol_to)
    try:
      rates = CurrencyRate.objects.filter(
          source=symbol_from,
          destination=symbol_to)
      if not rates:
        raise ObjectDoesNotExist
      return rates[0].rate
    except ObjectDoesNotExist:
      try:
        while (True):
          return fetch_rate(symbol_from, symbol_to)
      except MoneypitException:
        pass


def permutations(iterable, r=None):
  pool = tuple(iterable)
  n = len(pool)
  r = n if r is None else r
  if r > n:
    return
  indices = range(n)
  cycles = range(n, n-r, -1)
  yield tuple(pool[i] for i in indices[:r])
  while n:
    for i in reversed(range(r)):
      cycles[i] -= 1
      if cycles[i] == 0:
        indices[i:] = indices[i+1:] + indices[i:i+1]
        cycles[i] = n - i
      else:
        j = cycles[i]
        indices[i], indices[-j] = indices[-j], indices[i]
        yield tuple(pool[i] for i in indices[:r])
        break
    else:
      return
