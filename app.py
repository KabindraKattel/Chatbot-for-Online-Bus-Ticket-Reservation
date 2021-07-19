from flask import Flask, render_template, redirect, url_for, request, session
from jinja2 import Template
import json
import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
import yaml
import re
from rivescript import RiveScript
import os.path

app = Flask(__name__)

file = os.path.dirname(__file__)
brain = os.path.join(file, 'brain')
bot = RiveScript()
bot.load_directory(brain)
bot.sort_replies()

app.secret_key = '1234'

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)
count = 0


# root
@app.route('/')
def main():
    if 'loggedin' in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


# admin
@app.route('/login/admin')
def admin():
    if 'loggedin' in session:
        user = session['user']
        phone_no = session['phone']
        cursor = mysql.connection.cursor()
        day = datetime.datetime.now().strftime("%a")
        sql = Template(
            "SELECT busid, busno, busname, source, dest, dep_time, json_length(travel.bus_details.booked_arr->'$.{{day}}') FROM bus_details")
        sql = sql.render(day=day)
        cursor.execute(sql)
        mysql.connection.commit()
        busDetails = cursor.fetchall()
        cursor.close()
        return render_template('admin.html', user=user, busInfo=busDetails)
    return redirect(url_for('login'))


# info
@app.route('/login/admin/info', methods=['POST', 'GET'])
def info():
    cursor = mysql.connection.cursor()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    cursor.execute("select id from travel.users where travel.users.admin = '0'")
    user = cursor.fetchall()
    user1 = []
    for tuple in user:
        user = str(tuple).replace("(", "").replace(",)", "")
        user1.append(user)
    print(user1)
    book = []
    for i in range(len(user1)):
        sql = Template("""select cast(concat('[', group_concat(substring(seat_label, 2, length(seat_label) - 2)),']')
                      as json) allProperties from travel.user_booking where travel.user_booking.Pass_id = '{{val}}' and travel.user_booking.date = '{{date}}'""")
        sql = sql.render(val=user1[i], date=date)
        cursor.execute(sql)
        a = cursor.fetchone()
        sql = Template(
            """select Pass_name , Phone, bus_id from travel.user_booking where travel.user_booking.Pass_id = '{{val}}'""")
        sql = sql.render(val=user1[i])
        cursor.execute(sql)
        b = cursor.fetchone()
        for tuple in a:
            use1 = str(tuple).replace("(", "").replace(",)", "")
        if (use1 != "None"):
            book.append([use1, b])
        # print(fetch)
    cursor.close()
    print(book)
    return render_template("all_user.html", row=book)


# register
@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'phone' in request.form:
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE phone = %s", [phone])
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z]+', username):
            msg = 'Username should contain only alphabets'
        elif not username or not password or not phone:
            msg = 'Please fill out the form'
        else:
            cursor.execute("INSERT INTO users VALUES(NULL,%s,%s,%s,0)", [username, password, phone])
            mysql.connection.commit()
            cursor.close()
            msg = 'You have successfully registered'
    elif request.method == 'POST':
        msg = 'Please Fill out the form'
    return render_template('register.html', msg=msg)


# login
@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'phone' in request.form and 'password' in request.form:
        phone = request.form['phone']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE phone = %s AND password = %s', (phone, password))
        account = cursor.fetchone()
        if account and account['admin'] == 1:
            session['loggedin'] = True
            session['phone'] = account['phone']
            session['user'] = account['username']
            return redirect(url_for('admin'))
        elif account:
            session['loggedin'] = True
            session['phone'] = account['phone']
            session['user'] = account['username']
            session['id'] = account['id']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect Phone or Password'
            return render_template('index.html', msg=msg)

    return render_template('index.html', msg=msg)


# home
@app.route('/login/home')
def home():
    if 'loggedin' in session:
        user = session['user']
        phoneno = session['phone']
        return render_template('home.html', user=user, phoneno=phoneno)
    return redirect(url_for('login'))


# bot
@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.reply("localuser", userText))


