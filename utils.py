from core.constans import COUNTRY_CODE

def extract_country_name(l):
    return [item['country'] for item in l]



country_list = COUNTRY_CODE

if __name__ == '__main__':
    print(extract_country_name(country_list))