import re
from pynput import keyboard
from pynput.keyboard import Controller
import pyautogui
import openai
import time
import os
from colorama import init, Fore, Back, Style

start_keyword = 'gpt:'
end_keyword = ':gpt'
total_tokens_used = 0 # completion.usage.total_tokens
estimated_cost = total_tokens_used * 0.000002
buffer = ''
key_controller = None
chatgpt_model = None

def on_press(key):
    global buffer
    global total_tokens_used
    global estimated_cost

    

    if key == keyboard.Key.space:
        buffer += ' '
    elif key == keyboard.Key.backspace:
        if len(buffer): buffer = buffer[:-1]
    elif key == keyboard.Key.enter:
        buffer += '\n'
    else:
        try:
            buffer += key.char
        except Exception as e: #AttributeError
            pass
    
    match = re.search(f'{start_keyword}(.*?){end_keyword}', buffer, flags=re.DOTALL)


    if match and len(buffer) > (len(start_keyword) + len(end_keyword)) and start_keyword in buffer and end_keyword == buffer[-len(end_keyword):]:
        if match:
            text_to_convert = match.group(1)
            if not len(text_to_convert): return

            substring_start_index = buffer.find(start_keyword)
            substring_end_index = buffer.find(end_keyword, substring_start_index+1)
            substring_end_index += len(end_keyword) - 1
            total_characters_to_remove = substring_end_index - substring_start_index + 1
            for _ in range(total_characters_to_remove):
                key_controller.press(keyboard.Key.backspace)
                key_controller.release(keyboard.Key.backspace)

            temporary_text = "The response from chatGPT will be here shortly."
            pyautogui.write(temporary_text)
            buffer = ''

            try:
                completion = openai.ChatCompletion.create(
                model=chatgpt_model,
                messages=[
                    {"role": "user", "content": text_to_convert}
                ]
                )

                gpt_result = completion.choices[0].message.content
                total_tokens_used += completion.usage.total_tokens
                estimated_cost = total_tokens_used * 0.000002

                for _ in range(len(temporary_text)): #backspaces
                    key_controller.press(keyboard.Key.backspace)
                    key_controller.release(keyboard.Key.backspace)
                
                pyautogui.write(gpt_result)
                buffer = ''

                print(f'Total tokens used in the current session: {total_tokens_used}', end='\r')

            except Exception as e:
                pyautogui.write("\nSome exception occured, please check the terminal.")
                print(Fore.RED + e + Style.RESET_ALL)
                exit()
            buffer = ''

def main():

    global total_tokens_used
    global key_controller
    global chatgpt_model

    api_key = os.environ.get("API_KEY_OPENAI")
    chatgpt_model = os.environ.get("CHATGPT_MODEL")
    openai.api_key = api_key

    try:
        print("Connecting to openAI",end='\r')
        completion = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=[
            {"role": "user", "content": "Hi"}
        ]
        )
        total_tokens_used += completion.usage.total_tokens
        
    except Exception as e:
        print(Fore.RED + e + Style.RESET_ALL)
        exit()



    ascii_art = '''                                    ____ ____ _____ 
  _____  ___ __  _ __ ___  ___ ___ / ___|  _ \_   _|
 / _ \ \/ / '_ \| '__/ _ \/ __/ __| |  _| |_) || |  
|  __/>  <| |_) | | |  __/\__ \__ \ |_| |  __/ | |  
 \___/_/\_\ .__/|_|  \___||___/___/\____|_|    |_|  
          |_|                                       
'''



    print(Fore.GREEN + ascii_art + Style.RESET_ALL)
    print("by Digant Patel" + Fore.BLUE + "[http://digantpatel.com]" + Style.RESET_ALL)
    print("Close the terminal to exit the program")
    
    print(f"Type anything between {start_keyword} and {end_keyword} to get the chatGPT completion")

    
    key_controller = Controller()


    

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()