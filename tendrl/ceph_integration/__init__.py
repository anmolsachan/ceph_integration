try:
    from gevent import monkey
except ImportError:
    pass
else:
    monkey.patch_all()

from tendrl.commons import CommonNS
from tendrl.ceph_integration.objects.definition import Definition
from tendrl.ceph_integration.objects.config import Config
from tendrl.ceph_integration.objects.tendrl_context import TendrlContext
from tendrl.ceph_integration.objects.node_context import NodeContext

from tendrl.ceph_integration.flows.create_pool import CreatePool
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.ceph_integration.objects.pool.atoms.create import Create
from tendrl.ceph_integration.objects.pool.atoms.delete import Delete
from tendrl.ceph_integration.objects.pool.flows.delete import DeletePool
from tendrl.ceph_integration.objects.sync_object import SyncObject


class CephIntegrationNS(CommonNS):
    def __init__(self):

        # Create the "tendrl_ns.ceph_integration" namespace
        self.to_str = "tendrl.ceph_integration"
        self.type = 'sds'
        super(CephIntegrationNS, self).__init__()

CephIntegrationNS()
