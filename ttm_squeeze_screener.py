import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
from finta import TA

# Set the display option to show 2 decimal places and 1000 rows
pd.set_option('display.float_format', '{:.2f}'.format)
st.set_page_config(page_title='TTM Squeeze Screener',
                   page_icon=None,
                   layout="wide")

# Initialize S&P500 Tickers
sp500 = [
  'MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ATVI', 'ADM', 'ADBE', 'ADP', 'AAP',
  'AES', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALGN', 'ALLE',
  'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AMD', 'AEE', 'AAL',
  'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH',
  'ADI', 'ANSS', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ACGL', 'ANET', 'AJG',
  'AIZ', 'T', 'ATO', 'ADSK', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL',
  'BAC', 'BBWI', 'BAX', 'BDX', 'WRB', 'BBY', 'BIO', 'TECH', 'BIIB', 'BLK',
  'BK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BG',
  'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR',
  'CTLT', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CDAY', 'CF',
  'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS',
  'CSCO', 'C', 'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA',
  'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CTVA',
  'CSGP', 'COST', 'CTRA', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI',
  'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DIS',
  'DG', 'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DTE', 'DUK', 'DD', 'DXC', 'EMN',
  'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'ELV', 'LLY', 'EMR', 'ENPH',
  'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ETSY',
  'EG', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS',
  'FICO', 'FAST', 'FRT', 'FDX', 'FITB', 'FSLR', 'FE', 'FIS', 'FI', 'FLT',
  'FMC', 'F', 'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT',
  'GEHC', 'GEN', 'GNRC', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GL', 'GPN',
  'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'PEAK', 'HSIC', 'HSY', 'HES', 'HPE',
  'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUM', 'HBAN',
  'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'ILMN', 'INCY', 'IR', 'PODD', 'INTC',
  'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', 'IRM',
  'JBHT', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KDP', 'KEY',
  'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KHC', 'KR', 'LHX', 'LH', 'LRCX',
  'LW', 'LVS', 'LDOS', 'LEN', 'LNC', 'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW',
  'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA',
  'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM',
  'MCHP', 'MU', 'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR',
  'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NWL',
  'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI', 'NDSN', 'NSC', 'NTRS', 'NOC',
  'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC',
  'ON', 'OKE', 'ORCL', 'OGN', 'OTIS', 'PCAR', 'PKG', 'PANW', 'PARA', 'PH',
  'PAYX', 'PAYC', 'PYPL', 'PNR', 'PEP', 'PFE', 'PCG', 'PM', 'PSX', 'PNW',
  'PXD', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU',
  'PEG', 'PTC', 'PSA', 'PHM', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF',
  'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RVTY', 'RHI', 'ROK', 'ROL',
  'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE',
  'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SNA', 'SEDG', 'SO', 'LUV', 'SWK',
  'SBUX', 'STT', 'STLD', 'STE', 'SYK', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW',
  'TTWO', 'TPR', 'TRGP', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN',
  'TXT', 'TMO', 'TJX', 'TSCO', 'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL',
  'TSN', 'USB', 'UDR', 'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS',
  'VLO', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VTRS', 'VICI', 'V',
  'VMC', 'WAB', 'WBA', 'WMT', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL',
  'WST', 'WDC', 'WRK', 'WY', 'WHR', 'WMB', 'WTW', 'GWW', 'WYNN', 'XEL',
  'XYL', 'YUM', 'ZBRA', 'ZBH', 'ZION', 'ZTS'
]

