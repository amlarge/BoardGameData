# Databricks notebook source
import pandas as pd
import fuzzy_pandas as fpd
import re

# COMMAND ----------

df1=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA1.description.csv")
df2=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA2.description.csv")
df3=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA3.description.csv")

# COMMAND ----------

df1=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA1.description.csv")
df2=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA2.description.csv")
df3=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA3.description.csv")
dlist=[df2,df3]
for D in dlist:
  for idx,row in D.iterrows():
    if re.search('[a-zA-z]*2([c,t])?$',row['variable']):
      string=re.search('[a-zA-z]*2([c,t])?$',row['variable']).group(0)
      test=re.search('[a-zA-z]*',row['variable']).group(0)

      t=df1.loc[df1['variable'].str.contains(test, case=False),'variable'].to_string(index=False)
      print(t)
      print(string)
      df1.loc[df1['variable'].str.contains(test, case=False),'variable']=str(t)+', '+string
    else:
      df1.append(row)


# COMMAND ----------


df1=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA1.description.csv")
df2=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA2.description.csv")
df3=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA3.description.csv")
df4=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA4.description.csv")
df5=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA5.description.csv")
df6=pd.read_csv("/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA6.description.csv")

Dlist=[df2,df3,df4,df5,df6]
fulldata=df1[['variable','description']]
for D in Dlist:
  fulldata=fulldata.merge(D[['variable','description']],how='outer',on='description')

# COMMAND ----------

F=fulldata.set_index('description').stack().reset_index().drop('level_1', axis=1, inplace=False).drop_duplicates()

# COMMAND ----------

F.to_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA6_concat.csv')

# COMMAND ----------

FH=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P003-FH/04-DataAnalysis/pheno/FH_exam8_plasma_phenotype.description.csv')

# COMMAND ----------

df5[df5['description'].str.contains("FAMILY")]

# COMMAND ----------

t=df1.loc[df1['variable'].str.contains("site", case=False),'variable'].to_string(index=False)

df1.loc[df1['variable'].str.contains("site", case=False),'variable']=str(t)+', '+'site2c'
df1.loc[df1['variable'].str.contains("site", case=False),'variable']


# COMMAND ----------

t=df1.loc[df1['variable'].str.contains("site", case=False),'variable'].to_string(index=False)

t

# COMMAND ----------

F=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/00-ProjectData/original/main/MESA6_concat.csv')

# COMMAND ----------

G= F.groupby(['description'],as_index=False)['variable'].apply(', '.join).reset_index()
G.description=G.description.str.lower()
G.description=G.description.str.split(" exam [0-9]").str[0]

G

# COMMAND ----------

H=G.groupby(['description'],as_index=False)['variable'].apply(', '.join).reset_index()

# COMMAND ----------

G[G['description'].str.contains("age")]

# COMMAND ----------

H[H['description'].str.contains("age")]

# COMMAND ----------

H.to_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/04-DataAnalysis/pheno/ME_fuzzy_description.csv')

# COMMAND ----------

import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    s = df_2[key2].tolist()
    
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m
    
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    
    return df_1

# COMMAND ----------

fuzzy_merge(F, FH, 'description', 'description', threshold=80)

# COMMAND ----------

fpd.fuzzy_merge(F, FH,
                left_on=['description'],
                right_on=['description'],
                ignore_case=True,
                method='levenshtein',
                threshold=0.95,
                keep='all',
               join='full-outer')

# COMMAND ----------

#FR=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P001-FR/04-DataAnalysis/pheno/FR_pheno_annotations.csv')
DI=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P002-DI/04-DataAnalysis/pheno/DI_pheno_2015.description.csv')

# COMMAND ----------

FR.iloc[260:270]

# COMMAND ----------

for idx,row in DI.iloc[range(278,852,5),].iterrows():
  condition=row['LONGNAME']
  if pd.isna(condition):
    print(idx)
    break
  DI.iloc[idx+1,1]="Prevalent "+condition
  DI.iloc[idx+2,1]="Incident "+condition
  DI.iloc[idx+3,1]="Age at first "+condition
  DI.iloc[idx+4,1]='Age at '+condition+"-baseline age"

