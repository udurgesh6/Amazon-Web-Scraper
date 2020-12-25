#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv


# In[2]:


from bs4 import BeautifulSoup


# In[3]:


pip install selenium


# In[4]:


## Web driver for Chrome
from selenium import webdriver


# In[5]:


driver = webdriver.Chrome(executable_path=r'F:\chromedriver.exe')


# In[6]:


def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    return template.format(search_term)


# In[7]:


url = get_url('ultrawide montior')


# In[8]:


print(url)


# In[9]:


driver.get(url)


# In[12]:


soup = BeautifulSoup(driver.page_source, 'html.parser')


# In[13]:


results = soup.find_all('div', {'data-component-type': 's-search-result'})


# In[14]:


len(results)


# In[15]:


## Prototype the record


# In[16]:


item = results[0]


# In[17]:


atag = item.h2.a


# In[18]:


atag


# In[19]:


description = atag.text.strip()


# In[20]:


description


# In[22]:


url = 'https://www.amazon.com' + atag.get('href')


# In[23]:


price_parent = item.find('span', 'a-price')


# In[26]:


price = price_parent.find('span', 'a-offscreen').text


# In[27]:


item.i


# In[28]:


rating = item.i.text


# In[29]:


rating


# In[31]:


review_count = item.find('span', {'class': 'a-size-base', 'dir':'auto'}).text


# In[32]:


## Generalise the pattern


# In[33]:


def extract_record(item):
    
    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    # price
    price_parent = item.find('span', 'a-price')
    price = price_parent.find('span', 'a-offscreen').text
    
    
    # rank and rating
    rating = item.i.text
    review_count = item.find('span', {'class': 'a-size-base', 'dir':'auto'}).text
    
    
    result = {description, price, rating, review_count, url}
    
    return result


# In[34]:


records = []
results = soup.find_all('div', {'data-component-type': 's-search-result'})


for item in results:
    records.append(extract_record(item))


# In[35]:


## Error Handling


# In[41]:


def extract_record(item):
    
    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    try:     
        # price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return  
    
    
    try:
        # rank and rating
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir':'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    
    result = (description, price, rating, review_count, url)
    
    return result


# In[42]:


records = []
results = soup.find_all('div', {'data-component-type': 's-search-result'})


for item in results:
    record = extract_record(item)
    if record:
        records.append(record)


# In[43]:


records[0]


# In[44]:


for row in records:
    print(row[1])


# In[45]:


## Getting the next page


# In[46]:


def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    
    # add term query to url
    url = template.format(search_term)
    
    
    # add page query of place holder
    url += '&page{}'
    return url


# In[53]:


## Putting it all together
import csv
from bs4 import BeautifulSoup
from selenium import webdriver



def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    
    # add term query to url
    url = template.format(search_term)
    
    
    # add page query of place holder
    url += '&page{}'
    return url



def extract_record(item): 
    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    try:     
        # price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return  
    
    
    try:
        # rank and rating
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir':'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    
    result = (description, price, rating, review_count, url)
    
    return result

def main(search_term):
    """Run main program routine"""
    # startup the web driver
    driver = webdriver.Chrome(executable_path=r'F:\chromedriver.exe')
    
    records = []
    url = get_url(search_term)
    
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
        
    driver.close()
    
    # save data to csv file
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)


# In[54]:


main('shoes')


# In[ ]:




