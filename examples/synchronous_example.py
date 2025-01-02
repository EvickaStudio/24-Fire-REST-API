from fireapi import FireAPI

api_key = "your-api-key-here"
fire_api = FireAPI(api_key)

# Get server configuration
config = fire_api.vm.get_config()
print("Server Configuration:")
print(config)

# Get server status
status = fire_api.vm.get_status()
print("\nServer Status:")
print(status)

# Start the server
response = fire_api.vm.start_server()
print("\nStart Server Response:")
print(response)

# Stop the server
response = fire_api.vm.stop_server()
print("\nStop Server Response:")
print(response)
