from flask import Flask, request
from flask import render_template
from flask import url_for
from flask import redirect
import mysql.connector
from mysql.connector import Error
from datetime import datetime


app = Flask(__name__)


# database work function

# connect to database

def calculate_age(birth_date):
    """
    Calculates the age given a birth date in the format of "yyyy-mm-dd".
    """
    # Parse the birth date string into a datetime object
    birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')

    # Get the current date as a datetime object
    current_date_obj = datetime.now()

    # Calculate the difference between the two dates in days
    delta_days = (current_date_obj - birth_date_obj).days

    # Calculate the age in years
    age = delta_days // 365

    return age


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name)
        print("connectoin succesdully")
    except Error as err:

        print(f"Error: '{err}'")
    return connection


pow = "2183"


# # execute sql queries
def execute_query(connection, query, tuplee, ii):
    cursor = connection.cursor()
    try:
        if (ii == 1):
            cursor.execute(query, tuplee)
        elif (ii == 0):
            cursor.execute(query)
        connection.commit()
        print("query was succesful")
    except Error as err:

        print(f"Error: '{err}")

# read_query


def read_query(connection, query, tuplee, ii):
    cursor = connection.cursor()
    result = None
    try:
        if (ii == 1):
            cursor.execute(query, tuplee)
        else:
            cursor.execute(query)

        return cursor
    except Error as err:
        print(f"Error: '{err}'")


@app.route("/")
def hello_world():
    return render_template("firstpage.html")


# login/sign
@app.route("/retailer.login\signup")
def retailer():
    return render_template("rlsp.html")


@app.route("/user.login\signup")
def User():
    return render_template("uslp.html")


@app.route("/delivery.login\signup")
def Delivery():
    return render_template("dlsp.html")


# dota for login user
@app.route("/login\signup/userlogin", methods=["POST", "GET"])
def Userlogin():
    if request.method == "POST":
        l = []
        p = []
        t = []
        name = request.form["usn"]
        password = request.form["psw"]
        house_no = request.form["huno"]
        area = request.form["area"]
        state = request.form["state"]
        pincode = request.form["pin"]
        birthday = request.form["birthday"]

        age = calculate_age(birthday)

        query = """select * from user where username = %s;"""
        tuple1 = (name,)
        tuple2 = (name, password, house_no, area,
                  state, pincode, birthday, age)
        query1 = """INSERT INTO `User` ( `username`, `password`, `House_NO`, `area`, `state`, `PINCODE`, `WALLET`, `DOB`,`age`) VALUES ( %s, %s, %s, %s, %s, %s, '0.00', %s,%s);"""

        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, tuple1, 1)

        for i in result:
            p.append(i[1])
            l.append(i)
        print(l)
        print(p)
        if not l:
            execute_query(connection1, query1, tuple2, 1)
            connection2 = create_db_connection(
                "localhost", "root", pow, "dukaan")
            query3 = """select * from user where username = %s;"""
            tuple3 = (name,)

            resultt = read_query(connection2, query3, tuple3, 1)

            for i in resultt:
                t.append(list(i))

            query = """INSERT INTO `cart_entity` (`super_user_id`, `T_price`) VALUES (%s,  '0.00');"""
            tuple1 = (t[0][0],)
            execute_query(connection1, query, tuple1, 1)
            return render_template("uslp.html")
        if l:
            # error
            return redirect(url_for("uer", usr=l))

    else:
        return render_template("userlogin.html")


@app.route("/login\signup/usersign", methods=["POST", "GET"])
def usersign():
    if request.method == "POST":
        l = []
        p = []
        name = request.form["usn"]
        password = request.form["psw"]
        query = """select * from user where username = %s;"""
        tuple1 = (name,)

        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, tuple1, 1)

        for i in result:
            l.append(list(i))

        for i in l:
            p.append(i[0])
            p.append(i[1])
            p.append(i[2])
            p.append(i[3])
            p.append(i[4])
            p.append(i[5])
            p.append(i[6])
            p.append(i[7])
            p.append(i[8])
            p.append(i[9])

        if not l:
            # error no username
            return render_template("usersignn.html")

        if l:
            if (p[2] == password):
                print("reach")
                return redirect(url_for("userpage", userpagee=p))
            else:
                # error wrong password
                return render_template("usersignn.html")

    return render_template("usersignn.html")


