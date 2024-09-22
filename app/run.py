from flask import Flask, render_template, request, make_response, redirect, url_for
import datetime

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    # Obtener preferencias de las cookies
    font = request.cookies.get('font', 'Arial')
    color = request.cookies.get('color', '#000000')
    
    # Obtener enlaces visitados de las cookies
    visited_links = request.cookies.get('visited_links', '')
    visited_links = visited_links.split(',') if visited_links else []
    
    # Log de valores obtenidos de las cookies
    print(f"Font: {font}, Color: {color}, Visited Links: {visited_links}")

    return render_template('index.html', font=font, color=color, visited_links=visited_links)

# Ruta para guardar las preferencias
@app.route('/set_preferences', methods=['POST'])
def set_preferences():
    font = request.form.get('font')
    color = request.form.get('color')

    resp = make_response(redirect(url_for('index')))
    
    # Establecer un tiempo de expiración de 2 minutos (120 segundos)
    max_age = 120  # 120 segundos = 2 minutos
    resp.set_cookie('font', font, max_age=max_age)
    resp.set_cookie('color', color, max_age=max_age)
    
    # Log de las cookies que estamos guardando
    print(f"Setting cookies: Font={font}, Color={color}, Max Age={max_age} seconds")

    return resp

# Ruta para manejar los enlaces
@app.route('/visit/<link_name>')
def visit_link(link_name):
    links = {
        'Google': 'https://www.google.com',
        'YouTube': 'https://www.youtube.com',
        'Facebook': 'https://www.facebook.com'
    }

    # Obtener la URL correspondiente al nombre del enlace
    url = links.get(link_name)
    if not url:
        return redirect(url_for('index'))  # Si el enlace no está definido, redirige al índice

    # Obtener enlaces visitados de las cookies
    visited_links = request.cookies.get('visited_links', '').split(',')
    visited_links = [link for link in visited_links if link]  # Eliminar entradas vacías

    # Si el enlace no ha sido visitado antes, añadirlo
    if link_name not in visited_links:
        visited_links.append(link_name)

    # Actualizar cookies de enlaces visitados con tiempo de expiración de 2 minutos
    resp = make_response(redirect(url))
    max_age = 120  # 2 minutos en segundos
    resp.set_cookie('visited_links', ','.join(visited_links), max_age=max_age)

    # Log de las cookies actualizadas
    print(f"Visited Links after update: {visited_links}, Max Age={max_age} seconds")

    return resp

if __name__ == '__main__':
    app.run(debug=True)
