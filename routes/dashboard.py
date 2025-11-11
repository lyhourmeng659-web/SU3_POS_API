from app import app


@app.route('/dashboard')
def dashboard():  # put application's code here
    # arr = [1, 2]
    # print(arr[2])
    return '<center><h1>dashboard</h2></center>'