etfs = [
  'SQQQ', 'TQQQ', 'SPY', 'SOXS', 'SOXL', 'QQQ', 'XLF', 'PSQ', 'HYG', 'FXI',
  'LABU', 'EEM', 'IWM', 'TLT', 'TMF', 'EWZ', 'SPXU', 'SPXS', 'LQD', 'KWEB',
  'XLE', 'UNG', 'SH', 'GDX', 'KRE', 'QID', 'ARKK', 'SLV', 'TSLL', 'UVXY',
  'RSX', 'XLU', 'EFA', 'TZA', 'TNA', 'XLP', 'UVIX', 'IEMG', 'BITO', 'FNGD',
  'GOVT', 'VXX', 'XLV', 'VEA', 'XLI', 'SPXL', 'VWO', 'AGG', 'JNK', 'SMH',
  'JDST', 'IEFA', 'IEF', 'BIL', 'EWJ', 'BKLN', 'XBI', 'XLK', 'IYR', 'XLB',
  'SDOW', 'GLD', 'GDXJ', 'XLC', 'UPRO', 'BND', 'MSOS', 'YANG', 'EMB', 'SPTL',
  'USHY', 'XRT', 'SDS', 'RSP', 'QYLD', 'XLRE', 'XLY', 'SHY', 'VCIT', 'SPDN',
  'IAU', 'SPIB', 'VNQ', 'DUST', 'SJNK', 'LABD', 'JEPI', 'QLD', 'BOIL', 'IVV',
  'VOO', 'XOP', 'VCSH', 'IGSB', 'VIXY', 'USFR', 'MCHI', 'SPTI', 'JPST',
  'ASHR'
]


combined_list = []
combined_list = sp500 + etfs


# Define Data Download Function
# Downloads historical data for each ticker as a bulk package (MultiIndex df)
@st.cache_data(ttl=3500)
def download_data(tickers):
  # Download historical stock data for each ticker
  data = yf.download(tickers=tickers, period='200d')
  return data

# Define Squeeze Screener Function
@st.cache_data(ttl=3500)
def squeeze_screener(data, atr_mult=1.4):
  
  # Extract each ticker out of the MultiIndex df
  tickers = list(data.columns.get_level_values(1).unique())
  
  #Technical Indicator Parameters
  period = 20  # Indicator smoothing legth for BB and ATR
  atr_mult = atr_mult  # ATR Multiplier for Keltner Channels
  bb_stdev = 2  # Std multiplier for BB

  squeeze_tickers = pd.DataFrame()

  for ticker in tickers:
    # Create a working dataframe for the active ticker. This transforms it to a Single Index df
    df = data.loc[:, (slice(None), ticker)].copy()
    df.columns = df.columns.droplevel(1)

    # Convert columns to lowercase for finta/TA
    df.columns = df.columns.str.lower()

    # Add ticker ID column. Calculate Average Volume
    df['ticker'] = ticker
    df['avg volume'] = df['volume'].rolling(len(df)).mean() / 1000000

    # Calculate Range and EMA. Needed for downstream calculations
    df['EMA'] = df['close'].ewm(span=period, adjust=False).mean()
    df['Range'] = df['high'] - df['low']
    df['ATR'] = df['Range'].ewm(span=period, adjust=False).mean()
    df['Std'] = df['close'].rolling(period).std()

    # Calculate BB for EMA
    df['BB Low'] = df['EMA'] - bb_stdev * df['Std']
    df['BB High'] = df['EMA'] + bb_stdev * df['Std']

    # Calculate Keltner for EMA. ATR is needed for this calc
    df['Keltner Low'] = df['EMA'] - atr_mult * df['ATR']
    df['Keltner High'] = df['EMA'] + atr_mult * df['ATR']

    # Calculate SMA/EMAs
    df['SMA5'] = df['close'].rolling(5).mean()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()
    df['EMA100'] = df['close'].ewm(span=100, adjust=False).mean()
    df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()

    # Calculate Donchian Channel
    df['Donchian High'] = df['close'].rolling(period).max()
    df['Donchian Low'] = df['close'].rolling(period).min()
    df['Donchian Mid'] = (df['Donchian High'] + df['Donchian Low']) / 2

    # Calculate TTM Squeeze
    df['TTM Hist'] = df['SMA5'] - df['Donchian Mid']
    squeeze_on = (df['BB Low'] > df['Keltner Low']) | (df['BB High'] < df['Keltner High'])
    df['Squeeze'] = squeeze_on

    ### Initialized 'Condition' column (0 day, 1 day, or 2 day)
    df['Condition'] = None
    df['EMA Trend'] = None
    df['TTM Trend'] = None

    # Condition = Multiple EMAs are stacked upwards or downward
    c_stacked_ema_up = (df['close'].iloc[-1] > df['EMA20'].iloc[-1]) and (df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1]) and (df['EMA50'].iloc[-1] > df['EMA100'].iloc[-1])
    c_stacked_ema_down = (df['close'].iloc[-1] < df['EMA20'].iloc[-1]) and (df['EMA20'].iloc[-1] < df['EMA50'].iloc[-1]) and (df['EMA50'].iloc[-1] < df['EMA100'].iloc[-1]) 

    # Condition = TTM Histogram positive or negative
    c_ttmhist_up = df['TTM Hist'].iloc[-1] > 0
    c_ttmhist_down = df['TTM Hist'].iloc[-1] < 0

    # Condition = Squeeze fired today (0 day prior)
    c_sq_fire0 = df['Squeeze'].iloc[-3]==True and df['Squeeze'].iloc[-2]==True and df['Squeeze'].iloc[-1]==False

    # Condition = Squeeze fired 1 day prior
    c_sq_fire1 = df['Squeeze'].iloc[-4]==True and df['Squeeze'].iloc[-3]==True and df['Squeeze'].iloc[-2]==False

    # Condition = Squeeze fired 2 day prior
    c_sq_fire2 = df['Squeeze'].iloc[-5]==True and df['Squeeze'].iloc[-4]==True and df['Squeeze'].iloc[-3]==False

    # Condition = Squeeze not yet fired (in accumulation for at least 2 days)
    c_sq = df['Squeeze'].iloc[-1]==True and df['Squeeze'].iloc[-2]==True and df['Squeeze'].iloc[-3]==True

    if c_stacked_ema_up or c_stacked_ema_down:
      if c_stacked_ema_up:
        df.loc[df.index[-1], 'EMA Trend'] = 'Up'
      else:
        df.loc[df.index[-1], 'EMA Trend'] = 'Down'
    else:
      df.loc[df.index[-1], 'EMA Trend'] = 'Mixed'

    if c_ttmhist_up:
      df.loc[df.index[-1], 'TTM Trend'] = 'Up'
    else:
      df.loc[df.index[-1], 'TTM Trend'] = 'Down'

    if c_sq_fire0 or c_sq_fire1 or c_sq_fire2 or c_sq:
      if c_sq_fire0:
        df.loc[df.index[-1], 'Condition'] = '0 day'
      elif c_sq_fire1:
        df.loc[df.index[-1], 'Condition'] = '1 day'
      elif c_sq_fire2:
        df.loc[df.index[-1], 'Condition'] = '2 day'
      elif c_sq:
        df.loc[df.index[-1], 'Condition'] = 'Squeezed'

    squeeze_tickers = pd.concat([squeeze_tickers, df.iloc[[-1]]], axis=0)

  squeeze_tickers = squeeze_tickers.sort_values('avg volume', ascending=False).dropna()

  return squeeze_tickers


