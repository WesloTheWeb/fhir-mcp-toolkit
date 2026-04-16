from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("fhir-toolkit")

FHIR_BASE = "https://hapi.fhir.org/baseR4"
HEADERS = {"Accept": "application/fhir+json"}


@mcp.tool()
def get_patient(patient_id: str) -> dict:
    """Fetch a patient's demographic record from the FHIR server.
    
    Use when the user asks about a specific patient's name, birth date,
    gender, address, or other identifying information.
    """
    url = f"{FHIR_BASE}/Patient/{patient_id}"
    response = httpx.get(url, headers=HEADERS, timeout=10.0)
    response.raise_for_status()
    return response.json()


@mcp.tool()
def search_patients(name: str, count: int = 5) -> dict:
    """Search for patients by name on the FHIR server.
    
    Use when the user wants to find a patient but doesn't know the ID,
    only a name like 'Smith' or 'Jane'.
    """
    url = f"{FHIR_BASE}/Patient"
    params = {"name": name, "_count": count}
    response = httpx.get(url, params=params, headers=HEADERS, timeout=10.0)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    mcp.run()