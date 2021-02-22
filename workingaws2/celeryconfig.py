#!/usr/bin/env/ python3
from kombu.utils.url import safequote

aws_access_key = safequote("AKIAQQEMGEPYRZTKZCU2")
aws_secret_key = safequote("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")

broker_url = "sqs://{aws_access_key}:{aws_secret_key}@".format(
    aws_access_key=aws_access_key, aws_secret_key=aws_secret_key
)
#aws_access_key="AKIAQQEMGEPYSZONMRGL"
#aws_secret_key="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"
#SQS_URL="sqs://{aws_access_key}:{aws_secret_key}@".format(
#    aws_access_key=aws_access_key, aws_secret_key=aws_secret_key,
#)
broker_transport_options={'region':'ap-south-1'}
