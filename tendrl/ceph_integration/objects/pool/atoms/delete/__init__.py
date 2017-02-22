from tendrl.ceph_integration.manager.crud import Crud
from tendrl.ceph_integration import objects
from tendrl.ceph_integration.objects.pool import Pool
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class Delete(objects.CephIntegrationBaseAtom):
    obj = Pool
    def __init__(self, *args, **kwargs):
        super(Delete, self).__init__(*args, **kwargs)

    def run(self):
        pool_id = self.parameters['Pool.pool_id']

        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Deleting pool-id %s" %
                    self.parameters['Pool.pool_id'],
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        crud = Crud()
        ret_val = crud.delete(
            "pool",
            pool_id
        )
        if ret_val['response'] is not None and \
            ret_val['response']['error'] is True:
            Event(
                Message(
                    priority="info",
                    publisher=tendrl_ns.publisher_id,
                    payload={
                        "message": "Failed to delete pool %s."
                        " Error: %s" % (self.parameters['Pool.poolname'],
                                        ret_val['error_status'])
                    },
                    request_id=self.parameters['request_id'],
                    flow_id=self.parameters["flow_id"],
                    cluster_id=tendrl_ns.tendrl_context.integration_id,
                )
            )
            return False

        # TODO(shtripat) Use namespace tree and not etcd orm later
        tendrl_ns.etcd_orm.client.delete(
            "clusters/%s/Pools/%s" % (
                tendrl_ns.tendrl_context.integration_id,
                self.parameters['Pool.pool_id']
            ),
            recursive=True
        )

        Event(
            Message(
                priority="info",
                publisher=tendrl_ns.publisher_id,
                payload={
                    "message": "Deleted pool-id %s" %
                    self.parameters['Pool.pool_id'],
                },
                request_id=self.parameters['request_id'],
                flow_id=self.parameters['flow_id'],
                cluster_id=tendrl_ns.tendrl_context.integration_id,
            )
        )

        return True