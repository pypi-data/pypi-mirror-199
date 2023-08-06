import os

from PySide6.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlRequestInfo
from braveblock import braveblock

from devoud import rpath


class AdBlocker:
    def __init__(self, parent):
        self.parent = parent
        self.rules = None
        self.interceptor = None

    def is_enable(self):
        return self.parent.settings.get('adblock')

    def add_rules(self):
        rules = []
        files = next(os.walk(rpath('browser/page/web/adblocker/rules')), (None, None, []))[2]
        for name in files:
            with open(rpath(f'browser/page/web/adblocker/rules/{name}'), encoding="utf8") as rule_file:
                rules.extend(rule_file.readlines())
            print(f"[Блокировка]: Добавлены правила {name.rpartition('.')[0]}")
        self.rules = braveblock.Adblocker(rules=rules)


class RequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, rules):
        super().__init__()
        self.rules = rules
        self.resources_types = {QWebEngineUrlRequestInfo.ResourceType.ResourceTypeImage: 'image',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeScript: 'script',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeSubFrame: 'sub_frame',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeMainFrame: 'main_frame',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeMedia: 'media',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeWebSocket: 'websocket',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeStylesheet: 'stylesheet',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeCspReport: 'csp_report',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeFontResource: 'font',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypePing: 'ping',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeXhr: 'xhr',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeObject: 'object',
                                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeUnknown: 'other'
                                }

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        source = info.firstPartyUrl().toString()
        resource_type = self.resources_types.get(info.resourceType(), 'other')
        if self.rules.check_network_urls(url, source, resource_type):
            print(f"[Блокировка]: {resource_type} ({url})")
            info.block(True)
