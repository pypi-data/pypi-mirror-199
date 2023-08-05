from akerbp.mlpet.utilities import get_cognite_client

CLIENT = get_cognite_client(permission_scope="read")
CLIENT_FUNCTIONS = get_cognite_client(permission_scope="write")
