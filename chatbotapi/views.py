from rest_framework.decorators import api_view
from rest_framework.response import Response
import google.generativeai as palm
from collections import defaultdict
import math
import json


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def search_and_extract_info(item):
    driver = webdriver.Chrome()  # Đảm bảo bạn đã cài đặt ChromeDriver
    driver.get("https://www.amazon.com/")

    search_query = item['top']
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.ENTER)

    time.sleep(5)  # Đợi trang tải và kết quả tìm kiếm hiện ra
    # print("Trang sau khi tìm kiếm: ", driver.page_source)
    product_info = []
    products = driver.find_elements(By.CSS_SELECTOR, 'div.a-section.a-spacing-base')
    # print(products)
    for product in products[2:3]:
        # product_html = product.get_attribute('outerHTML')
        # print("code prodduct============",product_html)
        # Tìm và trích xuất thông tin từ mỗi sản phẩm
        img = product.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        product_name = product.find_element(By.CSS_SELECTOR, 'span.a-size-base-plus').text
        price = product.find_element(By.CSS_SELECTOR, 'span.a-price').text

        product_info.append({
            'image_url': img,
            'name': product_name,
            'price': price
        })

    driver.quit()
    return product_info


       
        
        
def hex_to_rgb(hex_color):
            # Loại bỏ ký tự "#" nếu có
            hex_color = hex_color.lstrip("#")

            # Chuyển mã HEX thành RGB
            rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    
            return rgb
        # Function to get the closest color name for a given RGB color
def get_closest_color_name(rgb_color):
            min_distance = float('inf')
            closest_color_name = ""

            for color, name in color_names.items():
                distance = get_color_distance(rgb_color, color)
                if distance < min_distance:
                    min_distance = distance
                    closest_color_name = name

            return closest_color_name    
        # Function to calculate the Euclidean distance between two RGB colors
def get_color_distance(color1, color2):
            r1, g1, b1 = color1
            r2, g2, b2 = color2
            return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)
        
        
color_names = defaultdict(str)

color_names[(255, 224, 189)] = "Light Skin"
color_names[(205, 174, 136)] = "Medium Light Skin"
color_names[(156, 126, 93)] = "Medium Skin"
color_names[(107, 78, 49)] = "Medium Dark Skin"
color_names[(59, 32, 9)] = "Dark Skin"

# Warm Fair: #eed0be
warm_fair_color = (237, 207, 188)
color_names[warm_fair_color] = "Warm Fair"

# Warm Light: #ede9e7
warm_light_color = (210, 187, 131)
color_names[warm_light_color] = "Warm Light"

# Warm Medium: #5a3211
warm_medium_color = (161, 111, 78)
color_names[warm_medium_color] = "Warm Medium"

# Warm Dark: #ede9e7
warm_dark_color = (90, 51, 12)
color_names[warm_dark_color] = "Warm Dark"

# Neutral Fair: #edeae4
neutral_fair_color = (236, 199, 188)
color_names[neutral_fair_color] = "Neutral Fair"

# Neutral Light: #edeae4
neutral_light_color = (208, 174, 133)
color_names[neutral_light_color] = "Neutral Light"

# Neutral Medium: #e6ddd7
neutral_medium_color = (158, 97, 79)
color_names[neutral_medium_color] = "Neutral Medium"

# Neutral Dark: #edeae4
neutral_dark_color = (88, 34, 13)
color_names[neutral_dark_color] = "Neutral Dark"

# Cool Fair: #edeae4
cool_fair_color = (224, 199, 198)
color_names[cool_fair_color] = "Cool Fair"

# Cool Light: #edeae4
cool_light_color = (193, 173, 146)
color_names[cool_light_color] = "Cool Light"

# Cool Medium: #edeae4
cool_medium_color = (144, 97, 92)
color_names[cool_medium_color] = "Cool Medium"

# Cool Dark: #edeae4
cool_dark_color = (70, 34, 31)
color_names[cool_dark_color] = "Cool Dark"

