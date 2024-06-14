from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('siwi'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

# Route for SIWI page
@app.route('/siwi', methods=['GET', 'POST'])
def siwi():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    siwis = conn.execute('SELECT * FROM siwis WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    if request.method == 'POST':
        siwi_info = request.form['siwi_info']
        conn = get_db_connection()
        conn.execute('INSERT INTO siwis (user_id, siwi_info) VALUES (?, ?)', (user_id, siwi_info))
        conn.commit()
        conn.close()
        flash('SIWI added successfully', 'success')
        return redirect(url_for('siwi'))

    return render_template('siwi.html', siwis=siwis)

# Route to delete a SIWI
@app.route('/delete_siwi/<int:siwi_id>', methods=['POST'])
def delete_siwi(siwi_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM siwis WHERE id = ?', (siwi_id,))
    conn.commit()
    conn.close()
    flash('SIWI deleted successfully', 'success')
    return redirect(url_for('siwi'))

# Route to logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
