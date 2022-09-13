from flask import Flask,render_template,request
import re
app = Flask(__name__)

def FormValidation(q):
    pattern = r'^[A-E]+$'  
    r = re.match(pattern,q)
    if not r:
        return 'Invalid Query'
    else:
        return ''

def VectorSpaceModel(q):
    import os
    import numpy as np
    files = os.listdir("Vector Space Model/Docs")
    C = ['A','B','C','D','E']
    tf = np.zeros((len(files),len(C)))
    idf = np.zeros(len(C))
    i = 0
    for d in files:
        f = open('Vector Space Model/Docs/'+d,'r')
        s = f.read()
        f.close()
        for c in C:
            c_count = s.count(c)
            tf[i][C.index(c)] = c_count
            if c_count != 0 :
                idf[C.index(c)]+=1
        print(tf[i])
        tf[i] = np.array(np.divide(tf[i],tf[i].max()))
        i+=1
    q = list(q)
    Q = np.zeros(len(C))
    for c in C:
        c_count = q.count(c)
        Q[C.index(c)] = c_count
        if c_count != 0 :
            idf[C.index(c)]+=1
    print(q,Q)
    Q = np.array(np.divide(Q,Q.max()))
    print(Q)
    print(tf)
    print(idf)
    idf = np.array(np.log2(np.divide(len(files)+1,idf)))
    idf[idf == np.inf] = 0
    idf[idf == np.nan] = 0
    print('idf',idf)
    Wij = np.array(np.multiply(tf,idf))
    print(Wij)
    Wq = np.array(np.multiply(Q,idf))
    print(Wq)
    Wq2 = np.sum(np.multiply(Wq,Wq))
    print(Wq2)
    numerator = np.sum(np.multiply(Wq,Wij),axis=1)
    denominator = np.sqrt(np.multiply(np.sum(np.multiply(Wij,Wij),axis=1),Wq2))
    print(numerator)
    print(denominator)
    res = {}
    i = 0
    for k in files:
        if denominator[i] != 0 :
            res[k] = round(numerator[i]/denominator[i],3)
        else:
            res[k] = 0
        i+=1
    return sorted(res.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    
        
           
        



@app.route('/', methods=['GET','POST'])
def form():
    if request.method == 'POST'  :
        
        # print(error)
        query = request.form['query']
        error = FormValidation(query)
        if error :
            return render_template('form.html',error=error,query=query)
        else:
            r = VectorSpaceModel(query)
            
            return render_template('form.html',error='',query=query,r=r)
        
    return render_template('form.html',error='',query='',r=[])

@app.route('/random')
def random():
    C = ['A','B','C','D','E']
    import os
    files = os.listdir("Vector Space Model/Docs")
    print(files)
    import random
    for d in files:
        f = open('Vector Space Model/Docs/'+d,'w')
        l = random.randint(2,6)
        s = ''
        for _ in range(l):
            s += C[random.randint(0,len(C)-1)]
        f.write(s)
        f.close()
        
    return 'nothing'
        

if __name__ == '__main__':
    app.run(debug = True)

