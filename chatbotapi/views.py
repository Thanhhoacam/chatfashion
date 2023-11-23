from rest_framework.decorators import api_view
from rest_framework.response import Response
import google.generativeai as palm
from collections import defaultdict
import math


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



@api_view(['GET', 'POST'])
def chatbot(request):
    if request.method == 'GET':
        return Response({"message": "Hello, please give me color skin hex code"})

    if request.method == 'POST':
        
        
        input_hex_color = request.data.get('color', '')
        
        current_conversation = request.data.get('content', '')
        choice = request.data.get('choice', '')
        conversation="There is no one-size-fits-all answer to this question, as the best clothes for you will depend on your individual style and preferences. However, there are some general tips that can help you choose clothes that flatter your skin tone and personality.\n\nIf you have a warm skin tone, you should look for clothes in warm colors like red, orange, yellow, and gold. These colors will make your skin look radiant and healthy. You should also avoid cool colors like blue, green, and purple, as these colors can make your skin look dull.\n\nIf you have a cool skin tone, you should look for clothes in cool colors like blue, green, and purple. These colors will make your skin look vibrant and healthy. You should avoid warm colors like red, orange, yellow, and gold, as these colors can make your skin look flushed.\n\nOnce you have chosen colors that flatter your skin tone, you can start to think about style. If you are a classic type, you will want to choose clothes that are timeless and elegant. Look for pieces that are well-made and will last for years. If you are a dramatic type, you will want to choose clothes that are bold and eye-catching. Look for pieces with interesting details and patterns. If you are a natural type, you will want to choose clothes that are comfortable and relaxed. Look for pieces made from natural fibers like cotton and linen. If you are a thinker type, you will want to choose clothes that are functional and practical. Look for pieces that are easy to care for and won't wrinkle easily. If you are a feeler type, you will want to choose clothes that make you feel good. Look for pieces that are soft and comfortable to wear.\n\nNo matter what your personality type, there are a few general rules of thumb that you can follow when choosing clothes. First, make sure that the clothes fit you well. Clothes that are too tight or too loose will make you look uncomfortable and sloppy. Second, choose clothes that are appropriate for the occasion. You wouldn't want to wear a cocktail dress to a job interview, for example. Third, don't be afraid to experiment with different styles and colors. The best way to find out what looks good on you is to try different things.\n\nWith a little bit of effort, you can find clothes that flatter your skin tone, personality, and style. So don't be afraid to experiment and have fun with fashion!"

        # Initialize the Palm chatbot (replace 'your_api_key' with your actual API key)
        palm.configure(api_key='AIzaSyCeSGV9fTHFnBW35s6LUqpQs8b7O7j9Ldc')
        mess='hi'
        responsedata=palm.chat(context="Speak like an expert on fashion", messages=[mess])
        if input_hex_color:
            input_rgb_color = hex_to_rgb(input_hex_color)
            color_name = get_closest_color_name(input_rgb_color)
            print("======================= Data in request:", input_hex_color,input_rgb_color,color_name)
            mess = f'I have {color_name} skin tone. What are suitable clothes( styles, and colors) for me? return follow json object'
            # Create a new conversation
            responsedata = palm.chat(context="Speak like an expert on fashion", messages=[mess])
        if choice!='no':
            print("======================= Data in request:", choice)
            mess = f'{conversation} and {choice} is my MBTI,base on MBTI and skin tone, What are suitable clothes( styles, and colors) '
            # Create a new conversation
            responsedata = palm.chat(context="Speak like an expert on fashion", messages=[mess])
        elif current_conversation:
            print("======================= Data in request:", current_conversation)
            mess = current_conversation
            # Create a new conversation
            responsedata = responsedata.reply(mess)
        

        # Get the bot's response
        bot_response = responsedata.last

        # You can add additional logic or processing here if needed

        # Return the bot's response
        return Response(bot_response)
