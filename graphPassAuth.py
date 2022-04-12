# importing the module
import cv2, os, random, sys
import customLib.databaseConnection as db

# window name
windowName = 'New Window'
# used for register 
docs = {}
click_coordinates = {}
xc, yc = 0, 1
# set radius = 30

def click_event(event, x, y, flags, params):

	global xc, yc
	# checking for left mouse clicks
	if event == cv2.EVENT_LBUTTONDOWN:
		xc, yc = x, y
		cv2.destroyAllWindows()

def inOut(center_x, center_y, x, y, r):
	if ((x - center_x) * (x - center_x) + (y - center_y) * (y - center_y) <= r * r):
		return True
	return False

# Registration Phase
def registerUser():
	userName = str(input("[+] Enter your username: ")).strip()
	name = str(input("[+] Enter your Name: ")).strip()
	email = str(input("[+] Enter your Email ID: ")).strip()
	# list of images [ file names ]
	files = os.listdir('.\static-images')
	random.shuffle(files)

	for imgfile in files[:3]:
		global xc, yc
		xc, yc = 0, 0
		# reading the image
		img = cv2.imread(f'.\static-images\\{imgfile}', 1)		
		img = cv2.resize(img, (800, 800))
		# img = cv2.circle(img, (200, 200), 30, (152, 20, 45), -1)
		cv2.imshow(windowName, img)
		cv2.setMouseCallback(windowName, click_event)		
		cv2.waitKey(-1)
		cv2.destroyAllWindows()
		click_coordinates[imgfile] = (xc, yc)
		# print(xc, " -HY- ", yc)
		# print(inOut(200, 200, xc, yc, 30))
	docs['name'] = name
	docs['username'] = userName
	docs['email'] = email
	docs['password'] = click_coordinates
	val = db.insertNewRecord(docs)
	if val is False:
		os.system('cls')
		print("Registration Successful")
	else:
		os.system('cls')
		print("Registration Failure [username/email is already registered]\n")
	return val

def loginUser():
	email = str(input('[+] Enter your email address:')).strip()
	newval = db.retrieveUserDetails(email)
	login_stats = []
	files = tuple(newval[3].keys())
	pass_coordinates = tuple(newval[3].values())
	click_coordinates.clear()
	for imgfile in files:
		global xc, yc
		xc, yc = 0, 0
		img = cv2.imread(f'.\static-images\\{imgfile}', 1)
		img = cv2.resize(img, (800, 800))
		cv2.imshow(windowName, img)
		cv2.setMouseCallback(windowName, click_event)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		click_coordinates[imgfile] = (xc, yc)
		for coord in pass_coordinates:
			val =  inOut(coord[0], coord[1], xc, yc, 30)
			if val is True:
				login_stats.append(True)
	if len(login_stats) == 3 and login_stats == [True, True, True]:
		os.system("cls")
		print("\nLogin Successful\n")
		print("--------------------------------")
		print(f"\n  Welcome {newval[1]}\n")
		return False
	else:
		os.system("cls")
		print("\nLogin Failed [email ID or password is incorrect or you are not registered]\n")
		return True

# driver Function
if __name__ == '__main__':
	while True:
		print("\n [+] Select a option:\n -> 1] Login \n -> 2] Register as new user \n -> 3] Exit\n")
		inval = int(input())
		os.system('cls')

		while True:
			if inval == 1:
				bool_login = loginUser()			
				if bool_login is False:
					ask_user = str(input("Enter (Y or y) to logout:"))
					os.system('cls')
					if ask_user in ('Y', 'y'):
						break
					break
				break
					
			
			elif inval == 2:
				bool_val = registerUser()
				if bool_val is False:
					break
				break
			
			elif inval == 3:
				sys.exit()
			else:
				print("\n [-] Option not found ")
				break
