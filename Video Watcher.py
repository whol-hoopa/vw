from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import datetime, time, random

def Log_in(driver):
    driver.find_element_by_xpath("""//*[@id="sbLogInCta"]""").click()
    time.sleep(random.uniform(0, 0.75))
    #Username
    driver.find_element_by_xpath("""//*[@id="sbxJxRegEmail"]""").send_keys("Username")
    #Password
    driver.find_element_by_xpath("""//*[@id="sbxJxRegPswd"]""").send_keys("Password")
    #Changing Iframe
    time.sleep(random.uniform(0, 0.75))
    captcha_iframe = driver.find_element_by_xpath("""//*[@id="sbCaptcha"]/div/div/iframe""")
    driver.switch_to_frame(captcha_iframe)
    #Clicking the captcha
    driver.find_element_by_class_name("recaptcha-checkbox-checkmark").click()
    while True:
        wait_for_user = input("Are you done Logining In: ").lower()
        if wait_for_user == "yes":
            print("Ok Starting Bot")
            break
        else:
            print("Will wait until you're done")
            pass

def open_new_tab(driver, window_to_open):
    driver.execute_script("window.open(arguments[0])", window_to_open);
    windowswitcher(driver)

def close_prev_tab(driver):
    current_handle = driver.current_window_handle
    handles = driver.window_handles
    for handle in handles:
        if handle != current_handle:
            driver.switch_to_window(handle)
            driver.close()
            driver.switch_to_window(current_handle)
            driver.switch_to_default_content()

def daily_poll(driver):
    open_new_tab(driver, "Website")
    windows = driver.window_handles
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'pollButtonsSection')))
        time.sleep(random.uniform(0, 0.75))
        driver.find_element_by_class_name("pollCheckbox").click()
        time.sleep(random.uniform(0, 0.75))
        driver.find_element_by_id("pollButtonsSection").click()
        driver.close()
        time.sleep(random.uniform(0, 0.25))
        driver.switch_to_window(windows[0])
        driver.switch_to_default_content()
        return
    except:
        driver.close()
        time.sleep(random.uniform(0, 0.25))
        driver.switch_to_window(windows[0])
        driver.switch_to_default_content()
        return

def windowswitcher(driver):
    #Gets All Windows
    current_handle = driver.current_window_handle
    handles = driver.window_handles
    for pos, handle in enumerate(handles):
        #Switches to the most recently opened window
        if handle != current_handle:
            driver.switch_to_window(handle)
            driver.switch_to_default_content()
            return

def find_right_playlists(driver):
    playlists = []
    driver.switch_to_default_content()
    all_playlists = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sbCard")))
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sbTrayListItemHeaderImgContainerWrapper")))
    #watchAgain_Playlists = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "playlistWatchAgain")))
    watchAgain_Playlists = driver.find_elements_by_class_name("playlistWatchAgain")
    print(len(all_playlists))
    #Finds the playlists that we need and puts it into the playlists table
    if len(watchAgain_Playlists) != 0:
        for playlist in all_playlists:
            if playlist.get_attribute("class") == "sbCard sbHomeCard watchCard cardType48 animateScaleDown" or playlist.get_attribute("class") == "sbCard sbHomeCard watchCard cardType48":
                playlist_parent = playlist.find_element_by_xpath("..")
                for watched_playlist in watchAgain_Playlists:
                    watched_playlist = watched_playlist.find_element_by_xpath("..")
                    if playlist_parent != watched_playlist:
                            playlists.append(playlist)
                if len(watchAgain_Playlists) == 0:
                        playlists.append(playlist)
        return playlists
    elif len(watchAgain_Playlists) == 0:
        for playlist in all_playlists:
            if playlist.get_attribute("class") == "sbCard sbHomeCard watchCard cardType48 animateScaleDown" or playlist.get_attribute("class") == "sbCard sbHomeCard watchCard cardType48":
                playlists.append(playlist)
        return playlists

