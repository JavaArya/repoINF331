from django.contrib import admin
from .models import salle
import csv
from django.http import HttpResponse

class SalleAdmin(admin.ModelAdmin):
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="salles.csv"'

        writer = csv.writer(response)
        writer.writerow(['Nom', 'Nombre de places'])

        for salle in queryset:
            writer.writerow([salle.name, salle.nombre_place])

        return response

    export_to_csv.short_description = "Exporter vers CSV"

    def import_from_csv(self, request, queryset):
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                name = row['Nom']
                nombre_place = int(row['Nombre de places'])
                salle.objects.create(name=name, nombre_place=nombre_place)

            self.message_user(request, "Importation réussie.")
        else:
            self.message_user(request, "Aucun fichier sélectionné.")

    import_from_csv.short_description = "Importer depuis CSV"

    actions = [export_to_csv, import_from_csv]

admin.site.register(salle, SalleAdmin)