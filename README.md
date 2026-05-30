# NYC Housing Alert

**NYC Housing Alert** is an automated tool that monitors the NYC Housing Connect lottery and sends an email notification when new listings appear.

The NYC housing lottery is competitive and hard to track manually a standard HTTP request returns an empty shell before any listings load. To get around this, the scraper uses **Playwright** to launch a headless Chromium browser, which loads the page and runs the JavaScript as normal. Playwright intercepts the underlying API response the page makes to fetch listings, pulling the structured data directly without parsing HTML.

From there the flow is straightforward:

1. **Scrape** compare against previously seen listing IDs stored in `data/seen.json`
3. **Notify** commit updated `seen.json` and `data/archive.json` back to the repo

GitHub Actions handles scheduling and persistence. After each run, the Action commits the updated state files back to the repository, so the next run always has an accurate record of what's already been seen. The repo itself serves as the database.

---

## Project Structure

```
orchestrates scrape, diff, notify, persist
tracker.py       # Diffing logic and archive management
storage.py       # JSON read/write utilities
      .github/
    alert.yml  # GitHub Actions workflow Secrets and variables headless browser automation
- [python-dotenv](https://pypi.org/project/python-dotenv/) email delivery (Python standard library)
