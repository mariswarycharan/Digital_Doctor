import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import re
import numpy as np
import base64

st.set_page_config(page_title="Medicine",page_icon="💊")

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64(r"D:\Downloads\grey-scale-shot-person-holding-pack-capsules-with-black.jpg")

page_bg_img = f"""
<style>
.stApp {{
background-image: url('data:image/jpg;base64,{img}');
background-size: cover;
}} 
</style>
"""
           
st.markdown(page_bg_img, unsafe_allow_html=True)



def apollo(product_name):
    container = {}
    url = f"https://www.apollopharmacy.in/search-medicines/{product_name.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all(
        "div", {"class": "ProductCard_productCardGrid__ZQBc1"})

    for result in search_results:
        title = result.find("p", {"class": "ProductCard_productName__f82e9"})
        price = result.find("span", {"class": "ProductCard_regularPrice__yMb6G"})
        if not price:
            price = result.find("span", {"class": "ProductCard_mrpText__b4mu9"})
        link = result.find("a", {"class": "ProductCard_proDesMain__LWq_f"})
        link = f"https://www.apollopharmacy.in{link['href']}"
        image = result.find("div", {"class": "ProductCard_bigAvatar__KUsDb"}).find("img")
        if title and price:
            container[title.text.strip()] = {
                "price": re.sub('[a-z,A-Z\"!@#$%^₹&*(){}?/;`~:<>+=-]', '', price.text.strip()),
                "link": link,
                "image": image["src"] if image else "Not available"
            }
    return container


def onemg(product_name):
    container = {}
    url = f"https://www.1mg.com/search/all?filter=true&name={product_name.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=(3.05, 27))
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("div", {"class": "col-xs-12 style__container___cTDz0"})

    for result in search_results:
        title = result.find("span", {"class": "style__pro-title___3zxNC"})
        price = result.find("div", {"class": "style__price-tag___B2csA"})
        link = result.find("div", {"class": "style__horizontal-card___1Zwmt"}).find("a")
        if title and price:
            container[title.text.strip()] = {
                "price":  re.sub('[a-z,A-Z\"!@#₹$%^&*(){}?/;`~:<>+=-]', '', price.text.strip()) ,
                "link": f"https://www.1mg.com{link['href']}",
                "image": "Not available"
            }
    return container


def pharmeasy(product_name):
    container = {}
    url = f"https://pharmeasy.in/search/all?name={product_name.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all("div", {"class": "Search_medicineLists__hM5Hk"})

    for result in search_results:
        title = result.find("h1", {"class": "ProductCard_medicineName__8Ydfq"})
        price = result.find("div", {"class": "ProductCard_gcdDiscountContainer__CCi51"})
        if not price: price = result.find("div", {"class": "ProductCard_ourPrice__yDytt"})
        else : price = price.find("span")
        image = result.find(
            "img", {"class": "ProductCard_productImage__dq5lq"})
        link = result.find("a", {"class": "ProductCard_medicineUnitWrapper__eoLpy ProductCard_defaultWrapper__nxV0R"})
        if title and price:
            container[title.text.strip()] = {
                "price":  re.sub('[a-z,A-Z\"!@#$%^₹&*(){}?/;`~:<>+=-]', '', price.text.strip()),
                 "link": f"https://www.1mg.com{link['href']}",
                "image": image["src"]
            }
    return container


def search(product_name):
    return {
        "apollopharmacy": apollo(product_name),
        "onemg": onemg(product_name),
        "pharmeasy": pharmeasy(product_name)
    }
    
search_product_name = st.text_input("Enter the product name")



search_button = st.button("Search")

