# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
   sudo pip install <package> -t .

"""
from __future__ import print_function

import os
import sys
import json
import re
import traceback

base_path = tmp_global_obj["basepath"]
cur_path = os.path.join(base_path, "modules", "camofox", "libs")

if cur_path not in sys.path:
    sys.path.append(cur_path)
    
global CamofoxClient
from camofoxObject import CamofoxClient

module = GetParams("module")

def _to_bool(value):
    """
    Convierte valores de checkbox/string de Rocketbot a booleano.
    """
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    value = str(value).strip().lower()
    return value in ["true", "1", "yes", "si", "sí", "on", "checked"]


def _get_client():
    """
    Crea cliente Camofox.
    base_url y user_id pueden venir desde parámetros del comando.
    Si no vienen, usa valores por defecto.
    """
    base_url = GetParams("base_url") or "http://localhost:9377"
    base_url = str(base_url).strip().rstrip("/")
    if base_url.lower().endswith("/health"):
        base_url = base_url[:-7]

    if not base_url:
        base_url = "http://localhost:9377"

    user_id = GetParams("user_id") or "rocketbot"

    return CamofoxClient(
        base_url=base_url,
        user_id=user_id
    )


try:
    if module == "start_server":
        server_path = GetParams("server_path")
        command = GetParams("command") or "npx -y @askjo/camofox-browser"
        wait_seconds = GetParams("wait_seconds") or 20
        health_timeout = GetParams("health_timeout") or 1
        poll_interval = GetParams("poll_interval") or 0.4
        var = GetParams("var")

        if not server_path:
            raise Exception("The server_path parameter is required.")

        client = _get_client()

        response = client.start_server(
            server_path=server_path,
            command=command,
            wait_seconds=wait_seconds,
            health_timeout=health_timeout,
            poll_interval=poll_interval
        )

        if var: 
            SetVar(var, response)

    if module == "health":
        var = GetParams("var")

        client = _get_client()
        response = client.health()

        if var:
            SetVar(var, response)


    if module == "create_tab":
        url = GetParams("url")
        session_key = GetParams("session_key") or "default"
        request_timeout = GetParams("request_timeout") or GetParams("timeout_seconds") or 60
        var = GetParams("var")

        if not url:
            raise Exception("The URL parameter is required.")

        client = _get_client()
        try:
            response = client.create_tab(
                url=url,
                session_key=session_key,
                request_timeout=request_timeout
            )
        except TypeError as te:
            # Compatibilidad con versiones antiguas cargadas en memoria.
            if "request_timeout" in str(te):
                response = client.create_tab(
                    url=url,
                    session_key=session_key
                )
            else:
                raise

        if var:
            SetVar(var, response)


    if module == "navigate":
        tab_id = GetParams("tab_id")
        url = GetParams("url")
        var = GetParams("var")

        if not tab_id:
            raise Exception("The tab_id parameter is required.")

        if not url:
            raise Exception("The URL parameter is required.")

        client = _get_client()
        response = client.navigate(
            tab_id=tab_id,
            url=url
        )

        if var:
            SetVar(var, response)


    if module == "snapshot":
        tab_id = GetParams("tab_id")
        var = GetParams("var")

        if not tab_id:
            raise Exception("The tab_id parameter is required.")

        client = _get_client()
        response = client.snapshot(tab_id=tab_id)

        if var:
            SetVar(var, response)


    if module == "click":
        tab_id = GetParams("tab_id")
        ref = GetParams("ref")
        var = GetParams("var")

        if not tab_id:
            raise Exception("The tab_id parameter is required.")

        if not ref:
            raise Exception("The ref parameter is required.")

        client = _get_client()
        response = client.click(
            tab_id=tab_id,
            ref=ref
        )

        if var:
            SetVar(var, response)
            
            
            
    if module == "evaluate":
        tab_id = GetParams("tab_id")
        expression = GetParams("expression")
        request_timeout = GetParams("request_timeout") or 30
        var = GetParams("var")

        if not tab_id:
            raise Exception("The tab_id parameter is required.")

        if not expression:
            raise Exception("The expression parameter is required.")

        client = _get_client()

        response = client.evaluate(
            tab_id=tab_id,
            script=expression,
            request_timeout=request_timeout
        )

        if var:
            SetVar(var, response)
            
    if module == "hover":
        tab_id = GetParams("tab_id")
        ref = GetParams("ref")
        selector = GetParams("selector")
        var = GetParams("var")

        if not tab_id:
            raise Exception("The tab_id parameter is required.")

        if not ref and not selector:
            raise Exception("The ref or selector parameter is required.")

        client = _get_client()

        response = client.hover(
            tab_id=tab_id,
            ref=ref,
            selector=selector
        )

        if var:
            SetVar(var, response)


    if module == "download_files":
        tab_id = GetParams("tab_id")
        save_path = GetParams("save_path")
        file_type = GetParams("file_type") or "Excel"
        overwrite = True if GetParams("overwrite") is None else _to_bool(GetParams("overwrite"))
        var = GetParams("var")

        if not tab_id:
            raise Exception("The tab_id parameter is required.")

        client = _get_client()
        response = client.wait_for_download_and_save(
            tab_id=tab_id,
            save_path=save_path,
            file_type=file_type,
            overwrite=overwrite
        )

        if var:
            SetVar(var, response)


    if module == "type_text":
        tab_id = GetParams("tab_id")
        ref = GetParams("ref")
        selector = GetParams("selector")
        text = GetParams("text")
        press_enter = _to_bool(GetParams("press_enter"))
        use_js_fallback = True if GetParams("use_js_fallback") is None else _to_bool(GetParams("use_js_fallback"))
        var = GetParams("var")

        if not tab_id:
            raise Exception("The tab_id parameter is required.")

        if not ref and not selector:
            raise Exception("The ref or selector parameter is required.")

        if text is None:
            text = ""

        client = _get_client()
        try:
            response = client.type_text(
                tab_id=tab_id,
                ref=ref,
                selector=selector,
                text=text,
                press_enter=press_enter,
                use_js_fallback=use_js_fallback
            )
        except TypeError:
            # Compatibilidad con versiones antiguas del cliente cargadas en memoria.
            response = client.type_text(
                tab_id=tab_id,
                ref=ref,
                text=text,
                press_enter=press_enter
            )

        if var:
            SetVar(var, response)


    if module == "screenshot":
        tab_id = GetParams("tab_id")
        save_path = GetParams("save_path")
        var = GetParams("var")

        if not tab_id:
            raise Exception("The tab_id parameter is required.")

        client = _get_client()
        response = client.screenshot(
            tab_id=tab_id,
            save_path=save_path
        )

        if var:
            SetVar(var, response)
            
    if module == "scroll":
        tab_id = GetParams("tab_id")
        direction = GetParams("direction")
        amount = GetParams("amount")
        var = GetParams("var")
        
        if not tab_id:
            raise Exception("The tab_id parameter is required.")
        
        if direction:
            direction = str(direction).strip()
        
        client = _get_client()
        response = client.scroll(
            tab_id=tab_id,
            direction=direction if direction else "down",
            amount=amount if amount else 500
        )
        
        if var:
            SetVar(var, response)
            
    

    if module == "stop_server":
        pid = GetParams("pid")
        var = GetParams("result_var")

        if not pid:
            raise Exception("The pid parameter is required.")

        client = _get_client()

        response = client.stop_server(pid=pid)
        

        if var:
            SetVar(var, response)

except Exception as e:
    traceback.print_exc()

    var = GetParams("var")

    error_response = {
        "ok": False,
        "error": str(e),
        "module": module
    }

    if var:
        SetVar(var, error_response)
    else:
        raise