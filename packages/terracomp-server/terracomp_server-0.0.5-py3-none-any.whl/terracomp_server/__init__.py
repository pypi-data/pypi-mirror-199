__version__ = "0.0.5"

from ._server import TerracompServer


async def start_server(host: str, port: int) -> None:
    server = TerracompServer(host=host, port=port)
    await server.mainloop()