if search_button:

    search_result = search(search_product_name)
    
    # price = []
    # link = []
    # image = []
    # pro_name = []

    # for i,j in search_result["apollopharmacy"].items():
    #     pro_name.append(i)
    #     price.append(j["price"])
    #     link.append(j["link"])
    #     image.append(j["image"])
      
    # apollopharmacy_data = pd.DataFrame(data={"Product_name":pro_name ,"price":price,"link":link,"image":image})
    # st.session_state['pro_name'] = len(pro_name)
    
    
    # add_list = []
    
    # for i in apollopharmacy_data["price"]:
    
    #     if "." in i :
    #         add_list.append(float(i))
                   
    #     if "." not in i and len(i) != 0:
    #         add_list.append(int(i))
        
    #     if i =="" and len(i) == 0:
    #         add_list.append(30)
    # apollopharmacy_data["price"] = add_list
    # st.session_state['apollopharmacy_data'] = apollopharmacy_data
    
    
    price_f = []
    link_f = []
    image_f = []
    pro_name_f = []

    
    for i,j in search_result["onemg"].items():
        pro_name_f.append(i)
        price_f.append(j["price"])
        link_f.append(j["link"])
        image_f.append(j["image"])
       

    onemg_data = pd.DataFrame(data={"Product_name":pro_name_f, "price":price_f,"link":link_f,"image":image_f},index=[ "PIT_"+str(i) for i in range(1,len(pro_name_f)+1)])
    st.session_state['pro_name_f'] = len(pro_name_f)
    
    
    add_list_o = []
    for i in onemg_data["price"]:
        if "." in i :
            add_list_o.append(float(i))
                   
        if "." not in i and len(i) != 0:
            add_list_o.append(int(i))
        
        if i =="" and len(i) == 0:
            add_list_o.append(30)
            
    onemg_data["price"] = add_list_o
    st.session_state['onemg_data'] = onemg_data
    

    price_e = []
    link_e = []
    image_e = []
    pro_name_e = []  
        
    for i,j in search_result["pharmeasy"].items():
        pro_name_e.append(i)
        price_e.append(j["price"])
        link_e.append(j["link"])
        image_e.append(j["image"])

    pharmeasy_data =   pd.DataFrame(data={ "Product_name" : pro_name_e, "price":price_e,"link":link_e,"image":image_e})
    st.session_state['pro_name_e'] = len(pro_name_e)

    add_list_p = []
    for i in pharmeasy_data["price"]:
        if "." in i :
            add_list_p.append(float(i))
                   
        if "." not in i and len(i) != 0:
            add_list_p.append(int(i))
        
        if i =="" and len(i) == 0:
            add_list_p.append(30)
        
    pharmeasy_data["price"] = add_list_p
    st.session_state['pharmeasy_data'] = pharmeasy_data  
    

if 'apollopharmacy_data' in st.session_state:
    st.title("apollopharmacy")  
    apollopharmacy_data = st.session_state.apollopharmacy_data
    apollopharmacy_data = apollopharmacy_data.sort_values(by='price').reset_index().drop("index", axis=1)
    result_a =  pd.DataFrame(data=apollopharmacy_data.values.tolist(),columns=["Product_name", "price","link","image"],index=[ "PID_"+str(i) for i in range(1,st.session_state.pro_name+1)])
    result_a.index.name = "Product ID"
    st.dataframe( result_a) 
    
    val1_view = st.text_input("Enter the product id :",value="PID_1")
    sort_df = result_a.loc[val1_view].values.tolist()

    st.subheader("Product name : " + sort_df[0]) 
    st.image(sort_df[-1])
    st.markdown("Link : " + sort_df[2])
    st.info( "Price : " + "₹" + str(sort_df[1]))
    
    
if 'onemg_data' in st.session_state:
    st.title("onemg")  
    onemg_data = st.session_state.onemg_data
    onemg_data = onemg_data.sort_values(by='price').reset_index().drop("index", axis=1)
    result_o =  pd.DataFrame(data=onemg_data.values.tolist(),columns=["Product_name", "price","link","image"],index=[ "PID_"+str(i) for i in range(1,st.session_state.pro_name_f+1)])
    
    if len(result_o) != 0:
    
        result_o.index.name = "Product ID"
        
        st.dataframe(result_o) 
        val1_view = st.text_input("Enter the product id:",value="PID_1")
        sort_df = result_o.loc[val1_view].values.tolist()

        st.subheader("Product name : " + sort_df[0]) 

        st.markdown("Link : " + sort_df[2])
        st.info( "Price : " + "₹" + str(sort_df[1]))
    
if 'pharmeasy_data' in st.session_state:
    
    st.title("pharmeasy")  
    pharmeasy_data = st.session_state.pharmeasy_data
    pharmeasy_data = pharmeasy_data.sort_values(by='price').reset_index().drop("index", axis=1)
    result_p =  pd.DataFrame(data=pharmeasy_data.values.tolist(),columns=["Product_name", "price","link","image"],index=[ "PID_"+str(i) for i in range(1,st.session_state.pro_name_e+1)])
    result_p.index.name = "Product ID"
    
    st.dataframe(result_p,use_container_width=True) 
    val1_view = st.text_input("Enter the product ID:",value="PID_1")
    sort_df = result_p.loc[val1_view].values.tolist()

    st.subheader("Product name : " + sort_df[0]) 
    st.markdown("Link : " + sort_df[2])
    st.info( "Price : " + "₹" + str(sort_df[1]))







