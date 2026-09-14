from dotenv import load_dotenv
import sys

from agent import agent 


load_dotenv()

thread_config = {
    "configurable": {
        "thread_id": "sql-agent-1"
    }
}


def main():
    print("SQL Question-Answering Agent shuru ho gaya hai. Band karne ke liye Ctrl+C dabayein.\n")

    while True:
        try:
            user_input = input("You: ")

            if not user_input:
                continue

            response = agent.invoke({
                "messages": [{"role": "user", "content": user_input }
                    ]
            },
            thread_config,
            )
            answer = response["messages"][-1].content
            print(f"AI: {answer}\n")

        except KeyboardInterrupt:
            print("\n\nChat band ho gayi. Thank you!")
            sys.exit(0)


if __name__ == "__main__":
    main()