import requests
import os
import signal
import subprocess
import time
import base64
import json
import re

class CamofoxClient:
    def __init__(self, base_url="http://localhost:9377", user_id="rocketbot"):
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.session = requests.Session()

    def health(self, timeout=15):
        r = self.session.get(f"{self.base_url}/health", timeout=float(timeout))
        r.raise_for_status()
        return r.json()

    def start_server(self, server_path, command="npx -y @askjo/camofox-browser", wait_seconds=20, health_timeout=1, poll_interval=0.4):
        """
        Starts Camofox Browser Server in background.

        server_path:
            Folder where the process will run.
            Can be any valid folder if using npx.
            If using npm start, it should be the camofox-browser repo folder.

        command examples:
            npx -y @askjo/camofox-browser
            npm start
            camofox-browser
        """
        if not server_path:
            raise Exception("server_path is required.")

        if not os.path.exists(server_path):
            raise Exception("server_path does not exist: {}".format(server_path))

        # Si el servidor ya esta arriba, no iniciar un nuevo proceso.
        try:
            health = self.health(timeout=health_timeout)
            if health.get("ok") is True:
                return {
                    "ok": True,
                    "already_running": True,
                    "pid": None,
                    "health": health
                }
        except Exception:
            pass

        env = os.environ.copy()
        env["CAMOFOX_CRASH_REPORT_ENABLED"] = "false"

        process = subprocess.Popen(
            command,
            cwd=server_path,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True
        )

        start_time = time.time()
        last_error = None
        wait_seconds = float(wait_seconds)
        poll_interval = max(0.1, float(poll_interval))
        health_timeout = max(0.2, float(health_timeout))

        while time.time() - start_time < wait_seconds:
            try:
                health = self.health(timeout=health_timeout)
                if health.get("ok") is True:
                    return {
                        "ok": True,
                        "pid": process.pid,
                        "health": health
                    }
            except Exception as e:
                last_error = str(e)
                time.sleep(poll_interval)

        return {
            "ok": False,
            "pid": process.pid,
            "error": "Camofox server did not respond in time.",
            "last_error": last_error
        }

    def stop_server(self, pid=None):
        """
        Stops Camofox process by PID.
        On Windows, uses taskkill to also kill child processes.
        """
        if not pid:
            raise Exception("pid is required.")

        pid = str(pid).strip()

        if os.name == "nt":
            cmd = 'taskkill /PID {} /T /F'.format(pid)
            result = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            stdout, stderr = result.communicate()

            return {
                "ok": result.returncode == 0,
                "pid": pid,
                "stdout": stdout.decode("utf-8", "ignore"),
                "stderr": stderr.decode("utf-8", "ignore")
            }
        try:
            os.kill(int(pid), signal.SIGTERM)
        except ProcessLookupError:
            pass

        return {
            "ok": True,
            "pid": pid
        }
        
    def create_tab(self, url, session_key="default", request_timeout=60):
        payload = {
            "userId": self.user_id,
            "sessionKey": session_key,
            "url": url
        }
        request_timeout = int(request_timeout)
        try:
            r = requests.post(f"{self.base_url}/tabs", json=payload, timeout=request_timeout)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.Timeout:
            url_str = str(url).strip().lower()
            if url_str in ["about:blank", "about:blank/"]:
                raise

            # Fallback: crea la pestaña en blanco y navega en un segundo paso.
            blank_payload = {
                "userId": self.user_id,
                "sessionKey": session_key,
                "url": "about:blank"
            }
            r = requests.post(f"{self.base_url}/tabs", json=blank_payload, timeout=request_timeout)
            r.raise_for_status()
            tab_data = r.json()

            tab_id = tab_data.get("tabId") or tab_data.get("id")
            if not tab_id:
                return tab_data

            nav_payload = {
                "userId": self.user_id,
                "url": url
            }
            nav_timeout = request_timeout if request_timeout >= 30 else 30
            nav_response = requests.post(
                f"{self.base_url}/tabs/{tab_id}/navigate",
                json=nav_payload,
                timeout=nav_timeout
            )
            nav_response.raise_for_status()
            tab_data["navigate"] = nav_response.json()

            return tab_data

    def navigate(self, tab_id, url):
        payload = {
            "userId": self.user_id,
            "url": url
        }
        r = requests.post(f"{self.base_url}/tabs/{tab_id}/navigate", json=payload, timeout=30)
        r.raise_for_status()
        return r.json()

    def snapshot(self, tab_id):
        r = requests.get(
            f"{self.base_url}/tabs/{tab_id}/snapshot",
            params={"userId": self.user_id},
            timeout=30
        )
        r.raise_for_status()
        return r.json()

    def _get_ref_role(self, tab_id, ref):
        """
        Intenta obtener el tipo de elemento del ref (textbox, button, link, etc.)
        leyendo el snapshot actual del tab.
        """
        if not ref:
            return None

        try:
            snap = self.snapshot(tab_id)
            snapshot_text = snap.get("snapshot", "") if isinstance(snap, dict) else ""
            if not snapshot_text:
                return None

            for line in str(snapshot_text).splitlines():
                if f"[{ref}]" in line:
                    # Ejemplo de linea: - textbox "RUT" [e1]: ...
                    m = re.search(r"-\s*([a-zA-Z_]+)", line)
                    if m:
                        return m.group(1).lower()
            return None
        except Exception:
            return None

    def _infer_selector_from_snapshot_ref(self, tab_id, ref):
        """
        Intenta inferir un selector CSS estable usando el contexto del snapshot.
        Ejemplos:
        - RUT -> input de texto (no password)
        - Contraseña -> input[type="password"]
        """
        if not ref:
            return None

        try:
            snap = self.snapshot(tab_id)
            snapshot_text = snap.get("snapshot", "") if isinstance(snap, dict) else ""
            if not snapshot_text:
                return None

            lines = str(snapshot_text).splitlines()
            ref_idx = -1
            ref_token = f"[{ref}]"
            for i, line in enumerate(lines):
                if ref_token in line:
                    ref_idx = i
                    break

            if ref_idx < 0:
                return None

            current_line = lines[ref_idx].lower()
            prev_line = lines[ref_idx - 1].lower() if ref_idx > 0 else ""
            next_line = lines[ref_idx + 1].lower() if ref_idx + 1 < len(lines) else ""
            context = " ".join([current_line, prev_line, next_line])

            if "contrase" in context or "password" in context:
                return 'input[type="password"]'

            if "rut" in context:
                return 'input[name*="rut"], input[id*="rut"], input[placeholder*="RUT"], input[type="text"], input:not([type])'

            return None
        except Exception:
            return None

    def click(self, tab_id, ref):
        payload = {
            "userId": self.user_id,
            "ref": ref
        }
        r = self.session.post(f"{self.base_url}/tabs/{tab_id}/click", json=payload, timeout=30)
        
        r.raise_for_status()
        return r.json()

    def hover(self, tab_id, ref):
        payload = {
            "userId": self.user_id,
            "ref": ref
        }
        r = self.session.post(f"{self.base_url}/tabs/{tab_id}/hover", json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    def hover(self, tab_id, ref=None, selector=None):
        payload = {
            "userId": self.user_id,
            "targetId": tab_id,
            "kind": "hover"
        }

        if ref:
            payload["ref"] = ref
        elif selector:
            payload["selector"] = selector
        else:
            raise Exception("ref or selector is required.")

        r = self.session.post(
            f"{self.base_url}/act",
            json=payload,
            timeout=30
        )

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return {
                "ok": False,
                "status_code": r.status_code,
                "error": str(e),
                "response": r.text,
                "payload": payload
            }

        try:
            return r.json()
        except Exception:
            return {
                "ok": True,
                "raw": r.text,
                "payload": payload
            }
    def evaluate(self, tab_id, script, request_timeout=30):
        # Compatibilidad: algunas versiones esperan "expression" y otras "script".
        payload_expression = {
            "userId": self.user_id,
            "expression": script
        }
        r = self.session.post(
            f"{self.base_url}/tabs/{tab_id}/evaluate",
            json=payload_expression,
            timeout=int(request_timeout)
        )

        if r.status_code == 400:
            payload_script = {
                "userId": self.user_id,
                "script": script
            }
            r = self.session.post(
                f"{self.base_url}/tabs/{tab_id}/evaluate",
                json=payload_script,
                timeout=int(request_timeout)
            )

        r.raise_for_status()
        return r.json()

    def _to_js_single_quoted(self, value):
        """
        Convierte un valor Python en literal JS entre comillas simples.
        Ejemplo: abc -> 'abc'
        """
        s = "" if value is None else str(value)
        s = s.replace("\\", "\\\\")
        s = s.replace("'", "\\'")
        s = s.replace("\r", "\\r")
        s = s.replace("\n", "\\n")
        return "'{}'".format(s)

    def _type_text_with_evaluate(self, tab_id, text, press_enter=False, selector=None):
        """
        Inyecta texto directamente usando JavaScript en el navegador,
        esquivando las restricciones de foco y validación agresiva del banco.
        """
        actual_selector = selector if selector else 'input[type="password"]'
        selector_js = json.dumps(actual_selector)
        text_js = json.dumps(text)
        enter_json = "true" if press_enter else "false"

        script = (
            "(() => {{"
            "  var el = document.querySelector({selector});"
            "  if (!el) {{"
            "    return {{ ok: false, error: 'Elemento no encontrado con el selector provisto.' }};"
            "  }}"
            "  try {{ el.focus(); }} catch (e) {{}}"
            "  el.value = {text};"
            "  el.dispatchEvent(new Event('input', {{ bubbles: true, cancelable: true }}));"
            "  el.dispatchEvent(new Event('change', {{ bubbles: true, cancelable: true }}));"
            "  el.dispatchEvent(new Event('blur', {{ bubbles: true, cancelable: true }}));"
            "  if ({press_enter}) {{"
            "    var evData = {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }};"
            "    el.dispatchEvent(new KeyboardEvent('keydown', evData));"
            "    el.dispatchEvent(new KeyboardEvent('keypress', evData));"
            "    el.dispatchEvent(new KeyboardEvent('keyup', evData));"
            "  }}"
            "  return {{ ok: true, valueLength: el.value.length }};"
            "}})();"
        ).format(selector=selector_js, text=text_js, press_enter=enter_json)

        return self.evaluate(tab_id=tab_id, script=script, request_timeout=30)
    def type_text(self, tab_id, ref, text, press_enter=False, selector=None, use_js_fallback=True):
        payload = {
            "userId": self.user_id,
            "text": text,
            "pressEnter": press_enter
        }
        if selector:
            payload["selector"] = selector
        else:
            payload["ref"] = ref

        ref_role = self._get_ref_role(tab_id, ref) if (ref and not selector) else None
        inferred_selector = self._infer_selector_from_snapshot_ref(tab_id, ref) if (ref and not selector) else None

        # Si viene ref (e1/e3), priorizar /type porque respeta el ref exacto (ej: RUT e1).
        # Si /type falla (500 u otro), usar evaluate como fallback.
        if ref and not selector:
            # Primer intento: selector inferido por snapshot para respetar campo correcto (RUT/Contraseña).
            if inferred_selector:
                try:
                    evaluate_response = self._type_text_with_evaluate(
                        tab_id=tab_id,
                        text=text,
                        press_enter=press_enter,
                        selector=inferred_selector
                    )
                    return {
                        "ok": True,
                        "mode": "evaluate_inferred_selector_by_ref",
                        "selector": inferred_selector,
                        "refRole": ref_role,
                        "response": evaluate_response
                    }
                except Exception:
                    pass

            try:
                r = self.session.post(f"{self.base_url}/tabs/{tab_id}/type", json=payload, timeout=30)
                r.raise_for_status()
                return {
                    "ok": True,
                    "mode": "type_first_by_ref",
                    "response": r.json()
                }
            except Exception:
                # Fallback a evaluate para sitios/versiones donde /type no funciona bien.
                if use_js_fallback:
                    try:
                        evaluate_response = self._type_text_with_evaluate(
                            tab_id=tab_id,
                            text=text,
                            press_enter=press_enter,
                            selector=selector
                        )
                        return {
                            "ok": True,
                            "mode": "evaluate_fallback_after_type_by_ref",
                            "response": evaluate_response
                        }
                    except Exception:
                        pass
                raise

        # Estrategia preferida: igual que en CMD, primero evaluate tras enfocar el ref.
        if use_js_fallback:
            try:
                evaluate_response = self._type_text_with_evaluate(
                    tab_id=tab_id,
                    text=text,
                    press_enter=press_enter,
                    selector=selector
                )
                return {
                    "ok": True,
                    "mode": "evaluate_first",
                    "response": evaluate_response
                }
            except Exception:
                # Si evaluate no funciona en esta versión/sitio, intentar /type.
                pass

        try:
            r = self.session.post(f"{self.base_url}/tabs/{tab_id}/type", json=payload, timeout=30)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            status_code = getattr(e.response, "status_code", None)
            if not use_js_fallback or status_code != 500:
                raise

            fallback_response = self._type_text_with_evaluate(
                tab_id=tab_id,
                text=text,
                press_enter=press_enter,
                selector=selector
            )
            return {
                "ok": True,
                "fallback": "evaluate",
                "response": fallback_response
            }
            
            
    def wait_for_download_and_save(self, tab_id, save_path=None, file_type="Excel", overwrite=True):
        import os
        import time
        import glob
        import shutil
        
        if not tab_id:
            raise Exception("tab_id is required.")

        tab_id = str(tab_id).strip()

        # 1. Mapeo y normalización estricta
        extension_by_type = {
            "EXCEL": "xlsx",
            "PDF": "pdf",
            "TXT": "txt"
        }

        file_type_normalized = str(file_type).strip().upper()
        selected_type = file_type_normalized if file_type_normalized in extension_by_type else "EXCEL"
        expected_ext = extension_by_type[selected_type]

        # 2. Configuración de rutas de destino
        if not save_path:
            save_path = os.path.join(os.getcwd(), "cartola_movimientos.{}".format(expected_ext))

        save_path = os.path.abspath(str(save_path).strip())

        target_dir = os.path.dirname(save_path)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir)

        if os.path.exists(save_path) and not overwrite:
            raise Exception("Target file already exists and overwrite is disabled: {}".format(save_path))

        # =========================================================================
        # VIGILANTE ROBUSTO PARA DESCARGAS EN SEGUNDO PLANO
        # - Considera archivos temporales (.crdownload/.tmp)
        # - Prioriza archivos nuevos o modificados desde el inicio
        # - Espera estabilidad breve para evitar mover archivos a medio escribir
        # - MEJORADO: Manejo de archivos de tamano 0 y busqueda en multiples patrones
        # =========================================================================
        download_dir = os.environ.get("TEMP") or os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp")
        
        patron_camofox = os.path.join(download_dir, "camofox-download-*")
        patron_ext = os.path.join(download_dir, "*.{}".format(expected_ext))
        patron_crdownload = os.path.join(download_dir, "*.crdownload")
        patron_tmp = os.path.join(download_dir, "*.tmp")
        # Busqueda amplia: cualquier archivo reciente en temp (con margen de error)
        patron_wildcard = os.path.join(download_dir, "*")

        found_file = None
        timeout = 90
        stable_seconds = 0.8
        start_time = time.time()
        start_guard = start_time - 3

        seen_files = {}
        preexisting = set(glob.glob(patron_camofox) + glob.glob(patron_ext) + 
                         glob.glob(patron_crdownload) + glob.glob(patron_tmp))

        consecutive_stable = {}
        
        while time.time() - start_time < timeout:
            tmp_files = glob.glob(patron_tmp)
            crdownload_files = glob.glob(patron_crdownload)
            
            # Buscar primero la extension elegida por el usuario
            archivos_actuales = glob.glob(patron_camofox) + glob.glob(patron_ext)
            
            # Si no hay archivos con extension esperada, busca en crdownload/tmp como fallback
            if not archivos_actuales:
                archivos_actuales = (glob.glob(patron_crdownload) + glob.glob(patron_tmp))
            
            # Si aún no hay nada, busca patrones mas amplios: archivos recientes en Temp
            if not archivos_actuales:
                # Busca CUALQUIER archivo modificado en los últimos 5 segundos
                all_temp_files = [f for f in glob.glob(patron_wildcard) if os.path.isfile(f)]
                archivos_actuales = [
                    f for f in all_temp_files 
                    if (time.time() - os.path.getmtime(f)) < 5 and os.path.getsize(f) > 0
                ]
            
            candidatos = []

            for path in archivos_actuales:
                if not os.path.exists(path):
                    continue

                try:
                    mtime = os.path.getmtime(path)
                    size = os.path.getsize(path)
                except OSError:
                    continue

                # CAMBIO IMPORTANTE: Permitir archivos pequenos pero no vacios
                # Algunos navegadores crean archivos muy pequenos antes de llenarlos
                if size <= 0:
                    continue

                filename = os.path.basename(path)
                is_camofox_pattern = filename.startswith('camofox-download-')
                
                is_new = path not in preexisting
                # No descartar archivos camofox-download-* aunque sean preexistentes
                if not is_new and not is_camofox_pattern and mtime < start_guard:
                    continue

                now = time.time()
                
                # Si es archivo reciente (modificado hace menos de 3s) y tiene tamaño, probablemente este listo
                time_since_modified = now - mtime
                
                if size > 1024 and time_since_modified < 3:  # Reciente y con contenido
                    prev = seen_files.get(path)
                    if prev and prev[0] == size and prev[1] == mtime and (now - prev[2]) >= 0.3:
                        # Si no cambio en 0.3s, es estable
                        candidatos.append((mtime, path))
                    else:
                        seen_files[path] = (size, mtime, now)
                elif is_camofox_pattern and size > 1024:  # camofox pattern - aceptar inmediatamente
                    # Si ya está estable (observado 2+ veces sin cambios), aceptar
                    prev = seen_files.get(path)
                    if prev:
                        if prev[0] == size and prev[1] == mtime and (now - prev[2]) >= 0.1:
                            # Estable desde hace 0.1s → aceptar
                            candidatos.append((mtime, path))
                        else:
                            # Cambió → registrar nueva observación
                            seen_files[path] = (size, mtime, now)
                    else:
                        # Primera observación: registrar PERO si tiene tamaño decente, aceptar también
                        # porque probablemente ya está descargado (especialmente si es preexistente)
                        seen_files[path] = (size, mtime, now)
                        if is_new or (not is_new and size > 40000):
                            # Es nuevo O preexistente con tamaño grande → probablemente listo
                            candidatos.append((mtime, path))
                else:
                    prev = seen_files.get(path)
                    # Verificar estabilidad normal para otros archivos
                    if prev and prev[0] == size and prev[1] == mtime and (now - prev[2]) >= stable_seconds:
                        consecutive_stable[path] = consecutive_stable.get(path, 0) + 1
                        if consecutive_stable[path] >= 2:
                            candidatos.append((mtime, path))
                    elif prev is None or prev[0] != size or prev[1] != mtime:
                        consecutive_stable[path] = 0
                        seen_files[path] = (size, mtime, now)
                    else:
                        seen_files[path] = (size, mtime, now)

            if candidatos:
                found_file = sorted(candidatos, key=lambda x: x[0], reverse=True)[0][1]
                break
            
            # Si hay archivos temporales, esperar mas
            if tmp_files or crdownload_files:
                time.sleep(1.0)
                continue
                
            time.sleep(0.5)

        # =========================================================================
        # MOVIMIENTO SEGURO DEL ARCHIVO A TU RUTA
        # =========================================================================
        if found_file and os.path.exists(found_file):
            try:
                actual_file = found_file
                
                # Si el archivo no tiene extension, asignar la esperada
                if not actual_file.endswith(('.xlsx', '.pdf', '.txt', '.crdownload', '.tmp')):
                    temp_rename = actual_file + '.' + expected_ext
                    os.rename(actual_file, temp_rename)
                    actual_file = temp_rename
                
                # Si el archivo descargado tiene extension .crdownload o .tmp, renombrarlo
                if actual_file.endswith('.crdownload') or actual_file.endswith('.tmp'):
                    temp_file = actual_file.rsplit('.', 1)[0] + '.' + expected_ext
                    os.rename(actual_file, temp_file)
                    actual_file = temp_file
                
                if os.path.exists(save_path) and overwrite:
                    os.remove(save_path)
                
                shutil.move(actual_file, save_path)
                
                return {
                    "ok": True,
                    "tabId": tab_id,
                    "fileType": selected_type,
                    "savePath": save_path,
                    "mode": "time_window_watcher",
                    "msg": "Archivo detectado por ventana de tiempo y movido con éxito."
                }
            except Exception as move_error:
                return {
                    "ok": False,
                    "error": f"Archivo detectado en Temp, pero falló al moverlo: {str(move_error)}"
                }

        # DEBUG: Listar archivos en temp para investigar
        all_files_in_temp = glob.glob(patron_wildcard)
        files_info = []
        for f in all_files_in_temp:
            if os.path.isfile(f):
                try:
                    size = os.path.getsize(f)
                    mtime = os.path.getmtime(f)
                    age = time.time() - mtime
                    files_info.append({
                        "name": os.path.basename(f),
                        "size": size,
                        "age_seconds": round(age, 2),
                        "in_preexisting": f in preexisting
                    })
                except:
                    pass
        
        return {
            "ok": False,
            "tabId": tab_id,
            "fileType": selected_type,
            "error": "Timeout: No se encontro ningun archivo descargado estable dentro del tiempo de espera.",
            "downloadDir": download_dir,
            "downloadStatus": 404,
            "debug_files_in_temp": files_info,
            "expected_ext": expected_ext,
            "timeout_seconds": timeout,
            "elapsed_seconds": round(time.time() - start_time, 2)
        }
    def screenshot(self, tab_id, save_path=None):
        def _save_bytes(target_path, content):
            target_path = os.path.abspath(str(target_path).strip())
            directory = os.path.dirname(target_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            with open(target_path, "wb") as f:
                f.write(content)
            return target_path

        r = requests.get(
            f"{self.base_url}/tabs/{tab_id}/screenshot",
            params={"userId": self.user_id},
            timeout=60
        )
        r.raise_for_status()

        # Algunas versiones responden JSON y otras devuelven imagen binaria.
        content_type = (r.headers.get("Content-Type") or "").lower()
        if "application/json" in content_type:
            data = r.json()
            if save_path and isinstance(data, dict):
                b64_value = data.get("base64") or data.get("imageBase64") or data.get("screenshotBase64")
                if b64_value:
                    raw_b64 = b64_value.split(",", 1)[1] if "base64," in b64_value else b64_value
                    image_bytes = base64.b64decode(raw_b64)
                    data["savedPath"] = _save_bytes(save_path, image_bytes)
            return data

        try:
            return r.json()
        except ValueError:
            saved_path = None
            if save_path:
                saved_path = _save_bytes(save_path, r.content)
            image_b64 = base64.b64encode(r.content).decode("utf-8")
            response = {
                "ok": True,
                "tabId": tab_id,
                "contentType": content_type or "application/octet-stream",
                "base64": image_b64
            }
            if saved_path:
                response["savedPath"] = saved_path
            return response
        
    def scroll(self, tab_id, direction: str, amount: int):
    # La URL DEBE incluir /tabs/{tab_id}/action
        url = f"{self.base_url}/tabs/{tab_id}/scroll"
        
        payload = {
            "userId": self.user_id,
            "direction":str(direction).lower(),
            "amount": int (amount)
        
        }
        
        r = requests.post(url, json=payload)
        r.raise_for_status()
        return r.json()
        