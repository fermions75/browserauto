import subprocess
import json
import sys
import os
import time
from user_data_process import process_user_data

def run_curl_command(personId):
    """Execute the curl command and return the response"""
    # personId = "RXZlbnRQZW9wbGVfNDEzNzY0NzQ="
    # The curl command (Windows format with ^ for line continuation)
    curl_command = [
        'curl',
        'https://app.money2020middleeast.com/api/graphql',
        '-H', 'accept: */*',
        '-H', 'accept-language: en-US,en;q=0.9',
        '-H', 'accept-charset: utf-8',
        '-H', 'authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3JlQXBpVXNlcklkIjoiVlhObGNsOHlOVGd5TnpZM09RPT0iLCJwZXJtaXNzaW9ucyI6WyJhcHBsaWNhdGlvbjpRWEJ3YkdsallYUnBiMjVmTVRZNE1RPT0iLCJzY2hlbWE6dXNlciJdLCJzZXNzaW9uSWQiOiI2OGQwZTBhNjM5OTEyMDk5N2QzMWY1ZTYiLCJ0eXBlIjoiYWNjZXNzLXRva2VuIiwidXNlcklkIjoiNjhjOWJkMmRkNmU3YThlZGFiNjJjYjBlIiwiZW1haWxWZXJpZmllZCI6dHJ1ZSwiaWF0IjoxNzU4NjkzNDYyLCJleHAiOjE3NTg3Nzk4NjIsImlzcyI6ImF1dGgtYXBpIn0.FdAKvVvH6cObGXuQmsg7w64Mq-0tnYlATXuUwvKXBppLbn7XbtSj4xbfiTAXJs_JM3-OQ25Q4pI8eVH9VDvhdwdA_CEScehr_jbRdPKfeKE9JdqDrUBenpkoPrE78g8fqn3U7nfTDDNKbAWMtCr6CwzeP6fi6SQgVkho4kd_bXF9hdtyPsXcCX6ra8FbqMJ3xItEl8qcgXgSs60dW__bHiI2AUojWMygjUyf0J9yRUdtnUpcFFZ_sTEk8qhHrpgi-KOH2N0oTbtkfPT2HKOUrHirshJJmIzVHijehE5wb8Uamhe9ucBLhwsyCiksESwJmlwgCMMrYLhc9C8RsxZL9qc0rmR8USU1vkjwWyxppWg-DLBWnJ_JoS1uAf-r0y9eomCHyBsE7FzI2wgpQG_ae_7cV7dAjDzQsAarCO6BAWsI27qTRNG_WIpzKKK0FqmHq6-5waOJov8cgssqQDQhuBvLrr9U5-pfAi1YcWPgJiEw21DqwSTdkF0TOqxgylLal4Odq_XtSylkL80Fk1erSXkNhWKZdaY3v5-v__ZPLyUlNcaF4RUijNn_rXrLByRKYgOvjPdA-fQKAv-VZW15m_vZYAnVLUolOOElU7gPbP6x8DexNCOIEunFa6NW8iYnUCYAD4ZHLvno9pQNvkrz9bCFjRhpno1NjC9Fhys5e0g',
        '-H', 'content-type: application/json',
        '-H', 'origin: https://app.money2020middleeast.com',
        '-H', 'priority: u=1, i',
        '-H', 'referer: https://app.money2020middleeast.com/',
        '-H', 'sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        '-H', 'sec-ch-ua-mobile: ?0',
        '-H', 'sec-ch-ua-platform: "Windows"',
        '-H', 'sec-fetch-dest: empty',
        '-H', 'sec-fetch-mode: cors',
        '-H', 'sec-fetch-site: same-origin',
        '-H', 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        '-H', 'x-client-origin: app.money2020middleeast.com',
        '-H', 'x-client-platform: Event App',
        '-H', 'x-client-version: 2.309.308',
        '-H', 'x-feature-flags: fixBackwardPaginationOrder',
        '-b', 'intercom-id-ineyz1by=03700be4-4162-4ae4-a898-f65676a74481; intercom-device-id-ineyz1by=78fd452c-bf40-42de-96f1-30e0d7eb2137; swapcard-cookie-consent={"accepted":true}; _ga=GA1.1.2102613950.1758343792; swapcard-auth-api-refresh-token=eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSWQiOiI2OGQwZTBhNjM5OTEyMDk5N2QzMWY1ZTYiLCJ0eXBlIjoicmVmcmVzaC10b2tlbiIsInVzZXJJZCI6IjY4YzliZDJkZDZlN2E4ZWRhYjYyY2IwZSIsImlhdCI6MTc1ODUxOTQ2MiwiaXNzIjoiYXV0aC1hcGkifQ.pBSlQA7wsRG6i3lietYkrQsjp4AJW3dfZPvrJybxLI_leOlCJUMuiCvJnhbaC0VZ6CH-vs1ugABMCf-3_pU0EXbIeffpUfNxDPsyyOYBx3gC-DXCNFlRHdusnaEcqs7Ilh-YAttlTnGLWDj12L8o2nMdz8J2k2pjxjhcoz6qN2HmyA3pF3Ooz6hu_ZfStOFqGofXWMZQJO9hpdt6xNfBg4-36UdoCSGof44xgNCVhS38JEd-cy30ZWqEKdN9JrSsicn7iXb-3xrw0r4A0FKPuuvYV42x1_dNP38t9kPqvckVSEbITEcQJJ-fLPsT4ozIgX2nGBKZrW92qlrt4oS9rWg5lb31Umo52lSqMEGW2ewEorhO92J9cTV1HTiIh5AuMT4-A5rfB78vv4bIKIdz8_QsnZqq5Lw9E8-Fn-tg5vOaTAu1-miJrnIIrrlZqIJ0AP8JSwtnCGwliwav4yd0uSY4ukHLNSlqpR5kaGvg_17iNGRj1lXurLS-e9Eg-ZEnJm-XwblMbKt_PPPJ2yVA43I38GbVTsTmphDLRU8bnbN5HqmO3TA2ENmdu-oCUQ6jXux41gZ8B1gNYKzo9P6d3IWQypyDr5xqM8-BAXZ1TS19XlVJQcdbzuuWvH8gf6IRSmX9Ztft--MmKiRbVI7cdGft9ueIYKvwiyJ1bQVxaHM; next-i18next=en-US; intercom-session-ineyz1by=ajUrTEFMcUtqcEgrbWdLU2RMdEpkMjlUOGZFb3N0OVRXODJlRWtBbHJtQ1gyNjBTYzJUZGxQRVBYbFFHd1lJR2RsU05SSURIR21waVE0Rmx3MEVzQlFWVkJTZUVDR2lBUzBYanQrVXRQVUE9LS1ReUZTWnJIMHJJbXpFZzdCeXZUNGZ3PT0=--051e32717333dddb9c819790ef7283fb16c90bf7; _ga_VWQ0TSBSYY=GS2.1.s1758693158$o13$g1$t1758693462$j60$l0$h0',
        '--data-raw', f'[{{"operationName":"EventPersonDetailsQuery","variables":{{"skipMeetings":true,"withEvent":true,"withHostedBuyerView":false,"personId":"{personId}","userId":"","eventId":"RXZlbnRfMjU3MTMzMA==","viewId":""}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"9c3dfb71349712f915cd47344f9163171b189babbdf179bbbaf3a7bf7e15b4ac"}}}}}},{{"operationName":"PersonUserId","variables":{{"personId":"{personId}"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"109137c30f77f624ffa4263a20e90a0a4fc9e9e7ddade6a7a5039a935b69e1b0"}}}}}},{{"operationName":"SingleCommunityQuery","variables":{{}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"0fbbcdbf8bde4a9b8986bb9982f3d875d0ffb56f8e742c28ec9e958cc2729f8c"}}}}}},{{"operationName":"CurrentEventPersonProviderQuery","variables":{{"eventId":"RXZlbnRfMjU3MTMzMA=="}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"dd75ad419aef13cd3cc94c3115b8323f05ea5b0bab929b74a953f455a2c873dd"}}}}}},{{"operationName":"ApplicationProvider_CurrentCommunity","variables":{{"communitySlug":"money-2020"}},"extensions":{{"persistedQuery":{{"version":1,"sha256Hash":"1d630032bb7429fef5056900473d82b31f00d49569654de2234017d4c0002bec"}}}}}}]'
    ]
    
    try:
        print("Executing curl command...")
        print("Command:", ' '.join(curl_command[:5]) + " ... (truncated)")
        
        # Execute the curl command
        result = subprocess.run(
            curl_command,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        
        # Print the return code
        print(f"Return code: {result.returncode}")
        
        if result.returncode == 0:
            print("Curl command executed successfully!")
            
            # Try to parse the response as JSON
            try:
                response_json = json.loads(result.stdout)
                print("Response JSON:")
                print(json.dumps(response_json, indent=2))
                return response_json
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print("Raw response:")
                print(result.stdout)
                return result.stdout
        else:
            print(f"Curl command failed with return code: {result.returncode}")
            print("Error output:")
            print(result.stderr)
            return None
            
    except subprocess.TimeoutExpired:
        print("Curl command timed out after 30 seconds")
        return None
    except FileNotFoundError:
        print("Error: curl command not found. Make sure curl is installed and in your PATH")
        return None
    except Exception as e:
        print(f"Error executing curl command: {e}")
        return None

def save_response_to_file(response, filename="response.json"):
    """Save the response to a file with UTF-8 encoding"""
    try:
        if isinstance(response, (dict, list)):
            # JSON data - save as formatted JSON with UTF-8 encoding
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(response, f, indent=2, ensure_ascii=False)
        else:
            # String data - save as text with UTF-8 encoding
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(response))
        print(f"Response saved to {filename}")
    except Exception as e:
        print(f"Error saving response to file: {e}")


def load_people():
   with open('people2.json', 'r', encoding='utf-8') as file:
      people = json.load(file)
   return people

def get_user_ids():
    people = load_people()
    user_ids = []

    for person in people['data']['view']['people']['nodes']:
        user_ids.append({"id" : person['id'], "name" : f"{person['firstName']} {person['lastName']}"})
    return user_ids





if __name__ == "__main__":
    user_ids = get_user_ids()
    processed_user_data_list = []

    print(user_ids)

    for user in user_ids:
        time.sleep(2)
        # Execute the curl command
        print(f"Getting data from the user - {user['id']} - {user['name']}")
        response = run_curl_command(user['id'])
    
        if response:
            print("\n" + "="*50)
            print("SUCCESS: Got response from curl command")
            print("="*50)
            
            processed_user_data = process_user_data(response[0], user['id'])
            processed_user_data_list.append(processed_user_data)
        else:
            print("\n" + "="*50)
            print("FAILED: Could not get response from curl command")
            print("="*50)

    print(processed_user_data_list)
    save_response_to_file(processed_user_data_list, "processed_user_data3.json")