from flask import Flask, redirect, render_template,request, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
from bson import  ObjectId
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://jeronimovelasquezescobar:6YdbeI3qb7u7oXG5@cluster0.vlwtqg1.mongodb.net/emp?retryWrites=true&w=majority'
mongo=PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/signupal')
def signupal():
    return render_template('signupal.html')
@app.route('/signup/crear', methods=['POST'])
def crearUsuario():
    nombre = request.form['Nombre']
    apellido = request.form['Apellido']
    correo = request.form['Correo']
    cont = request.form['Contraseña']
    conf = request.form['coo']
    if nombre and apellido and correo and cont and conf:
        if cont != conf:
            return redirect(url_for('signupal'))
        else:

            contrCif= generate_password_hash(cont)
            mongo.db.user.insert_one({
                'Nombre': nombre,
                'Apellido': apellido,
                'Correo': correo,
                'Contraseña':contrCif
            })
            return redirect(url_for('login'))
    else:
        return redirect(url_for('signupal'))

@app.route('/login/iniciar',methods=['POST'])
def loginI():
    correo= request.form['Correo']
    contraseña=request.form['Contraseña']
    if correo and contraseña:
        user=mongo.db.user.find_one({'Correo': correo })
        if user:
            if check_password_hash(user.get('Contraseña'),contraseña):
                user=user.get('_id')
                return redirect(url_for('home1'))
        return redirect(url_for('loginal'))
@app.route('/loginal')
def loginal():
    return render_template('loginal.html')
@app.route('/home1')
def home1():
    return render_template('inicio.html')
@app.route('/exp')
def exp():
    return render_template('exp.html')
@app.route('/databs')
def databs():
    return render_template('databs.html')
#RIEGO
@app.route('/databs/riego')
def riego():
    rgs = mongo.db.riegos.find()
    return render_template('riego.html',rgs=rgs)
@app.route('/databs/riegoE')
def riegoE():
    rgs = mongo.db.riegos.find()
    return render_template('riegoE.html',rgs=rgs)
@app.route('/databs/riegoEH')
def riegoEH():
    rgs = mongo.db.riegos.find()
    return render_template('riegoEH.html',rgs=rgs)
@app.route('/databs/riego/add',methods=['POST'])
def addRie():
    cc= request.form['cc']
    if cc:
        cc = int(cc)
    proF=request.form['Pro']
    ultF=request.form['Ult']
    horaI= request.form['Horai']
    horaF= request.form['Horaf']
    cc=mongo.db.agricultor.find_one({'_id':cc})
    if cc and horaI and horaF and proF and ultF:
        horaI1= datetime.strptime(horaI,"%H:%M")
        horaF1= datetime.strptime(horaF,"%H:%M")
        if horaI>horaF:
            return redirect(url_for('riegoEH'))
        dif = horaF1-horaI1
        dif = str(dif)
        mongo.db.riegos.insert_one({
            'HoraI':horaI,
            'HoraF':horaF,
            'Horas':dif,
            'Agricultor':cc,
            'UltimaF':ultF,
            'ProximaF':proF
        })
        
        return redirect(url_for('riego'))
    else:

        return redirect(url_for('riegoE'))

@app.route('/databs/riego/ed/<string:_id>',methods=['POST'])
def edRie(_id):
    cc= request.form['cc']
    if cc:
        cc = int(cc)
    proF=request.form['Pro']
    ultF=request.form['Ult']
    horaI= request.form['Horai']
    horaF= request.form['Horaf']
    cc=mongo.db.agricultor.find_one({'_id':cc})
    if cc and horaI and horaF and proF and ultF:
        horaI1= datetime.strptime(horaI,"%H:%M")
        horaF1= datetime.strptime(horaF,"%H:%M")
        if horaI>horaF:
            return redirect(url_for('riegoEH'))
        
        dif = horaF1-horaI1
        dif = str(dif)
        print(dif)
        mongo.db.riegos.update_one({'_id': ObjectId(_id)}, {'$set': {
            'HoraI':horaI,
            'HoraF':horaF,
            'Horas':dif,
            'Agricultor':cc,
            'UltimaF':ultF,
            'ProximaF':proF
        }})
        
        return redirect(url_for('riego'))
    else:

        return redirect(url_for('riegoE'))
@app.route('/databs/riego/delete/<string:_id>/')
def delRiego(_id):
    mongo.db.riegos.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('riego'))
