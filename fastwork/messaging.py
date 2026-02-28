import time
from typing import List, Dict, Any
from playwright.sync_api import Page
try:
    from fuzzywuzzy import process
except ImportError:
    process = None

class MessagingManager:
    def __init__(self, page: Page):
        self.page = page

    def get_unread_messages(self) -> List[Dict[str, str]]:
        """
        Navigates to the message inbox and fetches unread messages.
        """
        self.page.goto("https://fastwork.id/messages")
        self.page.wait_for_load_state("domcontentloaded")
        
        # Example logic, adjust selectors based on actual Fastwork structure
        messages = []
        try:
            # Assuming an inbox list where unread usually has a bold/unread class
            unread_items = self.page.locator(".conversation-list-item.unread")
            
            for i in range(unread_items.count()):
                item = unread_items.nth(i)
                sender = item.locator(".sender-name").inner_text()
                preview = item.locator(".message-preview").inner_text()
                link = item.get_attribute("href")
                
                messages.append({
                    "sender": sender,
                    "preview": preview,
                    "link": f"https://fastwork.id{link}" if link.startswith("/") else link
                })
        except Exception as e:
            print(f"Error fetching unread messages: {e}")
            
        return messages

    def send_message(self, conversation_url: str, text: str):
        """
        Opens a specific conversation thread and sends a message.
        """
        self.page.goto(conversation_url)
        self.page.wait_for_selector("textarea[placeholder*='Ketik pesan']")
        
        try:
            input_box = self.page.locator("textarea[placeholder*='Ketik pesan']")
            input_box.fill(text)
            
            send_btn = self.page.locator("button.send-button")
            send_btn.click()
            
            print(f"Message sent to {conversation_url}")
            time.sleep(1) # wait for message to appear in chat log
        except Exception as e:
            print(f"Error sending message: {e}")
            
    def auto_reply(self, keyword_map: Dict[str, str]):
        """
        Basic auto-responder. Reads unread messages, checks against a keyword map,
        and replies if a match is closely found.
        """
        unreads = self.get_unread_messages()
        print(f"Found {len(unreads)} unread message threads.")
        
        for msg in unreads:
            content = msg["preview"].lower()
            
            # Simple keyword matching
            for keyword, response in keyword_map.items():
                if keyword.lower() in content:
                    print(f"Auto-replying to '{msg['sender']}' due to keyword match '{keyword}'")
                    self.send_message(msg["link"], response)
                    break # Only reply once per thread per run


class OrderManager:
    def __init__(self, page: Page):
        self.page = page

    def get_active_orders(self) -> List[Dict[str, Any]]:
        self.page.goto("https://fastwork.id/orders?status=active")
        self.page.wait_for_load_state("domcontentloaded")
        
        orders = []
        try:
            cards = self.page.locator(".order-card")
            for i in range(cards.count()):
                card = cards.nth(i)
                title = card.locator(".order-title").inner_text()
                price = card.locator(".order-price").inner_text()
                status = card.locator(".order-status-badge").inner_text()
                
                orders.append({
                    "title": title,
                    "price": price,
                    "status": status
                })
        except Exception as e:
            print(f"Error reading orders: {e}")
            
        return orders
    
    def get_order_details(self, order_url: str):
        self.page.goto(order_url)
        self.page.wait_for_load_state("domcontentloaded")
        # Extend with specific detail extraction
        pass
