from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import screen_brightness_control as sbc
from ctypes import cast, POINTER
import comtypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# Configuração do Swagger
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "PC Control API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def set_volume(level):
    comtypes.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100, None)
    comtypes.CoUninitialize()

def get_volume():
    comtypes.CoInitialize()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    vol_level = int(volume.GetMasterVolumeLevelScalar() * 100)
    comtypes.CoUninitialize()
    return vol_level

@app.route("/set_brightness", methods=["POST"])
def set_brightness():
    """Define o brilho da tela.
    ---
    parameters:
      - name: level
        in: body
        required: true
        schema:
          type: object
          properties:
            level:
              type: integer
              minimum: 0
              maximum: 100
    responses:
      200:
        description: Brilho ajustado com sucesso
    """
    data = request.json
    level = data.get("level")
    if level is None or not (0 <= level <= 100):
        return jsonify({"error": "Invalid brightness level. Must be between 0 and 100."}), 400
    sbc.set_brightness(level)
    return jsonify({"message": "Brightness set successfully", "brightness": level})

@app.route("/get_brightness", methods=["GET"])
def get_brightness():
    """Obtém o brilho atual da tela.
    ---
    responses:
      200:
        description: Brilho atual retornado com sucesso
    """
    return jsonify({"brightness": sbc.get_brightness(display=0)})

@app.route("/set_volume", methods=["POST"])
def set_volume_route():
    """Define o volume do sistema.
    ---
    parameters:
      - name: level
        in: body
        required: true
        schema:
          type: object
          properties:
            level:
              type: integer
              minimum: 0
              maximum: 100
    responses:
      200:
        description: Volume ajustado com sucesso
    """
    data = request.json
    level = data.get("level")
    if level is None or not (0 <= level <= 100):
        return jsonify({"error": "Invalid volume level. Must be between 0 and 100."}), 400
    set_volume(level)
    return jsonify({"message": "Volume set successfully", "volume": level})

@app.route("/get_volume", methods=["GET"])
def get_volume_route():
    """Obtém o volume atual do sistema.
    ---
    responses:
      200:
        description: Volume atual retornado com sucesso
    """
    return jsonify({"volume": get_volume()})

@app.route("/static/swagger.json")
def swagger_json():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "PC Control API",
            "description": "API para controlar volume e brilho do PC",
            "version": "1.0.0"
        },
        "paths": {
            "/set_brightness": {
                "post": {
                    "summary": "Define o brilho",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": "true",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "level": {"type": "integer"}
                                }
                            }
                        }
                    ],
                    "responses": {"200": {"description": "Brilho ajustado"}}
                }
            },
            "/get_brightness": {
                "get": {
                    "summary": "Obtém o brilho",
                    "responses": {"200": {"description": "Brilho retornado"}}
                }
            },
            "/set_volume": {
                "post": {
                    "summary": "Define o volume",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": "true",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "level": {"type": "integer"}
                                }
                            }
                        }
                    ],
                    "responses": {"200": {"description": "Volume ajustado"}}
                }
            },
            "/get_volume": {
                "get": {
                    "summary": "Obtém o volume",
                    "responses": {"200": {"description": "Volume retornado"}}
                }
            }
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
