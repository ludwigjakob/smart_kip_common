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
```

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
This project uses third-party libraries under the following licenses:
- json (Python standard library, PSF License)
- abc (Python standard library, PSF License)
- python-dotenv (BSD-3-Clause)
- mysql-connector-python (GPL-2.0 with FOSS Exception)
- pandas (BSD-3-Clause)
- influxdb-client (MIT)
