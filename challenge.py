import pandas as pd
from ast import literal_eval

# Import both csv files to pandas
df1 = pd.read_csv("source1.csv")
df2 = pd.read_csv("source2.csv")

def question_one():
  # check unique campaigns in February
  feb_campaigns = df1.campaign[(df1.date >='2015-02-01') & (df1.date <= '2015-02-28')].unique()
  return(len(feb_campaigns))

def question_two():
  # set a counter for plant conversions
  plant_conversions = 0

  # create an initiative column
  list_a = [item.split("_")[0] for item in df1['campaign']]
  df1['initiative'] = list_a

  # iterate through actions list and return values from the dictionary
  plant_actions = df1.actions[df1['initiative'] == 'plants']
  for action in plant_actions:
    acts = literal_eval(action)
    for a in acts:
      if 'x' in a.keys() and 'conversions' in a.values():
        plant_conversions += a["x"]
      elif 'y' in a.keys() and 'conversions' in a.values():
        plant_conversions += a["y"]

  return plant_conversions

def question_three():

  # Creating a column for Audience and Asset
  listb = [item.split("_")[1] for item in df1['campaign']]
  listc = [item.split("_")[2] for item in df1['campaign']]
  # created a combo list to make it easy of only the audience and asset
  listbc = []
  i = 0
  while i < len(listb):
    x = listb[i] + "_" + listc[i]
    listbc.append(x)
    i += 1

  df1['audience'] = listb
  df1['asset'] = listc
  df1['aud_ass'] = listbc

  # Creating a conversions column for all rows
  actions = df1.actions
  for index, actions in df1.actions.iteritems():
    a = literal_eval(actions)
    x_conversions = 0
    y_conversions = 0
    for values in a:
      if ('x' in values.keys() and 'conversions' in values.values()):
        x_conversions += values['x']
      if ('y' in values.keys() and 'conversions' in values.values()):
        y_conversions += values['y']
      total_conversions = x_conversions + y_conversions
    df1.set_value(index, 'conversions', total_conversions)

  # Sorting through data by grouping Audience and Asset to conversions and spend

  converts = df1.groupby('aud_ass')['conversions'].sum()
  spend = df1.groupby('aud_ass')['spend'].sum()
  total = spend/converts

  # return same data
  least = min(total)
  what = total[total == least]

  return what

def question_four():
  # set up 2nd df to only include video campaigns
  valid_campaigns = df2[df2.object_type == "video"]
  list2a = [item.split("_")[0] for item in valid_campaigns.campaign]
  list2b = [item.split("_")[1] for item in valid_campaigns.campaign]
  list2c = [item.split("_")[2] for item in valid_campaigns.campaign]


  # match 1st df with 2nd campaigns
  lista = [item.split("_")[0] for item in df1['campaign']]
  listb = [item.split("_")[1] for item in df1['campaign']]
  listc = [item.split("_")[2] for item in df1['campaign']]
  df1['initiative'] = lista
  df1['audience'] = listb
  df1['asset'] = listc

  # creating unique identifiers for ABC
  initiative = df1.initiative.unique()
  audience = df1.audience.unique()
  asset = df1.asset.unique()

  # creating a list that puts random ABCs into correct order
  campaign_list2 = []
  counter = 0
  while counter < len(list2a):
    holder = []
    if list2a[counter] in initiative:
      holder.append(list2a[counter])
    elif list2b[counter] in initiative:
      holder.append(list2b[counter])
    elif list2c[counter] in initiative:
      holder.append(list2c[counter])

    if list2a[counter] in audience:
      holder.append(list2a[counter])
    elif list2b[counter] in audience:
      holder.append(list2b[counter])
    elif list2c[counter] in audience:
      holder.append(list2c[counter])

    if list2a[counter] in asset:
      holder.append(list2a[counter])
    elif list2b[counter] in asset:
      holder.append(list2b[counter])
    elif list2c[counter] in asset:
      holder.append(list2c[counter])

    camp = "_".join(holder)
    campaign_list2.append(camp)
    counter += 1

  # cretes dfs to work with only using what we need
  df3 = pd.DataFrame({"campaign": campaign_list2, "video":"yes"})
  unique_campaigns3 = df3.campaign.unique()
  unique_campaigns1 = df1.campaign.unique()


  spend = 0
  views = 0
  # iterate through the dfs using the unique campaigns
  for unique in unique_campaigns3:
    cash = df1.spend[df1.campaign == unique]
    print(cash)
    actions = df1.actions[df1.campaign == unique]

    # iterate through each action turn it into a list
    for action in actions:
      a = literal_eval(action)
      x_video_views = 0
      y_video_views = 0

      # iterate through each list of dicts to return values needed
      for values in a:
        if ('x' in values.keys() and 'views' in values.values()):
          x_video_views += values['x']
        if ('y' in values.keys() and 'views' in values.values()):
          y_video_views += values['y']

    # adds views to the views counters
    total_views = (x_video_views + y_video_views)
    views += (total_views)

    # add amount to spend counter
    if total_views > 0:
      print(cash.ix[cash.index].values)
      spend += (sum(cash.ix[cash.index].values))

    cpv = spend/views
  # return cost per view
  return cpv



# print("How many unique campaigns ran in February?  ", question_one())
# print("What is the total number of conversions on plants?  ", question_two())
# print("What audience, asset combination had the least expensive conversions?  ", question_three())
# print("What was the total cost per video view?  ", question_four())
question_four()


