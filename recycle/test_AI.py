from groq import Groq

# API KEY của bạn
client = Groq(api_key="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")

# Prompt cố định để chatbot luôn trả lời như giáo viên
system_prompt = """
Bạn là giáo viên toán THPT tại Việt Nam.
Nhiệm vụ của bạn:
- Giải thích bài toán từng bước
- Trả lời hoàn toàn bằng tiếng Việt
- Dùng ngôn ngữ dễ hiểu cho học sinh
- Nếu học sinh sai hãy giải thích lỗi
"""

def ask_ai(question):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content


# chạy thử chatbot
while True:

    user_input = input("Học sinh: ")

    if user_input.lower() == "exit":
        break

    answer = ask_ai(user_input)

    print("\nGiáo viên AI:\n")
    print(answer)
    print("\n-------------------------\n")