from .models import import_dossiers, dossier
import pandas as pd
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
from import_export import resources

def Create_Dossiers():
    my_model = import_dossiers.objects.latest("date_import")
    csv_file = my_model.import_op.path
    print(csv_file)
    df = pd.read_csv(csv_file, encoding="UTF-8", delimiter=';', decimal=',', skipinitialspace=True)
    df = df.fillna(0)
    df["PRIX/KG"] = df["PRIX/KG"].str.replace("NO PRICING","0")
    df["PRIX/KG"] = df["PRIX/KG"].str.replace(",", ".")
    df["PRIX/KG"] = df["PRIX/KG"].fillna(0)
    print(df)
    row_iter = df.iterrows()

    objs = [
        dossier(
            customer=row["CUSTOMER"],
            product=row["PRODUCT"],
            c4c = row["C4C"],
            channel = row["CHANNEL"],
            supplier = row["SUPPLIER"],
            sample_statue = row["SAMPLE STATUE"],
            comm_cust = row["COMM CUST"],
            result_next_step = row["RESULTS & NEXT STEP"],
            statue = row["SAMPLE STATUE"],
            y_mb = row["YMB"],
            y_vol = row["Y VOL kg"],
            vol_po_kg = row["VOL PO kg"],
            ref_prod_sap = row["REF PRODUIT SAP"],
            prix_kg = row["PRIX/KG"],
            rep = row["REP"],
            sap_id=row["SAP ID"],
            started_on = row["STARTED ON"],
            up_to_date = row["UP TO DATE"],
            other = row["OTHER"],
        )

        for index, row in row_iter

    ]

    create = dossier.objects.bulk_create(objs)

    return create

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class MyModelResource(resources.ModelResource):
    class Meta:
        model = dossier
        fields = ['customer', 'product', 'product', 'c4c', 'channel', ' supplier', 'sample_statue', 'result_next_step', ' statue ', 'y_mb', 'y_vol', 'vol_po_kg', 'ref_prod_sap', 'prix_kg', 'rep', 'sap_id', 'started_on', 'up_to_date ', 'other']

