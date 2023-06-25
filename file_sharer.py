from filestack import Client


class FileSharer:
    """
    Uploads a file with the specified file path to the FileStack cloud and
    generates a shareable link to the file.
    """
    def __init__(self, filepath, api_key="AeDf0UXiGRxqJrWMXoSmgz"):
        self.api_key = api_key
        self.filepath = filepath

    def share(self):
        """
        Upload a file to the filestack cloud and generate a shareable url to
        access it.
        :return: The url to access the uploaded file.
        """
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url

