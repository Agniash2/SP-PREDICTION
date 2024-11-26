import numpy as np
import pandas as pd
import yfinance as yf
from keras.models import load_model
import streamlit as st 
import matplotlib.pyplot as plt
model=load_model('/Users/akashakash/Desktop/STP.keras')

st.header("stock price prediction")
stock=st.text_input("enter stock symbol",'GOOG')
start='2010-01-01'
end='2024-01-01'
data=yf.download(stock,start,end)

st.subheader('Stock Data')
st.write(data)

data_train=pd.DataFrame(data.Close[0:int(len(data)*0.80)])
data_test=pd.DataFrame(data.Close[int(len(data)*0.80):len(data)])

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler(feature_range=(0,1))

pas_100_days=data_train.tail(100)
data_test=pd.concat([pas_100_days,data_test],ignore_index=True)
data_test_scale=scaler.fit_transform(data_test)

st.subheader(' PRICE VS Moving AVERAGE 50')
ma_50_days=data.Close.rolling(50).mean()
fig1=plt.figure(figsize=(8,6))
plt.plot(ma_50_days,'r')
plt.plot(data.Close,'g')
plt.show()
st.pyplot(fig1)     


st.subheader('Price VS Moving AVERAGE 50 VS Moving AVERAGE 100')
ma_100_days=data.Close.rolling(100).mean()
fig2=plt.figure(figsize=(8,6))
plt.plot(ma_50_days,'r')
plt.plot(ma_100_days,'b')
plt.plot(data.Close,'g')
plt.show()
st.pyplot(fig2)

st.subheader('Price VS Moving AVERAGE 100 VS Moving AVERAGE 200')
ma_200_days=data.Close.rolling(200).mean()
fig3=plt.figure(figsize=(8,6))
plt.plot(ma_100_days,'r')
plt.plot(ma_200_days,'b')
plt.plot(data.Close,'g')
plt.show()
st.pyplot(fig3)


a=[]
b=[]

for i in range(100,data_test_scale.shape[0]):
    a.append(data_test_scale[i-100:i])
    b.append(data_test_scale[i,0])
a,b=np.array(a),np.array(b)    

predict=model.predict(a)

scale= 1/scaler.scale_

predict=predict*scale
b=b*scale


st.subheader('Orginal VS Predicted Price')
fig4=plt.figure(figsize=(8,6))
plt.plot(predict,'r',label='Orginal Price')
plt.plot(b,'g',label="Predicted Price")
plt.xlabel("Time")
plt.ylabel("Price")
plt.show()
st.pyplot(fig4)