from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        print(result)
        print("\n\n\n\n\nVALUE:\n")
        print(result.getvalue())
        return result
    return None

def encode_html(html):
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        print(result)
        print("\n\n\n\n\nVALUE:\n")
        print(result.getvalue())
        return result.getvalue()   
    return None