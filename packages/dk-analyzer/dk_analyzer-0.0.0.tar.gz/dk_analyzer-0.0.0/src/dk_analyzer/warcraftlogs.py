import requests

from dk_analyzer.models import Event


def get_access_token(client_id: str, client_secret: str) -> str:
    response = requests.post(
        "https://www.warcraftlogs.com/oauth/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        timeout=5,
    )
    return response.json()["access_token"]


def fetch_report(report_id: str, fight_id: int, access_token: str) -> list[Event]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    body = f"""
query {{
    reportData {{
        report(code:"{report_id}"){{
            events(
                fightIDs:{fight_id},
                abilityID:45470,
                sourceClass:"DEATHKNIGHT",
                dataType:Healing,
                includeResources:true,
                limit:9000
            ) {{
                data
                nextPageTimestamp
            }}
        }}
    }}
}}
    """
    response = requests.post(
        "https://www.warcraftlogs.com/api/v2/client",
        headers=headers,
        json={"query": body},
        params={"code": report_id},
        timeout=5,
    )
    json_report = response.json()["data"]["reportData"]["report"]
    json_events = json_report["events"]["data"]
    return [Event(json_event) for json_event in json_events]
