from abc import ABC, abstractmethod


# Step 1: Define the abstract product (Response)
class Response(ABC):
    def __init__(self, user_input: str):
        self.user_input = user_input  # Atributul 'user_input' al clasei

    @abstractmethod
    def generate_message(self) -> str:
        pass

# Step 2: Create concrete response classes for different emotions
class CalmResponse(Response):
    def generate_message(self) -> str:
        return "Respiră adânc. Totul va fi în regulă. Poți să îmi spui mai multe?"

class EmpathicResponse(Response):
    def generate_message(self) -> str:
        return "Îți înțeleg emoțiile. Sunt aici să te ascult. Cum te pot ajuta?"

class LogicalResponse(Response):
    def generate_message(self) -> str:
        return "Hai să analizăm împreună situația și să găsim o soluție logică."

# Step 3: Define the abstract factory
class ResponseFactory(ABC):
    @abstractmethod
    def create_response(self, input_text: str) -> Response:  # Renunțăm la 'user_text'
        pass

# Step 4: Implement concrete factories
class CalmResponseFactory(ResponseFactory):
    def create_response(self, input_text: str) -> Response:  # Renunțăm la 'user_text'
        return CalmResponse(input_text)  # Folosim 'input_text'

class EmpathicResponseFactory(ResponseFactory):
    def create_response(self, input_text: str) -> Response:  # Renunțăm la 'user_text'
        return EmpathicResponse(input_text)  # Folosim 'input_text'

class LogicalResponseFactory(ResponseFactory):
    def create_response(self, input_text: str) -> Response:  # Renunțăm la 'user_text'
        return LogicalResponse(input_text)  # Folosim 'input_text'

# Step 5: Factory Selector (chooses the appropriate factory based on user emotion)
def get_response_factory(emotion: str) -> ResponseFactory:
    factories = {
        "anxious": CalmResponseFactory(),
        "sad": EmpathicResponseFactory(),
        "angry": LogicalResponseFactory()
    }
    return factories.get(emotion, CalmResponseFactory())  # Default to calm response

# Step 6: Emotion Detection Function (Basic Simulation)
def detect_emotion(user_input: str) -> str:
    keywords = {
        "anxious": ["îngrijorat", "anxietate", "panică"],
        "sad": ["trist", "deprimat", "plâng"],
        "angry": ["furios", "nervos", "frustrat"]
    }
    for emotion, words in keywords.items():
        if any(word in user_input.lower() for word in words):
            return emotion
    return "anxious"  # Default emotion if nothing matches

# Example usage
if __name__ == "__main__":
    user_input = input("Cum te simți azi? ")
    user_emotion = detect_emotion(user_input)
    factory = get_response_factory(user_emotion)
    response = factory.create_response(user_input)
    print(response.generate_message())
