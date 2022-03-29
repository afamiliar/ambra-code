#!/usr/bin/env python

# This code uses the Ambra SDK package to access the Ambra API
#   Looks up a given study based on accession number & then 
#   uses the study info to download to local as a zip.
#
#   amf
#   Oct 2021
#   Modified March 2022
#
#
#       NOTE on PHI_NAMESPACE:
# # each 'project'/bucket on Ambra will have a corresponding phi_namespace id
# #   not to be confused with the storage_namespace id
# #   the phi_namespace can be found within the Ambra URL for a study within the target project

#   TO DO:
#       handle when study/studies not found

from ambra_sdk.api import Api
from ambra_sdk.models import Study
import shutil
import argparse
import os
from exceptions import ImproperlyConfigured
import sys

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


def main():
    parser = argparse.ArgumentParser(
        description="A tool to download files from Ambra.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--download_type",
        nargs="?",
        choices=["all", "mrn", "accession_number"],
        required=True,
        help="Whether to download all available studies (all), studies for a given patient (mrn), or a single study (accession number).",
    )
    parser.add_argument(
        "--patient_mrn",
        nargs="?",
        help="MRN of the patient to download studies for.",
    )
    parser.add_argument(
        "--accession_number",
        nargs="?",
        help="Accession number of the study to download.",
    )
    parser.add_argument(
        "--ambra_phi_namespace",
        nargs="?",
        help="PHI namespace of the Ambra location the study/studies live in.",
    )

    args = parser.parse_args()

    if (args.download_type == 'mrn') and (args.patient_mrn is None):
        parser.error("missing --patient_mrn argument")
    if (args.download_type == 'accession_number') and (args.accession_number is None):
        parser.error("missing --accession_number argument")
    if (args.download_type == 'all') and (args.ambra_phi_namespace is None):
        parser.error("missing --ambra_phi_namespace argument")

    download_flag = args.download_type
    mrn = args.patient_mrn
    access_num = args.accession_number
    phi_namespace = args.ambra_phi_namespace

    api = Api.with_creds(url, username, password)

    # ********** find the study **********
    if download_flag == 'mrn':
        study_object = api \
            .Study \
            .list() \
            .filter_by(Study.patientid == mrn) \
            .first()
        query_object = []
        query_object.append(study_object)
    elif download_flag == 'accession_number':
        study_object = api \
            .Study \
            .list() \
            .filter_by(Study.accession_number == access_num) \
            .first()
        query_object = []
        query_object.append(study_object)
    elif download_flag == 'all':
        query_object = api \
            .Study \
            .list() \
            .filter_by(Study.phi_namespace == phi_namespace) \
            .all()

    for study in query_object:
        # print(study)
        # print(study.patient_name)
        r = api.Storage.Study.download(engine_fqdn=study.engine_fqdn,
                                       namespace=study.storage_namespace,
                                       study_uid=study.study_uid,
                                       bundle='dicom',
                                       phi_namespace=study.phi_namespace)
        if r.status_code == 200:
            if not os.path.exists(study.accession_number + '.zip'):
                out_fn = study.accession_number + '.zip'
            else:  # if a file with this accession num already exists, try adding a # to the end until it's unique
                ind = 1
                file_name_created = 0
                while file_name_created == 0:
                    if not os.path.exists(study.accession_number + '_' + str(ind) + '.zip'):
                        out_fn = study.accession_number + '_' + str(ind) + '.zip'
                        file_name_created = 1
                    else:
                        ind += 1
            with open(out_fn, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            print(r.raise_for_status())

    return 0

if __name__ == "__main__":
    sys.exit(main())
