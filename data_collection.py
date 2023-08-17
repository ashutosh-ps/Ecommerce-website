import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs
import os

url1 = "https://www.amazon.com/s?k=smart+phones&crid=K8YQ1XURW2B8&sprefix=smart+phones%2Caps%2C383&ref=nb_sb_noss_2"

names = []
prices = []
descriptions = []
reviews = []
images = []
links = []



for i in range(1,30):
    url = "https://www.flipkart.com/search?q=smart+phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=" + str(i)
    r = rq.get(url)
    # print(r)
    complete_data = bs(r.text, "lxml" )
    data = complete_data.find("div", class_ = "_1YokD2 _3Mn1Gg" )
    namesclass = data.find_all("div", class_ = "_4rR01T")
    for j in namesclass:
        name = j.text
        names.append(name)
    print( len(names) )

    pricesclass = data.find_all("div", class_ = "_30jeq3 _1_WHN1")
    for j in pricesclass:
        price = j.text
        prices.append(price)
    print( len(prices) )

    descriptionsclass = data.find_all("ul", class_ = "_1xgFaf")
    for j in descriptionsclass:
        description = j.text
        descriptions.append(name)
    print( len(descriptions) )
    
    reviewsclass = data.find_all("div", class_ = "_3LWZlK")
    for j in reviewsclass:
        review = j.text
        reviews.append(review)
    print( len(reviews) )

    linksclass = data.find_all("a", class_ = "_1fQZEK")
    for j in linksclass:
        link = j.get("href")
        links.append(link)
    print( len(links) )

    imagesclass = data.find_all("img", class_ = "_396cs4")
    for j in imagesclass:
        image_url = j.get("src")
        images.append(image_url)
        # print(image_url)

        # Download the image and save it to your local machine
        try:
            response = rq.get(image_url, stream=True)
            response.raise_for_status()

            # Get the file name from the URL and save the image in the current directory
            image_name = os.path.basename(image_url)
            image_name = image_name.replace('-', '_' )
            image_name = image_name.split('?')[0]
            image_name = "C:/Users/91797/OneDrive/Projects/E-commerse/images/" + image_name
            # print(image_name)
            with open(image_name , "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Image downloaded: {image_name}")
        except rq.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except rq.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except rq.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except rq.exceptions.RequestException as err:
            print("OOps: Something Else", err)
    
    print( len(images) )

df = pd.DataFrame({"Product": names, "Prices": prices, "Descriotion": descriptions, "Images": images, "Links": links } )   
df.fillna("null", inplace=True)
df.to_csv("C:/Users/91797/OneDrive/Projects/E-commerse/flipkart_data.csv", index = False)