@st.cache_data(ttl=3500)
def ema_crossover(data, ema_fast=20, ema_slow=50):

  # Extract each ticker out of the MultiIndex df
  tickers = list(data.columns.get_level_values(1).unique())

  # EMA length parameters
  ema_fast = ema_fast
  ema_slow = ema_slow

  ema_crossover_stocks = pd.DataFrame()

  # For all tickers submitted, download historical stock data, and calculate
  # technical indiators using the parameters above
  for ticker in tickers:
    # Create a working dataframe for the active ticker. This transforms it to a Single Index df
    df = data.loc[:, (slice(None), ticker)].copy()
    df.columns = df.columns.droplevel(1)

    # Convert columns to lowercase for finta/TA
    df.columns = df.columns.str.lower()

    # Add ticker ID column. Calculate Average Volume
    df['ticker'] = ticker
    df['avg volume'] = df['volume'].rolling(len(df)).mean() / 1000000

    # Calculate indicators
    df['ema_fast'] = TA.EMA(df, period=ema_fast)
    df['ema_slow'] = TA.EMA(df, period=ema_slow)
    df['ema_hist'] = df['ema_fast'] - df['ema_slow']
    df['fast RSI'] = TA.RSI(df, period=14)
    df['RSI'] = df['fast RSI'].rolling(5).mean()
    df['ADX'] = TA.ADX(df, period=20)

    # Condition 1 = (ema_hist[-1] > 0) and (ema_hist[-2] < 0) = crossover up
    # Condition 2 = (ema_hist[-1] < 0) and (ema_hist[-2] > 0) = crossover down
    # iloc[-4] was chosen to include crossovers 3-days prior
    
    c_ema_up = (df['ema_hist'].iloc[-1] > 0) and (df['ema_hist'].iloc[-4] < 0)
    c_rsi_up = df['RSI'].iloc[-1] > 60
    c_adx_up = df['ADX'] > 20
    c_long = c_ema_up & c_rsi_up & c_adx_up

    c_ema_dn = (df['ema_hist'].iloc[-1] < 0) and (df['ema_hist'].iloc[-4] > 0)
    c_rsi_dn = df['RSI'].iloc[-1] < 40
    c_adx_dn = df['ADX'] > 20
    c_short = c_ema_dn & c_rsi_dn & c_adx_dn
    

    # If crossover is detected, label up or down, then store the Ticker
    
    df['direction'] = None

    if c_long:
      df.loc[df.index[-1], 'direction'] = 'up'
      ema_crossover_stocks = pd.concat([ema_crossover_stocks, df.iloc[[-1]]], axis=0)

    elif c_short:
      df.loc[df.index[-1], 'direction'] = 'down'
      ema_crossover_stocks = pd.concat([ema_crossover_stocks, df.iloc[[-1]]], axis=0)

  try:
    ema_crossover_stocks = ema_crossover_stocks.sort_values('avg volume', ascending=False)
  except:
    st.text('No Tickers Found')

  return ema_crossover_stocks


