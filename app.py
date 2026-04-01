from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

# Function to generate a random 6-character Captcha (Letters and Numbers)
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/')
def index():
    # Generate a fresh Captcha every time the page loads
    fresh_captcha = generate_captcha()
    return render_template('login.html', captcha_text=fresh_captcha)

@app.route('/login_step_1', methods=['POST'])
def login_step_1():
    username = request.form.get('username')
    password = request.form.get('password')
    user_captcha = request.form.get('captcha_input')
    real_captcha = request.form.get('real_captcha')

    # 1. Check if Captcha is correct
    if user_captcha != real_captcha:
        return render_template('login.html', captcha_text=generate_captcha(), error="Invalid CAPTCHA!")

    # 2. Check if Username and Password are correct (Dummy credentials for testing)
    if username == "admin@example.com" and password == "SecurePass123":
        
        # 3. If everything is correct, generate the OTP
        otp_code = str(random.randint(100000, 999999))
        with open("otp_inbox.txt", "w") as file:
            file.write(otp_code)
            
        print(f"Server generated OTP for {username}: {otp_code}")
        return render_template('verify.html', message="OTP sent to your device!")
    
    else:
        return render_template('login.html', captcha_text=generate_captcha(), error="Invalid Username or Password!")

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_entered_otp = request.form['otp']
    
    with open("otp_inbox.txt", "r") as file:
        real_otp = file.read().strip()
        
    if user_entered_otp == real_otp:
        return "<h1>Login Successful! Welcome to the Dashboard.</h1>"
    else:
        return render_template('verify.html', message="Invalid OTP. Try again.")

if __name__ == '__main__':
    app.run(debug=True)
