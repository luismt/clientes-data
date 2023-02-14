from django.core.management.base import BaseCommand

from clientes.models import Cliente, FullSolution


class Command(BaseCommand):
    def handle(self, *args, **options):
        fullsolution = FullSolution.objects.all()
        clientes_query = Cliente.objects.all()
        contratos_list = [c.contrato for c in clientes_query]
        fullsolution = FullSolution.objects.exclude(contrato__in=contratos_list)


