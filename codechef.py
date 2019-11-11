from bs4 import BeautifulSoup
import  requests
try:
    url = requests.get('https://www.codechef.com/users/mornville')
    page_source = BeautifulSoup(url.content,'lxml')

    # For Username
    uls = page_source.find('ul', class_="side-nav")
    for ul in uls:
        newsoup = BeautifulSoup(str(ul), 'lxml')
        lis = newsoup.find_all('li')
        for li in lis:
            if "Username" in li.text:
                username = (li.text.split("★"))[1]
    # Other Content
    try:
        rating = page_source.findAll('div', class_="rating-number")[0].text
        global_rating = page_source.findAll('strong', class_="global-rank")[0].text
        problems_count = page_source.findAll('section', class_="problems-solved")
        for i in problems_count:
            newsoup = BeautifulSoup(str(i), 'lxml').find_all('h5')
            fully_solved = newsoup[0].text.split()[2]
            partially_solved = newsoup[1].text.split()[2]
        highest_rating = page_source.findAll('small')
        for i in highest_rating:
            if 'Highest Rating' in i.text:
                highest = i.text.split()[2][:-1]
        img = page_source.findAll('div', class_='user-details-container')
        for i in img:
            avatar = BeautifulSoup(str(i), 'lxml').find_all('img')[0]['src']
    except:
        print("Couldn't get the data")

    # print('Username: '+ username + 'Global Rank:' + global_rating)
    # print('Fully Solved:', fully_solved)
    # print('Partially Solved:', partially_solved)
    # print('Highest Rating:' + highest)
    # print('Avatar Url:', avatar)
except:
    print("Couldn't parse the url")

