#coding: utf-8
import bcrypt
import os
from flask import Flask, Markup, request, render_template, redirect, json, url_for, jsonify, Response, session, abort
from functools import wraps
app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
static = os.path.join(SITE_ROOT, 'static')
app.config['static'] = static
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/home/", methods=['POST','GET'])
def home():
	if request.method == 'POST':
		searched = False
		if request.form['name'] != '':
			results=[]
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			name = request.form['name']
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			print image
			ro = open(json_url, "r")
			data = json.loads(ro.read())
			
			for post in data["posts"]:
				subject1 = post["subject"]
				title1 = post["name"]
				author1 = post["author"]

				if name.upper() == subject1.upper():
					searched = True
					results.append(post)

				if name.upper() == title1.upper():
					searched = True
					results.append(post)
				if name.upper() == author1.upper():
					searched = True
					results.append(post)					

			if searched == True:
				results.sort()
				return  render_template('template5.html', results = results, csssheet = url, image = image,user = session.get('CURRENT_USER'))



			if searched == False:
				title = "I'm sorry we couldn't find that"
				result = 'The page you requested does not exist. If you are having trouble finding things, try navigating using the alien head. If you think it should exist then add it using our new upload feature!'

			return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user = session.get('CURRENT_USER'))



	#This will redirect the user to the page that matches their search. This redirects to their input	

	else:

		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
		ro = open(json_url, "r")
		data = json.loads(ro.read())
		results = data["posts"]
		results.sort()
		return render_template('templateex.html', csssheet = url, image = image,user = session.get('CURRENT_USER'),results=results)

#this allows the user to report their own sighting. They also have the option of adding an image.
@app.route("/upload/",methods=['POST','GET'])
def upload():

	if not session.get('logged_in'):
        	return login()
	else:
		if request.method == 'POST':
			Ysearch = False
			Csearch = False
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			if 'datafile' not in request.files:
				img = ''
			else:
				f = request.files['datafile']
				fname = f.filename
				f.save(os.path.join(app.config['static'], fname))	
				img = url_for('static',filename = fname)	
			
			with open(json_url) as f:
				data = json.load(f)
				name = request.form['uplName']
				subject = request.form['uplSubject']
				description = request.form['uplDescription']
				description1 = description.replace('\n', '<br>')
				user = session.get('CURRENT_USER')
				id = len(data['posts'])
				post = {'id':id, 'name':name, 'subject':subject, 'author':user['username'], 'description':description1, 'img':img, 'comments':[]}
				data["posts"].append(post)
				for dSubject in data["subjects"]:
					if dSubject == subject:
						Ysearch = True
				if Ysearch == False:
					data["subjects"].append(subject)


			with open(json_url, 'w') as f:
				json.dump(data, f)


			return redirect("/all/")

		else:
				url = url_for('static',filename='csstest.css')
				image = url_for('static',filename='logo1.png')
				type='post'

				return render_template('uplTemplate.html',type=type, csssheet = url, image = image,user = session.get('CURRENT_USER'))


@app.route('/login',methods=['POST','GET'])
@app.route('/login/',methods=['POST','GET'])
def login():
	
        url = url_for('static',filename='csstest.css')
        image = url_for('static',filename='logo1.png')

        if request.method == 'POST':
		loggedIn =False
		if request.form['username'] != '':
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			username = request.form['username']
			pw = request.form['password']
			pwd = pw.encode('utf-8')
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			ro = open(json_url, "r")
			data = json.loads(ro.read())
			for user in data["users"]:
					username1 = user["username"]
					pwd1 = user["password"]
					password1 = pwd1.encode('utf-8')
					if(password1 == bcrypt.hashpw(pwd, password1) and username1 == username):
						session['logged_in'] = True
						session['CURRENT_USER'] = user
						return redirect("/home/")

			if  loggedIn == False:
				title = "Incorrect details"
	        	        result = "I'm sorry, your details appear to be incorrect. If do not already have an account with us follow the register link."
	
        	   		return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user = session.get('CURRENT_USER'))
			
		else:
			title = "Incorrect details"
			result = "I'm sorry, your details appear to be incorrect. If do not already have an account with us follow the register link."

			return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user = session.get('CURRENT_USER'))


	else: 
		 return render_template('login.html', csssheet = url, image = image,user = session.get('CURRENT_USER'))



