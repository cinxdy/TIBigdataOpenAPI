import request

class requestAPI:
    serviceKey = ''
    numOfCnt = 0
    rank = 0
    title = ''
    body = ''
    writer = ''
    startDate = ''
    endDate = ''
    institution = ''
    category = ''

    def __init__(self):
        self.serviceKey = request.args.get('secretKey, "")
        self.numOfCnt = request.args.get('numOfCnt', 100)
        self.rank = request.args.get('rank', 1)
        self.title = request.args.get('title',"")
        self.body = request.args.get('body',"")
        self.writers = request.args.get('writers')
        self.startDate = request.args.get('startDate')
        self.endDate = request.args.get('endDate')
        self.institution = request.args.get('institution')
        self.category = request.args.get('category')

class responseAPI:
    response = {}
    
    resultCode = 0
    resultMSG = ''
    nunOfCnt = 0
    totalCnt = 0
    rank = 0
    title = ''
    body = ''
    writer = ''
    date = ''
    institution = ''
    institutionURL = ''
    category = ''
    fileURL = ''

    def __init__(self, data):
        