# COMMAND ----------

DI.iloc[270:290,]

# COMMAND ----------

FR.to_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P001-FR/04-DataAnalysis/pheno/FR_pheno_annotations_partialfill.csv')

# COMMAND ----------

DI.to_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P002-DI/04-DataAnalysis/pheno/DI_pheno_2015.description_partialfill.csv')

# COMMAND ----------

DI[pd.isna(DI.LONGNAME)].tail(30)

# COMMAND ----------

pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P003-FH/04-DataAnalysis/pheno/FH_exam8_plasma_phenotype.description.csv')

# COMMAND ----------

FH[pd.isna(FH.description)].head(30)

# COMMAND ----------

FR.LONGNAME.fillna('FR',inplace=True)
FR[pd.isna(FR.LONGNAME)]

# COMMAND ----------

H=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P004-ME/04-DataAnalysis/pheno/ME_fuzzy_description.csv')
H.head(20)

# COMMAND ----------

fpd.fuzzy_merge(H, FR,
                left_on=['description'],
                right_on=['LONGNAME'],
                ignore_case=True,
                method='levenshtein',
                threshold=0.6,
                keep='all',
               join='full-outer').head(40)

# COMMAND ----------

ME=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P002-DI/04-DataAnalysis/pheno/DI_pheno_2015.description.csv')
FH=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P003-FH/04-DataAnalysis/pheno/FH_exam8_plasma_phenotype.description.csv')
DI=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P002-DI/04-DataAnalysis/pheno/DI_pheno_2015.description_partialfill.csv')
FR=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P001-FR/04-DataAnalysis/pheno/FR_pheno_annotations_partialfill.csv')

# COMMAND ----------

FR.loc[2,['VARIABLE','LONGNAME']]

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P005-AR/04-DataAnalysis/pheno/AR_pheno_v2samples.description.csv')

# COMMAND ----------

pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P005-AR/04-DataAnalysis/pheno/AR_biolincc_2020b_v2_pheno.description.csv').iloc[50:80,]

# COMMAND ----------

ARp=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P005-AR/04-DataAnalysis/pheno/AR_pheno_v2samples.description.csv')

# COMMAND ----------

ARp

# COMMAND ----------

simple=[]

ARp=ARp.drop_duplicates().reset_index(drop=True)
for idx,row in ARp.iterrows():
  if row['description']=='ARp':
    simple.append(row['variable'])
  elif re.search('V5 V5',row['description']):
    string=re.split('V5',row['description'])[2].strip()
    simple.append(string)
  elif re.search('^V[1-9]',row['description']):
    string=re.split('V[1-9]',row['description'])[1].strip()
    simple.append(string)

    
  elif re.search('V[1-9]$',row['description']):
    string=re.split('V[1-9]',row['description'])[0].strip()
    simple.append(string)
    
    
  else:
    simple.append(row['description'].strip())
    
ARp['simple_desc']=simple

# COMMAND ----------

ARp[ARp.variable.str.contains('EGFRSCRCYSC_V5')]

# COMMAND ----------

ARp

# COMMAND ----------




# COMMAND ----------

ARp=ARp.dropna(subset=['variable'])
ARp.description.fillna('ARp',inplace=True)
ARp[pd.isna(ARp.description)]

# COMMAND ----------

ARp_grouped=ARp.groupby(['simple_desc'],as_index=False)['variable'].apply(', '.join).reset_index()

# COMMAND ----------

ARp_grouped.head(30)

# COMMAND ----------

ARbio=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P005-AR/04-DataAnalysis/pheno/AR_biolincc_2020b_v2_pheno.description.csv')
ARbio.iloc[50:100,]

# COMMAND ----------

ARbio=pd.read_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P005-AR/04-DataAnalysis/pheno/AR_biolincc_2020b_v2_pheno.description.csv')

ARbio=ARbio.dropna(subset=['variable'])

