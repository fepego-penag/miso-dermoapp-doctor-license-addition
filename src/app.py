from db_service import *
from request_validation_utils import *
from request_response_utils import *

ENV_TABLE_NAME = "Dermoapp-sprint1-doctor-DoctorDetails-W7SV13VH080Q"


def handler(event, context):
    try:
        if validate_property_exist("doctor_id", event['pathParameters']) and validate_property_exist('body', event):
            if validate_body_license(event['body']):
                doctorID = event['pathParameters']['doctor_id']
                response = add_doctor_license(event, doctorID)
                return return_status_ok(response)
        else:
            return return_error_response("missing or malformed request body", 412)
    except Exception as err:
        return return_error_response("cannot proceed with the request error: " + str(err), 500)


def add_doctor_license(request, doctorId):
    parsedBody = json.loads(request["body"])
    registry = {
        "doctor_id": doctorId,
        "license_number": str(parsedBody['license_number'])
    }
    if insert_item(registry):
        persistedData = get_item("doctor_id", doctorId)
        return persistedData
