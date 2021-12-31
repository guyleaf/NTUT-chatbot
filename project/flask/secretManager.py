from google.cloud import secretmanager


def access_secret_version(resource_id, version):

    client = secretmanager.SecretManagerServiceClient()
    name = f"{resource_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})

    payload = response.payload.data.decode("UTF-8")
    return payload
