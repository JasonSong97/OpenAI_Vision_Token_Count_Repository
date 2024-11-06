import tiktoken
import sys

sys.stdout.reconfigure(encoding='utf-8')

def num_tokens_from_string(string: str, encoding_name: str) -> int:
   """Returns the number of tokens in a text string."""
   encoding = tiktoken.get_encoding(encoding_name)
   num_tokens = len(encoding.encode(string))
   return num_tokens

def compare_encodings(example_string: str) -> None:
   """Prints a comparison of three string encodings."""
   # print the example string
   print(f'\nExample string: "{example_string}"')
   # for each encoding, print the # of tokens, the token integers, and the token bytes
   for encoding_name in ["r50k_base", "p50k_base", "cl100k_base", "o200k_base"]:
      encoding = tiktoken.get_encoding(encoding_name)
      token_integers = encoding.encode(example_string)
      num_tokens = len(token_integers)
      token_bytes = [encoding.decode_single_token_bytes(token) for token in token_integers]
      print()
      print(f"{encoding_name}: {num_tokens} tokens")
      print(f"token integers: {token_integers}")
      print(f"token bytes: {token_bytes}")

def num_tokens_from_messages(messages, model="gpt-4o-mini-2024-07-18"):
   """Return the number of tokens used by a list of messages."""
   try:
      encoding = tiktoken.encoding_for_model(model)
   except KeyError:
      print("Warning: model not found. Using o200k_base encoding.")
      encoding = tiktoken.get_encoding("o200k_base")
   if model in {
      "gpt-3.5-turbo-0125",
      "gpt-4-0314",
      "gpt-4-32k-0314",
      "gpt-4-0613",
      "gpt-4-32k-0613",
      "gpt-4o-mini-2024-07-18",
      "gpt-4o-2024-08-06"
      }:
      tokens_per_message = 3
      tokens_per_name = 1
   elif "gpt-3.5-turbo" in model:
      print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125.")
      return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0125")
   elif "gpt-4o-mini" in model:
      print("Warning: gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-mini-2024-07-18.")
      return num_tokens_from_messages(messages, model="gpt-4o-mini-2024-07-18")
   elif "gpt-4o" in model:
      print("Warning: gpt-4o and gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-2024-08-06.")
      return num_tokens_from_messages(messages, model="gpt-4o-2024-08-06")
   elif "gpt-4" in model:
      print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
      return num_tokens_from_messages(messages, model="gpt-4-0613")
   else:
      raise NotImplementedError(
         f"""num_tokens_from_messages() is not implemented for model {model}."""
      )
   num_tokens = 0
   for message in messages:
      num_tokens += tokens_per_message
      for key, value in message.items():
         num_tokens += len(encoding.encode(value))
         if key == "name":
               num_tokens += tokens_per_name
   num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
   return num_tokens

print(num_tokens_from_string("tiktoken is great!", "o200k_base"))
print(compare_encodings("antidisestablishmentarianism"))
print(compare_encodings("2 + 2 = 4"))
japanese = "お誕生日おめでとう".encode('utf-8', errors='ignore').decode('utf-8')
print(compare_encodings(japanese))
print()
print()


