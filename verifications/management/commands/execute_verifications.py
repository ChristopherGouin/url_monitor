import os
import sys
import datetime
import time
import requests
import ssl, socket

from django.core.management.base import BaseCommand
import django.utils.timezone
from django.conf import settings

from users.utils import lock
from urls.models import Url
from verifications.models import Verification

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))

class Command(BaseCommand):

    # @lock(os.path.join(CURRENT_FILE_DIR, os.path.basename(__file__)+".lock"))
    def handle(self, *args, **options):
        now = datetime.datetime.utcnow()
        
        urls = Url.objects.filter(is_auto_check=True)

        for url in urls:
            verification = Verification()
            verification.url = url
            verification.result = True

            verified_url = url.url
            if not verified_url.startswith('http://') and not verified_url.startswith('https://'):
                verified_url = "https://%s" % verified_url
        
            r = self.get_response(verified_url)
            
            verification.ssl_expiration_date = self.get_ssl_certificate_expiration_date(self.get_hostname(verified_url))

            verification.http_code = r.status_code

            verification.display_time = r.elapsed.total_seconds() * 1000

            verification.is_content_empty = self.get_header_response(verified_url)['Content-length'] == '0'

            self.check_http_code(verification, url)
            self.check_display_time(verification, url)
            self.check_is_content_empty(verification, url)
            self.check_ssl_expiration_date(verification, url)

            verification.save()


        with open(os.path.join(settings.LOG_DIR, os.path.basename(__file__)+"_exec.log"), "a") as f:
            f.write(str(datetime.datetime.utcnow())+" ==> Elapsed %s" % (datetime.datetime.utcnow() - now)+"\n")

    @staticmethod
    def get_response(url):
        return requests.get(url, verify=False)

    @staticmethod
    def get_header_response(url):
        return requests.head(url).headers

    @staticmethod
    def get_ssl_certificate_expiration_date(url):
        print(url)
        ctx = ssl.create_default_context()
        
        with ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url) as s:
            try:
                s.settimeout(3.0)
                s.connect((url, 443))
                cert = s.getpeercert()
                return datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            except ssl.CertificateError as e:
                print(f'{url} cert error {e}')
            except ssl.SSLError as e:
                print(f'{url} cert error {e}')
            except socket.timeout as e:
                return f'{url} could not connect'
    
    @staticmethod
    def get_hostname(url):
        if url.startswith('http://') or url.startswith('https://'):
            url = url.split('://')[1]
            url = url.split('/')[0]
        return url
    
    
    @staticmethod
    def check_http_code(verification, url_expected):
        if not url_expected.http_code is None:
            if verification.result:
                verification.result = verification.http_code == url_expected.http_code
    
    @staticmethod
    def check_display_time(verification, url_expected):
        if not url_expected.display_time is None:
            if verification.result:
                verification.result = float(verification.display_time) < float(url_expected.display_time)
    
    @staticmethod
    def check_is_content_empty(verification, url_expected):
        if verification.result:
            verification.result = verification.is_content_empty == url_expected.is_content_empty
    
    @staticmethod
    def check_ssl_expiration_date(verification, url_expected):
        now = datetime.datetime.utcnow()
        if not url_expected.ssl_expiration is None:
            if verification.result:
                verification.result = (verification.ssl_expiration_date - now).days > url_expected.ssl_expiration