import requests
import json
from dbcon import *
from datetime import datetime
import dicttoxml
import xmltodict
import ast
from collections import OrderedDict

import requests


def finalxml(line_itm_list,ship_add_dict,order_data):

    maindict={
                  "Documents": {
                    "Document": {
                      "Company": "ENL",
                      "Department": "SHOW",
                      "Type": "CORD",
                      "CustomerOrderID": 3868757852349,
                      "DocumentDescription": "rob@technicaldiving.co.nz",
                      "Status": "Open",
                      "PartDelv": "Yes",
                      "DelvMethod": "Standard Shipping",
                      "PartInvc": "Yes",
                      "Owner": "CASSALAKL",
                      "Customer": "Rob",
                      "Location": "Wellington",
                      "DocKey1": "WEB",
                      "DocKey2": "WEB",
                      "Addresses": {
                        "Address": {
                          "Type": "Delivery",
                          "Name": "Rob",
                          "NameCont": "",
                          "AddressLine1": "86 The Esplanade",
                          "AddressLine2": "021 535 378",
                          "AddressLine3": "Wellington",
                          "AddressLine4": 6023,
                          "AddressLine5": [
                            "Wellington",
                            "New Zealand"
                          ]
                        }
                      },
                      "Date": 20210601,
                      "DueDate": "",
                      "OpenDate": "",
                      "RequiredDate": "",
                      "TaxCode": "GST",
                      "TaxType": "Excl",
                      "TaxRate": 0.15,
                      "CurrencyCode": "NZD",
                      "ExchangeRate": 1,
                      "LineItems": {
                        "LineItem": [
                          {
                            "LineType": "Stck",
                            "ItemType": "",
                            "ItemCode": "NGT-1-USB",
                            "Unit": "Each",
                            "Quantity": 1,
                            "Pack": "Y",
                            "SubTotal": 330,
                            "BuildPack": "Yes"
                          },
                          {
                            "LineType": "Stck",
                            "ItemType": "",
                            "ItemCode": "NGT-1-USB",
                            "Unit": "Each",
                            "Quantity": 1,
                            "Pack": "Y",
                            "SubTotal": 330,
                            "BuildPack": "Yes"
                          }
                        ]
                      }
                    }
                  }
                }


    created_date = order_data['created_at']
    created_date = created_date[ 0 : 10]
    created_date = created_date.replace('-', '')

    maindict['Documents']['Document']['LineItems'] = line_itm_list
    maindict['Documents']['Document']['Addresses']['Address']= ship_add_dict
    maindict['Documents']['Document']['CustomerOrderID']= order_data['id']
    maindict['Documents']['Document']['Date']= created_date
    maindict['Documents']['Document']['DocumentDescription']= order_data['email']
    maindict['Documents']['Document']['DelvMethod']= order_data['shipping_lines'][0]['code']

    maindict['Documents']['Document']['Owner']= order_data['customer']['first_name']

    maindict['Documents']['Document']['Customer']= order_data['customer']['first_name'] +" "+order_data['customer']['last_name']
    maindict['Documents']['Document']['Location']= order_data['billing_address']['address1']

    maindict['Documents']['Document']['TaxCode']= order_data['tax_lines'][0]['title']
    maindict['Documents']['Document']['TaxRate']= order_data['tax_lines'][0]['rate']



    maindict['Documents']['Document']['CurrencyCode']= order_data['currency']

    #print(maindict)

    build_xml = dicttoxml.dicttoxml(maindict)

    return build_xml







def create_line_item_xml(l_items,row_data):
    #list of dict

    list_lineitem=[]

    if row_data['tags'] == 'Kits':
        for eachdata in l_items:

            dict_data_lineitem={}

            dict_data_lineitem["LineType"] = "Kits"
            dict_data_lineitem["ItemType"] = "STCK"
            dict_data_lineitem["ItemCode"] = eachdata['sku']
            dict_data_lineitem["Unit"] = "Each"
            dict_data_lineitem["Quantity"]= eachdata['quantity']
            dict_data_lineitem["Pack"]= "Y"
            dict_data_lineitem["SubTotal"]= eachdata['price']
            dict_data_lineitem["BuildPack"]= "Yes"

            list_lineitem.append(dict_data_lineitem)
    else:
        for eachdata in l_items:
            dict_data_lineitem = {}

            dict_data_lineitem["LineType"] = "Stck"
            dict_data_lineitem["ItemType"] = "STCK"
            dict_data_lineitem["ItemCode"] = eachdata['sku']
            dict_data_lineitem["Unit"] = "Each"
            dict_data_lineitem["Quantity"]= eachdata['quantity']
            dict_data_lineitem["Pack"]= "Y"
            dict_data_lineitem["SubTotal"]= eachdata['price']
            dict_data_lineitem["BuildPack"]= "Yes"

            list_lineitem.append(dict_data_lineitem)


    return list_lineitem


