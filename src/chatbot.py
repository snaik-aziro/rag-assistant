#!/usr/bin/env python3
"""
Local LLM Chatbot with RAG - Terminal-based chatbot using Ollama with a lightweight vector store for context retrieval
"""

import os
import sys
import json
import time
import subprocess
from typing import List, Dict, Optional
import requests
from colorama import init
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from vector_store import SimpleVectorStore

# Initialize colorama and rich console
init(autoreset=True)
console = Console()

class LocalChatbot:
    """A terminal-based chatbot using local Ollama models with RAG (Retrieval-Augmented Generation)"""

    def __init__(self, model_name: str = "llama2", ollama_host: str = "http://localhost:11434", use_rag: bool = True):
        self.model_name = model_name
        self.ollama_host = ollama_host
        self.use_rag = use_rag
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history_length = 10  # Keep last 10 exchanges
        
        # Initialize vector store for RAG
        self.vector_store: Optional[SimpleVectorStore] = None
        if self.use_rag:
            self._initialize_vectordb()

    def check_ollama_running(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=3)
            return response.status_code == 200
        except (requests.RequestException, requests.Timeout):
            return False

    def start_ollama_service(self) -> bool:
        """Attempt to start Ollama service"""
        console.print("[yellow]Attempting to start Ollama service...[/yellow]")

        try:
            # Try to start Ollama service
            subprocess.Popen(["ollama", "serve"],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)
            # Wait a bit for service to start
            time.sleep(3)
            return self.check_ollama_running()
        except FileNotFoundError:
            console.print("[red]Error: Ollama is not installed on this system.[/red]")
            console.print("[yellow]Please install Ollama from https://ollama.ai/[/yellow]")
            return False
        except Exception as e:
            console.print(f"[red]Error starting Ollama service: {e}[/red]")
            return False

    def check_and_pull_model(self) -> bool:
        """Check if model exists, pull it if not"""
        try:
            # Check available models
            response = requests.get(f"{self.ollama_host}/api/tags")
            available_models = [model['name'] for model in response.json().get('models', [])]

            if self.model_name not in available_models:
                console.print(f"[yellow]Model '{self.model_name}' not found. Pulling...[/yellow]")

                # Show progress with spinner
                with console.status(f"[bold green]Pulling {self.model_name} model...") as status:
                    try:
                        subprocess.run(["ollama", "pull", self.model_name],
                                     check=True,
                                     capture_output=True,
                                     text=True)
                        console.print(f"[green]✓ Successfully pulled {self.model_name}[/green]")
                        return True
                    except subprocess.CalledProcessError as e:
                        console.print(f"[red]Error pulling model: {e.stderr}[/red]")
                        return False
            else:
                console.print(f"[green]✓ Model '{self.model_name}' is available[/green]")
                return True

        except requests.RequestException as e:
            console.print(f"[red]Error checking models: {e}[/red]")
            return False

    def _initialize_vectordb(self) -> None:
        """Initialize the lightweight vector store with conversation data."""
        try:
            store = SimpleVectorStore()
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
            store.add_documents(conversation_documents)
            self.vector_store = store
            console.print(f"[green]✓ Initialized vector store with {len(conversation_documents)} conversation messages[/green]")
        except Exception as exc:
            console.print(f"[yellow]Warning: Could not initialize vector store: {exc}[/yellow]")
            console.print("[yellow]RAG will be disabled. Continuing without vector database...[/yellow]")
            self.use_rag = False
            self.vector_store = None

    def retrieve_context(self, query: str, n_results: int = 3) -> str:
        """Retrieve relevant context from vector store vector database"""
        if not self.use_rag or not self.chroma_collection:
            return ""
        
        try:
            results = self.chroma_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if results and 'documents' in results and results['documents']:
                documents = results['documents'][0]
                context = "\n".join([f"- {doc}" for doc in documents])
                return f"\n\nRelevant context from conversation:\n{context}\n"
            else:
                return ""
        except Exception as e:
            console.print(f"[yellow]Warning: Error retrieving context: {e}[/yellow]")
            return ""

    def generate_response(self, user_message: str) -> Optional[str]:
        """Generate response from the model with RAG context"""
        try:
            # Retrieve relevant context from vector database if RAG is enabled
            context = ""
            if self.use_rag:
                context = self.retrieve_context(user_message, n_results=3)
            
            # Prepare the user message with context
            enhanced_message = user_message
            if context:
                enhanced_message = f"""Based on the following context from previous conversations, answer the user's question. If the context doesn't contain relevant information, answer based on your general knowledge.

{context}

User question: {user_message}

Please provide a helpful answer based on the context above."""
            
            # Prepare the prompt with conversation history
            messages = self.conversation_history.copy()
            messages.append({"role": "user", "content": enhanced_message})

            # Make request to Ollama API
            payload = {
                "model": self.model_name,
                "messages": messages,
                "stream": False
            }

            response = requests.post(
                f"{self.ollama_host}/api/chat",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                ai_response = result.get('message', {}).get('content', '')

                # Add to conversation history
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": ai_response})

                # Trim history if too long
                if len(self.conversation_history) > self.max_history_length * 2:
                    self.conversation_history = self.conversation_history[-self.max_history_length * 2:]

                return ai_response
            else:
                console.print(f"[red]Error: HTTP {response.status_code} - {response.text}[/red]")
                return None

        except requests.RequestException as e:
            console.print(f"[red]Network error: {e}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            return None

    def display_welcome(self):
        """Display welcome message and instructions"""
        welcome_text = Text("🤖 Local LLM Chatbot with RAG", style="bold blue")
        subtitle = Text("Powered by Ollama + Local Vector Store - Running completely offline", style="dim cyan")
        rag_status = "[green]✓ RAG Enabled[/green]" if self.use_rag else "[yellow]⚠ RAG Disabled[/yellow]"

        panel = Panel.fit(
            f"{welcome_text}\n{subtitle}\n\n"
            f"RAG Status: {rag_status}\n"
            "The chatbot uses a lightweight vector store to retrieve relevant context from previous conversations.\n\n"
            "Commands:\n"
            "• Type your message and press Enter to chat\n"
            "• Type '/clear' to clear conversation history\n"
            "• Type '/model <name>' to switch models\n"
            "• Type '/quit' or '/exit' to exit\n\n"
            f"Current model: {self.model_name}",
            title="Welcome",
            border_style="blue"
        )

        console.print(panel)

    def run(self):
        """Main chat loop"""
        try:
            console.clear()

            # Check Ollama service
            console.print("[yellow]Checking Ollama service...[/yellow]")
            if not self.check_ollama_running():
                console.print("[yellow]Ollama service not running. Attempting to start...[/yellow]")
                if not self.start_ollama_service():
                    console.print("\n[red]❌ Failed to start Ollama service.[/red]")
                    console.print("[yellow]Please start Ollama manually by running: ollama serve[/yellow]")
                    console.print("[yellow]Or install Ollama from: https://ollama.ai/[/yellow]")
                    return

            # Check and pull model
            console.print("[yellow]Checking model availability...[/yellow]")
            if not self.check_and_pull_model():
                console.print("\n[red]❌ Failed to load model. Please check your Ollama installation.[/red]")
                console.print(f"[yellow]Try running: ollama pull {self.model_name}[/yellow]")
                return

            # Display welcome message
            self.display_welcome()

            # Main chat loop
            while True:
                try:
                    # Get user input
                    user_input = console.input("\n[bold cyan]You:[/bold cyan] ").strip()

                    if not user_input:
                        continue

                    # Handle commands
                    if user_input.lower() in ['/quit', '/exit']:
                        console.print("[yellow]Goodbye! 👋[/yellow]")
                        break

                    elif user_input.lower() == '/clear':
                        self.conversation_history = []
                        console.print("[green]✓ Conversation history cleared[/green]")
                        continue

                    elif user_input.lower().startswith('/model '):
                        new_model = user_input[7:].strip()
                        if new_model:
                            self.model_name = new_model
                            console.print(f"[green]✓ Switched to model: {self.model_name}[/green]")
                            if not self.check_and_pull_model():
                                console.print("[red]Warning: Model may not be available[/red]")
                        else:
                            console.print("[red]Please specify a model name[/red]")
                        continue

                    # Generate response
                    with console.status("[bold green]Thinking...[/bold green]") as status:
                        response = self.generate_response(user_input)

                    if response:
                        # Display AI response
                        response_panel = Panel.fit(
                            response,
                            title=f"🤖 {self.model_name}",
                            border_style="green"
                        )
                        console.print(response_panel)
                    else:
                        console.print("[red]Failed to generate response. Please try again.[/red]")

                except KeyboardInterrupt:
                    console.print("\n[yellow]Interrupted by user. Goodbye! 👋[/yellow]")
                    break
                except EOFError:
                    console.print("\n[yellow]Goodbye! 👋[/yellow]")
                    break
                except Exception as e:
                    console.print(f"[red]An error occurred: {e}[/red]")
        except Exception as e:
            console.print(f"[red]Fatal error: {e}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Local LLM Chatbot with RAG using Ollama and a local vector store",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chatbot.py
  python chatbot.py --model mistral
  python chatbot.py --no-rag
  python chatbot.py --model llama2 --host http://localhost:11434
        """
    )
    parser.add_argument("--model", default="llama2",
                       help="Model name to use (default: llama2)")
    parser.add_argument("--host", default="http://localhost:11434",
                       help="Ollama host URL (default: http://localhost:11434)")
    parser.add_argument("--no-rag", action="store_true",
                       help="Disable RAG (Retrieval-Augmented Generation)")

    args = parser.parse_args()

    # Create and run chatbot
    use_rag = not args.no_rag
    chatbot = LocalChatbot(model_name=args.model, ollama_host=args.host, use_rag=use_rag)
    chatbot.run()


if __name__ == "__main__":
    main()
