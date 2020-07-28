import asyncio
import logging

from aiohttp.web import (
    AppRunner as HTTPAppRunner,
    TCPSite as HTTPTCPSite,
    RouteTableDef as HTTPRouteTableDef
)

from booker.app import AppContext


async def server(runner: HTTPAppRunner) -> None:
    logging.info('HTTP server has started.')

    cancel_signal = asyncio.Event()

    try:
        await asyncio.wait({asyncio.create_task(cancel_signal.wait())})
    except asyncio.CancelledError:
        logging.debug('HTTP server is stopping.')

        await runner.cleanup()

        logging.info('HTTP server has stopped.')


async def start_server(
    context: AppContext,
    handlers: HTTPRouteTableDef
) -> None:
    logging.debug('HTTP server is starting.')

    context.http_app.add_routes(handlers)

    runner = HTTPAppRunner(context.http_app)

    await runner.setup()

    site = HTTPTCPSite(
        runner,
        context.config.http_host,
        context.config.http_port
    )

    await site.start()

    context.http_task = asyncio.create_task(server(runner))
