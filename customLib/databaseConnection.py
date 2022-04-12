try:
    from pymongo import MongoClient
    from decouple import config
except ModuleNotFoundError:
    from subprocess import call
    modules = ['pymongo', 'python-decouple']
    call ('pip install' + ' '.join(modules), shell=True)

username, password = config('user_name_gp'), config('password')
cluster_name, database_name = config('cluster_name'), config('database_name')

# Connection phase
def connDatabase():
    MONGO_URI = f'mongodb+srv://{username}:{password}@{cluster_name}.vi3i1.mongodb.net/{database_name}?retryWrites=true&w=majority'
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI)
    return client['userDetails']

# Used for registration phase
def insertNewRecord(docs):
    try:
        db = connDatabase()
        lec = db['Record']
        listOfItems = lec.find({ 
            "$or": [
                {"username": docs['username']}, 
                {"email": {"$eq": docs['email']}}
                ]
            })
        if len(list(listOfItems)) != 0 :
            t = True
        else:
            lec.insert_one(docs)
            t = False
        return t
    except Exception as e:
        print(e)
    return True

# Used for login phase
def retrieveUserDetails(email):
    try:
        db = connDatabase()
        lec = db['Record']
        passwd = {}
        username = ''
        email_id = ''
        listOfItems = lec.find({
            "email": {"$eq": email}
        })
        if lec.count_documents({"email": email}) != 0 :
            t = True
            for item in listOfItems:
                username = item['username']
                email_id = item['email']
                passwd = item['password']
        else:
            t = False
        return (t, username, email_id, passwd)
    except Exception as e:
        print(e)


