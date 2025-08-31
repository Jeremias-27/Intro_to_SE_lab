from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_protect
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    try:
        data = json.loads(request.body.decode("utf-8"))
        user_message = data.get("message", "").strip()
        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)
        
        system_prompt = """
                        You are an AI assistant for SE Lab Store.
                        The site sells products organized in categories.
                        Products include electronics, books, and gadgets.
                        Answer questions as if you are helping a customer navigate the site.
                        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=
                [ {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}],
        )
        reply = response.choices[0].message.content
        return JsonResponse({"reply": reply})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)