print('---------------------------------------------------------------------------------------------')
print('일반 텍스트 사용 시 토큰 개수---------------------------------------------------------------------------------------------')
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "토큰 넣으셈!!!!!!!!!!!!!!!!!!!!"))
example_messages = [
   { # 608
      "role": "system",
      "content": "You are specialized in analyzing Korean student writing documents using OCR data. \nYou critically evaluate student writing across various sections to provide constructive feedback.\nYour role is to provide(advise) useful feedback to help the student improve their writing.\nInformation is provided on three main sections.\n**1. Student Information:** 제목:[제목] 이름:[이름] 학년:[학년] 학교:[학교]\n**2. Logically inferred student's writing:**\n원문을 바탕으로 틀린 맞춤법을 수정하고 문맥상 이해하기 어려운 단어가 있는 경우에는 추론하여 적절한 단어로 바꾸어 글을 완성한다.\n**3. Evaluation Criteria:**\n학생의 글을 다음 5가지 영역에서 질문별로 객관적이고 구체적인 근거를 제시하여 분석한다.\n각 질문에 아쉬운 부분을 언급하고, 더 좋은 글을 위해 조언하며, 추천문장을 제안할 수 있다.\n학생의 특정 문장을 인용해서 객관성을 유지한다.\n\nFive Subsections:\n**Content Understanding**\n- To what extent has the student grasped the main ideas of the book?\n- How well does the student understand the relationships between key events and characters?\n- How convincing is the student’s interpretation of the book’s themes and messages?\n- Is the student’s summary of the book an appropriate length and focus?\n**Depth of Reflection**\n-How effectively does the review go beyond a simple summary to include personal insights?\n-How well has the student connected the book’s content with their own experiences?\n-To what extent is there evidence of empathy for the character’s actions and emotions?\n-How effectively has the review shown a deeper understanding of a particular theme or included a new perspective?\n\n**Logical Structure**\n-How clearly is the review organized with an introduction, body, and conclusion?\n-How effectively are appropriate transition words used between sentences to ensure a natural flow in the writing?\n-How smoothly are the transitions between paragraphs?\n-Are arguments and supporting details presented in a logical and coherent manner?\n\n**Creativity**\n-How original is the student’s perspective on the book?\n-How effectively has the student provided new interpretations or alternative viewpoints?\n-How unique are the expressions used, reflecting the student’s own voice?\n-How well does the student use metaphors, analogies, or other creative devices to enhance their interpretation? (5 points)\n\n**Words & Expression**\n반드시 반복되는 단어나 표현이 있는지 엄격하게 식별하고 언급합니다.\n-How clearly is the 주어 presented in each sentence?\n-모든 문장에서 주어와 서술어의 호응관계가 적절한 편입니까?\n-Is there a tendency for the same words or expressions to be frequently repeated in the student's writing?\n-How appropriate is the length of each sentence for clarity and readability?\n\n\nGuidance: \nHeading을 제외한 모든 결과를 한국어로 제공합니다."
   },
   {  # 610
      "role": "user",
      "content": "OCR: [<두부의 의미> 도서 : 막손이 두부 청원초등학교 5학년 최유찬 내용을 훑어보던 중 임진왜란 이후 포로로 잡혀간 사람들의 이야기인 것 같아 이 책을 골랐 다. 이 책에는 막손이라는 아이가 나온다. 막손이는 포로이긴 하지만 실은 뛰어난 다각형 인 재이다. 도자기의 기본인 흙을 느끼고 새로운 것을 배우는 속도 역시 빠르고 일본어도 능숙하 게 구사하기 때문이다. 그런데 막손이의 많은 능력 중 가장 배워야 한다고 생각이 드는 능력 은 끈기와 인내이다. 막손이에게는 힘든 일이 많았는데 어린 나이에 견디기 어려웠을 텐데도 끝까지 버틴 것이 대단하다. 특히 막손이가 신지에게 잡혀 노예가 되어 힘든 일을 하고 있을 대 큰 불평불만 없이 해내는 장면에서 막손이의 높은 끈기와 인내를 볼 수 있었다. 이렇게 꿋 꿋하고 강한 막손이가 한 번 크게 우는 장면이 나오는데, 조선의 맛이 나는 두부를 오랜만에 보았을 때다. 책의 제목에서 알 수 있듯이 막손이에게 두부란 단순한 음식이 아니다. 막손이 에게 두부란 삶의 의미이며, 고향을 향한 그리움이고, 서러움을 달래주는 위로이면서 조국에 대한 자긍심이다. 그래서 막손이는 일본에 조선의 두부를 전파하려 했다. 막손이가 제대로 된 두부를 만들려고 노력하는 모습은 마치 무형문화유산 분들이 자신의 재능을 완성하기까지 노 력한 장인정신과 비슷해 보엿다. 그리고 마손이가 일본 땅에서 조선의 두부를 지키기 위해 애 쓰는 모습은 일본에 굴복하지 않으려는 마음과 조선을 지키려는 간절한 투쟁으로 느껴졌다. 솔직히 나였다면 외국 땅에서 포로로 잡혀 갔을 때 조국의 문화를 지키지는 못했을 것 같다. 하지만 막손이의 이야기를 깊이 읽을수록 조국을 지키고 싶은 애국심이 나에게도 있다는 게 느껴졌다. 나도 막손이처럼 우리나라를 사랑하고 막손이가 보여준 끈기를 본받아 넘기 힘든 어려움이 와도 지지 않고 노력할 것이다. 막손이의 두부에서는 어떤 맛이 날까? 막손이의 두 부가 가르쳐준 참 맛, 참 의미를 기억하며 자라가고 싶다.]"
   },
]

