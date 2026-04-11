from scanner.service import run_scan
from rich import print


def main():
    repo = input("Repo URL: ")

    result = run_scan(repo)

    print("\n[bold]Result:[/bold]")
    print(result)

    if result["block"]:
        print("[red]❌ BLOCK[/red]")
    else:
        print("[green]✅ SAFE[/green]")


if __name__ == "__main__":
    main()