import boto3
from botocore.exceptions import EndpointConnectionError


def store_report(settings, environment):
    """Send test results to an s3 bucket."""

    session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key=''
    )

    timestamp_str_y = datetime.now().strftime("%Y")
    timestamp_str_m = datetime.now().strftime("%m")
    timestamp_str_d = datetime.now().strftime("%d")
    timestamp_str_h = datetime.now().strftime("%H")
    timestamp_str_h_m = datetime.now().strftime("%H:%M")


    s3_bucket = s3.Bucket(settings['s3_bucket_name'])
    report_file_name = 'report-{}-{}.html'.format(environment, timestamp_str)
    log_file_name = 'log-{}-{}.html'.format(environment, timestamp_str)

    try:
        s3_bucket.upload_file('/tmp/report.html', report_file_name)
        s3_bucket.upload_file('/tmp/log.html', log_file_name)
        screenshot_name = export_and_erase_screenshot(s3_bucket, environment, timestamp_str)
    except FileNotFoundError:
        logger.error('[store_report] Reports not found (either report.html or log.html is missing)')
    except EndpointConnectionError:
        logger.error('[store_report] Connection to remote bucket failed')
    else:
        logger.info(('[store_report] Result files successfully stored. '
                     'report=%s, log=%s'), report_file_name, log_file_name)

        return report_file_name, log_file_name, screenshot_name
