import requests
from bs4 import BeautifulSoup
import time

# Webhook URL (replace with your actual webhook URL from Discord)
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1318028154794676345/SWDjBNf384djs6gjDPxxeQecbhfrhKb8z7LrtL6OINV-746DeYqvSrhghBpESgCc5MSH"

# Initialize the previous server status
previous_status = None

# Function to scrape the server status
def get_server_status():
    url = "https://maplelegends.com/"
    response = requests.get(url)

    if response.status_code != 200:
        return "Error: Could not retrieve data from MapleLegends."

    soup = BeautifulSoup(response.content, "html.parser")

    # We assume the server status is within an element with the class 'server-status'
    # You might need to adjust this selector based on the actual webpage structure.
    status_section = soup.find("div", class_="server_status")

    if not status_section:
        return "Error: Server status not found on the website."

    # Extract the status message, adjust based on the actual structure
    status_text = status_section.get_text(strip=True)

    return status_text.lower()  # Lowercase to make comparison easier

# Function to send a message to Discord webhook
def send_to_discord(message):
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {response.status_code}")

# Check the server status periodically
def check_server_status():
    global previous_status

    while True:
        status = get_server_status()

        # Only send a message when the server goes online (status = "online")
        if status == "online" and previous_status != "online":
            send_to_discord("MapleLegends server is now **ONLINE**!")
            previous_status = "online"
        elif status == "offline":
            previous_status = "offline"

        # Wait before checking again (e.g., 5 minutes)
        time.sleep(60 * 3)

# Run the server status check
if __name__ == "__main__":
    check_server_status()