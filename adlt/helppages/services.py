import pkg_resources as pres

from docutils.core import publish_parts
from docutils import io


def render(path):
    with open(pres.resource_filename('adlt.helppages', 'pages/' + path + '.rst')) as f:
        parts = publish_parts(f, source_class=io.FileInput, writer_name='html')
    return parts
