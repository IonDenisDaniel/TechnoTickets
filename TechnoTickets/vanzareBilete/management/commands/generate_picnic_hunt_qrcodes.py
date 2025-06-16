import os
import uuid
import qrcode
from django.core.management.base import BaseCommand
from django.conf import settings
from vanzareBilete.models import QRCode

class Command(BaseCommand):

    title = "Generarea unui set de QR coduri pentru campania Picnic Hunt"

    def add_arguments(self, parser):
        parser.add_argument('Count', type=int)

    def handle(self, *args, **options):
        count = options['Count']
        out_dir = os.path.join(settings.MEDIA_ROOT, 'Picnic_Hunt_qrs')
        os.makedirs(out_dir, exist_ok=True)

        for i in range(count):
            token = uuid.uuid4().hex

            qr = QRCode.objects.create(token=token)
            target_url = f"{settings.BASE_URL}/picnic-hunt/scan/?code={token}"

            img = qrcode.make(target_url)

            file_path = os.path.join(out_dir, f"{token}.png")
            img.save(file_path)

        
        self.stdout.write(self.style.NOTICE(f"Au fost generate {count} QR couri."))
