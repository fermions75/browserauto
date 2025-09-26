def get_task(link, message):

    task = f'''
        TASK: Networking Automation for Money20/20 Middle East Event
        STEP 1: Navigate to the given url - {link}
        STEP 2: Wait for 2 seconds for the page to fully load
        STEP 3: Do not scroll down and click on the Connect button. It is visible in the screen.
        STEP 4: Write the message {message} in the text box
        STEP 5: Click on the Send connection request button
    '''
    return task

def get_linkedin_task(link, message):
    task = f'''
        TASK: Send a connection request to the given LinkedIn profile
        STEP 1: Navigate to the given url - {link}
        STEP 2: Wait for 2 seconds for the page to fully load
        STEP 3: If the connect button is visible, click on it. Else click on the more button and then click on the connect button.
        STEP 4: Send a connection request to the profile with the given message {message}. Dont forget to click on the Send button after writing the message.
    '''
    return task