# data fro login retailer
@app.route("/login\signup/retailerlogin", methods=["POST", "GET"])
def retailerlogin():
    if request.method == "POST":
        l = []
        p = []
        shopname = request.form["nm"]
        password = request.form["psw"]
        shopno = request.form["shopno"]
        area = request.form["area"]
        state = request.form["state"]
        pincode = request.form["pin"]

        query = """select * from shop where shopname = %s;"""
        tuple1 = (shopname,)
        tuple2 = (shopname, password, shopno, area, state, pincode)
        query1 = """INSERT INTO `shop` (`shopname`, `password`, `shop_no`, `area`, `state`, `PINCODE`) VALUES ( %s, %s, %s, %s, %s, %s );"""

        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, tuple1, 1)

        for i in result:
            p.append(i[2])
            l.append(i)

        if not l:

            execute_query(connection1, query1, tuple2, 1)
            return render_template("rlsp.html")

        if l:
            # error
            return redirect(url_for("uer", usr=l))

    else:
        return render_template("retailerlogin.html")


@app.route("/login\signup/retailersign", methods=["POST", "GET"])
def retailersign():
    if request.method == "POST":
        l = []
        p = []
        name = request.form["usn"]
        password = request.form["psw"]
        query = """select * from shop where shopname = %s;"""
        tuple1 = (name,)

        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, tuple1, 1)
        print(result)

        for i in result:
            l.append(list(i))

        for i in l:
            p.append(i[0])
            p.append(i[1])
            p.append(i[2])
            p.append(i[3])
            p.append(i[4])
            p.append(i[5])
            p.append(i[6])
            p.append(i[7])
        print(p)
        if not l:
            # error
            return render_template("retailersign.html")

        if l:
            if (p[2] == password):
                print("reach")
                return redirect(url_for("retailerpage", dp=p))
            else:
                # error
                return render_template("retailersign.html")

    return render_template("retailersign.html")


# data fro login reatailer

@app.route("/login\signup/deliverylogin", methods=["POST", "GET"])
def deliverylogin():
    if request.method == "POST":
        l = []
        p = []
        shopid = request.form["nm"]
        licenseid = request.form["psw"]
        unitname = request.form["unname"]
        password = request.form["pssw"]

        query = """select * from  Delivery_unit_entity where shop_id = %s and license_id = %s;"""
        tuple1 = (shopid, licenseid,)
        tuple2 = (shopid, licenseid, unitname, password,)
        query1 = """insert into Delivery_unit_entity (Shop_id, License_id, unit_name, password) values (%s, %s, %s, %s);
"""

        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, tuple1, 1)

        for i in result:
            l.append(i)

        if not l:
            execute_query(connection1, query1, tuple2, 1)

            return render_template("dlsp.html")

        if l:
            # error exist
            return redirect(url_for("uer", usr=l))

    else:
        return render_template("deliverylogin.html")


@app.route("/login\signup/deliverysign", methods=["POST", "GET"])
def deliverysign():
    if request.method == "POST":
        l = []
        p = []
        name = request.form["usn"]
        password = request.form["psw"]
        query = """select * from Delivery_unit_entity where License_id = %s;"""
        tuple1 = (name,)

        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, tuple1, 1)
        print(result)

        for i in result:
            p.append(i[3])
            l.append(i[0])
            l.append(i[1])
            l.append(i[2])
            l.append(i[3])
       
        if not l:
            # wrong usernaem
            return render_template("deliverysign.html")

        if l:
            if (p[0] == password):
                return redirect(url_for("deliverypage", usr=l,check = 0,change_delivery = 0))
            else:
                # wrong passowrd
                return render_template("deliverysign.html")

    return render_template("deliverysign.html")


