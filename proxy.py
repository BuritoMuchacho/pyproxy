import csv
import requests
import subprocess


class Proxy:
    """
    Main proxy class
    """
    __url = f'https://www.proxyscan.io/api/proxy?'  # API url


    def proxy(self, check=True, type=None, country_code=None, level=None) -> dict:
        """Returns a proxy as dictionary {'type': 'type://ip:port'}

        Args:
            check (bool, optional): check proxies' workability. Defaults to True.
            type (str, optional): proxy protocol. Defaults to None.
            country_code (str, optional): ISO code to search proxy. Defaults to None.
            level (str, optional): anonymity level. Defaults to None.

        Returns:
            dict: a dictionary containing connection type and address
        """

        if type:
            self.__url += f'type={type}&'  # search by protocol
        if country_code:
            self.__url += f'country={country_code.lower()}&'  # search by country code
        if level:
            self.__url += f'level={level.lower()}&'  # search by anonymity level

        while True:
            try:
                my_dict = requests.get(self.__url).json()[0]  # get a dict out of json  
            except:
                raise Exception('Invalid parameters')
            ctype = my_dict['Type'][0].lower() if len(my_dict['Type']) == 1 else my_dict['Type'][1].lower()  # get proxy protocol
            proxy = {ctype: f"{ctype}://{my_dict['Ip']}:{my_dict['Port']}"}  # dict with proxy
            if not check:
                return proxy
            else:
                try:
                    # try to get responce with proxy and return proxy if succeed
                    requests.get('https://api.myip.com', proxies=proxy, timeout=5 if ctype == 'https' else 2)
                    return proxy
                except:
                    continue


    def dict_proxies(self, num: int, check=True, type=None, country_code=None, level=None) -> list:
        """Returns a list of proxy dictionaries {'type': 'type://ip:port'}

        Args:
            num (int): a number of proxies to return.
            check (bool, optional): check proxies' workability. Defaults to True.
            type (str, optional): proxy protocol. Defaults to None.
            country_code (str, optional): ISO code to search proxy. Defaults to None.
            level (str, optional): anonymity level. Defaults to None.

        Returns:
            list: list of dictionaries with proxies
        """
        if type:
            self.__url += f'type={type}&'  # search by protocol
        if country_code:
            self.__url += f'country={country_code.lower()}&'  # search by country code
        if level:
            self.__url += f'level={level.lower()}&'  # search by anonymity level

        proxies = []  # list of proxies
        for _ in range(num):
            my_dict = requests.get(self.__url).json()[0]  # get a dict out of json      
            ctype = my_dict['Type'][0].lower() if len(my_dict['Type']) == 1 else my_dict['Type'][1].lower()  # get proxy protocol
            proxy = {ctype: f"{ctype}://{my_dict['Ip']}:{my_dict['Port']}"}  # dict with proxy
            if not check:
                proxies.append(proxy)  # add proxy to list
            else: 
                try:
                    # try to get responce with proxy
                    requests.get('https://api.myip.com', proxies=proxy, timeout=5 if ctype == 'https' else 2)
                    proxies.append(proxy)  # add proxy to list
                except:
                    # if previous proxy failed
                    proxies.append(self.proxy(type=type, country_code=country_code, level=level))  # get proxy by same filters
                    continue 
        return proxies
       

    def list_proxies(self, num: int, check=True, type=None, country_code=None, level=None) -> list:
        """Returns a list of proxy addresses

        Args:
            num (int): a number of proxies to return.
            check (bool, optional): check proxies' workability. Defaults to True.
            type (str, optional): proxy protocol. Defaults to None.
            country_code (str, optional): ISO code to search proxy. Defaults to None.
            level (str, optional): anonymity level. Defaults to None.

        Returns:
            list: list of strings with proxy addresses
        """
        if type:
            self.__url += f'type={type}&'  # search by protocol
        if country_code:
            self.__url += f'country={country_code.lower()}&'  # search by country code
        if level:
            self.__url += f'level={level.lower()}&'  # search by anonymity level

        proxies = []  # list of proxies
        for _ in range(num): 
            my_dict = requests.get(self.__url).json()[0]  # get a dict out of json
            ctype = my_dict['Type'][0].lower() if len(my_dict['Type']) == 1 else my_dict['Type'][1].lower()  # get proxy protocol    
            proxy = f"{my_dict['Type'][0].lower() if len(my_dict['Type']) == 1 else my_dict['Type'][1].lower()}://{my_dict['Ip']}:{my_dict['Port']}"  # string with proxy address
            if not check:
                proxies.append(proxy)  # add proxy to list
            else: 
                try:
                    # try to get responce with proxy
                    requests.get('https://api.myip.com', proxies={ctype: proxy}, timeout=5 if ctype == 'https' else 2)
                    proxies.append(proxy)  # add proxy to list
                except:  
                    # if previous proxy failed
                    proxies.append(self.proxy(type=type, country_code=country_code, level=level))  # get proxy by same filters
                    continue
        return proxies


    def to_csv(self, num: int, check=True, type=None, country_code=None, level=None):  
        """Writes proxies to csv file

        Args:
            num (int): a number of proxies to return.
            check (bool, optional): check proxies' workability. Defaults to True.
            type (str, optional): proxy protocol. Defaults to None.
            country_code (str, optional): ISO code to search proxy. Defaults to None.
            level (str, optional): anonymity level. Defaults to None.
        """

        def error(type=type, country_code=country_code, level=level):
            """Gets 1 proxy if the previous one has failed

            Args:
                type (str, optional): proxy protocol. Defaults to None.
                country_code (str, optional): ISO code to search proxy. Defaults to None.
                level (str, optional): anonymity level. Defaults to None.

            Returns:
                func: write proxy to file
            """
            if type:
                self.__url += f'type={type}&'  # search by protocol
            if country_code:
                self.__url += f'country={country_code.lower()}&'  # search by country code
            if level:
                self.__url += f'level={level.lower()}&'  # search by anonymity level

            my_dict = requests.get(self.__url).json()[0]  # get a dict out of json      
            ctype = my_dict['Type'][0].lower() if len(my_dict['Type']) == 1 else my_dict['Type'][1].lower()  # get proxy protocol
            proxy = {ctype: f"{ctype}://{my_dict['Ip']}:{my_dict['Port']}"}  # dict with proxy

            try:
                # try to get responce with proxy
                requests.get('https://api.myip.com', proxies=proxy, timeout=5 if ctype == 'https' else 2)
                return writer.writerow([ctype, my_dict['Ip'], my_dict['Port'], my_dict['Location']['country'], my_dict['Anonymity']])  # write proxy to csv
            except:
                error()  # repeat if previous failed


        if type:
            self.__url += f'type={type}&'  # search by protocol
        if country_code:
            self.__url += f'country={country_code.lower()}&'  # search by country code
        if level:
            self.__url += f'level={level.lower()}&'  # search by anonymity level

        with open('proxies.csv', 'w', newline='', encoding='utf-8') as f:  # open/create csv file
            writer = csv.writer(f, delimiter=',')  # initialize writer
            writer.writerow(['Type', 'Address', 'Port', 'Country', 'Anonymity'])  # write first row

            for _ in range(num):
                my_dict = requests.get(self.__url).json()[0]  # get a dict out of json      
                ctype = my_dict['Type'][0].lower() if len(my_dict['Type']) == 1 else my_dict['Type'][1].lower()  # get proxy protocol
                if not check:
                    writer.writerow([ctype, my_dict['Ip'], my_dict['Port'], my_dict['Anonymity']])  # write proxy to file
                else:
                    proxy = {ctype: f"{ctype}://{my_dict['Ip']}:{my_dict['Port']}"}  # dict with proxy
                    try:
                        # try to get responce with proxy
                        requests.get('https://api.myip.com', proxies=proxy, timeout=5 if ctype == 'https' else 2)
                        writer.writerow([ctype, my_dict['Ip'], my_dict['Port'], my_dict['Location']['country'], my_dict['Anonymity']])  # write proxy to file
                    except:
                        error()  # run error function if previous proxy failed
                        continue
            

    def connect(self, check=True, type=None, country_code=None, level=None):
        """Establish connection with proxy server (macOS)

        Args:
            check (bool, optional): check proxies' workability. Defaults to True.
            type (str, optional): proxy protocol. Defaults to None.
            country_code (str, optional): ISO code to search proxy. Defaults to None.
            level (str, optional): anonymity level. Defaults to None.

        Returns:
            func: establish connection with proxy 
        """
        ip = list(self.proxy(check=check, type=type, country_code=country_code, level=level).items())[0][1]  # get proxy ip

        # execute commands to connect to proxy depending on protocol
        if ip.split("://")[0] == 'https':
            subprocess.call(['networksetup -setsecurewebproxy "Wi-Fi" '
                f'"{ip.split("://")[1].split(":")[0]}" "{ip.split("//")[1].split(":")[1]}"'], shell=True)
        elif ip.split("://")[0] == 'http':
            subprocess.call(['networksetup -setwebproxy "Wi-Fi" '
                f'"{ip.split("://")[1].split(":")[0]}" "{ip.split("//")[1].split(":")[1]}"'], shell=True)
        elif ip.split("://")[0] == 'socks4' or 'socks5':
            subprocess.call(['networksetup -setsocksfirewallproxy "Wi-Fi" '
                f'"{ip.split("://")[1].split(":")[0]}" "{ip.split("//")[1].split(":")[1]}"'], shell=True)
        else:
            raise Exception('Unknown proxy connection type')

        return print(f'Successfully connected to {ip}')


    @staticmethod
    def disconnect(type=None):
        """Disconnect your device drom proxy (macOS)

        Args:
            type (str, optional): proxy protocol. Defaults to None.

        Returns:
            func: disconnect from proxy
        """
        # execute commands to disconnect from proxies depending on protocol
        if type == 'https':
            subprocess.call(['networksetup -setsecurewebproxystate "Wi-Fi" "off"'], shell=True)
        elif type == 'http':
            subprocess.call(['networksetup -setwebproxystate "Wi-Fi" "off"'], shell=True)
        elif type == 'socks4' or type == 'socks5':
            subprocess.call(['networksetup -setsocksfirewallproxystate "Wi-Fi" "off"'], shell=True)
        else:
            subprocess.call(['networksetup -setsecurewebproxystate "Wi-Fi" "off"'], shell=True)
            subprocess.call(['networksetup -setwebproxystate "Wi-Fi" "off"'], shell=True)
            subprocess.call(['networksetup -setsocksfirewallproxystate "Wi-Fi" "off"'], shell=True)

        return print('Successfully disconnected')
