import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linked_profile_url: str, mock: bool = True):
    """scrape information from LinkedIn profiles
        Manually scrape the information from the LinkedIn profile"""

    if mock:
        linked_profile_url = 'https://gist.githubusercontent.com/shiva-nag/00932cc15867e7e46ae36b387fd81c53/raw/8be0952846f6e8ae4912b1127543569f5bd39e84/shiva-nag.json'
        response = requests.get(
            linked_profile_url,
            timeout=10
        )
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedinurl": linked_profile_url
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10
        )

    data = response.json()
    data = {
        k: v
        for k,v in data.items()
        if v not in ([],"", "", None)
        and k not in ["people also viewed", "certification"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
           and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linked_profile_url="https://www.linkedin.com/in/shivashank/"
        )
    )