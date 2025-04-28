import asyncio
import os
import subprocess
import time

import uvicorn
from botasaurus.browser import browser, Driver
from botasaurus.window_size import WindowSize
from botasaurus_humancursor import WebCursor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


@browser(enable_xvfb_virtual_display=True, window_size=WindowSize.window_size_1920_1080)
def calibrate(driver: Driver, data):
    if not set_xauthority():
        return
    import pyautogui
    driver.get("https://frederik-uni.github.io/click-recorder/")  # Assuming you're using Selenium's driver.get method
    screen_width, screen_height = pyautogui.size()

    print(f"Screen size: {screen_width}x{screen_height}")

    clicks = 10
    start_x, start_y = 10, 149

    x_step = (screen_width - start_x) // (clicks + 1)
    y_step = (screen_height - start_y) // (clicks + 1)

    pyautogui.moveTo(start_x, start_y)
    pyautogui.click()

    for i in range(clicks + 1):
        x = start_x + x_step * i
        y = start_y + y_step * i
        print(f"Clicking at ({x - start_x}, {y - start_y}) [{x}, {y}]")  # Corrected the print statement
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(0.5)
    print(f"Clicking at ({1918 - start_x}, {1080 - start_y}) [{1918}, {1080}]")  # Corrected the print statement
    pyautogui.moveTo(1918, 1080)
    pyautogui.click()

    driver.save_screenshot("clicks.png")


def check_for_refresh(driver, initial_url, initial_title, timeout=10, interval=0.05):
    start_time = time.time()

    while time.time() - start_time < timeout:
        if driver.current_url != initial_url or driver.title != initial_title:
            return True
        time.sleep(interval)

    return False


def set_xauthority():
    xauthority_path = '/root/.Xauthority'
    os.environ['XAUTHORITY'] = xauthority_path

    if not os.path.exists(xauthority_path):
        try:
            subprocess.run(['xauth', 'generate', ':0', '.', 'trusted'], check=True)
            print(f"Generated .Xauthority file at {xauthority_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate .Xauthority file: {e}")
        return False
    return True


@browser(enable_xvfb_virtual_display=True)
def bypass_cloudflare(driver: Driver, url):
    if not set_xauthority():
        print("Failed to generate .Xauthority(it fails when it first generates)")
        if not set_xauthority():
            print("Failed to generate .Xauthority")
            return None
    import pyautogui
    start_x, start_y = 10, 149
    pyautogui.moveTo(start_x, start_y)
    pyautogui.click()

    cursor = WebCursor(driver)

    cursor.move_mouse_to_point(100, 100, True)
    driver.google_get(url)
    url = driver.current_url
    title = driver.title
    if title != "Just a moment...":
        print("Not protected")
        return None
    driver.short_random_sleep()
    all_links = driver.select_all("input")[0].parent
    pos = all_links.get_bounding_rect()
    x = pos.x + pos.height / 2 - 5
    y = pos.y + pos.height / 2 - 8

    driver.enable_human_mode()
    cursor.move_mouse_to_point(x, y)
    pyautogui.moveTo(start_x + x, start_y + y)
    pyautogui.click()

    driver.disable_human_mode()
    check_for_refresh(driver, url, title)
    cookies = driver.get_cookies_dict()
    user_agent = driver.user_agent

    return {"user_agent": user_agent, "cookies": cookies}


class UrlRequest(BaseModel):
    url: str


app = FastAPI()
semaphore = asyncio.Semaphore(1)


def bypass_cloudflare_wrapper(data):
    return bypass_cloudflare(data)


@app.post("/bypass-cloudflare")
async def bypass_cloudflare_api(data: UrlRequest):
    async with semaphore:
        try:
            result = await asyncio.to_thread(bypass_cloudflare_wrapper, data.url)
            if result is None:
                raise HTTPException(status_code=500, detail="The result from bypass_cloudflare is None")
            return result

        except Exception as e:
            print(e)
            raise HTTPException(status_code=501, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
