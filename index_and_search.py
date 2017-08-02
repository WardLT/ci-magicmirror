import boto3
import pickle

def index_images(folder_name, collection_name, bucket_name):
    s3 = boto3.resource('s3')
    client = boto3.client('rekognition')
    bucket = s3.Bucket(bucket_name)
    objects = [x for x in bucket.objects.all() if x.key.startswith(folder_name)]
    for i, object in enumerate(objects):
        try:
            response = client.index_faces(
                CollectionId=collection_name,
                Image={
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': object.key
                    }
                },
                ExternalImageId = folder_name + str(i),
                DetectionAttributes=[
                    'ALL'
                ]
            )
        except Exception as e:
            print(e)


def index_collection(names, collection_name, bucket, create=False):
    client = boto3.client('rekognition')
    if create:
        try:
            response = client.create_collection(CollectionId=collection_name)
        except Exception as e:
            print(e)
    for name in names:
        index_images(folder_name=name, collection_name=collection_name, bucket_name=bucket)


def search_image(image, collection_name, bucket_name, max_faces=3, method='S3'):
    client = boto3.client('rekognition')
    try:
        if method == 'S3':
            response = client.search_faces_by_image(
                CollectionId=collection_name,
                Image={
                        'S3Object': {
                            'Bucket': bucket_name,
                            'Name': image
                        }
                },
                MaxFaces=max_faces
            )
            return response
        elif method.lower() == 'byte':
            response = client.search_faces_by_image(
                CollectionId=collection_name,
                Image={
                    'Bytes': image
                },
                MaxFaces=max_faces
            )
            return response
        else:
            raise ValueError("method must be in ['S3', 'byte']")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    bucket_name = 'ci-magicmirror'
    collection_name = 'ci-faces'

    names = ['rohank', 'logany', 'monical', 'helenaa', 'beng', 'alexf']

    # Building the index (just to train)
    # client.delete_collection(CollectionId='ci-faces')
    # index_collection(names, 'ci-faces', 'ci-magicmirror', create=True)

    # Searching with byte image
    # uglybytes = pickle.load(open('byteimage'))
    # response = search_image(uglybytes, collection_name=collection_name, bucket_name=bucket_name, method='byte')

    # Searching with S3 object
    # key = 'beng/ben0.jpg'
    # response = search_image(key, collection_name=collection_name, bucket_name=bucket_name, method='S3')
