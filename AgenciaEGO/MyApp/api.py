from flask import Flask, jsonify, request

from autos import autos

app = Flask(__name__)

from flask import jsonify, request

#Endpoint para obtener todos los autos y la paginación
@app.route('/autos', methods=['GET'])
def getAutos():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    autos_paginados = autos[start_index:end_index]

    total_pages = -(-len(autos) // per_page) if autos else 0

    if not autos_paginados:
        return jsonify({"mensaje": "No hay autos disponibles"}), 204

    return jsonify({
        "mensaje": "Lista de Autos",
        "autos": autos_paginados,
        "total_pages": total_pages,
        "current_page": page
    })

#Endpoint para filtrar autos según su tipo (Auto, Comercial, PickUps, SUVs, Crossovers)
#recibe el parametro el tipo
@app.route('/autos/<string:tipo>', methods=['GET'])
def getAutoTipo(tipo):
    autoTipo = [auto for auto in autos if auto["tipo"] == tipo]
    if (len(autoTipo) > 0):
        return jsonify({"auto": autoTipo})
    return jsonify({"mensaje": "No Hay Autos de Este Tipo."}), 404

#Endpoint para agregar un nuevo auto
@app.route('/autos', methods=['POST'])
def addAuto():
    try:
        nuevoAuto = {
            "tipo": request.json["tipo"],
            "modelo": request.json["modelo"],
            "anio": int(request.json["anio"]),
            "precio": request.json["precio"],
            "caracteristicas": {
                "caracteristica": request.json["caracteristicas"]["caracteristica"],
                "descripcion": request.json["caracteristicas"]["descripcion"]
            }
        }
        autos.append(nuevoAuto)
        return jsonify({"mensaje": "Auto Agregado Correctamente", "autos": autos})
    except KeyError as e:
        return jsonify({"error": f"Campo {str(e)} faltante"}), 400
    except ValueError:
            return jsonify({"error": "El campo 'anio' debe ser un número entero"}), 400    

#Endpoint para editar el auto, recibe como parametro el nombre del auto (modelo)    
@app.route('/autos/<string:modelo>', methods=['PUT'])
def editAuto(modelo):
    autoEncontrado = [auto for auto in autos if auto["modelo"] == modelo]  
    if (len(autoEncontrado) > 0):
        try:
            autoEncontrado[0]["tipo"] = request.json["tipo"]
            autoEncontrado[0]["modelo"] = request.json["modelo"]
            autoEncontrado[0]["anio"] = int(request.json["anio"])
            autoEncontrado[0]["precio"] = request.json["precio"]
            autoEncontrado[0]["caracteristicas"]["caracteristica"] = request.json["caracteristicas"]["caracteristica"]
            autoEncontrado[0]["caracteristicas"]["descripcion"] = request.json["caracteristicas"]["descripcion"]
            return jsonify({
                "mensaje": "Auto Actualizado Correctamente",
                "auto": autoEncontrado[0]
            })
        except KeyError as e:
            return jsonify({"error": f"Campo {str(e)} faltante"}), 400
        except ValueError:
            return jsonify({"error": "El campo 'anio' debe ser un número entero"}), 400    
    return jsonify({"mensaje": "Auto no encontrado"}), 404
    
#Endpoint para eliminar un auto, recibe como parametro el nombre del auto (modelo)  
@app.route('/autos/<string:modelo>', methods=['DELETE'])
def eliminarAuto(modelo):
    autoEncontrado = [auto for auto in autos if auto["modelo"] == modelo]  
    if (len(autoEncontrado) > 0):
        autos.remove(autoEncontrado[0])
        return jsonify({
            "mensaje": "Auto Eliminado Correctamente",
            "auto": autos
        })
    return jsonify({
        "mensaje": f"No se encontró el auto con modelo '{modelo}'"
    }), 404
    
#Endpoint que retorna los autos ordenados de menor a mayor en cuanto al año    
@app.route('/autos/menor_anio', methods=['GET'])
def getAutoMenorAnio():
    autos_ordenados = sorted(autos, key=lambda x: x["anio"])
    return jsonify(autos_ordenados)

#Endpoint que retorna los autos ordenados de mayor a menor en cuanto al año    
@app.route('/autos/mayor_anio', methods=['GET'])
def getAutoMayorAnio():
    autos_ordenados = sorted(autos, key=lambda x: x["anio"], reverse=True)
    return jsonify(autos_ordenados)    

#Endpoint que retorna los autos ordenados de menor a mayor en cuanto al precio   
@app.route('/autos/menor_precio', methods=['GET'])
def getAutoMenorPrecio():
    autos_ordenados = sorted(autos, key=lambda x: x["precio"])
    return jsonify(autos_ordenados)   

#Endpoint que retora los autos ordenados de mayor a menor en cuanto al precio
@app.route('/autos/mayor_precio', methods=['GET'])
def getAutoMayorPrecio():
    autos_ordenados = sorted(autos, key=lambda x: x["precio"], reverse=True)
    return jsonify(autos_ordenados)   
    
if __name__ == '__main__':
    app.run(debug=True, port=4000)
