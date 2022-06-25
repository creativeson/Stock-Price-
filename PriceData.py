import yfinance as yf
import streamlit as st
import pandas as pd
import time
from datetime import date

st.write("""
#  Stock Price & Data App
You can pick stock to know their price, volume and some financial data here. There is a S&P 500 selection list on the left side. You can also type your favorite stock below.  
""")


@st.cache #you don't have to load every time
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df_sp500 = load_data()


#create a list to give selection for sidebar
sp500 = []
for i in range(503):
    sp500.append(df_sp500['Symbol'][i])
print(sp500)

st.sidebar.header("user input")
selected_company = st.sidebar.selectbox('Symbol', sp500)

selected_company = st.text_input('type company symbol here',selected_company)


# define the ticker symbol
tickerSymbol = selected_company

# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# get the historical prices for this ticker and update to current day
tickerDf = tickerData.history(period='1d', start='2012-5-11', end=date.today())


#create a dataframe that user select
df = pd.DataFrame(columns=['Stock',
                           'Company',
                           'Industry',
                           'GrossMargins',
                           'ebitdaMargins',
                           'ProfitMargins',
                           'Beta',                        
                           'FullTimeEmployees'])

info = yf.Ticker(selected_company).info


shortName = info['shortName']
industry = info['industry']
grossMargins = info['grossMargins']
ebitdaMargins = info['ebitdaMargins']
profitMargins = info['profitMargins']
beta = info['beta']
fullTimeEmployees = info['fullTimeEmployees']

st.write('The current company name is', shortName)

df = df.append({'Stock':selected_company,
                'Company':shortName,
                'Industry':industry,
                'GrossMargins': '{: .2%}'.format(grossMargins),
                'ebitdaMargins': '{: .2%}'.format(ebitdaMargins),
                'ProfitMargins': '{: .2%}'.format(profitMargins),
                'Beta':beta,
                'FullTimeEmployees':fullTimeEmployees,
               }, ignore_index=True).set_index('Stock') #remove index 0

st.table(df)

#to find exact price
def current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='5d')
    return todays_data['Close']

#to find latest date
def current_date(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='5d')
    return todays_data.index[4]


new_price = round(current_price(selected_company)[4],2)
yesterday_prace = round(current_price(selected_company)[3],2)
week_ago_price = round(current_price(selected_company)[0],2)
day_difference_p = (new_price-yesterday_prace)/yesterday_prace
week_difference_p = (new_price-week_ago_price)/week_ago_price
day_difference = round(new_price-yesterday_prace ,2)

#count market capital of selected company


mc = round(info['sharesOutstanding'] * new_price/1000000000, 2)

mc_difference = round(day_difference * info['sharesOutstanding']/1000000000,2)

#remove the timestamp
new_date = current_date(selected_company).date()

col1, col2, col3= st.columns(3)
col1.metric("Stock price (USD) "+ str(new_date), new_price, day_difference)
col2.metric("Change percentage(day)", '{: .2%}'.format(day_difference_p))
col2.metric("Change persentage(week)", '{: .2%}'.format(week_difference_p))
col3.metric("Market cap(billion)", mc, mc_difference)


st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume, height = 1)

st.markdown(f'<h1 style="color:#B8472F;font-size:24px;">{"recent news"}</h1>', unsafe_allow_html=True)

title = []
link = []

#create news title and link
for i in range(5):
    title.append(tickerData.news[i]['title'])
    link.append("[link]("+tickerData.news[i]['link']+")")

for i, j in zip(title, link):
    st.write(f"{i} {j}")
    

# GICS = df_sp500[df_sp500['Symbol']== selected_company]['GICS Sub-Industry']            
# st.write(GICS)            

try:
    GICS = df_sp500[df_sp500['Symbol']== selected_company]['GICS Sub-Industry'].reset_index(drop=True) 
    df_GICS = df_sp500[df_sp500['GICS Sub-Industry']== GICS[0]].reset_index(drop=True).drop(columns=['SEC filings'])        
    df_GICS
except:
    pass