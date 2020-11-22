from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import creds

def authenticate_client():
    ta_credential = AzureKeyCredential(creds.subscription_key)
    text_analytics_client = TextAnalyticsClient(endpoint=creds.endpoint,credential=ta_credential)
    return text_analytics_client

