import json 

class Esearch:
    def __init__(self, session, string):
        self.session = session
        self.string = string.replace(' ', '+')
    
    def get_count(self):
        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&rettype=count&format=json&term='
        url = base_url + self.string

        site = self.session.get(url).content
        json_site = json.loads(site)

        return json_site['esearchresult']['count']
    

    def get_uids(self, max):
        print('Retriving up to ' + str(max) + ' UIDs for the search "' + self.string + '"')

        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
        db = '?db=pubmed'
        term = '&term=' + self.string.replace(' ', '+')
        retmode = '&retmode=json'

        all_UIDs = []
        if max > 100000:

            retstart = 0
            count = int(self.get_count())
            retmax = '&retmax=100000'

            while max > retstart:
                url = base_url + db + term + retmode + '&retstart='+str(retstart) + retmax
                site = self.session.get(url).content
                json_site = json.loads(site.decode())

                all_UIDs = all_UIDs + json_site['esearchresult']['idlist']

                retstart = retstart + 100000
                retmax = max-retstart
                
                if retmax > 100000:
                    retmax = 100000
                retmax = '&retmax='+str(retmax)

        else:
            retmax = '&retmax=' + str(max)
            url = base_url + db + term + retmode + retmax
            site = self.session.get(url).content
            json_site = json.loads(site)
            
            all_UIDs = json_site['esearchresult']['idlist']

        print('Retrieved ' + str(len(all_UIDs)) + ' UIDs')
        return all_UIDs

        
