import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = {'Year': ['2000', '2010', '2014', '2020'],
'Sales': [2345, 5000, 5431, 7090]}
df = pd.DataFrame(data)
plt.bar(df['Year'], df['Sales'])
plt.xlabel('Year')
plt.legend()
plt.ylabel('Total Sales')
plt.title('Sales Performance:')
plt.show()


plt.plot(ypoints, linestyle = 'dotted')
plt.show()


