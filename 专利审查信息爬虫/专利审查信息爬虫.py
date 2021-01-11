from selenium import webdriver
import pandas as pd
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

# 截图，打印二维码，需要手动输入，也可以自行接入打码平台
# 实际上，如果你不用OCR或者打码平台的话，不需要截图
def get_auth_code():
    driver.save_screenshot('pictures.png')
    page_snap_obj = Image.open('pictures.png')
    authImg = driver.find_element_by_id("authImg")
    left = 760
    top = 580
    right = int(left + 100)
    bottom = int(top + 50)
    image_obj = page_snap_obj.crop((left, top, right, bottom))
    image_obj.show()
    auth_code = input('请输入验证码：')
    return auth_code

# 输入查询号
def input_query_data(shenqingh, auth_code):
    input_sqh = driver.find_element_by_id("select-key:shenqingh")
    input_sqh.clear()
    input_sqh.send_keys(shenqingh)
    input_auth = driver.find_element_by_id("very-code")
    input_auth.clear()
    input_auth.send_keys(auth_code)

# 查询一次
def do_a_query(shenqingh):
    auth_code = get_auth_code()
    input_query_data(shenqingh, auth_code)
    query = driver.find_element_by_id("query")
    query.click()

# 尝试查询
def work():
    do_a_query(shenqingh)
    try:
        noty_text = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, './/span[@class="noty_text"]'))
        )
        return 1
    except:
        pass
    try:
        record = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, './/table[@class="content_listx_patent"]/tbody/tr[1]'))
        )
        return record
    except:
        pass
    return 0

# 获取详情页面
def get_patent_detail(record):
    patent_type = record.find_element_by_name("record:zhuanlilx").get_attribute("title")
    patent_number = record.find_element_by_name("record:shenqingh").text
    patent_name = record.find_element_by_xpath('.//td[3]').text
    patent_owner = record.find_element_by_name("record:shenqingrxm").get_attribute("title")
    patent_date = record.find_element_by_name("record:shenqingr").get_attribute("title")
    patent_auth_date = record.find_element_by_name("record:shouquanggr").get_attribute("title")
    patent_class = record.find_element_by_name("record:zhufenlh").get_attribute("title")
    detail_button = record.find_element_by_xpath('.//a[@name="record:shenqingh"]')
    detail_button.click()
    innovator = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, './/span[@name="record_fmr:famingrxm"]'))
        ).get_attribute("title")
    # 截图
    driver.save_screenshot(os.path.join(os.path.dirname(__file__), '页面截图', '{}.png'.format(patent_number)))
    item = {
            "专利类型": patent_type,
            "申请号/专利号": patent_number,
            "发明名称": patent_name,
            "申请人": patent_owner,
            "申请日": patent_date,
            "授权公告日": patent_auth_date,
            "主分类号": patent_class,
            "发明人": innovator
    }
    return item



# 设定导出文件名
export_excel = (os.path.join(os.path.dirname(__file__), '专利查询结果.xlsx'))
# 创建浏览器
driver = webdriver.Firefox()
# 设定窗口大小，方便截图
driver.set_window_size(1280, 815)
# 打开查询网
driver.get('http://cpquery.sipo.gov.cn')
# 正式开始，等待登录
WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.ID, "select-key:shenqingh"))
        )
# 读专利号列表
df = pd.read_excel(os.path.join(os.path.dirname(__file__), '专利号列表.xlsx'))
# 建立空列表
item_list = []

for i in range(len(df)):
    shenqingh = str(df.iloc[i,0])
    record = work()
    while record == 1:
        print('验证码错误！')
        record = work()
    item = get_patent_detail(record)
    item_list.append(item)
    # 返回
    r = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "header_query"))
        )
    r.click()

df = pd.DataFrame(item_list)
df.to_excel(export_excel)