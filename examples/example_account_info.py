# examples/account_info_example.py

from WrapAI.info.account_info import VeniceApiKeyInfo
from secret_loader import load_secret  # or use your own secret loader
from pprint import PrettyPrinter



def main():
    # Load API key from environment, config, or prompt
    # Initialize pretty printer
    pp = PrettyPrinter(indent=2)


    api_key = load_secret("VENICE_API_KEY_ADMIN")
    if not api_key:
        print("API key not found. Please set VENICE_API_KEY_ADMIN in your environment or secrets file using a Venice Admin API Key.")
        return

    # Create API info instance
    info = VeniceApiKeyInfo(api_key)

    print("== List API Keys ==")
    try:
        response = info.list_api_keys()
        data = response.json()

        # Print both raw and formatted versions
        print("Raw response:")
        print(response.text)

        print("\nFormatted output:")
        pp.pprint(data)

    except Exception as e:
        print(f"Error listing API keys: {e}")

    print("\n== API Key Rate Limits ==")
    try:
        response = info.list_api_key_rate_limits()
        # Parse the JSON data
        data = response.json()

        # Print both raw and formatted versions
        print("Raw response:")
        print(response.text)

        print("\nFormatted output:")
        pp.pprint(data)

    except Exception as e:
        print(f"Error getting API key rate limits: {e}")

    print("\n== Model Rate Limits ==")
    try:
        response = info.get_model_rate_limits()
        print(response.text)

    except Exception as e:
        print(f"Error getting model rate limits: {e}")

if __name__ == "__main__":
    main()
