# Parsing Methods:

We generally used requests and beautifulsoup4 module for parsing the data from department websites.

Although, it wasn't enough for some departments (only cs at the moment) because their website were rendering with javascript. So, whenever we send a request we're recieving non-rendered html file which is useless. So, we had to use Selenium whenever this problem is the case.

# Contribution:

If you are going to add new departments, you don't need to open issue. Just send us a pull request!

Keep in mind, we don't like to use Selenium. If you have another solution beside Selenium, again pull requests are welcome!