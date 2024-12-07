import json

def parse_score_response(response_text):
    start_index = response_text.find('[')
    end_index = response_text.find(']') + 1
    trimmed_text = response_text[start_index:end_index]
    print("score_response_text:")
    print(trimmed_text)

    char_list = list(trimmed_text)
    char_list.pop(0)
    char_list.pop(len(trimmed_text)-1)
    modified_response = "".join(char_list)

    print("modified_response:", modified_response)

    splittedScoreList = modified_response.split(",")
    print("splittedScoreList:")
    print(splittedScoreList)
    scoreList = []
    for element in splittedScoreList:
        convertedScore = int(element)
        scoreList.append(convertedScore)
    
    print("convertedScore:")
    print(convertedScore)
    print("----------------------------------")
    return scoreList

def parse_interview_response(response_text):
    start_index = response_text.find('[')
    end_index = response_text.find(']') + 1
    trimmed_text = response_text[start_index:end_index]
    print("interview_response_text:")
    print(trimmed_text)          

    response_list = trimmed_text.strip('[]').split('",\n    "')
    response_list = [item.strip(' "\n') for item in response_list]

    # Separate questions and answers
    questions = []
    ai_responses = []
    return questions, ai_responses

def extract_response_data(response_text):
    # Separate questions and answers
    questions = []
    ai_responses = []

    for item in data:
        if item.startswith("Q"):  # Check if it's a question
            questions.append(item)
        elif item.startswith("A"):  # Check if it's an answer
            ai_responses.append(item)

    # Output the results
    print("Questions:", questions)
    print("AI Responses:", ai_responses)

# Example response from Gemini
response_text = f"""
```{
  "Q1": "What is the difference between `==` and `.equals()` in Java?",
  "A1": "The `==` operator compares object references; it checks if two variables point to the same object in memory.  The `.equals()` method compares the content or value of the objects.  For Strings and many other classes, `.equals()` is overridden to compare the content, but for other objects, it defaults to reference equality (like `==`).",
  "Q2": "In Spring Boot, what is the purpose of the `@Controller` and `@RestController` annotations?",
  "A2": "`@Controller` is a general-purpose annotation for creating Spring MVC controllers that handle incoming web requests. `@RestController` is a specialized annotation that combines `@Controller` with `@ResponseBody`. This means that methods annotated with `@RestController` automatically return data directly in the HTTP response body (usually JSON or XML), typically used for RESTful APIs.",
  "Q3": "Explain the concept of dependency injection in Spring Boot and its benefits.",
  "A3": "Dependency Injection (DI) is a design pattern where dependencies are provided to a class from the outside rather than being created within the class itself.  Spring Boot uses DI extensively.  Benefits include improved code testability (easier to mock dependencies), loose coupling (components are less interdependent), and better maintainability and reusability.",
  "Q4": "What is a `@Service` annotation in Spring and when would you use it?",
  "A4": "The `@Service` annotation in Spring marks a class as a service component.  Services typically contain business logic that operates on data. It's a specialization of `@Component` that provides better clarity and organization. Use `@Service` to annotate classes that handle business logic separate from controllers and repositories; this enhances readability and maintainability."
}```"""
start_index = response_text.find('{')
end_index = response_text.rfind('}') + 1
json_str = response_text[start_index:end_index]


print(json_str)
parsedData = json.loads(json_str)
first_data = parse_interview_response(response_text)

print("----------------------------------")
print("------------JSON STR----------------")
print(first_data)

# Parse the JSON string into a Python list
parsed_list = json.loads(first_data)

# Verify the result
print("----------------------------------")
print("------------PARSED----------------")

print(parsed_list)  # This will print the extracted list

