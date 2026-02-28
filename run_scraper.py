from fastwork import FastworkClient
import json
import sys
import argparse
import os

def run_all():
    parser = argparse.ArgumentParser(description="Fastwork Scraper for OpenClaw")
    parser.add_argument("--email", type=str, help="Fastwork account email", default=os.environ.get("FASTWORK_EMAIL"))
    parser.add_argument("--password", type=str, help="Fastwork account password", default=os.environ.get("FASTWORK_PASSWORD"))
    args = parser.parse_args()

    email = args.email
    password = args.password

    try:
        with FastworkClient(headless=True, session_file="session.json") as client:
            if not client.auth.is_logged_in():
                # Session expired or not found, try to auto-relogin
                if not email or not password:
                    print(json.dumps({"error": "Auth expired or not found, and no --email/--password provided to auto-login."}))
                    sys.exit(1)
                    
                success = client.auth.login(email, password)
                if not success:
                    print(json.dumps({"error": "Failed to auto-relogin. Credentials may be invalid or captcha triggered."}))
                    sys.exit(1)

            result = {}
            # 1. Scrape Public Data
            result["search_results"] = client.scraper.search_services("web")

            # 2. Get Seller Dashboard Details
            result["seller_dashboard"] = client.seller.get_dashboard_stats()
            
            # 3. Get Seller Products
            result["seller_products"] = client.seller.get_products()
            
            # 4. Get Active Orders
            result["active_orders"] = client.orders.get_active_orders()
            
            # 5. Get Messages
            result["unread_messages"] = client.messaging.get_unread_messages()
            
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    run_all()
