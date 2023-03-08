from QandA import QnAMatcher

matcher = QnAMatcher('sampleQA.csv')
user_input = input("Ask a question: ")
question, answer,similarity = matcher.find_similar_question(user_input)
print(question)  # prints "What's your name?"
print(answer)  # prints "My name is Chatbot"
print(similarity)
print(f"with a similarity score of {similarity:.2f}")
