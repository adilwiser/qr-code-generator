from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import qrcode
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Necessary for flash messages

# Ensure the static/qrcodes directory exists
QR_DIRECTORY = 'static/qrcodes'
if not os.path.exists(QR_DIRECTORY):
    os.makedirs(QR_DIRECTORY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr_code():
    data = request.form.get('data')

    if data:
        try:
            # Generate a unique filename using a timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f'qr_code_{timestamp}.png'
            file_path = os.path.join(QR_DIRECTORY, filename)

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')

            # Save the QR code image
            img.save(file_path)

            # Return the QR code image
            return send_file(file_path, as_attachment=True)

        except Exception as e:
            flash(f"An error occurred while generating the QR code: {e}", "error")
            return redirect(url_for('index'))
    else:
        flash("No data provided. Please enter some text to generate a QR code.", "warning")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
