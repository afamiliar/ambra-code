# This code uses the Ambra SDK package to access the Ambra API
#   Looks up a given study based on accession number & then 
#   uses the study info to download to local as a zip.
#
#   amf
#   Oct 2021
#

from ambra_sdk.api import Api
from ambra_sdk.models import Study
import shutil

url = 'https://access.dicomgrid.com/api/v3/'
username = '<ambra-user-email>'
password = '<ambra-user-password>'
access_num = '<an-accession-number>'

api = Api.with_creds(url, username, password)

# ********** find the study ********** 
study = api \
    .Study \
    .list() \
    .filter_by(Study.accession_number==access_num) \
    .first()

# ********** download the study ********** 
r = api.Storage.Study.download(engine_fqdn=study.engine_fqdn, \
                           namespace=study.storage_namespace, \
                           study_uid=study.study_uid, \
                           bundle='dicom', \
                           phi_namespace=study.phi_namespace)
if r.status_code == 200:
    with open(access_num+'.zip', 'wb') as f:
        shutil.copyfileobj(r.raw, f)
else:
    print(r.raise_for_status())
