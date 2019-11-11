from bs4 import BeautifulSoup
import  requests
try:
    url = requests.get('https://www.codechef.com/users/nishant403')
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
        # ratings of the user
        rating = page_source.findAll('div', class_="rating-number")[0].text
        global_rating = page_source.findAll('strong', class_="global-rank")[0].text
        # For Solved Problems count
        problems_count = page_source.findAll('section', class_="problems-solved")
        for i in problems_count:
            newsoup = BeautifulSoup(str(i), 'lxml').find_all('article')
            # For Completely Solved
            full_para = BeautifulSoup(str(newsoup[0]), 'lxml').find_all('p')
            count = 0
            for i in full_para:
                if(count==0):
                    fully_practice = len(BeautifulSoup(str(i), 'lxml').find_all('a'))
                count+=1
            fully_others = (count-1)
            # For Partially Solved
            partial_para = BeautifulSoup(str(newsoup[1]), 'lxml').find_all('p')
            count = 0
            for i in partial_para:
                if(count==0):
                    partial_practice = len(BeautifulSoup(str(i), 'lxml').find_all('a'))
                count+=1
            partial_others = (count-1)
        highest_rating = page_source.findAll('small')
        for i in highest_rating:
            if 'Highest Rating' in i.text:
                highest = i.text.split()[2][:-1]
        img = page_source.findAll('div', class_='user-details-container')
        for i in img:
            avatar = BeautifulSoup(str(i), 'lxml').find_all('img')[0]['src']
    except:
        print("Couldn't get the data")

    print('\nUsername: '+ username + 'Global Rank:' + global_rating)
    print('Highest Rating:' + highest)
    print('Avatar Url:', avatar)
    print("\nFully solved Problems - {0} Practice Problems and {1} Other Problems".format(fully_practice,fully_others) )
    print("Partially solved Problems - {0} Practice Problems and {1} Other Problems".format(partial_practice,partial_others) )
    print()
    # print('Partially Solved - \n Practice({0}) and Others({1})'%(partial_practice,partial_others))


except:
    print("Couldn't parse the url")

