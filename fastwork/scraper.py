from playwright.sync_api import Page
from typing import List, Dict, Any

class Scraper:
    def __init__(self, page: Page):
        self.page = page

    def search_services(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches Fastwork.id for services matching a query.
        """
        # Encode query to prevent URL issues
        import urllib.parse
        encoded_query = urllib.parse.quote_plus(query)
        self.page.goto(f"https://fastwork.id/search?q={encoded_query}")
        self.page.wait_for_load_state("domcontentloaded")
        
        results = []
        try:
            # Assumed generic product card structure
            cards = self.page.locator(".product-card, .service-card")
            for i in range(cards.count()):
                try:
                    card = cards.nth(i)
                    title = card.locator(".product-title, .title").inner_text()
                    freelancer = card.locator(".freelancer-name, .username").inner_text()
                    price = card.locator(".price").inner_text()
                    rating = card.locator(".rating, .review-score").inner_text()
                    url = card.locator("a").get_attribute("href")
                    
                    # Resolve relative URLs
                    if url and not url.startswith("http"):
                        url = f"https://fastwork.id{url}"

                    results.append({
                         "title": title,
                         "freelancer": freelancer,
                         "price": price,
                         "rating": rating,
                         "url": url
                    })
                except Exception as e:
                    # Handle individual card parsing errors gracefully
                    pass
        except Exception as e:
            print(f"Error scraping search results: {e}")
            
        return results

    def get_freelancer_profile(self, profile_url: str) -> Dict[str, Any]:
        """
        Scrapes a freelancer's public profile page.
        """
        self.page.goto(profile_url)
        self.page.wait_for_load_state("domcontentloaded")
        
        profile = {}
        try:
            profile["username"] = self.page.locator("h1.profile-name, .username").inner_text()
            profile["bio"] = self.page.locator(".profile-bio, .description").inner_text()
            profile["rating"] = self.page.locator(".overall-rating").inner_text()
            
            # Scrape services listed on profile
            services = []
            service_cards = self.page.locator(".service-card")
            for i in range(service_cards.count()):
                card = service_cards.nth(i)
                title = card.locator(".title").inner_text()
                link = card.locator("a").get_attribute("href")
                
                services.append({"title": title, "url": link})
                
            profile["services"] = services
            
        except Exception as e:
            print(f"Error scraping profile formatting: {e}")
            
        return profile
