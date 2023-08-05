import hashlib


def calculate_s3_etag(file_path, chunk_size=8 * 1024 * 1024):
    result = []

    with open(file_path, 'rb') as fp:
        while True:
            data = fp.read(chunk_size)
            if not data:
                break
            result.append(hashlib.md5(data))

    if result.__len__() < 1:
        return '{}'.format(hashlib.md5().hexdigest())

    if result.__len__() == 1:
        return '{}'.format(result[0].hexdigest())

    digests = b''.join(m.digest() for m in result)
    digests_md5 = hashlib.md5(digests)
    return '{}-{}'.format(digests_md5.hexdigest(), result.__len__())
