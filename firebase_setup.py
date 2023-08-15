import pyrebase

# Configuração do Firebase
firebase_config = {
    "type": "service_account",
    "project_id": "footballdata-394521",
    "private_key_id": "d0e6aadf84e8aa8511f8664c7a75f6ca6872edfe",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCwGz1YaxqrMunU\nbH5PfunBZErigRYrxKGWpIIURdNY1IUVHwN4ogvuVpgtqlaWSF0uiQ0/oSE39zJf\niiZPEuDsDP63py9NnKSRF3tzW0LrPq9mvnnDCjygf23X7nGgMWHzQ0ZD7tDGOc0P\nMHAqnfKna+J72bzyUNqxtR3GDnGioOjZcHyPqbiGHoE7x3aVnYoI/tUtOSM4pLiy\nh0SJW+VGw5P93NPzhSOq3RWQwmJYiyQyI/UZcnAgw02/xrBeqYdslQt+zzrKi+85\nVQCZdhS317Gpe8MMwrj/Acoj/FuBTNQjECNFCGda4E2P8sfEiZ1ZPIA0CS907zGF\nnSBGAnUBAgMBAAECggEAB5e7usdutawNsqkqfqUZ5nWQw03DUIfwhepvVPjtY7fR\nShJq0lAS7sfLKrLcpgDriuar9yRBu/mQ3CzRudiLm9nJP06lETX8Tr4iBjH3LhB8\nkak2M4902DWjnSr3Dqv6YrmHOsVojmyuYjsu0YOQU0wT485E4XdUyn3PfBB3hpun\ndx5pvHaIQ6LOc4vJTEDXZ3reZ3/++hU6qaQNejOZvlyroM1psEELTTqKO5NrmJnn\n9SVxMdUADjDpA1N6eRAzpUrs3pJUfS637Jp0XUVBg6IQMnDOrR9WfBm12qVbpCUx\neo77Fh+ynB1hlH4yj5xGVXXccRUSY9pEzNDfItQFbQKBgQDw8OJOx0xa16OhQ+59\n1b/Etp7gXHCimEwuCPL0vRJELPDCPhMGzdNM9iTE0RpfWk/Uq/Q3Atx2JWlTwUb9\nZs9S0xHOZ+E47Ct11mznaCIAjqDmQxB7X2RJz2m7jYmBfUKCK2jG1d2IE8a8E33R\nd7EkNlgKeIJaFy+OLkER42E3/QKBgQC7HPyLMC0pLaOo8vioiLVAHArgqUZ0Zzfw\n3UM+V4TRuBiB3zkZALGCTTzxfn4xAFC3oJNTwixv0i0xmBNQQT7tUeyP+2REGMAQ\nOujqr8Ipv8cm6+0rEZ/5aRe5od4mVs3TTMESLW0MypmjMeXDQanqwEF+O0HnZSId\nY02nr7G2VQKBgBsw1BlX3IIT+99jLzL8QFwOz/c592wiC9bWI7UC8WDIQZNqNfN6\nnvH8hUHA510DcCbsEO90XzTmG/Dbywsl4xfRwhytFHm8DVuLC1dCJTQy5G2X+/Aw\nX70Er0X/Pxlh7XOLOpPV5t5IfREUkgplm5QenejwmKVaIH/HMIi4RGxxAoGBAKua\nAeKE5GYHfTjM3E90UQXisfcoR30pzJwR0EG0chMECzXQSsUrZaBixamUoJa/+0bs\n9TCzu50x3FDHb68Cp3tuzs2deG8bY8l+vW2+kwtG3pZLeM8u8tACGcgdM2dl5I4M\nrmTFVGWOyShp8pYH+pVYjLgAEIjur0LUd7t53jmhAoGBAIbqZn/CALx6XpzxubHj\nWIgIFIevGpplFyqnbbuR4RxEMnp/ouJgqoRMHQLj8Tt1h2LNhUfHrg27nTN6cR6k\ngdSiMsm5BMItfRsX9Bt5BnaRIqsCotW3fF9Ec7eccSoHOPT/M8cTxL5AWrLqXFJ4\ntKJg3pUOAPMHc4QxsRUaimCZ\n-----END PRIVATE KEY-----\n",
    "client_email": "football-data@footballdata-394521.iam.gserviceaccount.com",
    "client_id": "100267629167911446263",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/football-data%40footballdata-394521.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

def initialize_firebase():
    firebase = pyrebase.initialize_app(firebase_config)
    return firebase.auth()

auth = initialize_firebase()
