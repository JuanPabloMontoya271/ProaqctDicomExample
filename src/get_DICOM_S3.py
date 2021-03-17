import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config

def dcm():
    AWS_ACCESS_KEY_ID = "AKIAQMXFNQFGDTPB77J2"
    AWS_SECRET_ACCESS_KEY = "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"
    bucket_name = 'proaqc-dicom-node'


    key='media/DICOM/listener/LURIE CHILDRENS/SCANS/DISCOVERY 690/1870858/WOOLLEY^LUKAS^^^/3070396/20210209/095302.dcm'
    # key='media/DICOM/listener/LURIE CHILDRENS/SCANS/DISCOVERY 690/1987196/CRACRAFT^TYNE^^^/3076758/20210219/161153.dcm'
    key_name = key
    # date_short = datetime.datetime.utcnow().strftime('%Y%m%d')
    # date_long = datetime.datetime.utcnow().strftime('%Y%m%dT000000Z')
    #
    # fields = {
    #             'acl': 'private',
    #             'date': date_short,
    #             'region': "us-east-2",
    #             'x-amz-algorithm': 'AWS4-HMAC-SHA256',
    #             'x-amz-date': date_long
    #         }
    #
    #
    # s3_client = boto3.client('s3',
    #                          aws_access_key_id="AKIAQMXFNQFGDTPB77J2",
    #                          aws_secret_access_key="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",
    #
    #                          )
    # #upload_details = s3_client.generate_presigned_post(bucket_name, key_name)
    #
    # # response = client.generate_presigned_url('get_object', Params={'Bucket': "proaqc-dicom-node",
    # #                                                                #                                                                    'Key': 'media/DICOM/listener/LURIE CHILDRENS/SCANS/DISCOVERY 690/1933802/PADILLA^LUIS^^^/3075123/20210217/142045.dcm',
    # #                                                                #
    # #                                                                #                                                                    }, ExpiresIn=100)
    #
    # response = s3_client.generate_presigned_url('get_object',
    #                                             Params={'Bucket': bucket_name,
    #                                                     'Key': key_name},
    #                                             Fields=fields,
    #                                             ExpiresIn=300)
    #
    # # response = s3_client.generate_presigned_post('get_object', bucket_name,
    # #                                              key_name,
    # #                                              Fields=fields,
    # #                                              ExpiresIn=300)
    #
    # print(response)

    s3_client = boto3.client('s3',
                             region_name="us-east-2",
                             aws_access_key_id="AKIAQMXFNQFGDTPB77J2",
                             aws_secret_access_key="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",
                             config=Config(signature_version='s3v4')

                             )
    try:

        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': key_name},
                                                    ExpiresIn=300)
        print('it works')
    except ClientError as e:
        print('error')
        logging.error(e)
        return None

    # The response contains the presigned URL
    print(response)

dcm()