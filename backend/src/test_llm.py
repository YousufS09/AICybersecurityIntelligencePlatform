from backend.src.llm_explainer import chatbot_reply


if __name__ == "__main__":
    response = chatbot_reply(
        user_message="What should I do next?",
        prediction="phishing",
        confidence=0.99,
        risk_level="High",
    )

    print("Chatbot Test Response")
    print("---------------------")
    print(response)