@st.cache_data(ttl=3500)
def turtle_screener(data, dc_period=20):

  # Extract each ticker out of the MultiIndex df
  tickers = list(data.columns.get_level_values(1).unique())

  turtle_stocks = pd.DataFrame()

  # For all tickers submitted, download historical stock data, and calculate
  # technical indiators using the parameters above
  for ticker in tickers:
    # Create a working dataframe for the active ticker. This transforms it to a Single Index df
    df = data.loc[:, (slice(None), ticker)].copy()
    df.columns = df.columns.droplevel(1)

    # Convert columns to lowercase for finta/TA
    df.columns = df.columns.str.lower()

    # Add ticker ID column. Calculate Average Volume
    df['ticker'] = ticker
    df['avg volume'] = df['volume'].rolling(len(df)).mean() / 1000000

    # Calculate indicators
    df['rolling high'] = df['close'].rolling(20).max()
    df['ema'] = TA.EMA(df, period=50)
    df['ATR'] = TA.ATR(df, period=20)
    df['rsi'] = TA.RSI(df, period=14)
    df['long stop'] = df['rolling high'] - 3 * df['ATR']

    # Condition 1 = "Previous Close is greater than the prior rolling high, day-1"
    # Condition 2 = "Previous Close is greater than the prior rolling high, day-2"
    # Condition 3 = "Previous close is greater than the 50-day EMA"
    c1 = df['close'].iloc[-1] >= df['rolling high'].iloc[-1]
    c2 = df['close'].iloc[-2] >= df['rolling high'].iloc[-2]
    c3 = df['close'].iloc[-1] >= df['ema'].iloc[-1]

    # If both conditions are met, store the Ticker
    if c1 and c2 and c3:
      turtle_stocks = pd.concat([turtle_stocks, df.iloc[[-1]]], axis=0)

  try:
    turtle_stocks = turtle_stocks.sort_values('avg volume', ascending=False)
  except:
    st.text('No Tickers Found')

  return turtle_stocks


####################
####################
####################


## Download data and set up data tables
data = download_data(combined_list)

tab1, tab2, tab3 = st.tabs(['TTM Squeeze', 'EMA Crossover', 'Turtle Trend'])

## Tab1 - TTM Squeeze Layout

