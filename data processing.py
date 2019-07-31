file_path = "HidalgoECIreplication/baidureading/"

# user-book pairs
uer_books=pd.read_csv(expanduser('~/{0}all_userbooks.csv'.format(file_path)), low_memory=False,header=None)
uer_books=uer_books.rename(columns={0:'user',1:'book',2:'phone',3:'time'})
uer_books.head()

#读入’bookinfoutf8'
info=pd.read_csv('~/{0}bookinfoutf8'.format(file_path), low_memory=False)
info=info.rename(columns={'图书名称': 'book_name','图书连接':'book','上下架状态（2-上，1-下）':'on_stock', '一级分类':'tag','文库价（元）':'price'})
info.head()

#匹配tag
user_tag=uer_books.merge(info,how='inner',on='book',sort=True)


# 阅读时长  毫秒-分钟
user_tag['time_m']=[round(xi/60000,2) for xi in user_tag['time'] ]
user_tag[['time','time_m']].describe()


#去掉不符合现实的数据：6个月，最大阅读时间不能超过259200mins，最小不能少于一分钟
data=user_tag.loc[(user_tag['time_m']<259200) &(user_tag['time_m']>1) ]
data=data.reset_index()
data['time_m'].describe()


# 算每个tag的书的数量
data['tag_nbook']=data.groupby(['user','tag'])['book'].transform('count')
data['tag_nbook'].describe()
#去重
data_by_tag=data[['user','tag','tag_nbook','phone']].drop_duplicates(keep='first')
data_by_tag=data_by_tag.reset_index(drop=True)

with open('databytag.txt', 'wb') as handle:
    pickle.dump(data_by_tag, handle)