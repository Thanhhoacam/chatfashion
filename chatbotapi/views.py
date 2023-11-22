from rest_framework.decorators import api_view
from rest_framework.response import Response
import google.generativeai as palm

@api_view(['GET', 'POST'])
def chatbot(request):

        mess = ''
        color = request.data.get('color', '')
        current_conversation = request.data.get('content', '') 
        if color : # or request.POST.get('content', '')
            print("======================= Data in request:", color)
            
            mess = f'I have {color} skin tone. What are suitable clothes, styles, and colors for me? Please show them in the form of an ordered list for easy reading.'
        elif current_conversation : # or request.POST.get('content', '')
            print("======================= Data in request:", current_conversation)
            mess=current_conversation

        palm.configure(api_key='AIzaSyCeSGV9fTHFnBW35s6LUqpQs8b7O7j9Ldc')

            

        # Create a new conversation
        responsedata = palm.chat(context="Speak like an expert on fashion.", messages=mess)

        # current_conversation = f"user :${content} , bot:${responsedata.last},"
        # print(current_conversation)
        return Response(responsedata.last)
