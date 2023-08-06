# COLORED LOGS IN PYTHON
You will be able to color Python logs with this little module. The colorable logs are as follows: `success log`, `warning log`, `error log`, and `info log`!
## MODULE FEATURES
In the logo you can add tags and text, the tag will be enclosed in square brackets. If you don't add the tag, the square brackets will be removed from the log and its color will be put on the text!
### HOW TO CALL THE MODULE ON MY PYTHON SCRIPT?
```py
from logs import Logs

# [TAG] Text here..
print(Logs.success_log(tag='', text=''))
print(Logs.warning_log(tag='', text=''))
print(Logs.error_log(tag='', text=''))
print(Logs.info_log(tag='', text=''))

# Text here..
print(Logs.success_log(text=''))
print(Logs.warning_log(text=''))
print(Logs.error_log(text=''))
print(Logs.info_log(text=''))
```
