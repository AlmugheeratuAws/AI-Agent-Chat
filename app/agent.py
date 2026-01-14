from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOllama
from app.tools import (
    find_books,
    create_order,
    order_status,
    restock_book,
    update_price,
    inventory_summary
)

llm = ChatOllama(
    model="llama3",
    temperature=0
)

tools = [
    Tool(
        name="find_books",
        func=find_books,
        description="Find books by title or author",
        return_direct=True
    ),
    Tool(
        name="create_order",
        func=create_order,
        description="Create an order given customer_id and items",
        return_direct=True
    ),
    Tool(
        name="restock_book",
        func=restock_book,
        description="Restock a book by ISBN",
        return_direct=True
    ),
    Tool(
        name="update_price",
        func=update_price,
        description="Update book price by ISBN",
        return_direct=True
    ),
    Tool(
        name="order_status",
        func=order_status,
        description="Get order status by ID",
        return_direct=True
    ),
    Tool(
        name="inventory_summary",
        func=inventory_summary,
        description="Get inventory summary",
        return_direct=True
    ),
]

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    max_iterations=5,
    early_stopping_method="force",
    agent_kwargs={
        "prefix": (
            "You are a Library Desk Agent.\n"
            "Use tools only when necessary.\n"
            "After receiving a tool result, answer clearly.\n"
            "Do not repeat tool calls.\n"
            "Stop after the final answer."
        )
    }
)