def generate_clothing_suggestions(res, palm, prompt):
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    print(model)

    

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=800,
    )
    print(completion.result)
    json_string = completion.result
    if json_string is not None:
        
        print(json_string)
        json_string = json_string.replace("```json", "").strip()
        json_string = json_string.replace("```", "").strip()
    else:
        json_string = {"nothing":"nothing is nothing"}

    

    json_data = json.loads(json_string)
    json_data["response"] = res
    # Pretty-print the JSON data
    print(json_data)
    print("print successfully")
    return json_data

@api_view(['GET', 'POST'])
def chatbot(request):
    if request.method == 'GET':
        return Response({"message": "Hello, please give me color skin hex code"})

    if request.method == 'POST':
        
        
        input_hex_color = request.data.get('color', '')
        
        current_conversation = request.data.get('content', '')
        
        mbti = request.data.get('mbti', '')

        
        # Initialize the Palm chatbot (replace 'your_api_key' with your actual API key)
        palm.configure(api_key='AIzaSyCeSGV9fTHFnBW35s6LUqpQs8b7O7j9Ldc')
        
        if mbti and input_hex_color:
            input_rgb_color = hex_to_rgb(input_hex_color)
            color_name = get_closest_color_name(input_rgb_color)
            print("======================= Data in request:", mbti, color_name)
            prompt = """
            I have """ + mbti + """ MBTI and """+color_name+""" skin tone. What are suitable clothes(property (skin_color, mbti_number) ,type(5) ,styles(5), colors(5) and 5 exmaple of mix, reason, personality) for me?
            Return in json format without space, "json".
            """
            mess="""I have """ + mbti + """ MBTI and """+color_name+ """skin tone. What are short and useful advices about clothes in order number."""
            
            responsedata = palm.chat(context="Speak like an expert on fashion", messages=[mess])
           
            res = responsedata.last.replace("\n", " ").strip()
            json_data = generate_clothing_suggestions(res,palm, prompt)
            return Response(json_data)


        if input_hex_color:
            input_rgb_color = hex_to_rgb(input_hex_color)
            color_name = get_closest_color_name(input_rgb_color)
            print("======================= Data in request:", input_hex_color,input_rgb_color,color_name)
            # mess = f'Return json format .I have {color_name} skin tone. What are suitable clothes( styles, and colors) for me?'
            # # Create a new conversation
            # responsedata = palm.chat(context="Speak like an expert on fashion and IT", messages=[mess])
            prompt = """
            I have """ + color_name + """ skin tone. What are suitable clothes(property ,type(5) ,styles(5), colors(5) and 5 exmaple of mix, reason, personality) for me?
            Return in json format without space, "json".
            """
            mess="I have " + color_name + " skin tone. What are short and useful advices about clothes in order number."
            
            responsedata = palm.chat(context="Speak like an expert on fashion", messages=[mess])
            res = responsedata.last.replace("\n", " ").strip()
            
            json_data = generate_clothing_suggestions(res,palm, prompt)
            
            

          
            
            
            
        if mbti:
            print("======================= Data in request:", mbti)
            prompt = """
            I have """ + mbti + """. What are suitable clothes(property (personality),type(5) ,styles(5), colors(5) and 5 exmaple of mix, reason, personality) for me?
            Return in json format without space, "json".
            """
            mess="I have " + mbti + ". What are short and useful advices about clothes in order number."
            
            responsedata = palm.chat(context="Speak like an expert on fashion", messages=[mess])
           
            res = responsedata.last.replace("\n", " ").strip()
            json_data = generate_clothing_suggestions(res,palm, prompt)
        
        


        elif current_conversation:
            print("======================= Data in request:", current_conversation)
            prompt = """
            I have """ + current_conversation + """. What are suitable clothes(property ,type ,styles, colors and 5 exmaple of mix, reason, personality) for me?
            Return in json format without space, "json".
            """
            mess="I have " + current_conversation + ". What are short and useful advices about clothes in order number."
            # Create a new conversation
            
            
            responsedata = palm.chat(context="Speak like an expert on fashion", messages=[mess])
           
            res = responsedata.last.replace("\n", " ").strip()
            json_data = generate_clothing_suggestions(res,palm, prompt)

        
        mix_data = json_data["mix"]

        for item in mix_data:
        # Gọi hàm search_and_extract_info và lưu kết quả vào item
            dataai = search_and_extract_info(item)
            print("====================",dataai)
            item['product'] = dataai
        
        return Response(json_data)
