from django.core.management.base import BaseCommand
from django.db import transaction
from accesscontrol.models import AccessEventModels
from credentials.models import CredentialsModel
import re

class Command(BaseCommand):
    help = 'Detecta AccessEventModels sin credential y sugiere/realiza asociación intentando inferir el código desde el access_point.name o visitor name.'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Aplicar las correcciones en la base de datos. Por defecto solo muestra lo que se haría (dry-run).')
        parser.add_argument('--limit', type=int, default=0, help='Límite de registros a procesar (0 = sin límite).')

    def handle(self, *args, **options):
        apply_changes = options['apply']
        limit = options['limit']

        qs = AccessEventModels.objects.filter(credential__isnull=True).select_related('access_point')
        total = qs.count()
        self.stdout.write(f'Eventos sin credential: {total}')
        if total == 0:
            return

        processed = 0
        fixed = 0
        skipped = 0

        for ev in qs.order_by('id'):
            if limit and processed >= limit:
                break
            processed += 1

            ap_name = (ev.access_point.name or '').strip()
            candidate = None
            tried = []

            # 1) buscar dígitos en access_point.name
            digits = ''.join(ch for ch in ap_name if ch.isdigit())
            if digits:
                tried.append(('digits', digits))
                try:
                    candidate = CredentialsModel.objects.get(credential_code=digits)
                except CredentialsModel.DoesNotExist:
                    # intentar zfill a 6
                    try:
                        candidate = CredentialsModel.objects.get(credential_code=digits.zfill(6))
                        tried.append(('zfill', digits.zfill(6)))
                    except CredentialsModel.DoesNotExist:
                        candidate = None

            # 2) si no candidato, intentar match exacto como string
            if not candidate and ap_name:
                tried.append(('exact', ap_name))
                try:
                    candidate = CredentialsModel.objects.get(credential_code=ap_name)
                except CredentialsModel.DoesNotExist:
                    candidate = None

            # 3) fallback: buscar visitor por nombre que coincida con access_point.name
            if not candidate and ap_name:
                qs_cred = CredentialsModel.objects.filter(visitor__name__icontains=ap_name)
                if qs_cred.exists():
                    candidate = qs_cred.first()
                    tried.append(('visitor_icontains', ap_name))

            if candidate:
                self.stdout.write(self.style.SUCCESS(f'[{ev.id}] found credential id={candidate.id} code={candidate.credential_code} via {tried} (ap_name="{ap_name}")'))
                if apply_changes:
                    with transaction.atomic():
                        ev.credential = candidate
                        ev.save()
                    fixed += 1
                else:
                    skipped += 1
            else:
                self.stdout.write(self.style.WARNING(f'[{ev.id}] no match for access_point "{ap_name}" tried={tried}'))

        self.stdout.write('\nResumen:')
        self.stdout.write(f'  Procesados: {processed}')
        if apply_changes:
            self.stdout.write(self.style.SUCCESS(f'  Corregidos: {fixed}'))
        else:
            self.stdout.write(f'  Sugeridos (sin aplicar): {skipped}')

        self.stdout.write('Hecho.')
