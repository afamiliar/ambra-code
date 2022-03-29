#!/usr/bin/env python3

# This code uses the Ambra SDK package to access the Ambra API
#   Looks up all studies in a user-defined Ambra bucket & then 
#   outputs the # of unique subjects found.
#
#
#   https://dicomgrid.github.io/sdk-python/index.html
#
#   amf
#   March 2022
#

from ambra_sdk.api import Api
from ambra_sdk.models import Study
import os
from exceptions import ImproperlyConfigured

url = 'https://access.dicomgrid.com/api/v3/'

username = os.getenv("AMBRA_USERNAME")
if username is None:
    raise ImproperlyConfigured(
        "You must supply a valid Ambra username in AMBRA_USERNAME."
    )

password = os.getenv("AMBRA_PASSWORD")
if password is None:
    raise ImproperlyConfigured(
        "You must supply a valid Ambra password in AMBRA_PASSWORD."
    )

# each 'project'/bucket on Ambra will have a corresponding phi_namespace id
#   not to be confused with the storage_namespace id
#   the phi_namespace can be found within the Ambra URL for a study within the target project
phi_namespace = os.getenv("AMBRA_PHI_NAMESPACE")
if phi_namespace is None:
    raise ImproperlyConfigured(
        "You must supply a valid Ambra PHI-namespace in AMBRA_PHI_NAMESPACE."
    )

# *************** download all studies in a given project *************** 

api = Api.with_creds(url, username, password)

# find all studies
query_object = api \
              .Study \
              .list() \
              .filter_by(Study.phi_namespace == phi_namespace)  \
              .all()

sub_list = []
study_count = 0
for study in query_object:
    # print(study.patientid)
    # print(study.patient_name)
    if study.patientid not in sub_list:
        sub_list.append(study.patientid)
    study_count += 1

n_subjs = str(len(sub_list))
n_studies = str(study_count)
print(f'Number of unique subjects found on Ambra: {n_subjs}')
print(f'Number of unique studies found on Ambra: {n_studies}')