#stacking the routes makes them the same
#this shows all years in which there are reported ufo sightings
@app.route("/subject/")
@app.route("/Subject/")
def Subject():
	searched = False
	results = []
	subject = request.args.get('subject', '')
	if subject == '':
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
	
		ro = open(json_url, "r")
		data = json.loads(ro.read())
		entries = data["subjects"]
		entries.sort()
		title = "Search by subject"
		return render_template('template3.html', results = entries, title = title, csssheet = url, image = image,user = session.get('CURRENT_USER'))
	else:
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			ro = open(json_url, "r")
			data = json.loads(ro.read())
			for post in data["posts"]:
				if post["subject"] == subject:
					searched = True
					results.append(post)
			if searched == True:
				results.sort()
				return  render_template('template5.html', results = results, csssheet = url, image = image,user = session.get('CURRENT_USER'))


			if searched == False:
				result = 'The page you requested does not exist. If you are having trouble finding things, try navigating using the alien head. If you think it should exist, try adding it to our database using our new upload feature!'

			return render_template('template2.html', title = result, csssheet = url, image = image,user = session.get('CURRENT_USER'))


#this shows all countries in which ufo sightings have happened
@app.route("/following/")
@app.route("/Following/")
def Following():
	searched = False
	results = []
	if not session.get('logged_in'):
        	return login()
	else:
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
		ro = open(json_url, "r")
		data = json.loads(ro.read())
		for user in data["users"]:
			if user["username"] == session.get('CURRENT_USER')['username']:
				for follows in user["following"]:
					for post in data["posts"]:
						if post["author"] == follows:
							results.append(post)
							searched = True
		if searched == True:
			results.sort()
			return  render_template('template5.html', results = results, csssheet = url, image = image, user = session.get('CURRENT_USER'))


		if searched == False:
			result = 'You do not follow anyone!'

		return render_template('template2.html', title = result, csssheet = url, image = image,user = session.get('CURRENT_USER'))



@app.route("/logout/")
@app.route("/logout")
def logout():
	session['logged_in'] = False
	session['CURRENT_USER']=''
	return home()



@app.route("/all/")
@app.route("/All/")
def All():
#This lists all posts saved in the directory
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static", "everything.json")
	url = url_for('static',filename='csstest.css')
	image = url_for('static',filename='logo1.png')
	ro = open(json_url, "r")
	data = json.loads(ro.read())
	results = data["posts"]
	results.sort()
	return  render_template('template5.html', results = results, csssheet = url, image = image,user=session.get('CURRENT_USER'))


@app.route("/register",methods=['POST','GET'])
@app.route("/register/",methods=['POST','GET'])
def register():
	
	url = url_for('static',filename='csstest.css')
	image = url_for('static',filename='logo1.png')

	if request.method == 'POST':
		Ysearch = False
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		username = request.form['username']
		pw = request.form['password']
		pwd = pw.encode('utf-8')
		password = bcrypt.hashpw(pwd, bcrypt.gensalt())
		pw2 = request.form['password2']
		bio = request.form['uplBio']
		if 'datafile' not in request.files:
			ppic = ''
		else:
			f = request.files['datafile']
			fname = f.filename
			f.save(os.path.join(app.config['static'], fname))	
			ppic = url_for('static',filename = fname)
		if username != '' and pw != '':
			if pw == pw2:
				user = {'username':username,'password':password,'following':[],'followers':0,'Ppic':ppic, 'bio':bio}
				with open(json_url) as f:
					data = json.load(f)

					for user1 in data["users"]:
						if user1["username"] == username:
							Ysearch = True
					if Ysearch == False:
						data["users"].append(user)
						with open(json_url, 'w') as f:
							json.dump(data, f)
						return redirect("/login/")

					if  Ysearch == True:
						title = "Username already in use"
						result = "I'm sorry, the username you have requested is unavailable. Please try another."

						return render_template('template2.html', title = title, result = result, csssheet = url, image = image)
			else:
				title = "Passwords don't match"
				result = "I'm sorry, your passwords do not match. Please try again."
				return render_template('template2.html', title = title, result = result, csssheet = url, image = image)

		else:

			title = "Missing fields"
			result = "Either the username or password is blank. Please try again."
			return render_template('template2.html', title = title, result = result, csssheet = url, image = image)


	else:
		return render_template('register.html', csssheet = url, image = image)






