import chromadb
import argparse
import sys
from rich.console import Console
from rich.table import Table

# Initialize ChromaDB client
chroma_client = chromadb.Client()

# Create collection for release dashboard conversation
collection = chroma_client.create_collection(name="release_dashboard_chat")

# Google Chat conversation data - Release Dashboard Project
conversation_documents = [
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
    "Shilav Shinde, Sep 18, 10:33 AM: Hi @Sagar Naik. As we don't have changelog data for 34, that's why we are unable to see the changelog details. Link: https://releasedashboard.cisco.com/change-log?selectedRelease=3.0.50.035.001&releaseName=3.0.50.035&releaseId=78&releaseType=Hotfix&version=3.0&category=3.0&startDate=9+Sep+2025&releaseDisplayName=3.0.50.035&parentReleaseName=Diamond&isCompletedRelease=false",
    "Sagar Naik, Sep 19, 12:25 PM: Hi @Shilav Shinde, can we have a session from you at 2.30 for release dashboard",
    "Shilav Shinde, Sep 19, 12:28 PM: Hi @Sagar Naik. Till now I got a brief idea about release dashboard, if you want a session I can give like whatever I have explore. But not much aware about all the factors/things of release dashboard.",
    "Sagar Naik, Sep 19, 12:29 PM: Fine, just explain the functionality and future plans, not the whole code. Explain what challenges you have faced etc. @Gautam Kumar can add more",
    "Shilav Shinde, Sep 19, 12:30 PM: Sure @Sagar Naik",
    "Gautam Kumar, Sep 19, 2:22 PM: Sure @Sagar Naik",
    "Sagar Naik, Sep 23, 11:57 AM: Hi. Please send status of the release dashboard. Did we connect with Sarf",
    "Shilav Shinde, Sep 23, 12:11 PM: Hi @Sagar Naik. On September 16th, I messaged Sarf to provide the changelog details for the platform refresh in release 3.0.50.035. He provided the scrubber and based on that, added the changelog details for the platform refresh in release 035.",
    "Sagar Naik, Sep 23, 12:13 PM: Any other release right now",
    "Shilav Shinde, Sep 23, 12:24 PM: The current active release is 3.0.50.036. This patch supposed to be promoted by today but it has been rescheduled, so it will be promoted on Thursday (25th September). I will be monitoring",
    "Sagar Naik, Sep 23, 12:24 PM: Sarf will promote it right, you should not do it, he should",
    "Shilav Shinde, Sep 23, 12:37 PM: No need to promote it to Sarf, the cron job promoted itself.",
    "Shilav Shinde, Sep 23, 1:52 PM: Hi @Sagar Naik. I reached out to Karthik for a DB setup meeting, but we haven't been able to connect yet. I followed up with him again today and am waiting for his response, as there is a dependency on him.",
    "Sagar Naik, Sep 23, 1:54 PM: Ping him on the group with Naresh on cc",
    "Sagar Naik, Sep 24, 7:39 PM: Please send me the status. Also send mail to Manjunadh @Shilav Shinde",
    "Shilav Shinde, Sep 24, 7:55 PM: Hi @Sagar Naik. I have already shared weekly status update mail to Manjunadh.",
    "Shilav Shinde, Sep 24, 8:00 PM: PNC-55366: We are not supporting the hyphenated version that's why in the add package functionality we have restricted hyphenated version, I'm working on it. As an immediate solution, we can add the package details from backend because of restriction for hyphenated version.",
    "Sagar Naik, Sep 24, 10:34 PM: Patch 34 does not have data. Can you clarify @Shilav Shinde. Link: https://releasedashboard.cisco.com/change-log?selectedRelease=3.0.50.034&releaseName=3.0.50.X&releaseId=58&releaseType=Patch&version=3.0&category=3.0&startDate=27+Nov+2024&releaseDisplayName=3.0.50.X&parentReleaseName=Diamond&isCompletedRelease=false&templateName=Confidence+template",
    "Shilav Shinde, Sep 24, 10:37 PM: As we don't have changelog data for patch 34",
    "Sagar Naik, Sep 24, 10:38 PM: What about 3.0.50.35.3",
    "Shilav Shinde, Sep 24, 10:41 PM: Checking on it..will let you know in sometime",
    "Sagar Naik, Sep 24, 10:50 PM: Ok",
    "Sagar Naik, Sep 24, 10:53 PM: Also check dates",
    "Shilav Shinde, Sep 24, 10:53 PM: Okay, sure",
    "Shilav Shinde, Sep 25, 9:34 AM: Hi @Sagar Naik. Added 'gateway' package for 3.0.50.035.002 manually from backend and created 3.0.50.035.003 hotfix. Also modified the date for 002 and 003 both. As we don't have data in releasechangelogs collection for 002 and 003, that's why both showing current patch in release dashboard. Also checked for release 036, showing 25th Sep 2025 as pd promotion date, it supposed to be extend by 30 Sep.",
    "Shilav Shinde, Oct 1, 11:21 AM: Hi @Sagar Naik. Quick update on the database backup - We have tried to back up the database using the mongo command with port forwarding to access the database. However, the OpenShift (OC) connection was disconnected during the process, which caused the backup operation to fail. We also implemented logic to retry the connection and resume the backup from where it stopped, but OC continued to deny the connection.",
    "Sagar Naik, Oct 8, 1:18 PM: Hi. Any update on db backup and other things",
    "Shilav Shinde, Oct 8, 1:19 PM: Hi",
    "Shilav Shinde, Oct 8, 1:25 PM: It's in progress. I'll provide you with a detailed update on the db_backup by evening. Still working on it.",
    "Sagar Naik, Oct 8, 1:40 PM: Ok",
    "Shilav Shinde, Oct 23, 9:19 AM: Hi @Sagar Naik. Health Check for Collections and status of release dashboard - Release 3.0.50.040 has started. As of now its in PD promotion stage, there is no data available since we don't have data in releasechangelogs collection. PD and PnC Tags - No tags data in pdpnctags collection for 040, Earlier received tags data for 039 release. Metrics Job Last Run (tenants) = '2025-10-01T05:30:00Z' (base_url: https://miggbo.atlassian.net/, jira_type:'cloud'). Releasechangelogs - No release change logs data available for 040. Earlier have releasechangelog data for 039. Tags - release/0.10.532, rc/0.10.533 fetched tags of core-platform package on 22-10-2025. cc: @Gautam Kumar",
    "Sagar Naik, Oct 24, 9:20 AM: Release 3.0.50.040 has started. As of now its in PD promotion stage, there is no data available since we don't have data in releasechangelogs collection. Support for hyphenated version task (PNC-55366): Done code changes, testing is in progress. DB backup mechanism and test environment (PNC-57488): awaiting a VM, accessible from the CAE console, from Karthikeyan to proceed with testing the workaround. No progress on backup and hyphenated version since 2 weeks?",
    "Shilav Shinde, Oct 24, 10:05 AM: Hi @Sagar Naik. We were unable to test the code changes of Hyphenated version due to dev environment. A VM is pending provision to proceed with testing the database backup activity. In the meantime, I implemented a workaround to test the code changes with the local database and am now validating those changes.",
    "Sagar Naik, Oct 24, 10:07 AM: Get it merged after validation. It should not affect the dashboard",
    "Shilav Shinde, Oct 24, 10:10 AM: Sure @Sagar Naik",
    "Shilav Shinde, Oct 29, 10:47 AM: Hi @Sagar Naik. Health Check for Collections and status of release dashboard - Release 3.0.50.041 has started. As of now its in PD promotion stage. Release 3.0.50.040 has been promoted, and the release change logs data is also available. PD and PnC Tags, Tags, Releasechangelogs, tenants collection data are up to date. cc: @Gautam Kumar",
]

