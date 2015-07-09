from django.views.generic.list import MultipleObjectMixin
from django.http import StreamingHttpResponse
from common.utils import generate_csv


class CSVExportMixin(MultipleObjectMixin):
    """Mixin for exporting data as CSV using GET requests"""
    def get(self, request, *args, **kwargs):
        concrete_model = self.model._meta.concrete_model
        output_fieldnames = [f.name for f in concrete_model._meta.get_fields() if f.name != 'id']
        qs = self.get_queryset()

        csv_data = generate_csv(qs, output_fieldnames)

        response = StreamingHttpResponse(csv_data, content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="criminal-justice-{}-rows.csv"'.format(qs.count())
        return response