@app.route("/deliverypage", methods=["POST", "GET"])
def deliverypage():
    usr = request.args.getlist("usr")
    check = request.args.getlist("check")
    od = request.args.getlist("od_id")
    cd =  request.args.getlist("change_delivery")
    connection1 = create_db_connection("localhost", "root", pow, "dukaan")
    if(check[0] == '1'):
        
        query = """start transaction;"""
        execute_query(connection1, query, (), 0)
        query = """update order_detail set order_status = %s where order_id = %s;"""
        execute_query(connection1, query, ("deliverd",od[0],), 1)
        query = """commit;"""
        execute_query(connection1, query, (), 0)
        query = """select * from order_detail as o ,delivery_unit_relation as d where d.order_id = o.order_id and license_id = %s;"""
        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, (usr[1],), 1)
        
        orderr = []
        for i in result:
            orderr.append(list(i))
    if(cd[0] == '1'):
        print(1)
        # transaction 5
        a = int(usr[0])
        query = """select  max(License_id) from delivery_unit_entity;"""
        result = read_query(connection1, query, (), 0)
        ppp = []
        for i in result:
            ppp.append(i)
        print(ppp)
        c = int(ppp[0][0])
    
        b = a + 1
        if(a == c):
            b = a-1
        
        query = """select * from order_detail as o ,delivery_unit_relation as d where d.order_id = o.order_id and license_id = %s;"""
        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, (usr[1],), 1)
        
        orderr = []
        for i in result:
            orderr.append(list(i))
        print(orderr)
        print(usr[0],usr[1],orderr[0][9],od[0])
        # transaction 6
        query = """start transaction;"""
        execute_query(connection1, query, (), 0)
        query = """delete from order_detail where order_id = %s;"""
        execute_query(connection1,query,(od[0],),1)
        query = """delete from delivery_unit_relation where  shop_id = %s and license_id = %s and super_user_id = %s and order_id = %s;"""
        execute_query(connection1,query,(usr[0],usr[1],orderr[0][9],od[0],),1)
        query = """insert into delivery_unit_relation(shop_id , license_id ,super_user_id , order_id) values(%s,%s,%s,%s);"""
        execute_query(connection1,query,(usr[0],b,orderr[0][9],od[0],),1)
        query = """insert into order_detail(order_id ,order_name  ,order_status , quantity , Price   , date_of_order , date_of_delivery) values(%s,%s,%s,%s,%s,%s,%s);"""
        execute_query(connection1,query,(od[0],orderr[0][1],"on the way",orderr[0][3],orderr[0][4],orderr[0][5],orderr[0][6],),1)
        query = """commit;"""
        execute_query(connection1, query, (), 0)
        query = """select * from order_detail as o ,delivery_unit_relation as d where d.order_id = o.order_id and license_id = %s;"""
        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, (usr[1],), 1)
        
        orderr = []
        for i in result:
            orderr.append(list(i))
    else:
        query = """select * from order_detail as o ,delivery_unit_relation as d where d.order_id = o.order_id and license_id = %s;"""
        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        result = read_query(connection1, query, (usr[1],), 1)
        
        orderr = []
        for i in result:
            orderr.append(list(i))
    
    return render_template("deliverypage.html",usr = usr,od = orderr,check = 0,change_delivery =0)
@app.route("/userpagee", methods=["POST", "GET"])
def userpage():

    my_list = request.args.getlist('userpagee')

    if request.method == "POST":

        my_list = request.args.getlist('userpagee')
        amount = float(request.form["usn"])
        userid = my_list[0]
        wallet = float(my_list[7])
        psw = request.form["psw"]

        if psw == my_list[2]:
            total_amount = wallet + amount
            print(amount)
            print(wallet)
            print(total_amount)
            l = []
            p = []
            connection1 = create_db_connection(
                "localhost", "root", pow, "dukaan")
            # transaction 3
            query = """start transaction;"""
            execute_query(connection1, query, (), 0)
            query = """update user set wallet = %s where user_id = %s;"""

            tuple1 = (total_amount, userid,)

            
            execute_query(connection1, query, tuple1, 1)
            query = """commit;"""
            execute_query(connection1, query, (), 0)
            query = """select * from user where user_id = %s"""
            tuple1 = (userid,)
            result = read_query(connection1, query, tuple1, 1)

            for i in result:
                l.append(list(i))

            for i in l:
                p.append(i[0])
                p.append(i[1])
                p.append(i[2])
                p.append(i[3])
                p.append(i[4])
                p.append(i[5])
                p.append(i[6])
                p.append(i[7])
                p.append(i[8])
                p.append(i[9])

            return redirect(url_for("userpage", userpagee=p))
        return render_template("userpage.html", usr=my_list)

    return render_template("userpage.html", usr=my_list)

