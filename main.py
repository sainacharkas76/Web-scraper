import requests
import time
import pandas as pd
from esearch import Esearch
from efetch import Efetch
from parser import parser
import functions

if __name__ == '__main__':

    my_parser = parser()
    args = my_parser.parse_args()

    if args.string.strip() == '':
        print('Please insert a valid string')
        quit()
    
    session = requests.Session()
    search = Esearch(session, args.string)

    if args.all:
        UIDs_list = search.get_uids(int(E.get_count()))
    else:
        UIDs_list = search.get_uids(args.quantity)

    time.sleep(2)

    if len(UIDs_list) == 0:
        print('No papers were found from the search')
        print('Try a different search term')
        quit()

    fetch = Efetch(session, UIDs_list)
    df = fetch.get_data_UIDs()
    pandas_df = pd.DataFrame(df)

    print("All papers' information have been retrieved")

    if args.score:
      dictionary = functions.request_words()
      if len(dictionary) == 0:
        print('The dictionary is empty. The scores will not be computed')
      else:
        print('Computing Scores') 
        scores = functions.compute_score(pandas_df, dictionary) 
        pandas_df['Score'] = scores
        print('Scores Computed')
    
    if args.format == 'csv':
        pandas_df.to_csv('database.csv', index=False)
    else:
        pandas_df.to_json('database.json')
    
    print('The database has been saved')
