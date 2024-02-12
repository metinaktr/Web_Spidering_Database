import pyodbc 
import networkx as nx



conn_str = (
     r'DRIVER={SQL Server};'
     r'SERVER=(local)\SQLEXPRESS;'
     r'DATABASE=search_data;'
     r'Trusted_Connection=yes;'
     
 )
conn = pyodbc.connect(conn_str)
 
c=conn.cursor()

c.execute('select url from pages_cw')
urls=[row[0] for row in c.fetchall()]

graph=nx.DiGraph()

     
for  url in urls:
    graph.add_node(url)
     
for url in urls:
    print(url)
    c.execute("select outgoing_links from pages_cw where  CONVERT(varchar, url) = ?",(url,))
   
    outgoing_links=c.fetchone()
    for link in outgoing_links:
        if link.startswith('http'):
            graph.add_edge(url,link)
            
pagerank=nx.pagerank(graph)

for url in urls:
    c.execute('update pages_cw set pagerank=? where CONVERT(varchar, url)=?',(pagerank[url],url))
              
conn.commit()

conn.close()
 