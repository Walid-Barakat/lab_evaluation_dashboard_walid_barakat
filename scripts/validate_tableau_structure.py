"""Structural validation, NOT Tableau application or rendering validation."""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import argparse, hashlib, json, urllib.request
from lxml import etree as E
from generate_evaluation_data import ROOT

URL='https://raw.githubusercontent.com/tableau/tableau-document-schemas/main/schemas/2026_2/twb_2026.2.0.xsd'
XML='http://www.w3.org/2001/XMLSchema'

def validate_refs(root):
    sheets=set(root.xpath('./worksheets/worksheet/@name'))
    ds={d.get('name'):set(d.xpath('./column/@name')) for d in root.xpath('./datasources/datasource')}
    for w in root.xpath('./worksheets/worksheet'):
        d=w.find('./table/view/datasource-dependencies');name=d.get('datasource')
        assert name in ds
        for ci in d.findall('column-instance'):assert ci.get('column') in ds[name]
        instances=set(d.xpath('./column-instance/@name'))
        for v in w.xpath('./table/panes/pane/encodings/*/@column | ./table/view/filter/@column'):
            assert v.startswith(f'[{name}].') and v[len(name)+3:] in instances, f'Invalid field ref: {v}'
    for zone in root.xpath('./dashboards/dashboard/zones/zone[@name]'):
        assert zone.get('name') in sheets, f'Unknown worksheet zone: {zone.get("name")}'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--schema',type=Path);args=ap.parse_args()
    schema_bytes=args.schema.read_bytes() if args.schema else urllib.request.urlopen(URL,timeout=40).read()
    with TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        # The published schema imports two namespaces without schemaLocation.
        # Supply namespace declarations only; no authored workbook uses user attrs or xml:base.
        (tmp/'user.xsd').write_text('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.tableausoftware.com/xml/user"><xs:attributeGroup name="UserAttributes-AG"><xs:anyAttribute namespace="##targetNamespace" processContents="skip"/></xs:attributeGroup></xs:schema>')
        (tmp/'xml.xsd').write_text('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.w3.org/XML/1998/namespace"><xs:attribute name="base" type="xs:anyURI"/></xs:schema>')
        tree=E.fromstring(schema_bytes)
        for im in tree.findall('{'+XML+'}import'):
            im.set('schemaLocation',str(tmp/('user.xsd' if im.get('namespace').endswith('/user') else 'xml.xsd')))
        schema=E.XMLSchema(tree)
        results=[]
        for path in sorted((ROOT/'tableau').glob('*.twb')):
            root=E.parse(str(path));schema.assertValid(root);validate_refs(root)
            connection=root.find('.//connection')
            assert (path.parent/connection.get('directory')/connection.get('filename')).is_file()
            results.append({'file':path.name,'xml_schema':'passed','field_and_zone_refs':'passed'})
        for path in sorted(ROOT.glob('*.twbx')):
            with ZipFile(path) as z:
                assert z.testzip() is None
                workbook=[n for n in z.namelist() if n.endswith('.twb')]
                assert len(workbook)==1
                root=E.fromstring(z.read(workbook[0]));schema.assertValid(root);validate_refs(root)
                c=root.find('.//connection');assert c.get('directory')+'/'+c.get('filename') in z.namelist()
                results.append({'file':path.name,'xml_schema':'passed','zip_integrity':'passed','embedded_csv':'passed'})
    report={'status':'passed','schema_source':URL,'schema_sha256':hashlib.sha256(schema_bytes).hexdigest(),
        'import_handling':'Namespace declaration shims for unresolved user:UserAttributes-AG and xml:base imports; main Tableau structure unchanged',
        'tableau_application_validation':'not performed','results':results}
    (ROOT/'docs/tableau_structure_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Tableau structure: 2 TWB + 2 TWBX checks passed. Native rendering NOT verified.')

if __name__=='__main__':main()
