from selenium.webdriver import Remote, ChromeOptions  # this is to browse the website
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection  # this is to perform Web Scraping
# using a Bright Data (you don't need is as a requirement however, it has captcha solver so keep that in mind
# because you are not going to be able to scrape website with captcha without this
# if you are planning to remove it just connect directly using commands:
# from selenium import webdriver and initialize your webdriver as "driver = webdriver.Chrome(options=options)"
from bs4 import BeautifulSoup  # to parse HTML
import os  # to have access to ENV Variables to get Bright Data Server key

SBR_WEBDRIVER = os.getenv("BD_SRV")  # get server key


def scrape_website(website):  # scrape website URL
    print("Connecting to Scraping Browser...")

    # crate server connection using Google Chrome and BD srv key
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:  # initialize driver
        driver.get(website)  # request website
        print("Waiting captcha to solve...")
        solve_res = driver.execute(  # if needed solve for captcha, if there i no captcha then code is going to skip it
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])  # solved if needed
        print("Navigated! Scraping page content...")
        html = driver.page_source  # get source HTML
        return html  # return HTML


def extract_body(html_content):  # extract body
    soup = BeautifulSoup(html_content, "html.parser")  # we parse the HTML
    body_content = soup.body  # get body from HTML
    if body_content:  # if we get some content then
        return str(body_content)  # we cast it as a string
    return ""


def clean_body(body_content):  # clean body
    soup = BeautifulSoup(body_content, "html.parser")  # parse body content as HTML
    for script_or_style in soup(["script", "style"]):  # ignore scripts and styles
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")  # get text from HTML
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()  # rejoin skipping extra blank spaces
    )
    return cleaned_content  # return cleaned data


def split_dom_content(dom_content, max_length=6000):  # this is to batch the data (here is set to max_tokens = 6000)
    return [  # however some models could have more or less (read documentation be fore modifying)
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)  # chuck the data in batches of
    ]  # max_length tokens each