#AGRICULTORES
@app.route('/databs/agricultores')
def agricultores():
    agr=mongo.db.agricultor.find()
    return render_template('agricultores.html',agr=agr)
@app.route('/databs/agricultoresE')
def agricultoresE():
    agr=mongo.db.agricultor.find()
    return render_template('agricultoresE.html',agr=agr)
@app.route('/databs/agricultoresRE')
def agricultoresRE():
    agr=mongo.db.agricultor.find()
    return render_template('agricultoresRE.html',agr=agr)
@app.route('/databs/agricultoresER')
def agricultoresER():
    agr=mongo.db.agricultor.find()
    return render_template('agricultoresER.html',agr=agr)

@app.route('/databs/agricultores/add',methods=['POST'])
def addAgr():
    nombre= request.form['Nombre']
    apellido=request.form['Apellido']
    salario=request.form['Salario']
    cedula=request.form['Cedula']
    if nombre and apellido and salario and cedula:
        cedula = int(cedula)
        if cedula <0:
            cedula = cedula*-1
        salario=int(salario)
        repetido = mongo.db.agricultor.find_one(cedula)
        if salario<0:
            salario=salario*-1
        if repetido:
            return redirect(url_for('agricultoresRE'))
        mongo.db.agricultor.insert_one({
            '_id':cedula,
            'Nombre':nombre,
            'Apellido':apellido,
            'Salario':salario
        })
        
        return redirect(url_for('agricultores'))
    else:

        return redirect(url_for('agricultoresE'))
@app.route('/databs/agricultores/ed/<int:_id>/',methods=['POST'])
def edAgr(_id):
    cc = request.form['Cedula']
    nombre = request.form['Nombre']
    apellido = request.form['Apellido']
    salario = request.form['Salario']
    salario=int(salario)
    if salario<0:
        salario=salario*-1
    cc=int(cc)
    if cc != _id:
        return redirect(url_for('agricultoresER'))
    if cc and nombre and apellido and salario:
        mongo.db.agricultor.update_one({'_id': _id}, {'$set': {'Apellido': apellido, 'Salario': salario, 'Nombre': nombre}})
        return redirect(url_for('agricultores'))
    else:
        print("False")
        return redirect(url_for('agricultoresER'))

@app.route('/databs/agricultores/delete/<int:_id>/')
def delAgr(_id):
    mongo.db.agricultor.delete_one({'_id': _id})
    return redirect(url_for('agricultores'))
#HORAS
@app.route('/databs/horas')
def horas():
    horasEx=mongo.db.horasExtra.find()

    return render_template('horas.html',horasEx=horasEx)
@app.route('/databs/horasE')
def horasE():
    horasEx=mongo.db.horasExtra.find()
    return render_template('horasE.html',horasEx=horasEx)
@app.route('/databs/horas/add',methods=['POST'])
def addHora():
    fecha= request.form['Fecha']
    horas=request.form['Horas']
    cc=request.form['cc']
    if cc:
        cc = int(cc)
    cc=mongo.db.agricultor.find_one({'_id':cc})
    if cc and fecha and horas:
        mongo.db.horasExtra.insert_one({
            'Agricultor':cc,
            'Fecha':fecha,
            'Horas':horas
        })
        
        return redirect(url_for('horas'))
    else:

        print("False")
        return redirect(url_for('horasE'))
@app.route('/databs/horas/ed/<string:_id>/', methods=['POST'])
def edH(_id):
    fecha = request.form['Fecha']
    horas = request.form['Horas']
    cc = request.form['cc']
    if cc:
        cc = int(cc)
    cc = mongo.db.agricultor.find_one({'_id': cc})
    if cc and fecha and horas:
        mongo.db.horasExtra.update_one({'_id': ObjectId(_id)}, {'$set': {'Fecha': fecha, 'Horas': horas, 'Agricultor': cc}})
        return redirect(url_for('horas'))
    else:
        print("False")
        return redirect(url_for('horasE'))



@app.route('/databs/horas/delete/<string:_id>/')
def delH(_id):
    mongo.db.horasExtra.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('horas'))

#FERTILIZACION
@app.route('/databs/fertilizacion')
def fertilizacion():
    fert=mongo.db.fertilizaciones.find()
    return render_template('fertilizacion.html',fert=fert)
