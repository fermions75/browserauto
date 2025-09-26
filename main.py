from browser_use import Agent, ChatOpenAI, Browser, ChatGoogle, ChatAzureOpenAI
from dotenv import load_dotenv
import asyncio
import json
from prompt import get_task, get_linkedin_task

load_dotenv()

# Windows
executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
user_data_dir='C:\\Users\\Farhan\\AppData\\Local\\Google\\Chrome\\User Data'
md_file_save_path='C:\\Users\\Farhan\\Desktop\\browse_data'
link = 'https://app.money2020middleeast.com/event/money2020/people/RXZlbnRWaWV3XzEwNTU3NDA=?filters=RmllbGREZWZpbml0aW9uXzgxODUzNA%253D%253D%3ARmllbGRWYWx1ZV8yODI4Njg3MA%253D%253D'

# Connect to your existing Chrome browser


async def load_people():
   with open('people.json', 'r', encoding='utf-8') as file:
      people = json.load(file)
   return people

async def process_people(people):
   persons = []
   print(f"Total people: {len(people['data']['view']['people']['nodes'])}")
   for person in people['data']['view']['people']['nodes']:
      if not person['userInfo']['hasSentRequest'] and person['userInfo']['connectionStatus'] == 'NOT_CONNECTED':
         persons.append({
            'name': f"{person['firstName']} {person['lastName']}",
            'message': f"Hi {person['firstName']}, Rohan here..leading a couple North American fintech initiatives and ex Morgan Stanley product/strategy guy..Would love to connect and learn about your experience building in Middle East.",
            'link': f"https://app.money2020middleeast.com/event/money2020/person/{person['id']}"
         })
   print(f"Total people to process: {len(persons)}")
   return persons


async def main():
   llm = ChatOpenAI(model="gpt-4.1-mini")
   # llm = ChatAzureOpenAI(model="gpt-4.1-mini")
   # llm = ChatGoogle(model="gemini-2.0-flash-001")
   # people = await load_people()
   # persons = await process_people(people)

   # cnt = 0
   # for person in persons:
   #    print(f"Processing person {cnt+1} of {len(persons)}")
   #    cnt += 1
   #    task = get_task(person['link'], person['message'])
   #    print(task)
   #    browser = Browser(
   #       cdp_url="http://localhost:9222"  # Connect to the Chrome instance with debugging enabled
   #    )
   #    agent = Agent(task=task, llm=llm, browser=browser)
   #    result = await agent.run()

   link = 'https://www.linkedin.com/in/georgedamouny/'
   message = "Hi, I am Farhan and would like to connect with you."
   task = get_linkedin_task(link, message)
   print(task)
   browser = Browser(
      cdp_url="http://localhost:9222"  # Connect to the Chrome instance with debugging enabled
   )
   agent = Agent(task=task, llm=llm, browser=browser)
   result = await agent.run()
   print(result)


if __name__ == "__main__":
    asyncio.run(main())