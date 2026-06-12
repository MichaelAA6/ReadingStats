
from playwright.sync_api import Playwright,expect


def test_run(playwright: Playwright) -> None:
    #run thr browser and context and create new page
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    #attempt to go to local host
    page.goto("http://localhost:5000/")
    #check that the header and subtext appear
    expect(page.locator("h1")).to_contain_text("Welcome to Reading Stats")
    expect(page.locator("body")).to_contain_text("Displaying Their Stats in Convenient Graph Form")
    #chcek graph appears and is there
    expect(page.locator("#altair-chart canvas")).to_be_visible()
    page.locator("#altair-chart canvas").click(position={"x":20,"y":90})
    #go through the pages and make sure they appear properly
    page.get_by_role("link", name="Goalkeepers").click()
    expect(page.locator("h1")).to_contain_text("Goalkeepers")
    page.get_by_role("link", name="Defenders").click()
    expect(page.locator("h1")).to_contain_text("Defenders")
    page.get_by_role("link", name="Midfielders").click()
    expect(page.locator("h1")).to_contain_text("Midfielders")
    page.get_by_role("link", name="Forwards").click()
    expect(page.locator("h1")).to_contain_text("Forwards")
    page.get_by_role("link", name="/25 Season").click()
    context.close()
    browser.close()