def create_address_xml(order_data,ship_addrs):

    dict_data_address={}
    dict_data_address["Type"] ="Delivery"
    dict_data_address["Name"] = ship_addrs['name']
    dict_data_address["NameCont"] = ''
    dict_data_address["AddressLine1"] =ship_addrs['address1']
    dict_data_address["AddressLine2"]= ship_addrs['address2']
    dict_data_address["AddressLine3"]= ship_addrs['city']
    dict_data_address["AddressLine4"]= ship_addrs['province']
    dict_data_address["AddressLine5"]= ship_addrs['country']
    dict_data_address["AddressLine6"]= ship_addrs['zip']


    return dict_data_address


def request_fun(ship_addrs,l_items,order_data):

    line_itm_list = create_line_item_xml(l_items,order_data)
    ship_add_dict = create_address_xml(order_data,ship_addrs)

    final_xml_str = finalxml(line_itm_list,ship_add_dict,order_data)


    final_xml_str = final_xml_str.decode("utf-8")

    final_xml_str = final_xml_str.replace('<item type="dict">', '<LineItem>')
    final_xml_str = final_xml_str.replace('</item>', '</LineItem>')
    final_xml_str = final_xml_str.replace('<root>', '')
    final_xml_str = final_xml_str.replace('</root>', '')


    mydb = mycus()
    mycursor = mydb.cursor()

    order_id = order_data['id']


    sql = "UPDATE shopify_api_fetch SET status=2 WHERE order_id='"+str(order_id)+"'"
    result = mycursor.execute(sql)

    mydb.commit()
    mycursor.close()
    mydb.close()





    url = "https://smtp.enl.co.nz:8123/ENLupg/documents/jadehttp.dll?solapp"

    payload=final_xml_str
    print("requestxml",payload)
    headers = {
      'Content-Type': 'application/xml'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    responsexml = response.text

    print("response_xml",responsexml)



    response_dict = xmltodict.parse(responsexml)

    json_data = json.dumps(response_dict)

    dict_data = ast.literal_eval(json_data)
    # normal_dict_response=dict(response_dict)
    #{'Results': {'Result': {'ResultCode': '0', 'DocumentID': 'CORD306445'}}}
    #print(dict_data)

    resultcode = dict_data['Results']['Result']['ResultCode']
    if resultcode =='0':
        document_id = dict_data['Results']['Result']['DocumentID']

        mydb = mycus()
        mycursor = mydb.cursor()

        order_id = order_data['id']


        sql = "UPDATE shopify_api_fetch SET status=1,document_id='"+document_id+"' WHERE order_id='"+str(order_id)+"'"
        result = mycursor.execute(sql)

        mydb.commit()
        mycursor.close()
        mydb.close()


def main_fun():
    mydb = mycus()
    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT * FROM shopify_api_fetch WHERE status='0' "

    mycursor.execute(sql)
    row = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    if len(row) > 0:
        for eachrow in row:

            order_data_str = eachrow['response']


            # json_acceptable_string = order_data_str.replace("'", "\"")
            # print(json_acceptable_string)
            order_data = ast.literal_eval(order_data_str)

            #here eachrow is a dictionary of single eachrow


            if order_data.__contains__('shipping_address'):
                shipping_address_dict  = order_data['shipping_address']
            else:
                if order_data.__contains__('billing_address'):
                    shipping_address_dict  = order_data['billing_address']
                else:
                    continue




               #its a dict
            line_items_list  = order_data['line_items']    #list of dict

            tags = order_data['tags']


            request_fun(shipping_address_dict,line_items_list,order_data)




if __name__ == "__main__":
    main_fun()
else:
    print("Executed when imported")
