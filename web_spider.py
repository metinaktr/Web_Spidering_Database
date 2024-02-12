import requests
from bs4 import BeautifulSoup

import pyodbc 


def crawler(start_url,max_pages=100):
   
    
   conn_str = (
       r'DRIVER={SQL Server};'
       r'SERVER=(local)\SQLEXPRESS;'
       r'DATABASE=search_data;'
       r'Trusted_Connection=yes;'
       
   )
   conn = pyodbc.connect(conn_str)
   
   c=conn.cursor()
   
             
   c.execute('''
              
             if not exists (select * from sysobjects where name='pages_cw' and xtype='U')
             create table pages_cw (
          
                     id int NOT NULL IDENTITY,
                     url TEXT,
                     content TEXT,
                     cleaned_content TEXT,
                     title TEXT,
                     outgoing_links TEXT,
                     pagerank REAL
                     )
              ''')
              
   conn.commit()
   url_frontier= [start_url]

   visited_pages= set()
   while url_frontier and len(visited_pages)<max_pages:
       
          url=url_frontier.pop(0)
       
          if url in visited_pages:
              continue
       
          print(f'Crawling {url}')
          
          response=requests.get(url)
          if response.status_code !=200:
             continue 
             
          soup= BeautifulSoup(response.content,'html.parser')
          print(str(soup))
          
          if soup.find('title'):
              title=soup.find('title').string
            
          outgoing_links=[]
          
          for link in soup.find_all('a'):
                href=link.get('href')
                if href:
                    outgoing_links.append(href)
            
          c.execute('INSERT INTO pages_cw(url,content,cleaned_content,title,outgoing_links) VALUES (?,?,?,?,?)',(url,str(soup),soup.get_text(),title,','.join(outgoing_links)))
         # c.execute('INSERT INTO pages(url,content) VALUES (?,?)',(url,str(soup))) 
          conn.commit()
          
          links=soup.find_all('a')
          
        
          
          for link in links:
              href= link.get("href")
              if href and 'http' in href and href not in visited_pages:
                  url_frontier.append(href) 
          
          visited_pages.add(url)   
   conn.close()
   print("Crawling Completed")
       
seed_urls=["http://www.bbc.co.uk/news/politics/eu-regions/E15000004",
           "https://www.cnn.com"]
    
for url in seed_urls:
        crawler(url,50)
     