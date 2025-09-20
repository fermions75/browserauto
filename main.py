from browser_use import Agent, ChatOpenAI, Browser, ChatGoogle
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Windows
executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
user_data_dir='C:\\Users\\Farhan\\AppData\\Local\\Google\\Chrome\\User Data'
md_file_save_path='C:\\Users\\Farhan\\Desktop\\browse_data'
link = 'https://app.money2020middleeast.com/event/money2020/people/RXZlbnRWaWV3XzEwNTU3NDA=?filters=RmllbGREZWZpbml0aW9uXzgxODUzNA%253D%253D%3ARmllbGRWYWx1ZV8yODI4Njg3MA%253D%253D'

# Connect to your existing Chrome browser
browser = Browser(
    cdp_url="http://localhost:9222"  # Connect to the Chrome instance with debugging enabled
)



async def main():
   # llm = ChatOpenAI(model="gpt-4.1-mini")
   # Initialize the model
   llm = ChatGoogle(model='gemini-2.5-flash')
   task = f'''TASK: Networking Automation for Money20/20 Middle East Event

STEP 1: Navigate to the event page
- Go to: {link}
- Wait for the page to fully load
- Verify you can see the list of people/attendees

STEP 2: For each of the 50 people in the list or grid, perform the following actions:
   a) If the connection request button is not clickable:
      - Move to next person
   b) If the connection request button is clickable:
      - Click on it to open in a new tab
      - Use this personalized message: "Hi `first_name`, Rohan here..leading a couple North American fintech initiatives and exMorgan Stanley product/strategy guy..Would love to connect and learn about your experience building in Middle East."
      - Send the connection request
   c) Go back to the main list and proceed to next person
   d) Repeat the process for the next 50 people
   e) Do not repeat the process for the same person
   f) Scroll down to the bottom of the page to load all the people
'''

   new_task = f"""
   TASK: 
   1. Use the go_to_url to go to the url: {link}
   2. Find a list of people in the page
   3. Use the click_element_by_index open the first person's Connections request button if it is clickable
   4. Use the send_keys to send the message: "Hi `first_name`, Rohan here..leading a couple North American fintech initiatives and exMorgan Stanley product/strategy guy..Would love to connect and learn about your experience building in Middle East."
   5. Use go_back and go back to the main list
   6. Scroll down to the bottom of the page to load all the people
   7. Repeat the process for the next 50 people
   8. Do not repeat the process for the same person
   """

   agent = Agent(task=task, llm=llm, browser=browser)
   result = await agent.run()


if __name__ == "__main__":
    asyncio.run(main())