#if a page is not found a friendly error message will appear
@app.errorhandler(404)
def page_not_found(error): 
	
	url = url_for('static',filename='csstest.css')
	image = url_for('static',filename='logo1.png')
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static", "everything.json")
	
	ro = open(json_url, "r")
	data = json.loads(ro.read())
	title = "I'm sorry we couldn't find that"
	result = 'The page you requested does not exist. If you are having trouble finding things, try navigating using the alien head. If you think it should exist then add it using our new upload feature!'

	return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user=session.get('CURRENT_USER'))




@app.errorhandler(405)
def page_not_found(error):

        url = url_for('static',filename='csstest.css')
        image = url_for('static',filename='logo1.png')
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static", "everything.json")

        ro = open(json_url, "r")
        data = json.loads(ro.read())
        title = "Something went wrong"
        result = "I'm sorry, I appear to be experiencing some issues with your request at the moment. Please try again later"

        return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user=session.get('CURRENT_USER'))


@app.errorhandler(500)
def page_not_found(error):

        url = url_for('static',filename='csstest.css')
        image = url_for('static',filename='logo1.png')
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static", "everything.json")

        ro = open(json_url, "r")
        data = json.loads(ro.read())
        title = "Something went wrong"
        result = "I'm sorry, I appear to be experiencing some issues with your request at the moment. Please try again later"

        return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user=session.get('CURRENT_USER'))



@app.route("/help")
def Help():

        url = url_for('static',filename='csstest.css')
        image = url_for('static',filename='logo1.png')
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "static", "everything.json")

        ro = open(json_url, "r")
        data = json.loads(ro.read())
        title = "Navigation Tips"
        result = "The menu is hidden under the alien head. Just hover your mouse over it and the menu will appear. You can search for sightings by name, year or country of origin using our search feature or you can display all. If you would like to report a sighting you can by registering an account with us and using our upload feature!"

        return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user=session.get('CURRENT_USER'))

		
		
		
		
@app.route("/user/")
@app.route("/User/")
def User():
	Ysearch = False
	searched = False
	results = []
	Suser = request.args.get('user', '')
	if Suser == '':
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
	
		ro = open(json_url, "r")
		data = json.loads(ro.read())
		entries = data["users"]
		entries.sort()
		title = "Search by user"
		return render_template('template3.html', results = entries, title = title, csssheet = url, image = image,user = session.get('CURRENT_USER'))
	else:
	
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			ro = open(json_url, "r")
			data = json.loads(ro.read())
			for Ruser in data["users"]:
				if Ruser["username"] == Suser:
					searched = True
					profilePic = Ruser['Ppic']
					name = Ruser['username']
					bio1 = Ruser['bio']
					bio = bio1.replace('\n', '<br>')
					followers = Ruser['followers']
			for post in data["posts"]:
				if post["author"] == Suser:
					searched = True
					results.append(post)
			if searched == True:
				results.sort()
				return  render_template('profile.html', results = results, csssheet = url, image = image,user = session.get('CURRENT_USER'),Uname=Suser,bio=bio,profilePic=profilePic, followers=followers)


			if searched == False:
				result = 'The page you requested does not exist. If you are having trouble finding things, try navigating using the alien head. If you think it should exist, try adding it to our database using our new upload feature!'

			return render_template('template2.html', title = result, csssheet = url, image = image,user = session.get('CURRENT_USER'))


				
				
				
				
				
				
				
	
				
				
				
				
				
@app.route("/comment/",methods=['POST','GET'])
@app.route("/Comment/",methods=['POST','GET'])
def Comment():
	postID = request.args.get('comment', '')			
	if not session.get('logged_in'):
		return login()
	else:
		if request.method == 'POST':
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			ro = open(json_url, "r")
			description = request.form['uplDescription']
			description1 = description.replace('\n', '<br>')
			user = session.get('CURRENT_USER')
			comment = {'author':user['username'], 'description':description1}
			data = json.loads(ro.read())
			for post in data["posts"]:
				if int(post["id"]) == int(postID):
					post["comments"].append(comment)
			with open(json_url, 'w') as f:
				json.dump(data, f)		
			return redirect('/all/')

		else:
				url = url_for('static',filename='csstest.css')
				image = url_for('static',filename='logo1.png')
				type = 'comment'

				return render_template('uplTemplate.html',type=type, csssheet = url, image = image,user = session.get('CURRENT_USER'))

				
				
				
				
				
