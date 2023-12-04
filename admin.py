from django.contrib import admin
from .models import Matiere
from django.http import HttpResponse
import csv

class MatiereAdmin(admin.ModelAdmin):
    # ...

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="matieres.csv"'

        writer = csv.writer(response)
        writer.writerow(['Nom Matiere', 'Code', 'Niveau', 'Nb Eleve', 'Nb Seance', 'Optionnel'])

        for matiere in queryset:
            writer.writerow([matiere.nom_matiere, matiere.code, matiere.niveau, matiere.nb_eleve, matiere.nb_seance, matiere.optionnel])

        return response

    export_to_csv.short_description = 'Exporter vers CSV'

    def import_from_csv(self, request, queryset):
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                nom_matiere = row['Nom Matiere']
                code = row['Code']
                niveau = int(row['Niveau'])
                nb_eleve = int(row['Nb Eleve'])
                nb_seance = int(row['Nb Seance'])
                optionnel = bool(row['Optionnel'])

                Matiere.objects.create(nom_matiere=nom_matiere, code=code, niveau=niveau, nb_eleve=nb_eleve, nb_seance=nb_seance, optionnel=optionnel)

            self.message_user(request, "Importation réussie.")
        else:
            self.message_user(request, "Aucun fichier sélectionné.")

    export_to_csv.short_description = 'Exporter vers CSV'
    import_from_csv.short_description = 'Importer depuis CSV'

    actions = [export_to_csv, import_from_csv]

admin.site.register(Matiere, MatiereAdmin)
    
    
