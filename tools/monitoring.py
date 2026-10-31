
def check_database_status():
    """Simulate checking production database health."""
    return {
        "service": "Production Database",
        "status": "DEGRADED",
        "response_time_ms": 8500,
        "normal_response_time_ms": 200,
        "active_connections": 100,
        "connection_pool_limit": 100
    }


def fetch_error_logs():
    """Simulate retrieving recent application error logs."""
    return [
        "ERROR: Database connection timeout",
        "ERROR: Connection pool exhausted",
        "ERROR: Connection refused by database server"
    ]


def check_api_health():
    """Simulate checking application API health."""
    return {
        "service": "Application API",
        "status": "HEALTHY",
        "response_time_ms": 120
    }
