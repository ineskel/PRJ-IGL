from django.core.management.base import BaseCommand
from Medicaments.models import Medicament  

class Command(BaseCommand):
    help = 'Populate the database with sample medicaments'

    def handle(self, *args, **options):
        medicaments = [
            {
                'nom': 'Paracétamol',
                'description': 'Analgésique et antipyrétique utilisé pour traiter la douleur et la fièvre.'
            },
            {
                'nom': 'Ibuprofène',
                'description': 'Anti-inflammatoire non stéroïdien (AINS) utilisé pour traiter la douleur et l\'inflammation.'
            },
            {
                'nom': 'Amoxicilline',
                'description': 'Antibiotique de la famille des pénicillines utilisé pour traiter diverses infections bactériennes.'
            },
            {
                'nom': 'Oméprazole',
                'description': 'Inhibiteur de la pompe à protons utilisé pour réduire la production d\'acide gastrique.'
            },
            {
                'nom': 'Metformine',
                'description': 'Médicament antidiabétique oral utilisé pour traiter le diabète de type 2.'
            },
            {
                'nom': 'Salbutamol',
                'description': 'Bronchodilatateur utilisé pour traiter l\'asthme et la BPCO.'
            },
            {
                'nom': 'Loratadine',
                'description': 'Antihistaminique utilisé pour traiter les allergies.'
            },
            {
                'nom': 'Sertraline',
                'description': 'Antidépresseur de type ISRS utilisé pour traiter la dépression et l\'anxiété.'
            },
            {
                'nom': 'Amlodipine',
                'description': 'Inhibiteur calcique utilisé pour traiter l\'hypertension artérielle.'
            },
            {
                'nom': 'Lévothyroxine',
                'description': 'Hormone thyroïdienne de synthèse utilisée pour traiter l\'hypothyroïdie.'
            }
        ]

        for medicament_data in medicaments:
            try:
                medicament = Medicament.objects.create(**medicament_data)
                self.stdout.write(self.style.SUCCESS(f'Successfully created medicament: {medicament.nom}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create medicament {medicament_data["nom"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Database population completed!'))