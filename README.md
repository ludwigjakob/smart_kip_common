# SmartKIP Common Library

Shared utilities and configuration for all SmartKIP services.

## Features
- Database connectors for InfluxDB and MariaDB
- Debug logging utilities
- Config file parsing (hardware definitions)
- Docker Compose setup for multi-service deployment

## Example Config
```json
{
  "mode": "debug",
  "actors": {
    "fans": [
      {"id": "fan1", "type": "digital", "in1": 16},
      {"id": "fan2", "type": "digital", "in1": 26}
    ],
    "sockets": [
      {"id": "socket1", "type": "tapo_p100", "host": "192.168.1.100"}
    ]
  }
}