# Add conversation documents to collection
document_ids = [f"msg_{i+1}" for i in range(len(conversation_documents))]
collection.add(
    ids=document_ids,
    documents=conversation_documents
)

print(f"\n✅ Added {len(conversation_documents)} conversation messages to ChromaDB collection\n")

# Initialize Rich console for formatted output
console = Console()


def process_query(query: str, n_results: int = 5):
    """Process a single query and display results"""
    console.print(f"\n[bold cyan]Query:[/bold cyan] [yellow]{query}[/yellow]")
    console.print("[dim]─" * 60 + "[/dim]")
    
    # Query the collection
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    # Extract and display only the document texts
    if results and 'documents' in results and results['documents']:
        documents = results['documents'][0]  # Get documents for first query
        
        # Display results in a structured format
        table = Table(show_header=True, header_style="bold magenta", width=100)
        table.add_column("Rank", style="dim", width=6, justify="center")
        table.add_column("Found Message", style="green", width=94, overflow="fold")
        
        for idx, doc in enumerate(documents, 1):
            table.add_row(str(idx), doc)
        
        console.print(table)
    else:
        console.print("[red]No results found[/red]")
    
    console.print()  # Empty line after results


def main():
    """Main function to handle command line arguments and interactive mode"""
    parser = argparse.ArgumentParser(
        description="Semantic search for Release Dashboard conversation using ChromaDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chroma.py --query "backlog jira tickets"
  python chroma.py --query "release 3.0.50.040" --results 5
  python chroma.py --interactive
  python chroma.py -q "database backup" -n 3
  python chroma.py -q "patch 34 changelog"
        """
    )
    parser.add_argument(
        '-q', '--query',
        type=str,
        help='Query text to search for'
    )
    parser.add_argument(
        '-n', '--results',
        type=int,
        default=3,
        help='Number of results to return (default: 3)'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode (enter queries one by one)'
    )
    
    args = parser.parse_args()
    
    # If query provided, process it and exit
    if args.query:
        process_query(args.query, args.results)
        return
    
    # If interactive mode, loop for queries
    if args.interactive or (not args.query and sys.stdin.isatty()):
        console.print("[bold green]Interactive Mode - Release Dashboard Conversation Search[/bold green]")
        console.print("[dim]Enter queries to search the conversation. Type 'quit' or 'exit' to stop.[/dim]\n")
        
        while True:
            try:
                query = console.input("[bold cyan]Enter query:[/bold cyan] ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ['quit', 'exit', 'q']:
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break
                
                process_query(query, args.results)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break
            except EOFError:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break
    else:
        # No arguments provided and not in interactive terminal
        parser.print_help()


if __name__ == "__main__":
    main()