@app.route('/databs/fertilizacion/add',methods=['POST'])
def addFert():
    fId=request.form['Id']
    can=request.form['Cantidad']
    pre=request.form['Precio']
    cc=request.form['cc']
    ufecha= request.form['Ult']
    pfecha=request.form['Pro']
    if cc:
        cc = int(cc)
    cc=mongo.db.agricultor.find_one({'_id':cc})
    if cc and ufecha and pfecha and can and fId and pre:
        can = int(can)
        pre = int(pre)
        fId = int(fId)
        if can <0:
            can *=-1
        if pre <0:
            pre *=-1
        if fId <0:
            fId *=-1
        canPre = can*pre
        mongo.db.fertilizaciones.insert_one({
            'idF':fId,
            'Cantidad':can,
            'Precio':pre,
            'CantPrecio': canPre,
            'Agricultor':cc,
            'UltimaF': ufecha,
            'ProximaF': pfecha
        })
        
        return redirect(url_for('fertilizacion'))
    else:

        print("False")
        return redirect(url_for('fertilizacionE'))
@app.route('/databs/fertilizacion/<string:_id>',methods=['POST'])
def edFert(_id):
    fId=request.form['Id']
    can=request.form['Cantidad']
    pre=request.form['Precio']
    cc = request.form['cc']
    if cc:
        cc = int(cc)
    ufecha= request.form['Ult']
    pfecha=request.form['Pro']
    cc=mongo.db.agricultor.find_one({'_id':cc})
    if cc  and ufecha and pfecha and can and fId and pre:
        can = int(can)
        pre = int(pre)
        fId = int(fId)
        if can <0:
            can *=-1
        if pre <0:
            pre *=-1
        if fId <0:
            fId *=-1
        canPre = can*pre
        mongo.db.fertilizaciones.update_one({'_id': ObjectId(_id)},{ '$set':{
            'idF':fId,
            'Cantidad':can,
            'Precio':pre,
            'CantPrecio': canPre,
            'Agricultor':cc,
            'UltimaF': ufecha,
            'ProximaF': pfecha
        }})
        
        return redirect(url_for('fertilizacion'))
    else:

        print("False")
        return redirect(url_for('fertilizacionE'))

@app.route('/databs/fertilizacion/delete/<string:_id>/')
def delFer(_id):
    mongo.db.fertilizaciones.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('fertilizacion'))
@app.route('/databs/fertilizacionE')
def fertilizacionE():
    fert=mongo.db.fertilizaciones.find()
    return render_template('fertilizacionE.html',fert=fert)
#PODA
@app.route('/databs/poda')
def poda():
    podas=mongo.db.podas.find()
    return render_template('poda.html',podas=podas)

@app.route('/databs/poda/add',methods=['POST'])
def addPoda():
    ult = request.form['UltP']
    pro = request.form['ProP']
    hrr=request.form['Herramientas']
    cc = request.form['cc']
    if cc:
        cc = int(cc)
    cc = mongo.db.agricultor.find_one({'_id': cc})
    if ult and pro and hrr and cc and hrr:
        mongo.db.podas.insert_one({
            'UltimaF':ult,
            'ProximaF':pro,
            'Herramientas':hrr,
            'AgricultorE': cc
        })
        
        return redirect(url_for('poda'))
    else:

        print("False")
        return redirect(url_for('podaE'))
@app.route('/databs/poda/ed/<string:_id>/', methods=['POST'])
def edPoda(_id):
    ult = request.form['UltP']
    pro = request.form['ProP']
    hrr=request.form['Herramientas']
    cc = request.form['cc']
    if cc:
        cc = int(cc)
    cc = mongo.db.agricultor.find_one({'_id': cc})
    print(cc)
    if ult and pro and hrr and cc:
        mongo.db.podas.update_one({'_id': ObjectId(_id)}, {'$set': {'UltimaF': ult, 'ProximaF': pro, 'Herramientas': hrr , 'AgricultorE': cc}})
        return redirect(url_for('poda'))
    else:
        print("False")
        return redirect(url_for('podaE'))
@app.route('/databs/poda/delete/<string:_id>/')
def delP(_id):
    mongo.db.podas.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('poda'))
@app.route('/databs/podaE')
def podaE():
    podas=mongo.db.podas.find()
    return render_template('podaE.html',podas=podas)
if __name__=="__main__":
    app.run(debug=True)

