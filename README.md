# Mox : solr

Denne Mox er beregnet til at gøre OS2MO søgbar i solr

Den nødvendige konfigurationsfil findes et af 3 steder:
 
 * inten specificeret som *MOX_MO_CONFIG* i environment
 * 'settings.ini' i 'current working directory'
 * 'settings.ini' i samme directory som filen 'config.py' 

Følgende kan konfigureres idenne konfigurationsfil

	[settings]

	MOX_LOG_LEVEL
	MOX_LOG_FILE
	OS2MO_SERVICE_URL
	OS2MO_SAML_TOKEN
	OS2MO_ORG_UUID
	OS2MO_CA_BUNDLE
	SOLR_URL

For en OS2MO i udviklingsmode (http) er det kun nødvendigt at angive *OS2MO_SERVICE_URL* og *SOLR_URL*


