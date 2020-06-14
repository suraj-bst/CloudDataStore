import webapp2
import os
from google.appengine.ext.webapp import template
import play_scraper
import os
from google.cloud import datastore


def app_fetcher():
    arr=play_scraper.search('top apps', page=1)
    length=min(10,len(arr))
    dict=[]
    for i in range(0,length):
        dict.append(arr[i]['app_id'])
    return dict




class home(webapp2.RequestHandler):
    def get(self):
        
        top10app=app_fetcher()
        top10appshow=[]
        client = datastore.Client('cloudapp-280210')
        
        
        for myapp in top10app:
            query = client.query(kind='App')
            query.add_filter('app_id', '=', myapp)
            results = list(query.fetch())
            dict=play_scraper.details(myapp)   
            for key,val in dict.items():
                if(val==None):
                    if(key=='video'):
                        dict[key]='https://www.youtube.com/watch?v=B-3yZwaGD_k'
                    else:
                        dict[key]="OPPS!"

                if(key=='description' and len((str)(dict[key])) > 1000 ):
                    dict[key]=(str)(dict[key][:1000])

            
            top10appshow.append(dict)
            if(len(results)==0):
                try:
                    app_key = client.key('App')
                    
                    new_user = datastore.Entity(key=app_key)

                    new_user['app_id']=dict['app_id']
                    new_user['category']=dict['category'][0]
                    new_user['description']=dict['description']
                    new_user['developer']=dict['developer']
                    new_user['developer_address']=dict['developer_address']
                    new_user['developer_email']=dict['developer_email']
                    new_user['icon']=dict['icon']
                    new_user['installs']=dict['installs']
                    new_user['reviews']=dict['reviews']
                    new_user['score']=dict['score']
                    dict['title']=dict['title']
                    new_user['url']=dict['url']
                    new_user['video']=dict['video']
                    client.put(new_user)
                except:
                    print(dict['description'])
        data=top10appshow            
        path = os.path.join(os.path.dirname(__file__), 'startup_page.html') 
        self.response.out.write(template.render(path, data))           
            

  
class app_details(webapp2.RequestHandler):    
    def get(self,app_id):
        dict=play_scraper.details(app_id)
        data=dict
        path = os.path.join(os.path.dirname(__file__), 'details_page.html')
        self.response.out.write(template.render(path, data)) 
  

application = webapp2.WSGIApplication([
    (r'/', home),(r'/app_details/<app_id>', app_details)
    ], debug=True)

def main():
    application.run()

if __name__ == "__main__":
    main()    

