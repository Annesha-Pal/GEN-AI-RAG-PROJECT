from src.generation import answer_question


question = input("Ask a question about your document: ")

answer = answer_question(question)

print("\nAnswer:")
print(answer)