with tab1:

  col1, col2 = st.columns([2, 1])

  with col2:
    squeeze_config_col1, squeeze_config_col2 = st.columns(2)
    with squeeze_config_col1:
        kc = st.number_input('KC', min_value=0.5, max_value=2.0, value=1.4,step=0.5)
    with squeeze_config_col2:
        vol = st.number_input('Volume', min_value=0.0, value=3.0, key=1)

    squeeze_targets = squeeze_screener(data, kc)
    squeeze_targets = squeeze_targets.set_index('ticker')
    squeeze_targets = squeeze_targets[[
        'avg volume', 'close', 'Condition', 'EMA Trend', 'TTM Trend'
    ]].sort_values(by=['Condition', 'avg volume'], ascending=[True, False])
    squeeze_targets = squeeze_targets[squeeze_targets['avg volume'] >= vol]

    inner_col1, inner_col2 = st.columns([3, 1])

    with inner_col1:
      st.table(squeeze_targets)
    with inner_col2:
      view_ticker = st.radio('Ticker', options=squeeze_targets.index)

  # Tradingview embed
  with col1:
    components.html(f'''
      <!-- TradingView Widget BEGIN -->
      <div class="tradingview-widget-container">
        <div id="tradingview_b5094"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget(
        {{
        "width": "100%",
        "height": 700,
        "symbol": "{view_ticker}",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "details": true,
        "studies": [
          "STD;Awesome_Oscillator",
          "STD;MA%Ribbon"
        ],
        "container_id": "tradingview_b5094"
      }}
        );
        </script>
      </div>
      <!-- TradingView Widget END -->
      ''', height=715)

## Tab2 -  EMA Crossover

with tab2:
  
  col1, col2 = st.columns([2, 1])

  with col2:
    vol_ema_crossover = st.number_input('Volume', min_value=0.25, value=1.00, step=0.25, key=2)    
    ema_crossover_stocks = ema_crossover(data)
    ema_crossover_stocks = ema_crossover_stocks.set_index('ticker')
    ema_crossover_stocks = ema_crossover_stocks[['avg volume', 'close', 'ema_hist', 'direction']].sort_values(by='avg volume', ascending=False)
    ema_crossover_stocks = ema_crossover_stocks[ema_crossover_stocks['avg volume'] >= vol_ema_crossover]

    inner_col1, inner_col2 = st.columns([3, 1])
    with inner_col2:
      view_ticker = st.radio('Ticker', options=ema_crossover_stocks.index)
    with inner_col1:
      st.table(ema_crossover_stocks)

  # Tradingview embed
  with col1:
    components.html(f'''
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_a0fda"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
      "width": "100%",
      "height": 700,
      "symbol": "{view_ticker}",
      "interval": "D",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "enable_publishing": false,
      "allow_symbol_change": true,
      "details": true,
      "studies": [
        "STD;MA%Ribbon",
        "STD;RSI"
      ],
      "container_id": "tradingview_a0fda"
    }}
      );
      </script>
    </div>
    <!-- TradingView Widget END -->
    ''', height=700)


## Tab3 - Turtle Trend

with tab3:
  
  col1, col2 = st.columns([2, 1])

  with col2:
    vol_turtle = st.number_input('Volume', min_value=0.25, value=1.00, step=0.25, key=3)    
    turtle_targets = turtle_screener(data)
    turtle_targets = turtle_targets.set_index('ticker')
    turtle_targets = turtle_targets[['avg volume', 'close', 'long stop', 'ema', 'rsi']].sort_values(by='avg volume', ascending=False)
    turtle_targets = turtle_targets[turtle_targets['avg volume'] >= vol_turtle]

    inner_col1, inner_col2 = st.columns([3, 1])
    with inner_col2:
      view_ticker = st.radio('Ticker', options=turtle_targets.index)
    with inner_col1:
      st.table(turtle_targets)


  # Tradingview embed
  with col1:
    components.html(f'''
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_a0fda"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
      "width": "100%",
      "height": 700,
      "symbol": "{view_ticker}",
      "interval": "D",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "enable_publishing": false,
      "allow_symbol_change": true,
      "details": true,
      "studies": [
        "STD;DMI",
        "STD;Donchian_Channels",
        "STD;RSI"
      ],
      "container_id": "tradingview_a0fda"
    }}
      );
      </script>
    </div>
    <!-- TradingView Widget END -->
    ''', height=700)
