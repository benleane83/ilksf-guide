import csv
import asyncio
from playwright.async_api import async_playwright

async def check_instagram(handle, playwright):
    if not handle or not handle.startswith('@'):
        return 'No handle'
    url = f"https://www.instagram.com/{handle[1:]}/"
    browser = await playwright.chromium.launch(headless=True)
    page = await browser.new_page()
    try:
        await page.goto(url, timeout=15000)
        page_text = await page.content()
        if "Sorry, this page isn't available." in page_text:
            status = 'Not Found'
        else:
            status = 'Valid'
    except Exception as e:
        status = f'Error: {e}'
    await browser.close()
    return status

async def main():
    with open('data/artist_bios.csv', newline='', encoding='utf-8') as infile, \
         open('data/artist_bios_checked.csv', 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Instagram Status']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        async with async_playwright() as playwright:
            for row in reader:
                status = await check_instagram(row['Bio Link'], playwright)
                row['Instagram Status'] = status
                writer.writerow(row)
                print(f"Checked {row['Bio Link']}: {status}")

if __name__ == '__main__':
    asyncio.run(main())