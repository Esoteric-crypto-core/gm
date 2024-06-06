# Captcha settings
# Input your captcha key
API_KEY = ''

# Choose one: -|- anti-captcha -|- 2captcha -|-
CAPTCHA_SERVICE = 'anti-captcha'

# Account settings

MIN_TIME = 7
MAX_TIME = 15

MIN_TIME_ACCOUNT = 15
MAX_TIME_ACCOUNT = 30

# Tasks settings
TASKS_ID = ["903134427529646177", "903134427496092045",
            "903134427458343407", "903134427382845867", "910388748538945778"]
DAILY_TASK = '903134427101827116'

CAPTCHA_SERVICES = {
    "anti-captcha": {'createTask': 'https://api.anti-captcha.com/createTask',
                     'getTask': 'https://api.anti-captcha.com/getTaskResult'},
    "capmonster": {'createTask': 'https://api.capmonster.cloud/createTask',
                   'getTask': 'https://api.capmonster.cloud/getTaskResult'},
    "2captcha": {'createTask': 'https://2captcha.com/in.php',
                 'getTask': 'https://2captcha.com/res.php'},
}


SITE_KEY = '0x4AAAAAAAaAdLjFNjUZZwWZ'

PAGE_URL = f'https://launchpad.gmnetwork.ai/mission?invite_code='
