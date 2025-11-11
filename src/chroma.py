#!/usr/bin/env python3
"""Demo script showcasing the simple vector store used by the chatbot."""

import argparse
from rich.console import Console
from rich.table import Table

from vector_store import SimpleVectorStore

console = Console()

CONVERSATION_DOCS = [
    "Sagar Naik: Hi @Gautam Kumar @Shilav Shinde, do we have backlog created for release dashboard. Is the KT done",
    "Shilav Shinde, Aug 7, 9:12 AM: Hi @Sagar Naik. Waiting for client laptop, not yet received. On last Monday, done the cisco secureIT password setup process.",
    "Gautam Kumar, Aug 7, 11:05 AM: Hi @Sagar Naik, I have given some brief about the project and codebase, as in what could be there, but proper KT hasn't started since Shilav hasn't received the laptop yet.",
    "Sagar Naik, Aug 7, 11:15 AM: What about the backlog, do we know the work and timeline",
    "Gautam Kumar, Aug 7, 11:19 AM: I don't have any jira tickets for the backlog, the timeline is still on the mail. You want me to create tickets for detail?",
    "Sagar Naik, Aug 7, 11:35 AM: Yes, please",
    "Gautam Kumar, Aug 7, 11:35 AM: Okay. I will create today.",
    "Gautam Kumar, Aug 7, 5:04 PM: Hi @Sagar Naik, I have created Jira tickets for the backlog: Search Functionality - PNC-55365, Package version enhancements - PNC-55366, JQL Query updates - PNC-55367 (Completed), Dev/QA Env - PNC-55368, R&D for Manual Updates & Backfilling - PNC-55369",
    "Sagar Naik, Sep 17, 7:36 PM: Hi @all. Please check if there is any 1.x or 3.x release today. I don't want to see any missing data of patch or hotfix",
    "Shilav Shinde, Sep 17, 7:56 PM: Hi @Sagar Naik. 3.0.50.036 patch is active on today, Dev cutoff job yet to be completed for this patch so I'll be keep monitoring",
    "Sagar Naik, Sep 18, 10:05 AM: I still don't see data on 34, what's the issue",
    "Sagar Naik, Sep 18, 10:11 AM: Also send me the link for version 3.0.50.035.001 @Gautam Kumar @Shilav Shinde",
    "Shilav Shinde, Sep 18, 10:33 AM: Hi @Sagar Naik. As we don't have changelog data for 34, that's why we are unable to see the changelog details.",
    "Sagar Naik, Sep 19, 12:25 PM: Hi @Shilav Shinde, can we have a session from you at 2.30 for release dashboard",
    "Shilav Shinde, Sep 19, 12:28 PM: Hi @Sagar Naik. Till now I got a brief idea about release dashboard, if you want a session I can give like whatever I have explore.",
    "Sagar Naik, Sep 19, 12:29 PM: Fine, just explain the functionality and future plans, not the whole code. Explain what challenges you have faced etc.",
    "Sagar Naik, Sep 23, 11:57 AM: Hi. Please send status of the release dashboard. Did we connect with Sarf",
    "Shilav Shinde, Sep 23, 12:11 PM: On September 16th, I messaged Sarf to provide the changelog details for the platform refresh in release 3.0.50.035.",
    "Shilav Shinde, Sep 23, 12:24 PM: The current active release is 3.0.50.036. This patch supposed to be promoted by today but it has been rescheduled.",
    "Shilav Shinde, Sep 23, 12:37 PM: No need to promote it to Sarf, the cron job promoted itself.",
    "Shilav Shinde, Sep 25, 9:34 AM: Added 'gateway' package for 3.0.50.035.002 manually from backend and created 3.0.50.035.003 hotfix.",
    "Shilav Shinde, Oct 1, 11:21 AM: Quick update on the database backup - port forwarding kept dropping the connection.",
    "Sagar Naik, Oct 24, 9:20 AM: Release 3.0.50.040 has started. Support for hyphenated version task: testing in progress.",
    "Shilav Shinde, Oct 24, 10:05 AM: Unable to test hyphenated version changes due to dev environment; validating workaround locally.",
    "Shilav Shinde, Oct 29, 10:47 AM: Release 3.0.50.041 has started. Release 040 has been promoted and change logs are available.",
]


def build_store() -> SimpleVectorStore:
    store = SimpleVectorStore()
    store.add_documents(CONVERSATION_DOCS)
    return store


def render_results(query: str, top_k: int) -> None:
    store = build_store()
    results = store.search(query, top_k=top_k)

    console.print(f"\n[bold cyan]Query:[/bold cyan] [yellow]{query}[/yellow]\n")
    if not results:
        console.print("[red]No results found[/red]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Rank", style="dim", width=6, justify="center")
    table.add_column("Score", width=8)
    table.add_column("Message", style="green")

    for idx, result in enumerate(results, start=1):
        table.add_row(str(idx), f"{result.score:.3f}", result.text)

    console.print(table)


def interactive_mode(top_k: int) -> None:
    store = build_store()
    console.print("[bold green]Interactive Mode - Release Dashboard Conversation Search[/bold green]")
    console.print("[dim]Enter queries to search the conversation. Type 'quit' to exit.[/dim]\n")

    while True:
        try:
            query = console.input("[bold cyan]Enter query:[/bold cyan] ").strip()
            if not query:
                continue
            if query.lower() in {"quit", "exit", "q"}:
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break

            results = store.search(query, top_k=top_k)
            if not results:
                console.print("[red]No results found[/red]\n")
                continue

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Rank", style="dim", width=6, justify="center")
            table.add_column("Score", width=8)
            table.add_column("Message", style="green")

            for idx, result in enumerate(results, start=1):
                table.add_row(str(idx), f"{result.score:.3f}", result.text)

            console.print(table)
            console.print()
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search the Release Dashboard conversation using the lightweight vector store",
    )
    parser.add_argument("-q", "--query", type=str, help="Query text to search for")
    parser.add_argument("-n", "--results", type=int, default=3, help="Number of results to return")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()

    if args.interactive or (not args.query):
        interactive_mode(args.results)
        return

    render_results(args.query, args.results)


if __name__ == "__main__":
    main()
