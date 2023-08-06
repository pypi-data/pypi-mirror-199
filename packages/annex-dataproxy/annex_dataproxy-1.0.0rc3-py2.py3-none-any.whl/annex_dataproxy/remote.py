import os
import requests
from annexremote import Master
from annexremote import SpecialRemote
from annexremote import RemoteError


api_url: str = "https://data-proxy.ebrains.eu/api/v1"


class DataProxyRemote(SpecialRemote):

    def _stat(self):
        self.authorization_headers = {
            "Authorization": f"Bearer {os.environ['EBRAINS_TOKEN']}"
        }
        self.bucket_name, *prefix = os.environ['DATAPROXY_PATH'].split('/')
        self.prefix = '/'.join(prefix)
        url = f"{api_url}/buckets/{self.bucket_name}/stat"
        stat = requests.get(url, headers=self.authorization_headers)
        return stat

    def initremote(self):
        self._stat()
        # print('initremote', self._stat().json())

    def prepare(self):
        self._stat()
        # print('prepare', self._stat().json())

    def transfer_store(self, key, filename):
        # print('transfer_store', key, filename)
        # store the file in `filename` to a unique location derived from `key`
        # raise RemoteError if the file couldn't be stored
        key = f'{self.prefix}/{key}'
        try:
            url = f"{api_url}/buckets/{self.bucket_name}/{key}"
            ul_url = requests.put(url, headers=self.authorization_headers).json()['url']
            cmd = f"curl -s '{ul_url}' --upload-file '{filename}'"
            # print(cmd)
            os.system(cmd)
        except Exception as e:
            raise RemoteError(f'Upload failed: {e}')

    def transfer_retrieve(self, key, filename):
        key = f'{self.prefix}/{key}'
        # print('transfer_retrieve', key, filename)
        try:
            url = f"{api_url}/buckets/{self.bucket_name}/{key}?redirect=false"
            js = requests.get(url, headers=self.authorization_headers).json()
            # print(js)
            dl_url = js['url']
            cmd = f"curl -s '{dl_url}' --output '{filename}'"
            # print(cmd)
            os.system(cmd)
        except Exception as e:
            raise RemoteError(f'Download failed: {e}')
        # get the file identified by `key` and store it to `filename`
        # raise RemoteError if the file couldn't be retrieved

    def checkpresent(self, key):
        key = f'{self.prefix}/{key}'
        # print('checkpresent', key)
        try:
            url = f"{api_url}/buckets/{self.bucket_name}"
            js = requests.get(
                    url, params={'prefix': key},
                    headers=self.authorization_headers).json()
            return len(js['objects']) > 0
        except Exception as e:
            raise RemoteError(str(e))
        # return True if the key is present in the remote
        # return False if the key is not present
        # raise RemoteError if the presence of the key couldn't be determined, eg. in case of connection error
        
    def remove(self, key):
        key = f'{self.prefix}/{key}'
        # print('remove', key)
        import sys
        try:
            url = f"{api_url}/buckets/{self.bucket_name}/{key}"
            sys.stderr.write(f'DELETE {key}: ')
            sys.stderr.flush()
            resp = requests.delete(url, headers=self.authorization_headers)
            sys.stderr.write(f'{resp.status_code}\n')
            # if not resp.ok:
            #    raise RemoteError(resp.text)
        except Exception as e:
            raise RemoteError(str(e))
        # remove the key from the remote
        # raise RemoteError if it couldn't be removed


def test_remote():
    master = Master()
    remote = DataProxyRemote(master)
    master.LinkRemote(remote)
    #master.Listen()
    remote.initremote()
    remote.prepare()
    remote.transfer_store('foo', 'git-annex-remote-dataproxy')
    remote.transfer_retrieve('foo', 'bar')
    print('check preset foo', remote.checkpresent('foo'))
    print('check preset bar', remote.checkpresent('bar'))
    remote.remove('foo')
    try:
        remote.remove('bar')
    except Exception as e:
        print('fail ok', e)

