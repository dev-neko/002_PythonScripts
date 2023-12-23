# print(driver.find_element_by_xpath('//*[contains(text()," に同意します")]'))
# driver.find_element_by_xpath('//*[contains(text()," に同意します")]').click()
# print(driver.find_elements_by_xpath(f'//*[text()=" に同意します"]'))

# driver.find_element_by_xpath(f'//*[@id="ans3025.0.0"]').click()
# driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/form/div[2]/div[2]/div[3]/span/span[1]/input').click()

# driver.find_element_by_xpath(f'//*[@id="ans3025.0.0"]').send_keys(Keys.SPACE)
# driver.find_element_by_xpath(f'/html/body/div[1]/div[2]/div/form/div[2]/div[2]/div[3]/span/span[1]/input').send_keys(Keys.SPACE)

# driver.find_element_by_xpath('/html/body').send_keys(Keys.UP)

# driver.find_element_by_xpath("//input[@type='radio'][@class='input radio fir-hidden'][@value='0']").send_keys(Keys.SPACE)

# ccc=driver.find_elements_by_xpath("//input[@type='radio'][@class='input radio fir-hidden']")
# print(ccc)
# ccc[0].send_keys(Keys.SPACE)
# ccc[1].send_keys(Keys.SPACE)
# ccc[2].send_keys(Keys.SPACE)
# ccc[3].send_keys(Keys.SPACE)
# ccc[4].send_keys(Keys.SPACE)

# driver.find_element_by_css_selector("input[type='radio'][value='0']").click()
# driver.find_element_by_css_selector("input[type='radio'][value='0']").send_keys(Keys.SPACE)

# driver.find_element_by_xpath(f'//*[text()=" に同意します"]/following-sibling::node()').click()
# driver.find_element_by_xpath(f'//*[text()=" に同意します"]/following-sibling::node()').send_keys(Keys.SPACE)

# driver.find_element_by_xpath(f'//*[text()=" に同意します"]/preceding-sibling::node()').click()
# driver.find_element_by_xpath(f'//*[text()=" に同意します"]/preceding-sibling::node()').send_keys(Keys.SPACE)

# driver.find_element_by_xpath(f'//*[text()="nyogupa439@mama3.org"]').click()
# driver.find_element_by_xpath('//*[contains(text(),"nyogupa439@mama3.org")]/../../..').find_element_by_xpath(f'//*[text()="メールフォーム「あああ」からの送信"]').click()

# driver.find_element_by_xpath('//*[contains(text(),"ウェルエイジング アドバイザーズに関するあなたのメンバーシップを確認してください")]').click()

# print(driver.find_element_by_xpath('//*[contains(text(),"ウェルエイジング アドバイザーズに関するあなたのメンバーシップを確認してください")]/../../..').get_attribute('innerHTML'))

# driver.find_element_by_xpath('//*[contains(text(),"nyogupa439@mama3.org")]').click()

# aaa=driver.find_elements_by_css_selector('div[id^="area_maildata_iframe_"]')
# for i in aaa:
# 	print(i.get_attribute('id'))
# 	if 'master' in i.get_attribute('id'):
# 		try:
# 			# iframeの要素が読み込まれるまで待機
# 			WebDriverWait(driver,10).until(
# 				expected_conditions.presence_of_element_located(
# 					(By.ID,'area_maildata_iframe_60268816_master')
# 				)
# 			)
# 		except TimeoutException as e:
# 			# 例外処理
# 			print(e)
# 		print('iframe OK')

# iframe=driver.find_element_by_id('area_maildata_iframe_60268816_master')#iframeをCSSセレクタで特定
# print(iframe.get_attribute('innerHTML'))
# driver.switch_to.frame(iframe)#親フレームからiframeに移動
# print(iframe.get_attribute('innerHTML'))

# iframe=driver.find_element(By.CSS_SELECTOR,"#area_maildata_iframe_60268816_master > iframe")
# iframe=driver.find_element(By.XPATH,'//*[matches(@id,"^area_maildata_iframe\d*?master$")]').find_element(By.TAG_NAME,'iframe')