ARbio.description.fillna('ARbio',inplace=True)
ARbio=ARbio.drop_duplicates().reset_index(drop=True)
simple=[]
for idx,row in ARbio.iterrows():
  if row['description']=='ARbio':
    simple.append(row['variable'])
  elif re.search('V5 V5',row['description']):
    string=re.split('V5',row['description'])[2].strip()
    simple.append(string)
  elif re.search('^V[1-9]',row['description']):
    string=re.split('V[1-9]',row['description'])[1].strip()
    simple.append(string)
    
  elif re.search('V[1-9]$',row['description']):
    string=re.split('V[1-9]',row['description'])[0].strip()
    simple.append(string)
  elif re.search('^Visit [1-9]',row['description']):
    string=re.split('Visit [1-9]',row['description'])[1].strip()
    simple.append(string)
  else:
    simple.append(row['description'].strip())
    
ARbio['simple_desc']=simple

# COMMAND ----------

ARbio

# COMMAND ----------

ARbio_grouped=ARbio.groupby(['simple_desc'],as_index=False)['variable'].apply(', '.join).reset_index(drop=True)

# COMMAND ----------

ARbio[ARbio.variable=='EGFRSCRCYSC_V5']

# COMMAND ----------

ARbio

# COMMAND ----------

AR_full=ARp_grouped.append(ARbio_grouped)
AR_full

# COMMAND ----------

AR_full[AR_full.duplicated(subset=['simple_desc'],keep=False)]

# COMMAND ----------

AR_full['variable']=[x.lower() for x in AR_full['variable']]

# COMMAND ----------

AR_full=AR_full[['simple_desc','variable']].drop_duplicates()

# COMMAND ----------

ARfull_grouped=AR_full.groupby(['simple_desc'],as_index=False)['variable'].apply(', '.join).reset_index(drop=True)
ARfull_grouped.to_csv('/dbfs/mnt/sapbio-client-001sap/001SAP21P005-AR/04-DataAnalysis/pheno/AR_full_grouped_partialfill.csv')

# COMMAND ----------

DI[pd.isna(DI['LONGNAME'])]

# COMMAND ----------

FRDI=FR.merge(DI,on='VARIABLE')[['VARIABLE','LONGNAME_x']].reset_index(drop=True)

# COMMAND ----------

FRDI.columns=['variable','description']

# COMMAND ----------

ARfull_grouped

# COMMAND ----------

FRDIAR=fpd.fuzzy_merge(FRDI.dropna(), ARfull_grouped.dropna(),
                left_on=['description'],
                right_on=['simple_desc'],
                ignore_case=True,
                method='levenshtein',
                threshold=0.6,
                keep='all',
               join='full-outer')

# COMMAND ----------

FRDIAR.columns=['FRDI_variable','FRDI_description','AR_variable','AR_description']
#FRDIAR2=FRDIA

# COMMAND ----------

FRDIAR.to_csv('/dbfs/FileStore/users/adam.large@sapient.bio/FRDIAR.csv')

# COMMAND ----------

# MAGIC %r
# MAGIC 
# MAGIC 
# MAGIC 
# MAGIC #library(SparkR)
# MAGIC 
# MAGIC meta <- read.df("/FileStore/users/adam.large@sapient.bio/FRDIAR.csv", header="true", inferSchema = "true", source="csv")
# MAGIC display(meta)
# MAGIC 
# MAGIC dim(meta)

# COMMAND ----------



# COMMAND ----------

fpd.fuzzy_merge(FRDI.dropna(), FH.dropna(),
                left_on=['description'],
                right_on=['description'],
                ignore_case=True,
                ignore_nonalpha=True,
                ignore_order_words=True,
                method='levenshtein',
                threshold=0.5,
                keep='all',
               join='full-outer').head(50)

# COMMAND ----------

pd.set_option("display.max_rows", 999)

# COMMAND ----------

ARfull_grouped.iloc[1:100,]

# COMMAND ----------

FR[pd.isna(FR.LONGNAME)]