# add bus
@app.route('/login/admin/add_bus', methods=['POST', 'GET'])
def add_bus():
    msg = ''
    if request.method == 'POST' and 'bus_no' in request.form and 'bus_name' in request.form and 'bus_source' in request.form and 'bus_destination' in request.form and 'dept_time' in request.form:
        bus_no = request.form['bus_no']
        bus_name = request.form['bus_name']
        bus_source = request.form['bus_source']
        bus_dest = request.form['bus_destination']
        dept_time = request.form['dept_time']
        price = request.form['price']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM bus_details WHERE busno = %s", [bus_no])
        bus = cursor.fetchone()
        if bus:
            msg = 'Bus Already Registered'
        else:
            add = Template(
                "INSERT INTO `travel`.`bus_details`(`busno`, `busname`, `source`, `dest`, `dep_time`, `avail_seats`, `ticket_price`,`booked_arr`) VALUES('{{bus_no}}', '{{bus_name}}','{{source}}','{{dest}}','{{time}}', '{}','{{price}}', '{}')")
            add = add.render(bus_no=bus_no, bus_name=bus_name, source=bus_source, dest=bus_dest, time=dept_time,
                             price=price)
            cursor.execute(add)
            mysql.connection.commit()
            cursor.close()
            msg = 'Bus Added Successfully'
    return render_template('add.html', user=session['user'], msg=msg)


# update bus
@app.route('/login/admin/update_bus', methods=['POST', 'GET'])
def update_bus():
    msg = ''

    if request.method == 'POST' and 'bus_no' in request.form and 'bus_source' in request.form and 'bus_destination' in request.form and 'dept_time' in request.form:
        bus_no = request.form['bus_no']
        bus_source = request.form['bus_source']
        bus_destination = request.form['bus_destination']
        dept_time = request.form['dept_time']
        dept_date = request.form['dept_date']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE bus_details SET source = %s, dest = %s, dept_date = %s, dep_time = %s WHERE busno = %s",
                       [bus_source, bus_destination, dept_date, dept_time, bus_no])
        mysql.connection.commit()
        cursor.close()
        msg = 'Bus updated successfully'
    return render_template('update.html', user=session['user'], msg=msg)


# book ticket
@app.route('/login/home/book', methods=['POST', 'GET'])
def srcdstn():
    Hideval = ''
    if request.method == 'POST' and 'Source' in request.form and 'Destination' in request.form and 'pickup' in request.form and 'date' in request.form:
        Hideval = request.form['hide']
        Source = request.form['Source']
        Destination = request.form['Destination']
        pickup = request.form['pickup']
        session['pickup'] = pickup
        date = request.form['date']
        session['date'] = date
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM passenger_details')
        mysql.connection.commit()
        cursor.execute("INSERT INTO passenger_details VALUES(%s,%s,%s,%s)", [Source, Destination, pickup, date])
        mysql.connection.commit()
        cursor.close()
        session['source1'] = Source
        session['destination'] = Destination
        return render_template('src-dstn.html', hide=Hideval, source=Source, dstn=Destination, Pickup=pickup, date=date)
    return render_template('src-dstn.html', hide=Hideval)


# bus details
@app.route('/login/home/book/busdetails', methods=['POST', 'GET'])
def busdetails():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        src1 = session["source1"]
        dstn = session['destination']
        dates = session['date']
        date_format = '%Y-%m-%d'
        days = datetime.datetime.strptime(dates, date_format).date().strftime("%a")
        session['days'] = days
        sql = Template(
            'SELECT busid, busno, busname, source, dest, dep_time, avail_seats->> "$.{{day}}",ticket_price FROM bus_details where (source= "{{source}}" AND dest="{{dest}}")')
        sql = sql.render(day=days, source=src1, dest=dstn)
        cursor.execute(sql)
        busDetails = cursor.fetchall()
        cursor.close()
        return render_template("busdetails.html", busDetails=busDetails)


# seat plan
@app.route('/login/home/book/busdetails/seatplan', methods=['POST', 'GET'])
def seat_plan():
    bus_id = request.args.get('message1')
    session['bus_id'] = bus_id
    days = session['days']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT ticket_price FROM bus_details where (busid = %s)', [bus_id])
    price = cursor.fetchone()
    sql = Template('SELECT json_unquote(booked_arr-> "$.{{day}}") FROM bus_details where (busid = %s)')
    sql = sql.render(day=days)
    cursor.execute(sql, [bus_id])
    booked_arr = cursor.fetchone()
    for tuple in price:
        prc = str(tuple).replace("(", "").replace(",)", "")
    for tuple in booked_arr:
        barr = str(tuple).replace("(", "").replace("[", "").replace("\"", "").replace("]", "").replace(",)", "")
    return render_template('Seatplan.html', price=prc, barr=barr, bus_id=bus_id)


