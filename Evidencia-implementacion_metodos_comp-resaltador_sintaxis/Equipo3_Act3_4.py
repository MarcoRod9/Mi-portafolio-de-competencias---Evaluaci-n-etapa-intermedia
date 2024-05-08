# Analizador Lexico Python
# TC2037 Implementacion de metodos computacionales
# Grupo 605
# Actividad 3.4 Analizador Lexico.
# A01652327 | Diego Esparza Hurtado
# A00834672 | Marco Antonio Rodriguez Amezcua

# Correr con comando: 'python Equipo3_Act3_4.py'
# En caso de querer modificar el archivo .py a leer, modificar en la linea: 119
# En caso de querer modificar el nombre del archivo .html de salida, modificar en la linea: 131


# Se importa la libreria re para generar las expresiones regulares.
import re

# Se definen las expresiones regulares, su categoria lexica y su color.
expresionesRegulares = [
    
    # Imaginario (pointfloat | exponentfloat) jJ
    (r'((\d[_]?)*\.(\d[_]?)*([eE][-]?(\d[_]?)+)?|(\d(_?\d)*))([jJ])', 'IMAGINARIO', 'Purple'),
    (r'((\d[_]?)+[eE][-]?(\d[_]?)+)([jJ])', 'IMAGINARIO', 'Purple'),

    # Flotantes (pointfloat | exponentfloat).
    (r'(\d[_]?)*\.(\d[_]?)*([eE][-]?(\d[_]?)+(\.\d[_]?)?)?', 'FLOTANTE', 'Coral'),
    (r'(\d[_]?)+[eE][-]?(\d[_]?)+', 'FLOTANTE', 'Coral'),

    # Enteros (decinteger | bininteger | octinteger | hexinteger).
    (r'0[bB](_?[01])+|0[oO](_?[0-7])+|0[xX](_?[\da-fA-F])+|[1-9]\d*(_?\d)*|0+', 'ENTERO', 'DarkKhaki'),

    #Delimitadores.
    (r'\(|\)|\[|\]|\{|\}|\,|\.|\;|\-\>|\+\=|\-\=|\*\=|\/\=|/\/\=|\%\=|\@\=|\&\=|\|\=|\^\=|\>\>\=|\<\<\=|\*\*\=', 'DELIMITADOR', "Teal"),

    # Operadores.
    (r'\+|\-|\*|\*\*|\/|\/\/|\%|\@|\<\<|\>\>|\&|\||\^|\~|\:\=|\<\=?|\>\=?|\=\=|\!\=', 'OPERADOR', "Blue"),

    # Delimitadores.
    (r'\(|\)|\[|\]|\{|\}|\,|\:|\.|\;|\@|\=|\-\>|\+\=|\-\=|\*\=|\/\=', 'DELIMITADOR', "Teal"),

    # Identificadores.
    (r'[_]?[_]?[a-zA-Z][a-zA-Z0-9_]*', 'IDENTIFICADOR', "HotPink"),

    # Palabras reservadas / Cambiarlas.
    (r'False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield', 'RESERVADA', 'LimeGreen'),

    # Espacios en blanco.
    (r'\s', 'ESPACIO', "White"), # espacios en blanco

    # Comentario.
    (r'#.*$', 'COMENTARIO', "Brown"),
    
    # Simbolos de error.
    (r'\$|\?|\`', 'ERROR', "Red"),

    # Literales
    (r"(['\"]{1,3}).*?\1", 'LITERALES', "Orange"),
]

# Palabras reservadas
palabrasReservadas = ['False','None','True','and','as','assert','async','await','break','class','continue','def','del','elif','else','except','finally','for','from','global','if','import','in','is','lambda','nonlocal','not','or','pass','raise','return','try','while','with','yield']

# Se inicializa una variable global para almacenar todo el codigo que se utilizara para generar el HTML.
global html

# Se inicia el archivo HTML.
html = f"<html><head><style>"

# Se agregan los tipos de categoria y su respectivo color para ser posteriormente agregados y pintados en el HTML.
for patron, tipo, color in expresionesRegulares:
    html += f"span.{tipo} {{ color: {color}; }} "
html += f"</style></head><body>"

# Arreglo para almacenar cada categoria lexica y su respectivo color.
tipoColores = []
# Se agrega una tupla con el tipo y color al arreglo tipoColores si este no se encuentra aun en el arreglo.
for patron, tipo, color in expresionesRegulares:
    if ((tipo, color) not in tipoColores):
        tipoColores.append((tipo, color))

# Para cada categoria lexica se agrega un cuadrado de su color y el nombre de la categoria lexica al archivo HTML para mayor comprension.
for tipo, color in tipoColores:
    if tipo != 'ESPACIO':
        html += f'<span style="display:inline-block; width: 1em; height: 1em; background-color: {color};"></span> <span style="color: {color};">{tipo}</span>'
        html += f'<br>'

html += f'<br>'
html += f'<br>'

# Funcion para reconocer los tokens.
def reconocer_tokens(expresion):

    # Se utiliza la variable html previamente declarada.
    global html

    # Se revisa la linea.
    while expresion:
        encontrado = False
        # Se busca si existe un patron con el metodo de re 'match'.
        for patron, tipo, color in expresionesRegulares:
            match = re.match(patron, expresion)
            # En caso de que haya una coincidencia, se agrega al archivo HTML con su respectiva categoria lexica.
            if match:
                encontrado = True
                token = match.group(0)
                if tipo == 'ESPACIO':
                    html += f'<span>&nbsp;</span>'
                else:
                    if tipo == 'IDENTIFICADOR' and token in palabrasReservadas:
                        tipo = 'RESERVADA'
                    html += f"<span class={tipo}>{token}</span> "
                expresion = expresion[len(token):]
                break
        # En caso de que no se encuentre, se agrega como error con su respectivo color rojo.
        if not encontrado:
            tipo = 'ERROR'
            html += f"<span class={tipo}>{expresion}</span> "
            return f'Error: expresion mal formada: {expresion}'

# Se lee el archivo de entrada de python en busqueda de los tokens.
with open('archivo.py', 'r') as archivo:
    # Se obtienen los tokens y se agregan por linea.
    for linea in archivo:
        if not linea:
            continue
        tokens = reconocer_tokens(linea)
        html += f'<br>'

# Se termina de escribir el codigo del HTML.
html += f"</body></html>"

# Se escribe el archivo de salida de HTML+CSS
with open('Archivo_Salida.html', 'w') as f:
    f.write(html)