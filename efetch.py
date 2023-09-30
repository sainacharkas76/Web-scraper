import json
import time
from functions import medline_formatting, progress_bar

class Efetch:
    def __init__(self, session, UIDs):
        self.session = session
        self.UIDs = UIDs
    
    def get_data_UID(self, UID):
        time.sleep(0.4)
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&rettype=medline&id='
        url = url + UID
        site = self.session.get(url).content

        data = site.decode()
        data = medline_formatting(data)

        return data
    
    def get_data_UIDs(self):
        titles  = []
        pubblication_dates = []
        abstracts = []
        journal_titles = []
        cois = []
        dois = []
        authors = []
        keywords = []
        pubblication_types = []

        count = 1
        i = 0
        while i < len(self.UIDs):
            UID = self.UIDs[i]
            data = self.get_data_UID(UID)

            title = self.get_title(data)
            pubblication_date = self.get_pubblication_date(data)
            abstract = self.get_abstract(data)
            journal_title = self.get_journal_title(data)
            coi = self.get_coi(data)
            doi = self.get_doi(data)
            author = self.get_authors(data)
            keyword = self.get_keywords(data)
            pubblication_type = self.get_pubblication_type(data)

            if title == None and pubblication_date == None and abstract == None and doi == None:
                self.UIDs.sort(key = UID.__eq__)
                continue

            titles.append(title)
            pubblication_dates.append(pubblication_date)
            abstracts.append(abstract)
            journal_titles.append(journal_title)
            cois.append(coi)
            dois.append(doi)
            authors.append(author)
            keywords.append(keyword)
            pubblication_types.append(pubblication_type)

            progress_bar(count, len(self.UIDs))
            count += 1

            i += 1

        dict = {
            'PMID' : self.UIDs,
            'doi' : dois,
            'Title': titles,
            'Publication Date' : pubblication_dates,
            'Journal Title' : journal_titles,
            'Authors' : authors,
            'Keywords' : keywords,
            'Abstract' : abstracts,
            'Publication type' : pubblication_types,
            'Conflict Of Interests': cois,
        }

        return dict

    
    def get_pubblication_date(self, data):
        for tag in data:
            if tag[0] == 'DP':
                return tag[1]
    
    def get_title(self, data):
        for tag in data:
            if tag[0] == 'TI':
                return tag[1]
    
    def get_abstract(self, data):
        for tag in data:
            if tag[0] == 'AB':
                return tag[1]
    
    def get_journal_title(self, data):
        for tag in data:
            if tag[0] == 'JT':
                return tag[1]
                
    def get_coi(self, data):
        for tag in data:
            if tag[0] == 'COIS':
                return tag[1]
    
    def get_doi(self, data):
        for tag in data:
            if tag[0] == 'LID' and tag[1][-5:] == '[doi]':
                return tag[1][:-6]
            if tag[0] == 'AID' and tag[1][-5:] == '[doi]':
                return tag[1][:-6]
    
    def get_authors(self, data):
        all_AU = ''
        for tag in data:
            if tag[0] == 'AU':
                all_AU = all_AU + tag[1] + ', '
        return all_AU[:-2]
    
    def get_keywords(self,data):
        all_keywords = ''
        for tag in data:
            if tag[0] == 'OT' or tag[0] == 'MH':
                all_keywords = all_keywords + tag[1] + ', '
        return all_keywords[:-2]
    
    def get_pubblication_type(self, data):
        all_attributes = ''
        for tag in data:
            if tag[0] == 'PT':
                all_attributes = all_attributes + tag[1] + ', '
        return all_attributes[:-2]
