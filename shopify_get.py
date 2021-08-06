import requests
import json
from dbcon import *
from datetime import datetime




def data_insert(order_id,response):
    print("data_insert")
    str_orderid = str(order_id)

    mydb = mycus()
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM shopify_api_fetch WHERE order_id ='"+str_orderid+"' "

    mycursor.execute(sql)
    row = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    if len(row) > 0:
        pass
    else:
        print("data_insert_--------else")
        string_response = str(response)
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d")
        status="0"

        mydb = mycus()
        mycursor = mydb.cursor()
        sql = "INSERT INTO shopify_api_fetch (order_id,response,created_at,status) VALUES (%s,%s,%s,%s)"
        val = (str_orderid,
               string_response,
               dt_string,
               status
               )

        result = mycursor.execute(sql, val)
        shopify_insert_id = mycursor.lastrowid
        mydb.commit()
        mycursor.close()
        mydb.close()

def seperate_order(mainlist):
    for eachitem in mainlist:
        print("seperate_order")
        orderid = eachitem['id']
        response = eachitem['response']
        data_insert(orderid,response)

    return True


def main_fun():
    url = "https://92b7ccadc73b54fccbc2bdfc0c72da80:0668d37c5f053a387c922841b287e220@enl-nz.myshopify.com/admin/api/2021-04/orders.json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    shpy_data_dict = response.json()

    json_data = json.dumps(shpy_data_dict, indent=1, sort_keys=True)

    filepath = "shopyfi_order.json"
    a_file = open(filepath, "w")
    json.dump(shpy_data_dict, a_file)
    a_file.close()

    list1 = shpy_data_dict["orders"]

    mainlist = []

    i = 0
    for eachdict in list1:
        orderdict={}
        print(eachdict["id"])

        orderdict["id"] = str(eachdict["id"])
        orderdict["response"] = eachdict

        mainlist.append(orderdict)
        i = i+1

    seperate_order(mainlist);

    filepath = "got_order.json"
    a_file = open(filepath, "w")
    json.dump(mainlist, a_file)
    a_file.close()


if __name__ == "__main__":
    main_fun()
else:
    print("Executed when imported")
