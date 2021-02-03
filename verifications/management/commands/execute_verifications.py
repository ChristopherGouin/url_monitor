import os
import sys
import datetime
import time
import requests
import ssl, socket
import OpenSSL.crypto as crypto

from django.core.management.base import BaseCommand
import django.utils.timezone
from django.conf import settings
from django.core.mail import send_mail

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

            verification.http_code = r.status_code
            verification.display_time = r.elapsed.total_seconds() * 1000
            
            verification.ssl_expiration_date = self.get_ssl_certificate_expiration_date(self.get_hostname(verified_url))


            headers = self.get_header_response(verified_url)
            verification.is_content_empty = 'Content-length' in headers and headers['Content-length'] == '0'
            

            http_code_result = self.check_http_code(verification, url)
            display_time_result = self.check_display_time(verification, url)
            is_content_empty_result = self.check_is_content_empty(verification, url)
            ssl_expiration_date_result = self.check_ssl_expiration_date(verification, url)

            verification.result = http_code_result and display_time_result and is_content_empty_result and ssl_expiration_date_result


            verification.save()

            self.format_description(verification, url)

            verification.save()

            if url.is_mail_report and not verification.result:
                self.send_mail_verification(verification)


        with open(os.path.join(settings.LOG_DIR, os.path.basename(__file__)+"_exec.log"), "a") as f:
            f.write(str(datetime.datetime.utcnow())+" ==> Elapsed %s" % (datetime.datetime.utcnow() - now)+"\n")

    @staticmethod
    def get_response(url):
        return requests.get(url, verify=False)

    @staticmethod
    def get_header_response(url):
        return requests.head(url , verify=False).headers

    @staticmethod
    def get_ssl_certificate_expiration_date(hostname):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.connect((hostname, 443))
            cert = s.getpeercert(True)
            x509 = crypto.load_certificate(crypto.FILETYPE_ASN1,cert)
        
        return datetime.datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
           
    @staticmethod
    def get_hostname(url):
        if url.startswith('http://') or url.startswith('https://'):
            url = url.split('://')[1]
            url = url.split('/')[0]
        return url
    
    
    @staticmethod
    def check_http_code(verification, url_expected):
        # On vérifi que le test doit etre effectué
        if not url_expected.http_code is None: 
            return verification.http_code == url_expected.http_code
        else:
            return True

    
    @staticmethod
    def check_display_time(verification, url_expected):
        # On vérifi que le test doit etre effectué
        if not url_expected.display_time is None:
           return float(verification.display_time) < float(url_expected.display_time)
        else:
            return True
    
    @staticmethod
    def check_is_content_empty(verification, url_expected):
        # On execute le test si verification résult est toujours vrai 
        # pour ne pas faussé un test déja en echec 
        return verification.is_content_empty == url_expected.is_content_empty
    
    @staticmethod
    def check_ssl_expiration_date(verification, url_expected):
        now = datetime.datetime.utcnow()
        # On vérifi que le test doit etre effectué
        if not url_expected.ssl_expiration is None:
            return (verification.ssl_expiration_date - now).days > url_expected.ssl_expiration
        else:
            return True

    @staticmethod
    def format_description(verification, url):
        now = datetime.datetime.utcnow()
        template_text = "Valeur attendue : %s - Valeur optenue: %s"

        verification.description = \
            "code http souhaité: %d, résultat: %d /// " % (url.http_code, verification.http_code, ) \
            + "temps de réponse maximum: %s ms, resultat: %s ms /// " % (str(url.display_time), str(verification.display_time), ) \
            + "contenu vide: %s , resultat: %s /// " % (str(url.content), str(verification.content), ) \
            + "délai d'expiration ssl: %d jours, resultat: %d jours" % (url.ssl_expiration, (verification.ssl_expiration_date - now).days, )

    @staticmethod
    def send_mail_verification(verification):
        send_mail(
            '%s verifications failed - %s' % (verification.created, str(verification.url)),
            verification.description,
            'christo.tpe@gmail.com',
            ['christo.tpe@gmail.com'],
            fail_silently=False
        )
