import os
import contextlib

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()


class Chatbot:

    def __init__(self, personality="Happy"):

        self.personality = personality
        self.messages = []

        self.model = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            max_tokens=None,
            timeout=60,
            max_retries=2,
        )

    def set_personality(self, personality):

        self.personality = personality

    def personality_prompt(self):

        modes = {

            "Happy": """
You are ZERO, a friendly and cheerful AI assistant.
Be warm, positive and helpful.
Answer the user's question directly.
Do not add unnecessary introductions, disclaimers,
extra commentary, metadata, or technical information.
""",

            "Sad": """
You are ZERO, a calm and comforting AI assistant.
Use a gentle and supportive tone.
Answer the user's question directly.
Do not add unnecessary introductions, disclaimers,
extra commentary, metadata, or technical information.
""",

            "Angry": """
You are ZERO, a direct and confident AI assistant.
Use a firm but respectful tone.
Answer the user's question clearly.
Never insult the user.
Do not add unnecessary introductions, disclaimers,
extra commentary, metadata, or technical information.
""",

            "Professional": """
You are ZERO, a professional AI assistant.
Give clear, accurate and well-structured answers.
Use a professional tone.
Do not add unnecessary introductions, disclaimers,
extra commentary, metadata, or technical information.
""",

            "Funny": """
You are ZERO, a friendly AI assistant.
You may use light humor when appropriate.
Always answer the user's question clearly.
Do not add unnecessary introductions, disclaimers,
extra commentary, metadata, or technical information.
"""
        }

        return modes.get(
            self.personality,
            modes["Happy"]
        )

    def clean_response(self, content):

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, str):
                    text_parts.append(item)

                elif isinstance(item, dict):

                    if item.get("type") == "text":
                        text_parts.append(
                            item.get("text", "")
                        )

            return "".join(text_parts).strip()

        return str(content).strip()

    def ask(self, user_prompt):

        system_message = HumanMessage(
            content=self.personality_prompt()
        )

        conversation = [system_message]

        conversation.extend(self.messages)

        conversation.append(
            HumanMessage(
                content=user_prompt
            )
        )

        try:

            # Hide unwanted Google SDK output
            with open(os.devnull, "w") as devnull:

                with contextlib.redirect_stderr(devnull):

                    response = self.model.invoke(
                        conversation
                    )

            answer = self.clean_response(
                response.content
            )

            # Save conversation
            self.messages.append(
                HumanMessage(
                    content=user_prompt
                )
            )

            self.messages.append(
                AIMessage(
                    content=answer
                )
            )

            return answer

        except Exception as e:

            return f"Sorry, I couldn't process that request. {str(e)}"

    def clear_chat(self):

        self.messages = []