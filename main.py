from browser_use import Agent, ChatOpenAI, Browser
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Windows
executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
user_data_dir='C:\\Users\\Farhan\\AppData\\Local\\Google\\Chrome\\User Data'


# Connect to your existing Chrome browser
browser = Browser(
    executable_path=executable_path,
    profile_directory='Farhan',
    user_data_dir=user_data_dir,
)



async def main():
    llm = ChatOpenAI(model="gpt-4.1-mini")
    task = 'Visit https://duckduckgo.com and search for "browser-use founders"'
    agent = Agent(task=task, llm=llm, browser=browser)
    result = await agent.run()
    print(result)
    

if __name__ == "__main__":
    asyncio.run(main())