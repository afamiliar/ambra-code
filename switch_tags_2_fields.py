# Documentation: https://dicomgrid.github.io/sdk-python/index.html
#               https://access.dicomgrid.com/api/v3/api.html
#
#   can find customfield UUID in the URL when under Settings/Customfields/...

import pandas as pd
import os

from ambra_sdk.api import Api
from ambra_sdk.models import Study
from ambra_sdk.service.filtering import Filter, FilterCondition
from ambra_sdk.service.sorting import Sorter, SortingOrder

# set Ambra stuff
# url = 'https://access.dicomgrid.com/api/v3/' # CHOP clinical account
url = 'https://choparcus.ambrahealth.com/api/v3/' # CHOP Arcus account
username=os.getenv("AMBRA_USERNAME")
password=os.getenv("AMBRA_PASSWORD")

api = Api.with_creds(url, username, password)

# Loop through all namespaces user has access to
user_info = api.Session.user().get()
for phi_namespace in user_info.namespaces:
    if 'D3b' in phi_namespace.name:
    # if 'Lurie' in phi_namespace.name:
        print(f' ============= {phi_namespace.name} =============')
        studies = api \
            .Study \
            .list() \
            .filter_by(Study.phi_namespace == phi_namespace.uuid)  \
            .all()
        for study in studies:
            try:
                for tag in study.tags:
                    # switch tag to customfield
                    if tag == 'processed_Flywheel':
                        api.Study.set( # service namespace
                                study_id=study.uuid, \
                                customfield_param={'8d7bb9c5-eaac-4b5d-b534-8cf92ee1601c':'Yes'},\
                            ).get()
                    elif tag == 'error':
                        api.Study.set( # service namespace
                                study_id=study.uuid, \
                                customfield_param={'8d7bb9c5-eaac-4b5d-b534-8cf92ee1601c':'Error'},\
                            ).get()
                    # delete the tag
                    api.Tag.delete( # service namespace
                        object='Study', \
                        object_id=study.uuid, \
                        tag=tag, \
                    ).get()
            except:
                continue


                    # elif tag == 'error':

