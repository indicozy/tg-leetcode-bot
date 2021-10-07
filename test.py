import requests
output = requests.options('https://leetcode-rating.herokuapp.com/update-scores')
print(output)