@app.route("/userpagee/order_placed", methods=["POST", "GET"])
def order_placed():
    my_list = request.args.getlist('dlist')
    cancell = request.args.getlist('cancel')
    connection1 = create_db_connection("localhost", "root", pow, "dukaan")
  
    if(cancell[0] == '1'):
        
        q = request.args.getlist('q')
        p = request.args.getlist('p')
        s = request.args.getlist('s')
        l = request.args.getlist('l')
        o = request.args.getlist('o')
        m = float(q[0])
        n = float(p[0])
        mo = m*n
 
        # transaction 2 cancel order
        query = """start transaction;"""
        execute_query(connection1, query, (), 0)
        
        query = """delete from order_detail where order_id = %s"""
        execute_query(connection1, query, (o[0],), 1)
        
        query = """delete from delivery_unit_relation where shop_id = %s and  license_id = %s and super_user_id = %s and  order_id = %s;"""
        execute_query(connection1, query, (s[0],l[0],my_list[0],o[0],), 1)
        
        query = """update user set wallet = wallet + %s where user_id = %s;"""
        execute_query(connection1, query, (mo,my_list[0],), 1)
        
        query = """update shop set account = account - %s where shop_id = %s;"""
        execute_query(connection1, query, (mo,s[0],), 1)
        
        query = """commit;"""
        execute_query(connection1, query, (), 0)
        
       
       
    
    print(my_list)
    print(1)
    query = """select * from user where user_id = %s;"""
    result = read_query(connection1,query,(my_list[0],),1)
    p = []
    for i in result:
        p.append(i[0])
        p.append(i[1])
        p.append(i[2])
        p.append(i[3])
        p.append(i[4])
        p.append(i[5])
        p.append(i[6])
        p.append(i[7])
        p.append(i[8])
        p.append(i[9])           
    # print(p)
    # print(2)
    query = """select * from order_detail as o ,delivery_unit_relation as d,user as u where d.order_id = o.order_id and u.user_id = d.super_user_id and u.user_id = %s;"""
   
    result = read_query(connection1, query, (my_list[0],), 1)
    pr = []
    for i in result:
        pr.append(list(i))
  
    return render_template("order_placed.html", usr=p,pro = pr)
@app.route("/userpagee/cart", methods=["POST", "GET"])
def cart():
    my_list = request.args.getlist('dlist')
    my_list2 = []
    buy =  request.args.getlist('buy')
    
    if(buy[0] == "1"):
        pid = request.args.getlist('p_id')
        pq = request.args.getlist('Product_quantity')
        price = request.args.getlist('Price')
        name =  request.args.getlist('pname')
        pr = float(price[0])
        pqq = float(pq[0])
        wallet = float(my_list[7])
        shop_id = request.args.getlist('shop_id')
        if(wallet > pr*pqq):
            money = pr*pqq
            iddd = wallet+pr+pqq
            connection1 = create_db_connection(
            "localhost", "root", pow, "dukaan")
            query = """update product_entity set quantity = quantity - %s where P_id = %s;"""
            execute_query(connection1, query, (pq[0],pid[0],), 1)
            
            # transaction 1 add money/sub
            query = """start transaction;"""
            execute_query(connection1, query, (), 0)
            query = """ update user set wallet = wallet - %s where  user_id = %s ;"""
            execute_query(connection1, query, (money,my_list[0],), 1)
            query = """update shop set account = account + %s where shop.shop_id = %s"""
            execute_query(connection1, query, (money,shop_id[0],), 1)
            query = """insert into transaction_entity(Transcation_id,T_Amount,T_quantity,Super_User_Id) values(%s,%s,%s,%s);"""
            execute_query(connection1, query, (iddd,money,pqq,my_list[0],), 1)
            query = """commit;"""
            execute_query(connection1, query, (), 0)
            
            # transaction 2 recipt genereated
            query = """start transaction;"""
            execute_query(connection1, query, (), 0)
            query = """insert into order_relation(transaction_id ,shop_id) values(%s,%s)"""
            execute_query(connection1, query, (iddd,shop_id[0],), 1)
            query = """DELETE FROM container_relation WHERE super_user_id = %s and p_id = %s and Product_quantity = %s;"""
            execute_query(connection1, query, (my_list[0],pid[0],pq[0],), 1)
            query = """insert into  delivery_unit_relation(shop_id ,license_id , super_user_id , order_id) values(%s,%s,%s,%s);"""
            execute_query(connection1, query, (shop_id[0],shop_id[0],my_list[0],iddd), 1)
            query = """insert into order_detail(order_id,order_name,order_status,quantity,Price,date_of_order,date_of_delivery) values(%s,%s,%s,%s,%s,%s,%s)"""
            execute_query(connection1, query, (iddd,name[0],"on the way",pq[0],money,'2023-01-01','2023-01-01'), 1)
            query = """commit;"""
            execute_query(connection1, query, (), 0)
          
           
    connection1 = create_db_connection(
        "localhost", "root", pow, "dukaan")
   
    query = "select * from user where user_id = %s;"
    result = read_query(connection1, query, (my_list[0],), 1)
   
    mylist = []
    for i in result:
        mylist.append(list(i))
       
  
    my_list = mylist[0]
    query = """update cart_entity set T_price = (select sum(product_quantity*price) from container_relation ,product_entity where container_relation.p_id=product_entity.p_id and super_user_id = cart_entity.super_user_id group by container_relation.super_user_id) ;
"""

    connection1 = create_db_connection(
        "localhost", "root", pow, "dukaan")
    execute_query(connection1, query, (), 0)

  
    query = """select * from container_relation as c,product_entity as p where c.p_id = p.p_id and super_user_id = %s;"""
    user_id = my_list[0]
    connection1 = create_db_connection("localhost", "root", pow, "dukaan")
    result = read_query(connection1, query, (user_id,), 1)
    for i in result:
        my_list2.append(list(i))
   
    
    return render_template("cart.html", usr=my_list, usr2=my_list2)