for model in [
   "gpt-3.5-turbo",
   "gpt-4-0613",
   "gpt-4",
   "gpt-4o",
   "gpt-4o-mini"
   ]:
   print(model)
   # example token count from the function defined above
   print(f"{num_tokens_from_messages(example_messages, model)} prompt tokens counted by num_tokens_from_messages().")
   # example token count from the OpenAI API
   response = client.chat.completions.create(model=model,
   messages=example_messages,
   temperature=0,
   max_tokens=1)
   print(f'{response.usage.prompt_tokens} prompt tokens counted by the OpenAI API.')
   print()

print('---------------------------------------------------------------------------------------------')
print('메소드 사용시 토큰 개수---------------------------------------------------------------------------------------------')
def num_tokens_for_tools(functions, messages, model):
   # Initialize function settings to 0
   func_init = 0
   prop_init = 0
   prop_key = 0
   enum_init = 0
   enum_item = 0
   func_end = 0
   
   if model in [
      "gpt-4o",
      "gpt-4o-mini"
   ]:
      
      # Set function settings for the above models
      func_init = 7
      prop_init = 3
      prop_key = 3
      enum_init = -3
      enum_item = 3
      func_end = 12
   elif model in [
      "gpt-3.5-turbo",
      "gpt-4"
   ]:
      # Set function settings for the above models
      func_init = 10
      prop_init = 3
      prop_key = 3
      enum_init = -3
      enum_item = 3
      func_end = 12
   else:
      raise NotImplementedError(
         f"""num_tokens_for_tools() is not implemented for model {model}."""
      )
   
   try:
      encoding = tiktoken.encoding_for_model(model)
   except KeyError:
      print("Warning: model not found. Using o200k_base encoding.")
      encoding = tiktoken.get_encoding("o200k_base")
   
   func_token_count = 0
   if len(functions) > 0:
      for f in functions:
         func_token_count += func_init  # Add tokens for start of each function
         function = f["function"]
         f_name = function["name"]
         f_desc = function["description"]
         if f_desc.endswith("."):
               f_desc = f_desc[:-1]
         line = f_name + ":" + f_desc
         func_token_count += len(encoding.encode(line))  # Add tokens for set name and description
         if len(function["parameters"]["properties"]) > 0:
               func_token_count += prop_init  # Add tokens for start of each property
               for key in list(function["parameters"]["properties"].keys()):
                  func_token_count += prop_key  # Add tokens for each set property
                  p_name = key
                  p_type = function["parameters"]["properties"][key]["type"]
                  p_desc = function["parameters"]["properties"][key]["description"]
                  if "enum" in function["parameters"]["properties"][key].keys():
                     func_token_count += enum_init  # Add tokens if property has enum list
                     for item in function["parameters"]["properties"][key]["enum"]:
                           func_token_count += enum_item
                           func_token_count += len(encoding.encode(item))
                  if p_desc.endswith("."):
                     p_desc = p_desc[:-1]
                  line = f"{p_name}:{p_type}:{p_desc}"
                  func_token_count += len(encoding.encode(line))
      func_token_count += func_end
      
   messages_token_count = num_tokens_from_messages(messages, model)
   total_tokens = messages_token_count + func_token_count
   
   return total_tokens


tools = [{
   "type": "function",
   "function": {
      "name": "get_current_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
         "type": "object",
         "properties": {
            "location": {
               "type": "string",
               "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {
               "type": "string", 
               "description": "The unit of temperature to return",
               "enum": [
                  "celsius", 
                  "fahrenheit"
               ]
            },
         },
         "required": [
            "location"
         ],
      },
   }
}]

example_messages = [
   {
      "role": "system",
      "content": "You are a helpful assistant that can answer to questions about the weather.",
   },
   {
      "role": "user",
      "content": "What's the weather like in San Francisco?",
   },
]

for model in [
   "gpt-3.5-turbo",
   "gpt-4",
   "gpt-4o",
   "gpt-4o-mini"
   ]:
   print(model)
   # example token count from the function defined above
   print(f"{num_tokens_for_tools(tools, example_messages, model)} prompt tokens counted by num_tokens_for_tools().")
   # example token count from the OpenAI API
   response = client.chat.completions.create(
      model=model,
      messages=example_messages,
      tools=tools,
      temperature=0
   )
   print(f'{response.usage.prompt_tokens} prompt tokens counted by the OpenAI API.')
   print()

print('---------------------------------------------------------------------------------------------')
print('2가지 제한 사항 모두 반영 / 이미지 토큰 개수 구하는 공식---------------------------------------------------------------------------------------------')
from math import ceil

