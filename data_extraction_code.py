#Final Code

import json
import csv
'''
This program extracts all the required data from the json and csv files through the function extract intially all 
values which are supposed to be extracted.

following which the data extraction portion starts, condensing all the different extracted formats into 3 types, 
all the data is parsed with string methods and hence is then passed onto the last code snippet for writing it into 
the resultant csv file
'''
def extract(file_index):
    method_num = 0
    business_name = ''
    business_city = ''
    business_country = ''
    business_street_address = ''
    business_zipcode = ''
    business_description = ''

    invoice_number = ''
    invoice_issue_date = ''
    invoice_due_date = ''
    invoice_description = ''
    invoice_tax = ''

    customer_name = ''
    customer_address_line1 = ''
    customer_address_line2 = ''
    customer_email = ''
    customer_phoneno = ''

    item_name = []
    item_qty = []
    item_rate = []

    data_list = []
    particulars_list = []
    '''The Below code access the .JSON and .CSV files and loads their data in the program
    in two lists namely data_list and particular list respectively'''
    json_path = 'Extracted_outputs/output' + str(file_index) + '/structuredData.json'
    with open(json_path,'r',encoding='utf-8-sig') as input_data:
        data = json.load(input_data)
        data_list = data['elements']
    #Extracting Business Related Information
    business_details = ''
    for i in range(len(data_list)):
        if('Text' in data_list[i]):
            if(data_list[i]['Text'][:7] == 'Invoice'):
                break
            business_details += data_list[i]['Text'].strip() + " "
    business_details = business_details.strip()
    business_detail_list = business_details.split(" ")
    business_name = business_detail_list[0] + " " + business_detail_list[1]
    business_city = business_detail_list[-3]
    for k in range(2,len(business_detail_list)):
        if(business_detail_list[k] == business_detail_list[-3]):
            break
        business_street_address += business_detail_list[k]
    business_country = business_detail_list[-2]
    business_zipcode = business_detail_list[-1]
    #Extracting Invoice number, Tax and issue date
    for i in range(len(data_list)):
            if('Text' in data_list[i]):
                if (data_list[i]['Text'][:8].strip() == "Invoice#"):
                    info = ''
                    info_list = []
                    for j in range(i,len(data_list)):
                        if('Text' in data_list[j]):
                            if(data_list[j]['Text'].strip() == business_name):
                                break
                            info += data_list[j]['Text'].strip()
                    if(info[9] != " "):
                        info = info[:9] + " " + info[9:]
                    for j in range(len(info)):
                        if(info[j:j+5] == "Issue" and info[j-1] != " "):
                            info = info[:j] + " " + info[j:]
                        elif(info[j:j+4] == 'date' and info[j+4] != " "):
                            info = info[:j+4] + " " + info[j+4:] 
                    info_list = (info.strip()).split()
                    invoice_number = info_list[1]
                    invoice_issue_date = info_list[4]
                elif(data_list[i]['Text'].strip() == business_name):
                    business_description = data_list[i+1]['Text']
                elif(data_list[i]['Text'].strip()[:5] == 'Tax %'):
                    if(len(data_list[i]['Text'].strip()) > 5):
                        invoice_tax += data_list[i]['Text'][5:].strip()
                    elif('Text' in data_list[i+1]):
                        if(data_list[i+1]['Text'][0] == '$'):
                            invoice_tax += data_list[i+2]['Text'].strip()
                        else:
                            invoice_tax += data_list[i+1]['Text'].strip()
                    else:
                        invoice_tax += data_list[i+2]['Text'].strip()
                    break
            else:
                pass
        

    #finding out which format the data is in and hence assigning it a suitable method number
    format_chkr  = 'Extracted_outputs/output' + str(file_index) + '/tables' + '/fileoutpart0.csv'
    t_list = []
    with open(format_chkr,'r',encoding='utf-8-sig') as temp_file:
        d = csv.reader(temp_file)
        for lines in d:
            t_list.append(lines)
    if(t_list[0][0].strip() == "ITEM"):
        csv_path = 'Extracted_outputs/output' + str(file_index) + '/tables' + '/fileoutpart2.csv'
        method_num = 1
    elif(t_list[0][0].strip() == "BILL TO"):
        csv_path = 'Extracted_outputs/output' + str(file_index) + '/tables' + '/fileoutpart4.csv'
        method_num = 2
    elif(t_list[0][0].strip() == "DETAILS"):
        csv_path = 'Extracted_outputs/output' + str(file_index) + '/tables' + '/fileoutpart4.csv'
        method_num = 3
    else:
        csv_path = 'Extracted_outputs/output' + str(file_index) + '/tables' + '/fileoutpart4.csv'
        method_num = 1

    #Item name, rate and qty are extracted through the required csv files
    with open(csv_path,'r',encoding='utf-8-sig') as input_file:
            csvinputfile = csv.reader(input_file)
            for lines in csvinputfile:
                particulars_list.append(lines)
    for i in range(len(particulars_list)):
        item_name.append(particulars_list[i][0])
        item_qty.append(particulars_list[i][1])
        item_rate.append(particulars_list[i][2])  

    #All data except item name, rate and qty is extracted through the json file in method number 1
    if(method_num == 1):
        for i in range(len(data_list)):
            if('Text' in data_list[i]):
                if(data_list[i]['Text'].strip() == "BILL TO"):
                    customer_name = data_list[i+1]['Text'].strip()
                    s1 = data_list[i+2]['Text'].strip()
                    s2 = data_list[i+3]['Text'].strip()
                    if((s2 in ['m','om','com','.com']) or ('.com' in s2)):
                        customer_email = s1 + s2
                        customer_phoneno = data_list[i+4]['Text'].strip()
                        customer_address_line1 = data_list[i+5]['Text'].strip()
                        customer_address_line2 = data_list[i+6]['Text'].strip()
                    else:
                        customer_email = s1
                        customer_phoneno = s2
                        customer_address_line1 = data_list[i+4]['Text'].strip()
                        customer_address_line2 = data_list[i+5]['Text'].strip()
                elif(data_list[i]['Text'].strip()[:7] == 'DETAILS'):
                    if(len(data_list[i]['Text']) > 8):
                        invoice_description += data_list[i]['Text'][7:].strip()
                    for j in range(i+1,len(data_list)):
                        if('Text' in data_list[j]):
                            if(data_list[j]['Text'][:9] == 'Due date:'):
                                break
                            if(data_list[j]['Text'].strip() == 'PAYMENT'):
                                continue
                            invoice_description = data_list[j]["Text"].strip()
                            invoice_description += " "
                    invoice_description.strip()
                if(data_list[i]['Text'][:9] == 'Due date:'):
                        invoice_due_date = data_list[i]['Text'][10:20]
                        break
            else:
                pass    
    #The Billing info, Invoice Details and due date is extracted from the .csv file through this method
    elif(method_num == 2):
        second_section_detail_list = []
        customer_detail_list = []
        
        customer_csv_path = 'Extracted_outputs/output' + str(file_index) + '/tables' + '/fileoutpart0.csv'
        with open(customer_csv_path,'r',encoding='utf-8-sig') as input_file:
            csvinputfile = csv.reader(input_file)
            for lines in csvinputfile:
                second_section_detail_list.append(lines)
        customer_details = ''
        for i in range(1,len(second_section_detail_list)):
            customer_details += second_section_detail_list[i][0].strip()
        for i in range(1,len(customer_details)):
            if(customer_details[i].isupper() and customer_details[i-1] != " " and customer_details[i-1].isalpha()):
                customer_details = customer_details[:i] + " " + customer_details[i:]
        for i in range(len(customer_details)):
            if(customer_details[i:i+3] == 'com' and customer_details[i+3] != " "):
                customer_details = customer_details[:i+3] + " " + customer_details[i+3:]
        customer_detail_list = (customer_details.strip()).split(" ");
        customer_name = customer_detail_list[0] + " " + customer_detail_list[1]
        s = customer_detail_list[3]
        if((s in ['m','om','com','.com']) or ('.com' in s)):
            customer_email = customer_detail_list[2] + customer_detail_list[3]
            customer_phoneno = customer_detail_list[4]
        else:
            customer_email = customer_detail_list[2]
            customer_phoneno = customer_detail_list[3]
        for j in range(5,len(customer_detail_list)):
            if(j == len(customer_detail_list) - 1):
                customer_address_line2 = customer_detail_list[j]
                break
            customer_address_line1 = customer_address_line1 + customer_detail_list[j] + " "
        customer_address_line1.strip()
        customer_address_line2.strip()
        #-----------------------------------------------------
        invoice_details = ''
        for i in range(1,len(second_section_detail_list)):
            if(second_section_detail_list[i][1].strip() != ''):
                invoice_details += second_section_detail_list[i][1].strip()
            else:
                break
        invoice_description = invoice_details.strip()
        #------------------------------------------------------
        payment_details = ''
        for i in range(1,len(second_section_detail_list)):
            if(second_section_detail_list[i][2] != ''):
                payment_details += second_section_detail_list[i][2].strip()
            else:
                break
        payment_details_list = payment_details.split(" ")
        invoice_due_date = payment_details_list[2][:10]    
    #The Invoice Details and due date is extracted from the .csv file through this method
    elif(method_num == 3):
        for i in range(len(data_list)):
            if('Text' in data_list[i]):
                if(data_list[i]['Text'].strip() == "BILL TO"):
                    customer_name = data_list[i+1]['Text'].strip()
                    s1 = data_list[i+2]['Text'].strip()
                    s2 = data_list[i+3]['Text'].strip()
                    if((s2 in ['m','om','com','.com']) or ('.com' in s2)):
                        customer_email = s1 + s2
                        customer_phoneno = data_list[i+4]['Text'].strip()
                        customer_address_line1 = data_list[i+5]['Text'].strip()
                        customer_address_line2 = data_list[i+6]['Text'].strip()
                    else:
                        customer_email = s1
                        customer_phoneno = s2
                        customer_address_line1 = data_list[i+4]['Text'].strip()
                        customer_address_line2 = data_list[i+5]['Text'].strip()
                    break
            else:
                pass      
        second_section_detail_list = []
        customer_csv_path = 'Extracted_outputs/output' + str(file_index) + '/tables' + '/fileoutpart0.csv'
        with open(customer_csv_path,'r',encoding='utf-8-sig') as input_file:
            csvinputfile = csv.reader(input_file)
            for lines in csvinputfile:
                second_section_detail_list.append(lines)
        #-------------------------------
        invoice_details = ''
        for i in range(1,len(second_section_detail_list)):
            if(second_section_detail_list[i][0].strip() != ''):
                invoice_details += second_section_detail_list[i][0].strip()
            else:
                break
        invoice_description = invoice_details.strip()
        #------------------------------------------------------
        if(len(second_section_detail_list[0]) == 2 and second_section_detail_list[0][1].strip() == 'PAYMENT'):
            payment_details = ''
            for i in range(1,len(second_section_detail_list)):
                if(second_section_detail_list[i][1] != ''):
                    payment_details += second_section_detail_list[i][1].strip()
                else:
                    break
            payment_details_list = payment_details.split(" ")
            invoice_due_date += payment_details[10:20]
        else:
            for i in range(len(data_list)):
                if('Text' in data_list[i]):
                    if(data_list[i]['Text'][:9] == 'Due date:'):
                        invoice_due_date = data_list[i]['Text'][10:20]
                        break
                else:
                    pass
    #Finally all the extracted data is pushed into the required csv file
    with open("ExtractedData.csv",'a',newline='') as outputFile:
        all_data = []
        writer = csv.writer(outputFile)
        for i in range(len(item_name)):
            data = [business_city,business_country,business_description,business_name,business_street_address,business_zipcode,customer_address_line1,customer_address_line2,customer_email,customer_name,customer_phoneno,item_name[i],item_qty[i],item_rate[i],invoice_description,invoice_due_date,invoice_issue_date,invoice_number,invoice_tax]
            all_data.append(data)
        writer.writerows(all_data)


#pushing the headers only once in the .csv files
with open("ExtractedData.csv",'a',newline='') as outputFile:
        header_list = ['Bussiness__City','Bussiness__Country','Bussiness__Description','Bussiness__Name','Bussiness__StreetAddress','Bussiness__Zipcode','Customer__Address__line1','Customer__Address__line2','Customer__Email','Customer__Name','Customer__PhoneNumber','Invoice__BillDetails__Name',	'Invoice__BillDetails__Quantity','Invoice__BillDetails__Rate',	'Invoice__Description','Invoice__DueDate','Invoice__IssueDate','Invoice__Number','Invoice__Tax']
        writer = csv.writer(outputFile)
        writer.writerow(header_list)
