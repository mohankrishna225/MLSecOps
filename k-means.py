#!/usr/bin/env python
# coding: utf-8


#importing useful modules
import pandas as pd
import numpy as np
from os import system


#Read the Data
data = pd.read_csv('/var/log/httpd/access_log-344632', error_bad_lines=False, sep=" ", names=['IP','Space','Blank','Date', 'TimeZone', 'Method', 'StatusCode', 'Bytes', 'Path', 'Browser'])


data2 = pd.read_csv('/var/log/httpd/access_log', error_bad_lines=False, sep=" ", names=['IP','Space','Blank','Date', 'TimeZone', 'Method', 'StatusCode', 'Bytes', 'Path', 'Browser'])

data = data.append(data2, ignore_index=True)


#Feature Selection
data = data.drop(['Space', 'Blank'], axis=1)
data = data.drop(['Date','TimeZone','Method','Bytes','Path','Browser'], axis=1)


#To drop the null values from the dataset
data.dropna

#Feature Selection
data= data.groupby(['IP','StatusCode']).StatusCode.agg('count').to_frame('Count').reset_index()
data.insert(0, 'IPCount', range(len(data)))
new_data = data.drop(['IP'], axis=1)


from sklearn.preprocessing import StandardScaler

#Data Scaling
sc = StandardScaler()
data_scaled = sc.fit_transform(new_data)


from sklearn.cluster import KMeans

#Creating Model
model = KMeans(n_clusters=4)

#Fit and Predict
pred  = model.fit_predict(data_scaled)

#Adding Cluster Labels to dataset
data_pred = pd.DataFrame(data_scaled, columns=['IP_Scaled', 'StatusCode_Scaled','Count_Scaled'])
data_pred['Cluster'] = pred
data_final = pd.concat([data, data_pred], axis=1, sort=False)

#library for plotting the graph
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px


#Plotting Scatter Graph Using Plotly
Graph   = px.scatter(data_final, 'Count', 'IP', 'Cluster', hover_data=['StatusCode'], color_continuous_scale='Jet')
layout  = go.Layout(title='No of Requests Per IP', hovermode='closest')
figure  = go.Figure(data=Graph, layout=layout)
graph = pyo.plot(figure, filename='/root/Desktop/ML_SecOps/Graph_IPCount.html', auto_open=False)


#Finding IP resulting to DoS attacks
IPCluster_to_be_blocked = []
for index, row in data_final.iterrows():
    if data_final['Count'].loc[index] > 200:
          IPCluster_to_be_blocked.append(data_final['Cluster'].loc[index])
IPCluster_to_be_blocked = max(set(IPCluster_to_be_blocked), key = IPCluster_to_be_blocked.count)

#Find the cluster to be blocked

print(IPCluster_to_be_blocked)


#Block the IPs and create the Data
for index_in_data, row_in_data in data_final.iterrows():
    if data_final['Cluster'].loc[index_in_data] == IPCluster_to_be_blocked:
                system("sudo iptables -A INPUT -s {0} -p tcp --destination-port 80 -j DROP".format(data_final['IP'].loc[index_in_data]))
                print(data_final['IP'].loc[index_in_data])

data_final.to_csv('/root/Desktop/ML_SecOps/BlockIP_Data.csv', index=False)




