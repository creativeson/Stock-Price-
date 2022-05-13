import yfinance as yf
import streamlit as st
import pandas as pd
import time
from datetime import date


st.write("""
#  Stock Price & Data App
Shown are the stock closing price and volume of sp500 stock!
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
for i in range(504):
    sp500.append(df_sp500['Symbol'][i])
print(sp500)

st.sidebar.header("user input")
selected_company = st.sidebar.selectbox('Symbol', sp500)

title = st.text_input('company symbol', str(selected_company))


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
                           'ProfitMargins',
                           'Beta',
                           'Marketcap',
                           'FullTimeEmployees'])

info = yf.Ticker(selected_company).info

longName = info['longName']
industry = info['industry']
grossMargins = info['grossMargins']
profitMargins = info['profitMargins']
beta = info['beta']
marketcap = info['marketCap']
fullTimeEmployees = info['fullTimeEmployees']

st.write('The current company name is', longName)

df = df.append({'Stock':selected_company,
                'Company':longName,
                'Industry':industry,
                'GrossMargins': '{: .2%}'.format(grossMargins),
                'ProfitMargins': '{: .2%}'.format(profitMargins),
                'Beta':beta,
                'Marketcap':marketcap, 
                'FullTimeEmployees':fullTimeEmployees,
               }, ignore_index=True)

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


c4 = round(current_price(selected_company)[4],2)
c1 = round(current_price(selected_company)[1],2)
c0 = round(current_price(selected_company)[0],2)
p1 = (c1-c0)/c0
p2 = (c4-c0)/c0
p3 = round(c1-c0 ,2)
#remove the timestamp
new_date = current_date(selected_company).date()

col1, col2, col3 = st.columns(3)
col1.metric("Stock price (USD) "+ str(new_date), c1, p3)
col2.metric("percentage(day)", '{: .2%}'.format(p1))
col2.metric("persentage(week)", '{: .2%}'.format(p2))

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)

df_sp500
