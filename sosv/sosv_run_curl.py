import subprocess
import json
import sys
import os
import time

def run_sosv_curl_command(to_thing_id):
    """Execute the SOSV curl command and return the response"""
    message = "Steph here- cofounder of WasteSync, an AI platform modernizing waste management. We automate compliance, emissions tracking & invoicing, helping haulers cut costs and streamline operations. Early traction-would love to connect and share more."
    # The curl command for SOSV matchmaking
    curl_command = [
        'curl',
        f'https://api-prod.grip.events/1/container/8836/thing/user_id/match_manual/yes/to_thing/{to_thing_id}',
        '-H', 'accept: application/json',
        '-H', 'accept-language: en-gb',
        '-H', 'cache-control: No-Cache',
        '-H', 'content-type: application/json',
        '-H', 'login-source: web',
        '-H', 'origin: https://matchmaking.grip.events',
        '-H', 'pragma: No-Cache',
        '-H', 'priority: u=1, i',
        '-H', 'referer: https://matchmaking.grip.events/ctm2025/app/home/network/list/114042?page=1&sort=name',
        '-H', 'sec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        '-H', 'sec-ch-ua-mobile: ?0',
        '-H', 'sec-ch-ua-platform: "Windows"',
        '-H', 'sec-fetch-dest: empty',
        '-H', 'sec-fetch-mode: cors',
        '-H', 'sec-fetch-site: same-site',
        '-H', 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        '-H', 'x-authorization: b27e4174-06b5-4682-b1f5-455fc9e2ac17',
        '-H', 'x-grip-version: Web/43.0.1',
        '--data-raw', f'{{"message":"{message}"}}'
    ]
    
    try:
        print("Executing SOSV curl command...")
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

def save_response_to_file(response, filename="sosv_response.json"):
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



def load_investors():
    """Load investors from the JSON file"""
    with open('sosv/investors3.json', 'r', encoding='utf-8') as file:
      people = json.load(file)
    return people




def get_investor_ids():
    """Extract investor IDs from the loaded data"""
    investors = load_investors()
    # print(investors)
    if not investors:
        return []
    
    investor_ids = []
    
    # Adjust this based on the actual structure of your investors.json file
    if 'data' in investors:
        for investor in investors['data']:
            investor_ids.append({
                "id": investor['id'],
                "name": investor['name'],
                "company": investor['company_name']
            })
    else:
        # If the structure is different, try to find investor data
        print("Warning: Unexpected JSON structure in investors.json")
        print("Available keys:", list(investors.keys()) if isinstance(investors, dict) else "Not a dictionary")
    
    return investor_ids

if __name__ == "__main__":
    # Option 2: Run with multiple investors (uncomment to use)
    print("\n" + "="*50)
    print("Processing multiple investors...")
    print("="*50)
    
    investor_ids = get_investor_ids()
    success_response = []
    if investor_ids:
        print(f"Found {len(investor_ids)} investors")
        
        for investor in investor_ids:  # Limit to first 5 for testing
            time.sleep(2)  # Add delay between requests
            print(f"\nSending message to {investor['name']} ({investor['company']}) - ID: {investor['id']}")
            response = run_sosv_curl_command(investor['id'])
            success_response.append({
                "name": investor['name'],
                "company": investor['company'],
                "id": investor['id'],
                "response": response
            })
            if response:
                print("✓ Success")
                
            else:
                print("✗ Failed")
        save_response_to_file(success_response, "sosv_success_response.json")
    else:
        print("No investors found to process")