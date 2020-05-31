import socket
import subprocess
import csv
import re
from concurrent.futures import ThreadPoolExecutor


Banner = '''#######################################################

                    Script for resolving ip/domain-name
                                    &
                        testing for Reachability

            ######################################################'''

print(Banner)

resolv_file = "Resolved.csv"

with open("host_ip.txt") as f:
    data = f.read()

data_file = open(resolv_file ,"w")
fieldnames = ["IP" , "Domain-Name", "Reachability"]
thewriter = csv.DictWriter(data_file,fieldnames=fieldnames)
thewriter.writeheader()


ip_list = []
for n in data.splitlines():
    ip_list.append(n)

file_object_fail = open("cant_resolve.txt","w")

def reach(ip_name):
    response = subprocess.Popen(['ping' ,'-c','2', ip_name],stdout=subprocess.PIPE)
    response.wait()
    if response.returncode != 0:
        Reachable = "NO"
        print(f"{ip_name} NOT REACHABLE !!")
    else:
        print(f"{ip_name} is reachable")
        Reachable = "YES"

    return Reachable

def main(ip_name):
    '''function for resolving ip into domain names,Checking Reachability for each host
         and writing esults to a CSV file'''

    # Check whether input is ip or a domain name
    check = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    host = re.search(check , ip_name)
    if host != None:
        name_or_ip = "ip"
    else:
        name_or_ip = "name"


    try:
        #Get domain-name if input is an ip
        if name_or_ip == "ip":
            name = socket.gethostbyaddr(ip_name)[0]
            get_ip = ip_name
            print(f"{ip_name} resolved to {name} ")
           
        else:
        #Get IP if input is a domain-name
            get_ip = socket.gethostbyname(ip_name)
            name = ip_name
            print(f"{ip_name} resolved to {get_ip} ")

        #Reachability test
        Reachable = reach(ip_name)


    except (socket.herror, socket.gaierror):
        print(f"\nError: Cannot Resolve {ip_name}\n")
        Reachable = reach(ip_name)
        file_object_fail.write(f"{ip_name},{Reachable}\n")
        if name_or_ip == "ip":
            get_ip = ip_name
            name = ''
        elif name_or_ip == "name":
            name = ip_name
            get_ip = ''

    finally:
        items = [get_ip , name , Reachable]
        thewriter = csv.writer(data_file)
        thewriter.writerow(items)




if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        execute = executor.map(main , ip_list)
    
    data_file.close()
    file_object_fail.close()