def adjust_image_size(width: int, height: int):
   # Step 1: 초기 크기가 2048을 초과하는 경우, 비율을 유지하며 조정
   if width > 2048 or height > 2048:
      aspect_ratio = width / height
      if width > height:
         width, height = 2048, int(2048 / aspect_ratio)
      else:
         width, height = int(2048 * aspect_ratio), 2048
   
   # Step 2: 최단 변이 768 이상인 경우, 다시 비율을 유지하며 크기를 조정
   if width >= height and height > 768:
      width, height = int((768 / height) * width), 768
   elif height > width and width > 768:
      width, height = 768, int((768 / width) * height)
   print('변환 후의 width, height', width, height)
   return width, height

def calculate_gpt4o_image_tokens(width: int, height: int, detail: str = "high"):
   # low 디테일일 경우 고정된 85 토큰 반환
   if detail == "low":
      return 85

   # high 디테일일 경우 크기 조정 및 타일 계산
   width, height = adjust_image_size(width, height)
   
   # 타일 수 계산
   tiles_width = ceil(width / 512)
   tiles_height = ceil(height / 512)
   
   # 토큰 개수 계산
   total_tokens = 85 + 170 * (tiles_width * tiles_height)
   
   return total_tokens

# 테스트 예시
width = 3024
height = 4032

# high 디테일 모드에서의 토큰 개수 계산
print("high 디테일 모드 - 이미지의 토큰 개수:", calculate_gpt4o_image_tokens(width, height, detail="high"))
# low 디테일 모드에서의 토큰 개수 계산
print("low 디테일 모드 - 이미지의 토큰 개수:", calculate_gpt4o_image_tokens(width, height, detail="low"))

print()
print()

print('---------------------------------------------------------------------------------------------')
print('가장 긴 변만 반영 / 이미지 토큰 개수 구하는 공식---------------------------------------------------------------------------------------------')
from math import ceil

def adjust_image_size(width: int, height: int):
   # Step 1: 가장 긴 변을 2048로 맞추고, 비율에 맞게 조정
   if width > height:
      if width > 2048:
         aspect_ratio = height / width
         width, height = 2048, int(2048 * aspect_ratio)
   else:
      if height > 2048:
         aspect_ratio = width / height
         width, height = int(2048 * aspect_ratio), 2048
   
   print('변환 후의 width, height', width, height)
   return width, height

def calculate_gpt4o_image_tokens(width: int, height: int, detail: str = "high"):
   # low 디테일일 경우 고정된 85 토큰 반환
   if detail == "low":
      return 85

   # high 디테일일 경우 크기 조정 및 타일 계산
   width, height = adjust_image_size(width, height)
   
   # 타일 수 계산
   tiles_width = ceil(width / 512)
   tiles_height = ceil(height / 512)
   
   # 토큰 개수 계산
   total_tokens = 85 + 170 * (tiles_width * tiles_height)
   
   return total_tokens

# 테스트 예시
width = 3024
height = 4032

# high 디테일 모드에서의 토큰 개수 계산
print("high 디테일 모드 - 이미지의 토큰 개수:", calculate_gpt4o_image_tokens(width, height, detail="high"))
# low 디테일 모드에서의 토큰 개수 계산
print("low 디테일 모드 - 이미지의 토큰 개수:", calculate_gpt4o_image_tokens(width, height, detail="low"))

print()
print()



print('---------------------------------------------------------------------------------------------')
print('이미지 토큰 개수 구하는 공식---------------------------------------------------------------------------------------------')
from math import ceil

def calculate_gpt4o_image_tokens(width: int, height: int, detail: str = "high"):
   # low 디테일일 경우 고정된 85 토큰 반환
   if detail == "low":
      return 85

   # high 디테일일 경우, 이미지 크기 조정 없이 타일 수 계산
   tiles_width = ceil(width / 512)
   tiles_height = ceil(height / 512)
   
   # 토큰 개수 계산
   total_tokens = 85 + 170 * (tiles_width * tiles_height)
   
   return total_tokens

# 테스트 예시
width = 3024
height = 4032

# high 디테일 모드에서의 토큰 개수 계산
print("high 디테일 모드 - 이미지의 토큰 개수:", calculate_gpt4o_image_tokens(width, height, detail="high"))
# low 디테일 모드에서의 토큰 개수 계산
print("low 디테일 모드 - 이미지의 토큰 개수:", calculate_gpt4o_image_tokens(width, height, detail="low"))