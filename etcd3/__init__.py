from __future__ import absolute_import

from importlib.metadata import PackageNotFoundError, version

import etcd3.etcdrpc as etcdrpc
from etcd3.client import Endpoint
from etcd3.client import Etcd3Client
from etcd3.client import MultiEndpointEtcd3Client
from etcd3.client import Transactions
from etcd3.client import client
from etcd3.exceptions import Etcd3Exception
from etcd3.leases import Lease
from etcd3.locks import Lock
from etcd3.members import Member

__author__ = 'Louis Taylor'
__email__ = 'louis@kragniz.eu'

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = 'unknown'

__all__ = (
    'etcdrpc',
    'Endpoint',
    'Etcd3Client',
    'Etcd3Exception',
    'Transactions',
    'client',
    'Lease',
    'Lock',
    'Member',
    'MultiEndpointEtcd3Client'
)
