from pydantic import ValidationError
from extract import fetch_launches
from models import Launch
from load import save

def run():
    valid, bad = [], 0
    for x in fetch_launches():
        try:
            provider = x["launch_service_provider"]
            valid.append(Launch(
                id=x["id"],
                name=x["name"],
                status=x["status"]["name"],
                agency=provider["name"],
                agency_type=provider.get("type"),
                net=x["net"],
                fail_reason=x.get("failreason"),
                mission_type=(x.get("mission") or {}).get("type"),
            ))
        except (ValidationError, KeyError, TypeError):
            bad += 1
    save(valid)
    print(f"Saved {len(valid)} launches, rejected {bad}")

if __name__ == "__main__":
    run()