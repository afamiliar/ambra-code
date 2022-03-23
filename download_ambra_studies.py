# This code uses the Ambra SDK package to access the Ambra API
#   Looks up all studies in a user-defined Ambra bucket & then 
#   uses the study info to download to local as a zip (named by corresponding accession #).
#
#   Requires user to have download permissions on the bucket.
#
#   https://dicomgrid.github.io/sdk-python/index.html
#
#   amf
#   Oct 2021
#

from ambra_sdk.api import Api
from ambra_sdk.models import Study
import shutil
import os

url = 'https://access.dicomgrid.com/api/v3/'
username = '<ambra-user-email>'           # Ambra account user name
password = '<ambra-user-password>'        # Ambra account password

api = Api.with_creds(url, username, password)

# *************** define the target project *************** 

# each 'project'/bucket on Ambra will have a corresponding phi_namespace id
#   not to be confused with the storage_namespace id
#   the phi_namespace can be found within the Ambra URL for a study within the target project
phi_namespace = '<phi-namespace-id>' # for the given bucket on Ambra

# *************** download all studies in a given project *************** 

# find all studies
query_object = api \
              .Study \
              .list() \
              .filter_by(Study.phi_namespace==phi_namespace)  \
              .all()

for study in query_object:
    # print(study.patient_name)
    r = api.Storage.Study.download(engine_fqdn=study.engine_fqdn, \
                               namespace=study.storage_namespace, \
                               study_uid=study.study_uid, \
                               bundle='dicom', \
                               phi_namespace=study.phi_namespace)
    if r.status_code == 200:
        if not os.path.exists(study.accession_number+'.zip'):
          out_fn = study.accession_number+'.zip'
        else: # if a file with this accession # already exists, try adding a # to the end until it's unique
          ind = 1
          file_name_created=0
          while file_name_created==0:
            if not os.path.exists(study.accession_number+'_'+str(ind)+'.zip'):
              out_fn = study.accession_number+'_'+str(ind)+'.zip'
              file_name_created=1
            else:
              ind+=1
        with open(out_fn, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        print(r.raise_for_status())
