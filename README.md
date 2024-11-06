# OpenAI Vision Token Count Repository

## 목적
- OpenAI Vision 사용 시, 각 gpt 버전 별 토큰 개수를 측정하는 레포지토리
- 토큰을 구분하는 방법 확인
- Vision 사용 시, 토큰 개수 구하는 공식 확인

## 결과

### 토큰 구분 방법
```
r50k_base: 5 tokens
token integers: [415, 29207, 44390, 3699, 1042]
token bytes: [b'ant', b'idis', b'establishment', b'arian', b'ism']

p50k_base: 5 tokens
token integers: [415, 29207, 44390, 3699, 1042]
token bytes: [b'ant', b'idis', b'establishment', b'arian', b'ism']

cl100k_base: 6 tokens
token integers: [519, 85342, 34500, 479, 8997, 2191]
token bytes: [b'ant', b'idis', b'establish', b'ment', b'arian', b'ism']

o200k_base: 6 tokens
token integers: [493, 129901, 376, 160388, 21203, 2367]
token bytes: [b'ant', b'idis', b'est', b'ablishment', b'arian', b'ism']
```

### 토큰 구분 예시 및 token_integers 배열 확인인
```
# 1
Example string: "antidisestablishmentarianism"

r50k_base: 5 tokens
token integers: [415, 29207, 44390, 3699, 1042]
token bytes: [b'ant', b'idis', b'establishment', b'arian', b'ism']

p50k_base: 5 tokens
token integers: [415, 29207, 44390, 3699, 1042]
token bytes: [b'ant', b'idis', b'establishment', b'arian', b'ism']

cl100k_base: 6 tokens
token integers: [519, 85342, 34500, 479, 8997, 2191]
token bytes: [b'ant', b'idis', b'establish', b'ment', b'arian', b'ism']

o200k_base: 6 tokens
token integers: [493, 129901, 376, 160388, 21203, 2367]
token bytes: [b'ant', b'idis', b'est', b'ablishment', b'arian', b'ism']


# 2
Example string: "2 + 2 = 4"
r50k_base: 5 tokens
token integers: [17, 1343, 362, 796, 604]
token bytes: [b'2', b' +', b' 2', b' =', b' 4']

p50k_base: 5 tokens
token integers: [17, 1343, 362, 796, 604]
token bytes: [b'2', b' +', b' 2', b' =', b' 4']

cl100k_base: 7 tokens
token integers: [17, 489, 220, 17, 284, 220, 19]
token bytes: [b'2', b' +', b' ', b'2', b' =', b' ', b'4']

o200k_base: 7 tokens
token integers: [17, 659, 220, 17, 314, 220, 19]
token bytes: [b'2', b' +', b' ', b'2', b' =', b' ', b'4']


# 3
Example string: "お誕生日おめでとう"

r50k_base: 14 tokens
token integers: [2515, 232, 45739, 243, 37955, 33768, 98, 2515, 232, 1792, 223, 30640, 30201, 29557]
token bytes: [b'\xe3\x81', b'\x8a', b'\xe8\xaa', b'\x95', b'\xe7\x94\x9f', b'\xe6\x97', b'\xa5', b'\xe3\x81', b'\x8a', b'\xe3\x82', b'\x81', b'\xe3\x81\xa7', b'\xe3\x81\xa8', b'\xe3\x81\x86']

p50k_base: 14 tokens
token integers: [2515, 232, 45739, 243, 37955, 33768, 98, 2515, 232, 1792, 223, 30640, 30201, 29557]
token bytes: [b'\xe3\x81', b'\x8a', b'\xe8\xaa', b'\x95', b'\xe7\x94\x9f', b'\xe6\x97', b'\xa5', b'\xe3\x81', b'\x8a', b'\xe3\x82', b'\x81', b'\xe3\x81\xa7', b'\xe3\x81\xa8', b'\xe3\x81\x86']

cl100k_base: 9 tokens
token integers: [33334, 45918, 243, 21990, 9080, 33334, 62004, 16556, 78699]
token bytes: [b'\xe3\x81\x8a', b'\xe8\xaa', b'\x95', b'\xe7\x94\x9f', b'\xe6\x97\xa5', b'\xe3\x81\x8a', b'\xe3\x82\x81', b'\xe3\x81\xa7', b'\xe3\x81\xa8\xe3\x81\x86']

o200k_base: 8 tokens
token integers: [8930, 9697, 243, 128225, 8930, 17693, 4344, 48669]
token bytes: [b'\xe3\x81\x8a', b'\xe8\xaa', b'\x95', b'\xe7\x94\x9f\xe6\x97\xa5', b'\xe3\x81\x8a', b'\xe3\x82\x81', b'\xe3\x81\xa7', b'\xe3\x81\xa8\xe3\x81\x86']
```

### 일반 텍스트 이용 시 gpt 버전 별 토큰 비교
```
일반 텍스트 사용 시 토큰 개수---------------------------------------------------------------------------------------------
gpt-3.5-turbo
Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125.
1770 prompt tokens counted by num_tokens_from_messages().
1770 prompt tokens counted by the OpenAI API.

gpt-4-0613
1770 prompt tokens counted by num_tokens_from_messages().
1770 prompt tokens counted by the OpenAI API.

gpt-4
Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.
1770 prompt tokens counted by num_tokens_from_messages().
1770 prompt tokens counted by the OpenAI API.

gpt-4o
Warning: gpt-4o and gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-2024-08-06.
1215 prompt tokens counted by num_tokens_from_messages().
1215 prompt tokens counted by the OpenAI API.

gpt-4o-mini
Warning: gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-mini-2024-07-18.
1215 prompt tokens counted by num_tokens_from_messages().
1215 prompt tokens counted by the OpenAI API.
```


### 메소드 이용 시 gpt 버전 별 토큰 비교
```
메소드 사용시 토큰 개수---------------------------------------------------------------------------------------------
gpt-3.5-turbo
Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125.
105 prompt tokens counted by num_tokens_for_tools().
105 prompt tokens counted by the OpenAI API.

gpt-4
Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.
105 prompt tokens counted by num_tokens_for_tools().
105 prompt tokens counted by the OpenAI API.

gpt-4o
Warning: gpt-4o and gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-2024-08-06.
101 prompt tokens counted by num_tokens_for_tools().
101 prompt tokens counted by the OpenAI API.

gpt-4o-mini
Warning: gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-mini-2024-07-18.
101 prompt tokens counted by num_tokens_for_tools().
101 prompt tokens counted by the OpenAI API.
```


### 2가지 제한사항 적용 결과
```
# 공식문서의 2가지 제한사항(width, height) 반영
2가지 제한 사항 모두 반영 / 이미지 토큰 개수 구하는 공식---------------------------------------------------------------------------------------------
변환 후의 width, height 768 1024
high 디테일 모드 - 이미지의 토큰 개수: 765
low 디테일 모드 - 이미지의 토큰 개수: 85

# 공식문서의 1가지 제한사한(가장 긴 변) 반영
가장 긴 변만 반영 / 이미지 토큰 개수 구하는 공식---------------------------------------------------------------------------------------------
변환 후의 width, height 1536 2048
high 디테일 모드 - 이미지의 토큰 개수: 2125
low 디테일 모드 - 이미지의 토큰 개수: 85

# 공식문서의 1가지 제한사한(가장 짧은 변) 반영
이미지 토큰 개수 구하는 공식---------------------------------------------------------------------------------------------
high 디테일 모드 - 이미지의 토큰 개수: 8245
low 디테일 모드 - 이미지의 토큰 개수: 85
```

## 공식문서
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [OpenAI Cookbook with tiktoken](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
