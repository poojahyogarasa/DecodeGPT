from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from chatbot import generate_response

import os
import time

from database import (
    initialize_database,
    save_message,
    get_history
)

console = Console()

start_time = time.time()
message_count = 0

initialize_database()

console.print(
    Panel.fit(
        "[bold cyan]DecodeGPT v1.0[/bold cyan]\nAI Knowledge Assistant",
        title="Welcome"
    )
)

console.print(
    "[green]Type /exit to quit[/green]\n"
)

while True:

    user_input = input("You: ")

    # Exit
    if user_input.lower() in ["/exit", "exit"]:

        console.print(
            "\n[bold red]Goodbye![/bold red]"
        )

        break

    # Clear Screen
    if user_input.lower() == "/clear":

        os.system("cls")

        continue

    # Help Command
    if user_input.lower() == "/help":

        console.print("""
Commands
--------------------------------
/help     Show commands
/history  View chat history
/stats    View session statistics
/export   Export chat history
/clear    Clear screen
/exit     Exit DecodeGPT
""")

        continue

    # Stats Command
    if user_input.lower() == "/stats":

        duration = int(
            time.time() - start_time
        )

        console.print(f"""
Session Statistics
--------------------------------
Messages : {message_count}
Duration : {duration} sec
""")

        continue

    # History Command
    if user_input.lower() == "/history":

        history = get_history()

        if not history:

            console.print(
                "\n[yellow]No chat history found.[/yellow]\n"
            )

            continue

        console.print(
            "\n[bold cyan]Recent Chat History[/bold cyan]"
        )

        console.print(
            "--------------------------------"
        )

        for role, message in history:

            console.print(
                f"[green]{role}:[/green] {message[:100]}"
            )

        console.print()

        continue

    # Export Command
    if user_input.lower() == "/export":

        history = get_history()

        with open(
            "chat_export.txt",
            "w",
            encoding="utf-8"
        ) as f:

            for role, message in history:

                f.write(
                    f"{role}: {message}\n\n"
                )

        console.print(
            "[bold green]Chat exported successfully![/bold green]"
        )

        continue

    # Save User Message
    save_message(
        "user",
        user_input
    )

    message_count += 1

    # Generate AI Response
    response = generate_response(
        user_input
    )

    # Save Bot Response
    save_message(
        "assistant",
        response
    )

    # Display Response
    console.print(
        "\n[bold green]DecodeGPT[/bold green]"
    )

    console.print(
        Markdown(response)
    )

    console.print()