from pytrends.request import TrendReq
import pandas
import os

if(__name__ == "__main__"):
    with open(os.path.dirname(__file__) + '/techno.txt') as f:
        lines = f.readlines()
        for techno in lines:
            pytrends = TrendReq(hl='en-US', tz=360)
            pytrends.build_payload(kw_list=[techno])

            df = pytrends.interest_over_time()
            print(df)
