########################################
# flask/db setup
########################################

from flask import Flask, render_template, request, make_response
app = Flask(__name__)

# sqlite3 is built in python3, no need to pip3 install
import sqlite3

# process command line arguments
import argparse
parser = argparse.ArgumentParser(description='Create a database for the twitter project')
parser.add_argument('--db_file', default='twitter_clone.db')
args = parser.parse_args()

########################################
# helper functions
########################################

def print_debug_info():
    '''
    Print information stored in GET/POST/Cookie variables to the terminal.
    '''
    # request is different from request*s*

    # these variables are set by the information after the ? in the URL;
    # args = arguments; the information after the ? is called the query arguments;
    # these variables are just for 1 webpage
    print("request.args.get('username')=",request.args.get('username'))
    print("request.args.get('password')=",request.args.get('password'))

    # this information comes from a POST form,
    # the methods for the route must include 'POST';
    # these variables are just for 1 webpage
    print("request.form.get('username')=",request.form.get('username'))
    print("request.form.get('password')=",request.form.get('password'))

    # these variables pass between different webpages;
    # these are "persistent"; the other variables are "effemeral"
    print("request.cookies.get('username')=",request.cookies.get('username'))
    print("request.cookies.get('password')=",request.cookies.get('password'))


def is_valid_login(con, username, password):
    '''
    Return True if the given username/password is a valid login;
    otherwise return False.
    '''

    # query the database for users with the given username/password
    sql = """
    SELECT username,password
    FROM users
    WHERE username='"""+str(username)+"""'
      AND password='"""+str(password)+"""';
    """
    print('is_valid_login: sql=',sql)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    # if the total number of rows returned is 0,
    # then no username/password combo was not found
    if len(list(rows))==0:
        return False

    # if the total number of rows returned is > 0,
    # then the username/password combo was found
    else:
        return True


########################################
# custom routes
########################################

@app.route('/')     
def root():
    con = sqlite3.connect(args.db_file)
    print_debug_info()

    messages = []
    sql = 'select sender_id,message,created_at from messages order by created_at desc;'
    cur_messages = con.cursor()
    cur_messages.execute(sql)
    for row_messages in cur_messages.fetchall():

        # get the username/age from sender_id
        sql='select username,age from users where id='+str(row_messages[0])+';'
        cur_users = con.cursor()
        cur_users.execute(sql)
        for row_users in cur_users.fetchall():
            pass

        # build the message dictionary
        messages.append({
            'message': row_messages[1],
            'created_at': row_messages[2],
            'username': row_users[0],
            'age': row_users[1]
            })

    # render the jinja2 template and pass the result to firefox
    return render_template('root.html', messages=messages)
    
"""
    # modify the behavior of this route depending on whether the user is logged in

    username = request.cookies.get('username')
    password = request.cookies.get('password')
    is_logged_in = is_valid_login(con, username, password)

    return render_template('root.html', is_logged_in=is_logged_in)
"""

@app.route('/login', methods=['GET','POST'])
def login():
    con = sqlite3.connect(twitter_clone.db)
    print_debug_info()

    # the basic idea:
    # we will get the information from the POST request;
    # if it's correct, set some cookies;
    # we can always check using cookies to determine whether someone is logged in or not
    form_username = request.form.get('username')
    form_password = request.form.get('password')
    print('form_username=', form_username)
    print('form_password=', form_password)

    has_clicked_form = form_username is not None
    print('has_clicked_form=', has_clicked_form)

    if has_clicked_form:
        login_info_correct = is_valid_login(con, form_username, form_password)
        if login_info_correct:
            # if someone has clicked on the form;
            # and the form information is correct;
            # then we should set the cookies
            response = make_response(render_template('login.html'))
            response.set_cookie('username', form_username)
            response.set_cookie('password', form_password)
            return response

        else:
            # if someone has clicked on the form;
            # and the form information is wrong;
            # then we should display an error
            return render_template('login.html', display_error=True)

    else:
        # if someone has not clicked on the form;
        # do nothing special
        return render_template('login.html')
    

@app.route('/logout')     
def logout():
    print_debug_info()
    #return render_template('logout.html')
    response = make_response(render_template('logout.html'))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('password', '', expires=0)
    return response
    

@app.route('/message', methods=['GET','POST'])     
def message():
    if request.form.get('message'):
        con = sqlite3.connect('twitter_clone.db')
        cur = con.cursor()
        sql = """
            SELECT id, username FROM users;
        """
        cur.execute(sql)
        rows = cur.fetchall()
        
        for row in rows:
            if row[1] == request.cookies.get('username'):
                sender_id = row[0]
            print(row)
        
        message = request.form.get('message')
        
        con = sqlite3.connect('twitter_clonee.db')
        cur = con.cursor()
        
        sql = """
        INSERT INTO messages (sender_id, message) VALUES (?, ?);
        """
        cur.execute(sql, (sender_id, message,))
        con.commit()
        
        if len(message) == 0:
            message_success = False
        
        else:
            message_success = True

        if message_success:
            res = make_response(render_template(
                'message.html',
                message_success=True,
                username=request.cookies.get('username'),
                password=request.cookies.get('password'),
                message=request.form.get('message')
            ))
            return res
        
        else:
            return render_template(
                'message.html',
                username=request.cookies.get('username'),
                password=request.cookies.get('password'),
                message_unsuccessful=True
            )
    
    else:
        res = make_response(render_template(
            'message.html',
            username=request.cookies.get('username'),
            password=request.cookies.get('password'),
            message_default=True
        ))
        
        return res
    

@app.route('/user', methods=['GET','POST'])     
def user():
    if request.method == 'GET':
        return render_template('user.html')
    
    con = sqlite3.connect('twitter_clone.db')
    cur = con.cursor()
   
    username = request.form.get('username')
    password = request.form.get('password')
    repeatpassword = request.form.get('repeatpassword')
    age = request.form.get('age')
   
    if password == repeatpassword:
        if len(username) == 0:
            user_success = False
            length_error = True
            
            if length_error and user_success == False:
                res = make_response(render_template(
                    'user.html',
                    password_error=True
                ))
                return res
        
        elif len(password) == 0:
            user_success = False
            length_error = True
            
            if length_error and user_success == False:
                res = make_response(render_template(
                    'user.html',
                    length_error=True
                ))
                return res
        
        elif len(age) == 0:
            user_success = False
            length_error = True
            
            if length_error and user_success == False:
                res = make_response(render_template(
                    'user.html',
                    length_error=True
                ))
                return res
        
        else:
            user_success = True
            
            if len(username) != 0 and len(password) != 0 and len(age) != 0:
                
                try:
                    sql = """
                    INSERT into users (username, password, age) values (?, ?, ?);
                    """
                    cur.execute(sql, (username, password, age))
                    con.commit()

                except sqlite3.IntegrityError:
                    username_error = True
                    if username_error:
                        res = make_response(render_template(
                            'user.html',
                            username_error=True
                        ))
                        return res
                
                if user_success:
                    res = make_response(render_template(
                        'user.html',
                        user_success=True,
                    ))
                    return res
                
                else:
                    return render_template(
                        'user.html',
                        user_unsuccessful=True
                    )
    
    else:
        password_error = True
        
        if password_error:
            res = make_response(render_template(
                'create_user.html',
                password_error=True
            ))
            return res

########################################
# boilerplate
########################################

if __name__=='__main__':
    app.run()