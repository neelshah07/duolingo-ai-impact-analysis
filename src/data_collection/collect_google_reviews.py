import os
import pandas as pd
from google_play_scraper import reviews


def scrape_google_play_reviews(
    app_id="com.duolingo",
    language="en",
    country="us",
    target_reviews=1000,
):
    """
    Scrapes Google Play reviews using pagination.

    Parameters
    ----------
    app_id : str
        Google Play App ID

    language : str
        Review language

    country : str
        Country code

    target_reviews : int
        Number of reviews to collect

    Returns
    -------
    pandas.DataFrame
    """

    print("=" * 60)
    print("Starting Google Play Review Scraper...")
    print("=" * 60)

    all_reviews = []
    continuation_token = None

    while len(all_reviews) < target_reviews:

        try:

            result, continuation_token = reviews(
                app_id,
                lang=language,
                country=country,
                count=200,
                continuation_token=continuation_token,
            )

            if not result:
                print("\nNo more reviews available.")
                break

            all_reviews.extend(result)

            print(f"Collected {len(all_reviews)} reviews")

        except Exception as e:
            print("\nError while scraping:")
            print(e)
            break

    print("\nCreating DataFrame...")

    df = pd.DataFrame(all_reviews)

    print("DataFrame Created Successfully")
    print(f"Shape : {df.shape}")

    # Create folder if it doesn't exist
    save_directory = "data/raw/google_play"
    os.makedirs(save_directory, exist_ok=True)

    save_path = os.path.join(
        save_directory,
        "duolingo_reviews.csv"
    )

    df.to_csv(save_path, index=False)

    print("\nDataset Saved Successfully")
    print(f"Location : {save_path}")

    return df


def main():

    df = scrape_google_play_reviews(
        app_id="com.duolingo",
        language="en",
        country="us",
        target_reviews=1000
    )

    print("\n")
    print("=" * 60)
    print("SCRAPING COMPLETED")
    print("=" * 60)

    print(df.head())


if __name__ == "__main__":
    main()