# confirm book
@app.route('/login/home/book/busdetails/seatplan/seat_confirm', methods=['POST', 'GET'])
def seat_confirm():
    if request.method == 'POST':
        busid1 = session.get('bus_id')
        seat1 = request.get_json()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        length = len(seat1[0])
        arr = []
        for i in range(0, length):
            arr = arr + ["%s"]
        print(arr)
        char = ""
        for i in range(0, length):
            if (i < (length - 1)):
                char = char + arr[i] + ","
            else:
                char = char + arr[i]
        days = session['days']
        sql = Template("UPDATE `travel`.`bus_details` SET `booked_arr` = json_set( booked_arr, '$.{{day}}' , "
                       "json_array({{str_temp}})) WHERE (`busid` = {{busid1}})")
        sql = sql.render(str_temp=char, busid1=busid1, day=days)
        cursor.execute(sql, (seat1[0]))
        mysql.connection.commit()
        sql1 = Template(
            "UPDATE `travel`.`bus_details` SET avail_seats = json_set( avail_seats, '$.{{day}}',{{avail}}) WHERE (`busid` = {{busid1}})")
        sql1 = sql1.render(avail=seat1[1], busid1=busid1, day=days)
        cursor.execute(sql1)
        mysql.connection.commit()
        cursor.close()
    return '', 200


@app.route('/login/home/book/busdetails/seatplan/payment_confirm', methods=['POST', 'GET'])
def booked():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        Pass_id = session['id']
        Phone = session['phone']
        Pass_name = session['user']
        date = session['date']
        source = session['source1']
        pickup = session['pickup']
        dest = session['destination']
        bus_id = session['bus_id']
        bookArr = request.get_json()
        seat_id = bookArr[0]
        seat_label = json.dumps(bookArr[1])
        print(seat_label)
        amount = bookArr[2]
        sql = Template("""INSERT INTO `travel`.`user_booking` (`Pass_id`, `Phone`, `Pass_name`, `date`, `source`, `pickup`,
              `dest`, `bus_id`, `sel_seats`,`seat_label`, `amount`) VALUES ('{{Pass_id}}', '{{Phone}}', '{{Pass_name}}', '{{date}}',
              '{{source}}','{{pickup}}','{{dest}}', '{{bus_id}}', '{{seat_id}}', '{{seat_label}}','{{amount}}')""")
        sql = sql.render(Pass_id=Pass_id, Phone=Phone, Pass_name=Pass_name, date=date, source=source, pickup=pickup,
                         dest=dest, bus_id=bus_id, seat_id=seat_id, seat_label=seat_label, amount=amount)
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
    return '', 200


@app.route('/login/home/user/current_booking', methods=['POST', 'GET'])
def user_booked():
    cursor = mysql.connection.cursor()
    date = session['date']
    id = session['id']
    sql = Template("""SELECT travel.bus_details.busname,travel.bus_details.busno,travel.user_booking.source,
                  travel.user_booking.pickup,travel.user_booking.dest,travel.bus_details.dep_time,travel.user_booking.seat_label,
                  json_length(travel.user_booking.seat_label) 'NO',travel.bus_details.ticket_price,travel.user_booking.amount
                  FROM travel.user_booking INNER JOIN travel.bus_details ON travel.user_booking.bus_id = travel.bus_details.busid
                  where travel.user_booking.date ='{{date}}' and travel.user_booking.Pass_id='{{id}}'""")
    sql = sql.render(date=date, id=id)
    cursor.execute(sql)
    user_current_booking = cursor.fetchall()
    cursor.close()
    return render_template("userbooking.html", current=user_current_booking, date=date, user=session['user'],
                           phone=session['phone'])


@app.route('/login/home/user/week_booking', methods=['POST', 'GET'])
def weekly_booked():
    cursor = mysql.connection.cursor()
    id = session['id']
    sql = Template("""SELECT travel.user_booking.bus_id,travel.bus_details.busname,travel.bus_details.busno,travel.user_booking.date,travel.user_booking.source,
                  travel.user_booking.pickup,travel.user_booking.dest,travel.bus_details.dep_time,travel.user_booking.seat_label,
                  json_length(travel.user_booking.seat_label) 'NO',travel.bus_details.ticket_price,travel.user_booking.amount
                  FROM travel.user_booking INNER JOIN travel.bus_details ON travel.user_booking.bus_id = travel.bus_details.busid
                  where travel.user_booking.Pass_id='{{id}}'""")
    sql = sql.render(id=id)
    cursor.execute(sql)
    user_weekly_booking = cursor.fetchall()
    cursor.close()
    return render_template("user_weekly_booking.html", week=user_weekly_booking, user=session['user'],
                           phone=session['phone'])


