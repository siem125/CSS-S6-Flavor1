from service import run_scan
from rich import print


def main():

    repo = input("Repo URL: ")

    try:

        result = run_scan(repo)

        print("\n[bold]Result:[/bold]")
        print(result)

        if result.get("block"):
            print("[red]❌ BLOCK[/red]")
        else:
            print("[green]✅ SAFE[/green]")

    except Exception as e:

        print(f"[red]ERROR:[/red] {e}")


if __name__ == "__main__":
    main()