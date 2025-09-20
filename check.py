from browser_use import Agent, ChatOpenAI, Browser
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Windows
executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
user_data_dir='C:\\Users\\Farhan\\AppData\\Local\\Google\\Chrome\\User Data'
md_file_save_path='C:\\Users\\Farhan\\Desktop\\browse_data'


# Connect to your existing Chrome browser
browser = Browser(
    cdp_url="http://localhost:9222"  # Connect to the Chrome instance with debugging enabled
)



async def main():
#    llm = ChatOpenAI(model="gpt-4.1-mini")

    page = await browser.new_page('https://github.com')
    print("Page loaded")
    elements = page.get_element_by_prompt("Sign in button", llm)
    print("Elements found")
    print(elements)
#    agent = Agent(task=task, llm=llm, browser=browser)
#    result = await agent.run()
#    print(result)


if __name__ == "__main__":
    asyncio.run(main())