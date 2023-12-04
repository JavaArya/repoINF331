from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Professeur, Horaire, Horaireprof

class ProfesseurAdmin(admin.ModelAdmin):
    # ...

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="professeurs.csv"'

        writer = csv.writer(response)
        writer.writerow(['Nom', 'Email', 'Téléphone', 'Nombre de séances'])  # En-têtes de colonne

        for professeur in queryset:
            writer.writerow([professeur.nom_prof, professeur.email, professeur.telephone, professeur.nombre_seance])  # Valeurs des objets

        return response

    export_to_csv.short_description = 'Exporter vers CSV'

    def import_from_csv(self, request, queryset):
        # ...
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                nom_prof = row['Nom Prof']
                email = row['Email']
                telephone = int(row['Téléphone'])
                nombre_seance = int(row['Nombre de séances'])
                
                professeur = Professeur.objects.create(nom_prof=nom_prof, email=email, telephone=telephone, nombre_seance=nombre_seance)
                
                horaires = row['Horaires'].split(';')
                
                for horaire in horaires:
                    horaire_obj, created = Horaire.objects.get_or_create(plage=horaire)
                    Horaireprof.objects.create(Professeur=professeur, Horaire=horaire_obj, jour=row['Jour'])
            
            self.message_user(request, "Importation réussie.")
        else:
            self.message_user(request, "Aucun fichier sélectionné.")

    import_from_csv.short_description = 'Importer depuis CSV'

    actions = [export_to_csv, import_from_csv]

admin.site.register(Professeur, ProfesseurAdmin)
admin.site.register(Horaire)
admin.site.register(Horaireprof)