import asyncio

from fireapi import AsyncFireAPI


async def main():
    api_key = "your-api-key-here"
    fire_api = AsyncFireAPI(api_key)

    # Get server configuration
    config = await fire_api.vm.get_config()
    print("Server Configuration:")
    print(config)

    # Get server status
    status = await fire_api.vm.get_status()
    print("\nServer Status:")
    print(status)

    # Start the server
    response = await fire_api.vm.start_server()
    print("\nStart Server Response:")
    print(response)

    # Stop the server
    response = await fire_api.vm.stop_server()
    print("\nStop Server Response:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