@app.route("/retailerpage", methods=["POST", "GET"])
def retailerpage():
    mylist = request.args.getlist("dp")

    if request.method == "POST":
        pname = request.form["usn"]
        category = request.form["ctg"]
        price = request.form["pr"]
        quantity = request.form["qt"]
        q = int(quantity)
        if q > 0:
            query = """INSERT INTO `product_entity` (`P_name`, `Categories`, `Price`, `Quantity`, `shop_id`) VALUES (%s, %s, %s, %s, %s);"""
            tuple1 = (pname, category, price, quantity, mylist[0])
            connection1 = create_db_connection(
                "localhost", "root", pow, "dukaan")
            execute_query(connection1, query, tuple1, 1)
        else:
            # pop error
            
            return render_template("retailerpage.html", dp=mylist)
    print(mylist)
    return render_template("retailerpage.html", dp=mylist)


@app.route("/retailerpage/yourproduct", methods=["POST", "GET"])
def yourproduct():
    mylist = request.args.getlist("dp")
    my_list2 = []

    query = """ select * from product_entity where shop_id = %s;"""
    tuple1 = (mylist[0],)
    print(mylist[0])

    connection1 = create_db_connection("localhost", "root", pow, "dukaan")
    result = read_query(connection1, query, tuple1, 1)
    print(result)
    for i in result:
        my_list2.append(list(i))
    print(my_list2)

    return render_template("yourproduct.html", dp=mylist, pl=my_list2)


@app.route("/userpage/nxtp", methods=["POST", "GET"])
def nxtp():
    # roll up
    query = """ select shop_id,p_name,Categories,sum(price) as total_price from product_entity group by shop_id ,p_name,Categories with rollup;"""
    connection1 = create_db_connection(
        "localhost", "root", pow, "dukaan")
    result = read_query(connection1, query, (), 1)
    l = []
    for i in result:
        l.append(list(i))
        
    print("this rollup")  
    for i in l:
        print(i)
        print("\n")
    return render_template("nxtp.html", usr=l)


