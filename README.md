#Google Chat Alert Framework

## Description
This project provides a Python-based framework that enables sending alerts to Google Chat using webhook URLs. The project comprises of multiple components working in tandem:

* main.py - The main script that initializes all modules and starts threads for different scripts.
* log_handler.py - A script responsible for handling logging throughout the project.
* send_to_google_chat.py - A script with a function for sending messages to Google Chat.

### Features
Unified logging mechanism
Multi-threading support
Configuration via config.ini file
Log rotation with compression using

### Dependencies
* Python 3.x
* requests library for HTTP requests
* configparser for handling configuration files

### Setup and Installation
1. Clone the Repository
   
   ` git clone https://github.com/irnutsmurt/gchat-alert-framework.git `

2. Navigate to Project Folder
   
   ` cd gchat-alert-framework `

3. Install Dependencies
   
   ` pip install -r requirements.txt `

4. Setup Configurations
* Edit config.ini to add your specific configurations for each script. The loop time for each script can be configured here.

5. Run the Main Script
   
   ` python main.py `

## Usage

### Sending a Google Chat Alert
You can use the `send_to_google_chat` function from `send_to_google_chat.py` in your scripts to send messages.

```
from send_to_google_chat import send_to_google_chat

def send_to_google_chat(message, webhook_url):
    logger.info('Sending message to Google Chat')
    response = requests.post(webhook_url, json={"text": message})
    if response.status_code != 200:
        logger.error(f'Webhook error with status code {response.status_code}')
    else:
        logger.info('Message sent successfully')
```
### Adding New Scripts

1. Import the script in main.py.
```
from your_new_script import your_function
```
2. Add a new thread in `main.py` similar to `example1_thread` and include it in the __main__ section.
3. Update `config.ini` to add new configurations if needed.

### How to Format Messages for Google Chat

There is a lot of ways to configure messages for Google Chat that is outlined in the [Google Documentation](https://developers.google.com/chat/format-messages), but for this example we'll use a simple text formatting as its the least complex.

This example function formats a series of messages that can be sent to Google Chat in a readable manner. The function goes through a list of issues and formats each issue as a message. Each message will contain details like the issue's title, when it was first detected, the related MITRE ATT&CK technique, and remediation steps. Here's how it works:

```
def format_for_gchat():
    logger.info('Formatting messages for Google Chat')
    messages = []
    for issue in issues:
        message = (
            f"*Title:* {issue['title']},\n"
            f"*first_detected:* {issue['first_detected']},\n"
            f"*mitre_attack_technique_name:* {issue['mitre_attack_technique_name']},\n"
            f"*remediation_steps:* {issue['remediation_steps']}\n"
        )
        messages.append(message)
    return "\n".join(messages)   
```

1. Initialize an empty list messages: This will store each formatted message.
2. Iterate through issues: For each issue, the function generates a formatted message.
    * The function assumes issues is a list of dictionaries, each containing fields like 'title', 'first_detected', 'mitre_attack_technique_name', and 'remediation_steps'.
3. Create message string: This string contains the relevant issue details in a Google Chat-friendly format.
4. Append to messages: Each formatted message is appended to the list.
5. Join and Return: Finally, all the messages in the list are joined into a single string separated by newlines and returned.

```
def send_to_google_chat(message, webhook_url):  # webhook_url added as parameter
    logger.info(f"Sending message to Google Chat: {message}")  # Log message
    payload = {
        "text": message
    }
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            logger.info("Successfully sent message to Google Chat")
        else:
            logger.warning(f"Failed to send message to Google Chat. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while sending message to Google Chat: {e}")
```
6. This example function will take the message generated in the previous function and the webhook we defined and send it to the sent_to_google_chat.py script. It needs formatted text and webhook url as it does not contain its own
7. Accept message and webhook_url as parameters: This allows you to send different messages to different Google Chat webhooks.
8. Create Payload: A dictionary named payload is created, where text is set to the message.
9. Send HTTP POST Request: Using the requests.post() method, the message is sent to the Google Chat API via the given webhook URL.
10. Handle Response: The function checks the HTTP status code to determine if the message was successfully sent. If it fails, a warning is logged.

## Using config.ini for Script Configuration
One of the essential aspects of the framework is its use of a config.ini file for holding various settings. This file is particularly useful for storing variables like API keys, webhook URLs, and loop times for each script that's a part of the framework. The main.py script reads these configurations to execute each script appropriately.

Here's a brief rundown:

1. Structure of config.ini: The config.ini is divided into sections, one for each script (example1, example2, example3). Each section contains key-value pairs for the api_key, webhook_url, and loop_time_seconds.
```
[example1]
api_key = 
webhook_url = 
loop_time_seconds = 86400

[example2]
api_key = 
webhook_url = 
loop_time_seconds = 60

[example3]
api_key = 
webhook_url = 
loop_time_seconds = 300
```

2. Initialize ConfigParser: The main.py script uses Python's ConfigParser class to read this config.ini file.
```
config = ConfigParser()
config.read('config.ini')
```

3. Retrieve Settings: For each script, main.py retrieves the loop time, as specified in config.ini.
```
example1_loop_time = int(config['example1']['loop_time_seconds'])
example2_loop_time = int(config['example2']['loop_time_seconds'])
example3_loop_time = int(config['example3']['loop_time_seconds'])
```
4. Usage in Threads: The retrieved loop_time_seconds is then used in the respective threads to set the interval at which each script's function (run_example1, run_example2, run_example3) should be run.
```
time.sleep(example1_loop_time)
```

This way, the config.ini serves as a centralized configuration file that allows you to easily manage and tune the behavior of all the individual scripts from one place.

