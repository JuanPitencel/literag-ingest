from rich.console import Console
from rich.progress import (
    Progress, 
    SpinnerColumn, 
    TextColumn, 
    BarColumn, 
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn
)
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint


console = Console()


class IngestDashboard:
    def __init__(self):
        self.progress = None
        self.tasks = {}
    
    def start(self, pdf_name: str):
        """Show initial banner."""
        console.clear()
        console.print(Panel(
            f"[bold blue]LiteRAG Ingest[/bold blue]\n\n"
            f"Processing: [green]{pdf_name}[/green]",
            title="📄 Document Ingestion",
            expand=False
        ))
    
    def create_progress(self):
        """Create progress display."""
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.description}"),
            BarColumn(bar_width=40),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console
        )
        return self.progress
    
    def show_extraction_result(self, pages: int):
        """Show extraction results."""
        console.print(f"\n✅ Extracted [bold green]{pages}[/bold green] pages\n")
    
    def show_chunking_result(self, chunks: int):
        """Show chunking results."""
        console.print(f"✅ Created [bold green]{chunks}[/bold green] chunks\n")
    
    def show_complete(self, collection: str, total_chunks: int):
        """Show completion message."""
        table = Table(title="✅ Ingestion Complete", show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Collection", collection)
        table.add_row("Total chunks", str(total_chunks))
        table.add_row("Status", "Ready for queries")
        
        console.print("\n")
        console.print(table)
        console.print("\n")
    
    def show_error(self, message: str):
        """Show error message."""
        console.print(f"\n[bold red]❌ Error:[/bold red] {message}\n")


# Singleton instance
dashboard = IngestDashboard()