@app.route('/login/home/book/busdetails/seatplan/cancelreq', methods=['POST'])
def cancel_req():
    if request.method == 'POST':
        seatInfo = request.get_json()
        session['booked_busid'] = seatInfo[0]
        session['booked_date'] = seatInfo[1]
        session['booked_seats'] = seatInfo[2]

    return '', 200


@app.route('/login/home/book/busdetails/seatplan/cancel')
def cancel():
    seats = session['booked_seats']
    busid = session['booked_busid']
    date = session['booked_date']
    cursor = mysql.connection.cursor()
    sql = Template("""select travel.user_booking.source, travel.user_booking.dest, travel.user_booking.date, 
                       travel.user_booking.seat_label, travel.bus_details.busname , travel.bus_details.ticket_price
                       FROM travel.user_booking INNER JOIN travel.bus_details ON travel.user_booking.bus_id = travel.bus_details.busid where json_contains(seat_label,'{{seats}}') and bus_id ='{{busid}}' and date = '{{date}}'""")
    sql = sql.render(seats=seats, busid=busid, date=date)
    cursor.execute(sql)
    details = cursor.fetchone()
    print(details)
    cursor.close()
    return render_template("cancel.html", details=details, user=session['user'], phone=session['phone'])


@app.route('/login/home/book/busdetails/seatplan/cancelconf', methods=['POST'])
def cancel_conf():
    if request.method == 'POST':
        cancelInfo = request.get_json()
        session['cancelInfo'] = cancelInfo
        cancelLabel = json.dumps(cancelInfo)
        busid = session['booked_busid']
        date = session['booked_date']
        cursor = mysql.connection.cursor()
        date_format = '%Y-%m-%d'
        days = datetime.datetime.strptime(date, date_format).date().strftime("%a")
        sql = Template("""SELECT  travel.user_booking.seat_label,travel.user_booking.sel_seats,
                      travel.bus_details.booked_arr->"$.{{days}}"  FROM travel.user_booking
                       INNER JOIN travel.bus_details ON travel.user_booking.bus_id = travel.bus_details.busid
                       where json_contains(seat_label, '{{arr}}') and travel.user_booking.date='{{date}}' 
                       and travel.user_booking.bus_id='{{busid}}'into @seat_label, @sel_seats, @bookedArr""")
        sql = sql.render(arr=cancelLabel, date=date, busid=busid, days=days)
        cursor.execute(sql)
        mysql.connection.commit()
        for val in cancelInfo:
            print(val)
            sql = Template("SELECT JSON_UNQUOTE(JSON_SEARCH( @seat_label, 'one', '{{val}}')) into @Result")
            sql = sql.render(val=val)
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.execute("select JSON_EXTRACT(@sel_seats, @Result) into @answer")
            mysql.connection.commit()
            sql = Template(
                "SELECT JSON_UNQUOTE(replace((JSON_SEARCH( @bookedArr, 'one',@answer )),'$','$.{{days}}')) into @indexx")
            sql = sql.render(days=days)
            cursor.execute(sql)
            mysql.connection.commit()

            sql = Template("""UPDATE `travel`.`user_booking` SET `seat_label` = JSON_REMOVE( seat_label, @Result),
                          `sel_seats` = JSON_REMOVE( sel_seats, @Result ) where date = '{{date}}' and bus_id = '{{busid}}'
                          and json_contains(seat_label, '[\"{{array}}\"]')""")
            sql = sql.render(date=date, busid=busid, array=cancelInfo[-1])
            cursor.execute(sql)
            mysql.connection.commit()
            sql = Template(
                """UPDATE `travel`.`bus_details` SET  travel.bus_details.booked_arr = JSON_REMOVE(travel.bus_details.booked_arr, @indexx),
                avail_seats = json_replace( avail_seats, '$.{{day}}',JSON_EXTRACT(avail_seats, '$.{{day}}') + 1) where travel.bus_details.busid = '{{busid}}'""")
            sql = sql.render(busid=busid, day=days)
            cursor.execute(sql)
        sql = Template(
            "DELETE FROM travel.user_booking where json_length(seat_label)='0' and date='{{date}}' and bus_id='{{busid}}'")
        sql = sql.render(date=date, busid=busid)
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
    return '', 200


# logout
@app.route('/login/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('phone', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
