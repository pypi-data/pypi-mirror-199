import requests
import environ
import os

from django.http import HttpResponse


def getIP():
    return "127.0.0.1"


env = environ.Env()
environ.Env.read_env()


class WatchmapMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        watchmap_register_url = env('WATCHMAP_SERVER_REGISTER_URL')
        if not watchmap_register_url:
            raise Exception('WATCHMAP_SERVER_REGISTER_URL is not set')

        requests.post(watchmap_register_url, data={
            'ip': getIP(),
            'port': os.environ['PORT'],
            'name': env('WATCHMAP_SERVICE_NAME')
        })

    def __call__(self, request):
        service_name = env('WATCHMAP_SERVICE_NAME')
        url = env('WATCHMAP_SERVER_REQUEST_MONITOR_URL')
        if not url:
            raise Exception('WATCHMAP_SERVER_REQUEST_MONITOR_URL is not set')
        if not service_name:
            raise Exception('WATCHMAP_SERVICE_NAME is not set')
        requests.post(url, data={
            'name': service_name,
        })
        response = self.get_response(request)
        return HttpResponse(response)