def slide_right(driver, container):
    container_title = WebDriverWait(container, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sbTrayTitle')))
    ActionChains(driver).move_to_element(container_title).perform()
    button_next = WebDriverWait(container, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sbHCTNavNext')))
    ActionChains(driver).move_to_element(button_next).perform()
    button_next.click()
    
def choose_playlist(driver):
    playlists = find_right_playlists(driver)
    print(len(playlists))
    if len(playlists) == 0:
        return False
    #Find a playlist randomly from playlists table
    ran_num = random.randint(0, len(playlists) - 1)
    #I'm going to Find the id of the randomly chosen playlist so it can try to find the id instead
    ran_playlist = playlists[ran_num]
    ran_playlist_id = ran_playlist.get_attribute("id")
    print(ran_playlist_id)
    #Find Containers of playlists
    All_playlists_containers = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sbTray")))
    playlists_containers = []
    #Finds the Correct Containers
    for playlists_container in All_playlists_containers:
        class_name = playlists_container.get_attribute("class")
        if class_name == "sbTray sbTrayNumberOfRowsIs1 sbHCTBookendBlk sbTrayV3":
            playlists_containers.append(playlists_container)
    #Go through each one and find the one with the randomly chosen playlist
    for container in playlists_containers:
        if container.get_attribute("class") == "sbTray sbTrayNumberOfRowsIs1 sbHCTBookendBlk sbTrayV3":
            href = container.find_element_by_class_name("sbTrayTitle").get_attribute("href")
            print(href)
            if href != "Website#2" and href != "Website#2":
                #Using find_elements_instead of find_element because it's faster
                list_of_one_element = container.find_elements_by_id(ran_playlist_id)
                print(str(len(list_of_one_element)) + ' len(list_of_one_element)')
                if len(list_of_one_element) == 1:
                    #container_title = container.find_element_by_class_name("sbTrayTitleLink")
                    button_prev = container.find_element_by_class_name("sbHCTNavPrev")
                    while True:
                        try:
                            #And click it
                            #WebDriverWait(driver, 5).until(EC.element_to_be_selected(list_of_one_element[0]))
                            list_of_one_element[0].click()
                            return
                        except:
                            time.sleep(random.uniform(0, 0.75))
                            slide_right(driver, container)

def find_already_watched_videos(already_watched_videos):
    _watched_videos = []
    for video in already_watched_videos:
        class_name = video.get_attribute("class")
        if class_name == "iconWatch iconCheckmark":
            _watched_videos.append(video)
    return _watched_videos

def pause_video(driver):
    head = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "sbPlaylistVideoContainer")))
    iframe_head = WebDriverWait(head, 5).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to_frame(iframe_head)
    children_iframe = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to_frame(children_iframe)
    video = WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((By.CLASS_NAME, "absolute-wrapper")))
    ActionChains(driver).move_to_element(video).perform()
    pause = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "play-button-state")))
    print(pause.get_attribute("class"))
    if pause.get_attribute("class") == "play-button-state playing-state":
        pause.click()
    driver.switch_to_default_content()

def go_through_videos(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'sbPlaylistVideosContainer')))
    #Finds how many videos there are
    amount_of_videos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sbPlaylistVideoNumber")))
    #Finds how many videos that are already watched
    already_watched_videos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "iconWatch")))
    #This is also part of finding the videos that are already watched but it finds if the element fits into a certain class
    _watched_videos = find_already_watched_videos(already_watched_videos)
    #This is part is where all the automation happens like clicks
    for _ in range(len(_watched_videos), len(amount_of_videos)):
        driver.switch_to_default_content()
        already_watched_videos = driver.find_elements_by_class_name("iconWatch")
        _watched_videos = find_already_watched_videos(already_watched_videos)
        time.sleep(random.uniform(0, 1))
        amount_of_videos[len(_watched_videos)].click()
        print("There are " + str(len(amount_of_videos)) + " videos")
        print("Watched " + str(len(_watched_videos)) + " Already")
        time.sleep(random.uniform(0, 1))
        pause_video(driver)
        while True:
            current_already_watched_num_videos = len(find_already_watched_videos(driver.find_elements_by_class_name("iconWatch")))
            time.sleep(random.uniform(0, 1))
            if current_already_watched_num_videos != len(_watched_videos):
                break
        if _ + 1 >= len(amount_of_videos):
            return

def full_auto():
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.ID, 'earningCardsWrap')))
    driver.implicitly_wait(7.5)
    _any_playlists_left = choose_playlist(driver)
    if _any_playlists_left == False:
        print("Nice you've just Completed Watching all the playlists")
        return False
    else:
        go_through_videos(driver)
        open_new_tab(driver, "Website#4")
        time.sleep(5)
        close_prev_tab(driver)
    
chrome_options = Options()
chrome_options.add_extension("C:/uBlock-Origin_v1.16.12.crx")
driver_path = "C:/chromedriver.exe"
driver = webdriver.Chrome(executable_path = driver_path, chrome_options = chrome_options)
driver.set_window_rect(0, 0, 600, 700)
driver.implicitly_wait(7.5)
driver.get("Website#5")

Log_in(driver)
daily_poll(driver)
while True:
    if_continue = full_auto()
    pass
    if if_continue == False:
        break
