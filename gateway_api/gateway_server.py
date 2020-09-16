"""Some example of gateway's handlers.
You can change, add and remove handlers depending on gateway's architecture"""

import json

from finteh_proto.server import BaseServer
from finteh_proto.dto import (
    TransactionDTO,
    OrderDTO,
    DepositAddressDTO,
    ValidateAddressDTO,
)


class GatewayServer(BaseServer):
    def __init__(self, host="0.0.0.0", port=8080, ctx=None):
        super(GatewayServer, self).__init__(host, port, ctx)

        self.add_methods(
            ("", self.validate_address),
            ("", self.get_deposit_address),
            ("", self.init_new_tx),
        )

    async def init_new_tx(self, request):
        order_data = json.loads(request.msg[1]["params"])
        order = OrderDTO(
            order_id=order_data["order_id"],
            in_tx=TransactionDTO(**order_data["in_tx"]).normalize(),
        )

        # TODO Doing check and broadcast stuff

        out_tx = TransactionDTO(**order_data["in_tx"])
        return self.jsonrpc_response(request, out_tx)

    async def get_deposit_address(self, request):
        req_data = json.loads(request.msg[1]["params"])
        deposit_address_body = DepositAddressDTO(**req_data)
        deposit_address_body.deposit_address = "DEPOSIT ADDRESS"
        return self.jsonrpc_response(request, deposit_address_body)

    async def validate_address(self, request):
        req_data = json.loads(request.msg[1]["params"])
        validate_address_body = ValidateAddressDTO(**req_data)
        validate_address_body.is_valid = True
        return self.jsonrpc_response(request, validate_address_body)
