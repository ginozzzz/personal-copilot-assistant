#!/usr/bin/env python3
"""
Bulk add subscribers to a Mailchimp audience using urllib (stdlib only).

Usage:
    python add_subscribers.py --api-key KEY --list-id ID --csv subscribers.csv

CSV Format: email,first_name,last_name,tags
    email,first_name,last_name,tags
    jane@example.com,Jane,Doe,customer,vip
    john@example.com,John,Smith,newsletter

Notes:
    - Uses the dedicated tags endpoint (POST /lists/{id}/members/{hash}/tags)
      which is the correct way to apply tags in Mailchimp.
    - The add_or_update_member endpoint does NOT reliably apply tags;
      always use the separate tags endpoint after upserting the member.
"""

import argparse
import csv
import hashlib
import json
import time
import urllib.request
import urllib.parse
import urllib.error
import sys


def api_request(method: str, url: str, api_key: str, data: dict | None = None) -> dict:
    """Make a raw Mailchimp API request using urllib."""
    body = json.dumps(data).encode("utf-8") if data else None

    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise Exception(f"API error {e.code}: {error_body}") from e
    except urllib.error.URLError as e:
        raise Exception(f"Connection error: {e.reason}") from e


def hash_email(email: str) -> str:
    """MD5 hash of lowercase email — used as Mailchimp subscriber ID."""
    return hashlib.md5(email.lower().encode("utf-8")).hexdigest()


def get_base_url(api_key: str) -> str:
    """Extract data center from API key and build base URL."""
    parts = api_key.rsplit("-", 1)
    if len(parts) != 2:
        sys.exit("Invalid API key format. Expected: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-usXX")
    return f"https://{parts[1]}.api.mailchimp.com/3.0"


def add_or_update_member(
    base_url: str,
    api_key: str,
    list_id: str,
    email: str,
    first_name: str = "",
    last_name: str = "",
    tags: list[str] | None = None,
    status: str = "subscribed",
) -> dict:
    """Upsert a member then apply tags via the dedicated tags endpoint."""
    email_hash = hash_email(email)
    member_data = {
        "email_address": email,
        "status_if_new": status,
        "status": status,
        "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name,
        },
    }

    # Step 1: Upsert member
    member_url = f"{base_url}/lists/{list_id}/members/{email_hash}"
    member = api_request("PUT", member_url, api_key, member_data)

    # Step 2: Apply tags via the dedicated tags endpoint
    if tags:
        tag_data = {"tags": [{"name": tag.strip(), "status": "active"} for tag in tags]}
        tag_url = f"{base_url}/lists/{list_id}/members/{email_hash}/tags"
        api_request("POST", tag_url, api_key, tag_data)

    return member


def read_csv(path: str) -> list[dict]:
    """Read subscriber records from a CSV file."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description="Bulk add subscribers to Mailchimp audience")
    parser.add_argument("--api-key", required=True, help="Mailchimp API key (format: xxxxx-usXX)")
    parser.add_argument("--list-id", required=True, help="Mailchimp audience (list) ID")
    parser.add_argument("--csv", required=True, help="Path to CSV file with subscriber data")
    parser.add_argument(
        "--status",
        default="subscribed",
        choices=["subscribed", "pending", "unsubscribed"],
        help="Subscription status (default: subscribed)",
    )
    parser.add_argument(
        "--rate-limit-delay",
        type=float,
        default=0.1,
        help="Delay between API calls in seconds (default: 0.1)",
    )
    args = parser.parse_args()

    base_url = get_base_url(args.api_key)
    subscribers = read_csv(args.csv)

    print(f"Adding {len(subscribers)} subscriber(s) to audience {args.list_id} ...")
    print(f"Status: {args.status}")
    print()

    success = 0
    failed = 0

    for row in subscribers:
        email = row.get("email", "").strip()
        if not email:
            print(f"  SKIP: missing email in row: {row}")
            continue

        first_name = row.get("first_name", "").strip()
        last_name = row.get("last_name", "").strip()
        tags = [t.strip() for t in row.get("tags", "").split(",") if t.strip()] or None

        try:
            add_or_update_member(
                base_url=base_url,
                api_key=args.api_key,
                list_id=args.list_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                tags=tags,
                status=args.status,
            )
            print(f"  OK:   {email}")
            success += 1
        except Exception as e:
            print(f"  FAIL: {email} — {e}")
            failed += 1

        time.sleep(args.rate_limit_delay)

    print()
    print(f"Done — {success} added/updated, {failed} failed")


if __name__ == "__main__":
    main()
