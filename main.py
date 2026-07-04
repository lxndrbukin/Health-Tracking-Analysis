from ingest import main as ingest
from auth import main as auth

def main():
    auth()
    ingest()

if __name__ == '__main__':
    main()