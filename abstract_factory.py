from abc import ABC, abstractmethod


# Singleton Pattern - Session Manager
class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.history = []
        return cls._instance

    def add_message(self, user: str, message: str):
        self.history.append((user, message))

    def get_history(self):
        return self.history

    def show_history(self):
        print("\nIstoricul conversației:")
        for user, message in self.history:
            print(f"{user}: {message}")

    def save_history_to_file(self, filename="chat_history.txt"):
        with open(filename, "w", encoding="utf-8") as file:
            for user, message in self.history:
                file.write(f"{user}: {message}\n")


# Adapter Pattern - Response Generator Interface
class ResponseGenerator(ABC):
    @abstractmethod
    def generate(self, user_input: str) -> str:
        pass


# Concrete Adapters for different response sources
class AIModelResponseGenerator(ResponseGenerator):
    def generate(self, user_input: str) -> str:
        return f"[AI Model] Generating response for: {user_input}"


class DatabaseResponseGenerator(ResponseGenerator):
    def generate(self, user_input: str) -> str:
        return f"[Database] Retrieved response for: {user_input}"


# Builder Pattern - Response Builder
class ResponseBuilder:
    def __init__(self):
        self._message = ""
        self._recommendation = ""
        self._follow_up = ""

    def set_message(self, message: str):
        self._message = message
        return self

    def set_recommendation(self, recommendation: str):
        self._recommendation = recommendation
        return self

    def set_follow_up(self, follow_up: str):
        self._follow_up = follow_up
        return self

    def build(self):
        return f"{self._message}\n{self._recommendation}\n{self._follow_up}".strip()


# Abstract Factory Pattern - Response System
class Response(ABC):
    def __init__(self, user_input: str, generator: ResponseGenerator):
        self.user_input = user_input
        self.generator = generator

    @abstractmethod
    def generate_message(self) -> str:
        pass


class CalmResponse(Response):
    def generate_message(self) -> str:
        return self.generator.generate(self.user_input)


class EmpathicResponse(Response):
    def generate_message(self) -> str:
        return self.generator.generate(self.user_input)


class LogicalResponse(Response):
    def generate_message(self) -> str:
        return self.generator.generate(self.user_input)


class ResponseFactory(ABC):
    @abstractmethod
    def create_response(self, user_text: str) -> Response:
        pass


class CalmResponseFactory(ResponseFactory):
    def create_response(self, user_text: str) -> Response:
        return CalmResponse(user_text, AIModelResponseGenerator())


class EmpathicResponseFactory(ResponseFactory):
    def create_response(self, user_text: str) -> Response:
        return EmpathicResponse(user_text, DatabaseResponseGenerator())


class LogicalResponseFactory(ResponseFactory):
    def create_response(self, user_text: str) -> Response:
        return LogicalResponse(user_text, AIModelResponseGenerator())


def get_response_factory(emotion: str) -> ResponseFactory:
    factories = {
        "anxious": CalmResponseFactory(),
        "sad": EmpathicResponseFactory(),
        "angry": LogicalResponseFactory()
    }
    return factories.get(emotion, CalmResponseFactory())


def detect_emotion(user_input: str) -> str:
    keywords = {
        "anxious": ["îngrijorat", "anxietate", "panică"],
        "sad": ["trist", "deprimat", "plâng"],
        "angry": ["furios", "nervos", "frustrat"]
    }
    for emotion, words in keywords.items():
        if any(word in user_input.lower() for word in words):
            return emotion
    return "anxious"


if __name__ == "__main__":
    session = SessionManager()
    while True:
        user_input = input("Tu: ")
        if user_input.lower() == "exit":
            print("Chatbot: O zi frumoasă! Ne revedem curând.")
            session.save_history_to_file()
            break

        session.add_message("User", user_input)
        user_emotion = detect_emotion(user_input)
        factory = get_response_factory(user_emotion)
        response = factory.create_response(user_input)

        response_text = response.generate_message()
        session.add_message("Bot", response_text)

        print(f"Chatbot: {response_text}")

    session.show_history()