@app.route("/edit/",methods=['POST','GET'])
@app.route("/Edit/",methods=['POST','GET'])
def Edit():
	postID = request.args.get('edit', '')			
	if not session.get('logged_in'):
		return login()
	else:
		if request.method == 'POST':
			search = False
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			ro = open(json_url, "r")
			if 'datafile' not in request.files:
				img = ''
			else:
				f = request.files['datafile']
				fname = f.filename
				f.save(os.path.join(app.config['static'], fname))	
				img = url_for('static',filename = fname)	
			user = session.get('CURRENT_USER')
			data = json.loads(ro.read())
			for post in data["posts"]:
				if int(post["id"]) == int(postID):
					if user["username"] == post["author"]:
						post['name'] = request.form['uplName']
						post['subject'] = request.form['uplSubject']
						description = request.form['uplDescription']
						description1 = description.replace('\n', '<br>')
						post['description'] = description1
						post['img'] = img
						search = True
			if search == True:
				with open(json_url, 'w') as f:
					json.dump(data, f)		
				return redirect('/all/')
			else:
				url = url_for('static',filename='csstest.css')
				image = url_for('static',filename='logo1.png')
				SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
				json_url = os.path.join(SITE_ROOT, "static", "everything.json")

				ro = open(json_url, "r")
				data = json.loads(ro.read())
				title = "Cannot Edit"
				result = "You cannot edit this post."

				return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user=session.get('CURRENT_USER'))
					

		else:
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			ro = open(json_url, "r")
			type = 'edit'
			data = json.loads(ro.read())
			result=''
			for post in data["posts"]:
				if int(post["id"]) == int(postID):
					result = post
				

			return render_template('uplTemplate.html',type=type, csssheet = url, image = image,user = session.get('CURRENT_USER'), result=result)

			
				
				
				
				
				
@app.route("/delete/")
@app.route("/Delete/")
def Del():
	postID = request.args.get('delete', '')			
	if not session.get('logged_in'):
		return login()
	else:
		search = False
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
		ro = open(json_url, "r")
		user = session.get('CURRENT_USER')
		data = json.loads(ro.read())
		for post in data["posts"]:
			if int(post["id"]) == int(postID):
				if user["username"] == post["author"]:
					del data["posts"][int(postID)]
					search = True
		
		if search == True:
			with open(json_url, 'w') as f:
				json.dump(data, f)		
			return redirect('/all/')								
		else:
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")

			ro = open(json_url, "r")
			data = json.loads(ro.read())
			title = "Wrong user logged in"
			result = "You cannot delete this post."

			return render_template('template2.html', title = title, result = result, csssheet = url, image = image,user=session.get('CURRENT_USER'))
					
				
				
				
				

				
@app.route("/follow/")
@app.route("/Follow/")
def Follow():
	Suser = request.args.get('follow', '')			
	if not session.get('logged_in'):
		return login()
	else:
		search = False
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
		ro = open(json_url, "r")
		user = session.get('CURRENT_USER')
		data = json.loads(ro.read())
		for dUser in data["users"]:
			if dUser["username"] == session.get('CURRENT_USER')['username']:
				for follows in dUser["following"]:
					if follows == Suser:
						search = True
						
						
				if search == False:
					dUser["following"].append(Suser)
					session['CURRENT_USER'] = dUser
					for fUser in data["users"]:
							if fUser["username"] == Suser:
								fUser['followers']+=1
							

		with open(json_url, 'w') as f:
			json.dump(data, f)		
		return redirect('/user/?user='+Suser)				


		
@app.route("/unfollow/")
@app.route("/Unfollow/")
def Unfollow():
	Suser = request.args.get('unfollow', '')			
	if not session.get('logged_in'):
		return login()
	else:
		search = False
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
		ro = open(json_url, "r")
		user = session.get('CURRENT_USER')
		data = json.loads(ro.read())
		for dUser in data["users"]:
			if dUser["username"] == session.get('CURRENT_USER')['username']:
				for follows in dUser["following"]:
					if follows == Suser:
						dUser["following"].remove(Suser)
						session['CURRENT_USER'] = dUser
						for fUser in data["users"]:
							if fUser["username"] == follows:
								fUser['followers']-=1

		with open(json_url, 'w') as f:
			json.dump(data, f)		
		return redirect('/user/?user='+Suser)		
		
		

if __name__ == "__main__":

	app.run(host='0.0.0.0', debug=True)
