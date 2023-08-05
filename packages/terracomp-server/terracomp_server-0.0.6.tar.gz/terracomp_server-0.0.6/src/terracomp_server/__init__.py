__version__ = "0.0.6"

from ._server import TerracompServer


async def start_server(host: str, port: int) -> None:
    server = TerracompServer(host=host, port=port)
    await server.mainloop()