@app.route("/retailerpage/AU", methods=["POST", "GET"])
def AU():
    dp = request.args.getlist('dpp')
    print(dp)
    print(1)
    # pivot
    query = """
            SELECT state,
            sum(CASE WHEN state = 'Berlin' THEN 1 ELSE 0 END) AS Berlin_user,
            sum(CASE WHEN state = 'Niedersachsen' THEN  1 ELSE 0 END) AS Niedersachsen_user,
            sum(CASE WHEN state = 'Saarland' THEN 1 ELSE 0 END) AS Saarland_user,
            sum(CASE WHEN state = 'Brandenburg' THEN  1 ELSE 0 END) AS Brandenburg_user,
            sum(CASE WHEN state = 'Thüringen' THEN 1 ELSE 0 END) AS Thuringen_user,
            sum(CASE WHEN state = 'Sachsen-Anhalt' THEN  1 ELSE 0 END) AS Hamburg_user,
            sum(CASE WHEN state = 'Hamburg' THEN 1 ELSE 0 END) AS Berlin_user,
            sum(CASE WHEN state = 'Hessen' THEN  1 ELSE 0 END) AS Hessen_user,
            sum(CASE WHEN state = 'Rheinland-Pfalz' THEN 1 ELSE 0 END) AS Rheinland_Pfalz_user,
            sum(CASE WHEN state = 'Baden-Württemberg' THEN  1 ELSE 0 END) AS Baden_Wurttemberg_user,
            sum(CASE WHEN state = 'Bremen' THEN 1 ELSE 0 END) AS Bremen_user,
            sum(CASE WHEN state = 'Nordrhein-Westfalen' THEN  1 ELSE 0 END) AS Nordrhein_Westfalen_user,
            sum(CASE WHEN state = 'Bayern' THEN 1 ELSE 0 END) AS Bayern_user,
            sum(CASE WHEN state = 'Nordrhein-Westfalen' THEN  1 ELSE 0 END) AS Nordrhein_Westfalen_user,
            sum(CASE WHEN state = 'Bayern' THEN 1 ELSE 0 END) AS Bayern_user,
            sum(CASE WHEN state = 'Schleswig-Holstein' THEN  1 ELSE 0 END) AS Schleswig_Holstein_user,
            sum(CASE WHEN state = 'Mecklenburg-Vorpomme' THEN 1 ELSE 0 END) AS  Mecklenburg_Vorpomme_user,
            sum(CASE WHEN state = 'Hessen' THEN  1 ELSE 0 END) AS Hessen_user,
            sum(CASE WHEN state = 'Sachsen' THEN 1 ELSE 0 END) AS Sachsen_user,
            sum(CASE WHEN state = 'sd' THEN  1 ELSE 0 END) AS sd_user
            FROM user
            GROUP BY state;

            """
    connection1 = create_db_connection(
        "localhost", "root", pow, "dukaan")
    result = read_query(connection1, query, (), 1)
    l = []
    print("this is pivot query")
    for i in result:
        l.append(list(i))
    
    for i in l:
        print(i)
        print("\n")
        
    # slicing  
    query = """select order_id , count(*) as "total_product" from order_detail where date_of_delivery = '2023-02-03' group by order_id;"""
    connection1 = create_db_connection(
        "localhost", "root", pow, "dukaan")
    result = read_query(connection1, query, (), 1)
    l = []
    for i in result:
        l.append(list(i))
      
    print("This is slicing query")
    print("order_id , total_product")
    for i in l:
        print(i)
        print("\n")  
        

    # drill down
    query = """select username,user_id,shop_id,sum(T_Amount) from user,transaction_entity,order_relation where transaction_entity.super_user_id = user.user_id and transaction_entity.transcation_id = order_relation.transaction_id group by user.user_id,order_relation.shop_id"""
    connection1 = create_db_connection(
        "localhost", "root", pow, "dukaan")
    result = read_query(connection1, query, (), 1)
    l = []
    for i in result:
        l.append(list(i))
      
    print("This is drill down query")
    print(" username   | user_id | shop_id | sum(T_Amount) |")
    for i in l:
        print(i)
        print("\n")  
        
    
    
    return render_template("au.html",dp = dp, usr=l)


@app.route("/userpagee/showproduct", methods=["POST", "GET"])
def showproduct():
    my_list = request.args.getlist('dlist')
    addd = request.args.getlist('add')
    idd = request.args.getlist('id')
  
  
    if(addd[0] == '1'):
     
        query = """select * from container_relation where p_id = %s and super_user_id = %s;"""
        connection1 = create_db_connection("localhost", "root", pow, "dukaan")
        su = my_list[0]
        result = read_query(connection1, query, (idd[0],su,), 1)
       
        mylist3 = []
        for i in result:
            mylist3.append(list(i))
       
        if(len(mylist3) == 0):
            query = """insert into container_relation values(%s,%s,%s);;"""
            connection1 = create_db_connection("localhost", "root", pow, "dukaan")
            su = my_list[0]
            execute_query(connection1, query, (su,idd[0],1,), 1)
        else:
            query = """update container_relation set product_quantity = product_quantity +1 where super_user_id = %s and p_id = %s;"""
            connection1 = create_db_connection("localhost", "root", pow, "dukaan")
            su = my_list[0]
            execute_query(connection1, query, (su,idd[0],), 1)
    my_list2 = []
    # print(my_list)

    query = """select * from product_entity where quantity > %s;"""

    connection1 = create_db_connection("localhost", "root", pow, "dukaan")
    result = read_query(connection1, query, (0,), 1)
    for i in result:
        my_list2.append(list(i))
    # print(my_list2)

    return render_template("showproduct.html", usr=my_list, usr2=my_list2)


@app.route("/<usr>")
def uer(usr):
    # for i in usr:s
    #     print(i)
    # print(usr[0])
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
