import time
from os import system
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

ChromePath = r"chromedriver.exe"
options1 = Options()
options1.add_argument('--headless')
options1.add_argument('--disable-gpu')
options1.add_argument("useAutomationExtension=False")
options1.add_argument("--log-level=3")
options1.add_argument("--disable-extensions")
url = "https://www.betbrain.com/"
driver = webdriver.Chrome(ChromePath, options=options1)
system("cls")
print("Loading...")
driver.get(url)
time.sleep(4)
system("cls")
timeout=15
final = []
interval=3.5
investment = float(input("Investment: "))
length = int(input("Number of pages to scan: "))
def find_substring(substring, string):
    indices = []
    index = -1  # Begin at -1 so index + 1 is 0
    while True:
        # Find next index of substring, by starting search from index + 1
        index = string.find(substring, index + 1)
        if index == -1:  
            break  # All occurrences have been found
        indices.append(index)
    return indices

def getGames(match):
	match = ","+ match.replace("\n", ",")
	simplified = []
	if match.find("Draw") == -1:
		loc = find_substring(",", match)
		x=0
		for i in loc:
			x+=1
			try:
				if x > 12:
					break
				simplified.append(match[i+1:loc[loc.index(i)+1]])
			except:
				return
		finalDict = {"Time":simplified[0], "Match":simplified[1], "Sport":simplified[2], "League":simplified[3], "Home":simplified[6], "HomeBroker":simplified[7], "Away":simplified[10], "AwayBroker":simplified[11]}
		return finalDict
	else:
		p = 2

def getOdds():
	time.sleep(interval)
	driver.find_element_by_xpath("""//*[@id="app"]/div/section/section/main/div[1]/div[2]/div[1]/a[2]""").click()
	time.sleep(interval)
	l = 0 
	while l < length:
		l += 1
		driver.find_element_by_xpath('''//*[@id="app"]/div/section/section/main/div[3]/button''').click()
		system('cls')
		print("Completed page: "+str(l)+" of "+str(length)+".")
		time.sleep(2)
	matches = driver.find_elements_by_class_name("Match")
	system("color 0A")
	matchList = []
	final = []
	for match in matches:
		matchList.append(match.text)
	for match in matchList:
		x = getGames(match)
		if x != None:
			final.append(x)
	for i in final:
		homeOdds = i["Home"].replace("(", "")
		awayOdds = i["Away"].replace("(", "")
		homeOdds = float(homeOdds.replace(")", ""))
		awayOdds = float(awayOdds.replace(")", ""))

		Ap = round(((1/homeOdds)*100)+((1/awayOdds)*100),3)
		if Ap < 100:
			profit = (investment / Ap) - investment
			homeBet = (investment * ((1/homeOdds)*100))/Ap
			awayBet = (investment * ((1/awayOdds)*100))/Ap
			print("\nArbitrage found:")
			print("Date/Time: ", i["Time"])
			print("Sport: ", i["Sport"])
			print("League: ", i["League"])
			print("Match: ", i["Match"])
			print("Profit $", round(((homeBet*homeOdds)-investment), 2), "when betting $", round(homeBet,2), "on Home team through", i["HomeBroker"])
			print("Home odds:", str(homeOdds))
			print("Profit $", round(((awayBet*awayOdds)-investment), 2), "when betting $", round(awayBet,2), "on Away team through", i["AwayBroker"])
			print("Away odds:", str(awayOdds), "\n")
	print("Done, press any key to close()")
	system("pause >nul")
	driver.close()
	driver.quit()
try:
	element_present = EC.presence_of_element_located((By.XPATH, """//*[@id="wisepop-150759"]/div[2]"""))
	WebDriverWait(driver, timeout).until(element_present)
	try:
		time.sleep(interval)
		driver.find_element_by_xpath("""//*[@id="wisepop-150759"]/div[2]""").click()
		time.sleep(interval)
		driver.find_element_by_xpath('''//*[@id="app"]/div/span/div/button''').click()
		getOdds()
	except:
		print("Error, restarting at slower speed.")
		driver.refresh()
		time.sleep(10)
		system("cls")
		interval = 10
		getOdds()
except TimeoutException:
	print("Timed out")

