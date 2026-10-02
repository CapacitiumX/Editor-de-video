import sys
import subprocess
import importlib.util

# --- AUTO-INSTALADOR SILENCIOSO ---
def verificar_e_instalar(paquete, nombre_import=None):
    if nombre_import is None:
        nombre_import = paquete
    if importlib.util.find_spec(nombre_import) is None:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", paquete, "--quiet"])
        except:
            pass

verificar_e_instalar("requests")
verificar_e_instalar("Pillow", "PIL")
verificar_e_instalar("sounddevice")
verificar_e_instalar("soundfile")
verificar_e_instalar("numpy")
verificar_e_instalar("edge_tts")

import urllib3
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk, colorchooser, simpledialog
import os, requests, ssl, threading, time, re, random, asyncio
from io import BytesIO
from PIL import Image, ImageTk, ImageDraw, ImageEnhance, ImageFont, ImageColor, ImageOps, ImageFilter
import sounddevice as sd
import soundfile as sf
import numpy as np
import edge_tts

# CONFIGURACIÓN DE SEGURIDAD MAC
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass

class CapacitiumX_30Fotos_Pro:
    def __init__(self, root):
        self.root = root
        self.root.title("CAPACITIUMX - 30 FOTOS, ANIMACIONES & TRANSICIONES PRO 🎬✨")
        self.root.geometry("1550x980")
        self.root.configure(bg="#050505")

        self.clips = []
        self.selected_clip_index = None
        self.is_playing = False
        self.full_story_text = ""
        self.playhead_x = 150
        self.ultima_busqueda = "Tema"
        
        # Variables de Voz y Mute
        self.grabando_voz = False
        self.ruta_mi_voz = None
        self.mute_activado = tk.BooleanVar(value=False)
        
        # VOCES OFICIALES NEURONALES DE MICROSOFT EDGE 100% OPERATIVAS
        self.voces_disponibles = {
            "Dalia (México 🇲🇽 - Femenina)": "es-MX-DaliaNeural",
            "Jorge (México 🇲🇽 - Masculina)": "es-MX-JorgeNeural",
            "Luciano (México 🇲🇽 - Masculina Pro)": "es-MX-LucianoNeural",
            "Álvaro (España 🇪🇸 - Masculina)": "es-ES-AlvaroNeural",
            "Elvira (España 🇪🇸 - Femenina)": "es-ES-ElviraNeural",
            "Lucía (España 🇪🇸 - Femenina Pro)": "es-ES-LuciaNeural",
            "Elena (Argentina 🇦🇷 - Femenina)": "es-AR-ElenaNeural",
            "Tomás (Argentina 🇦🇷 - Masculina)": "es-AR-TomasNeural"
        }
        self.voz_sel = tk.StringVar(value="Dalia (México 🇲🇽 - Femenina)")

        self.desktop = os.path.expanduser("~/Desktop")
        self.magic_folder = os.path.join(self.desktop, "FOTOS_PARA_EL_VIDEO")
        if not os.path.exists(self.magic_folder):
            os.makedirs(self.magic_folder)

        # --- 12 ESTILOS DE FUENTE PARA MAC ---
        self.fuentes_dict = {
            "Impact (Póster)": "/System/Library/Fonts/Supplemental/Impact.ttf",
            "Helvetica Bold": "/System/Library/Fonts/Helvetica.ttc",
            "Futura Medium": "/System/Library/Fonts/Supplemental/Futura.ttc",
            "Arial Black": "/Library/Fonts/Arial Black.ttf",
            "Times Bold": "/System/Library/Fonts/Times.ttc",
            "Bodoni": "/System/Library/Fonts/Supplemental/Bodoni 72.ttc",
            "Copperplate": "/System/Library/Fonts/Supplemental/Copperplate.ttc",
            "Didot": "/System/Library/Fonts/Supplemental/Didot.ttc",
            "Optima": "/System/Library/Fonts/Supplemental/Optima.ttc",
            "Papyrus": "/System/Library/Fonts/Supplemental/Papyrus.ttc",
            "Verdana": "/Library/Fonts/Verdana.ttf",
            "Courier Bold": "/System/Library/Fonts/Courier.dfont"
        }
        self.fuentes_finales = {n: r for n, r in self.fuentes_dict.items() if os.path.exists(r)}
        if not self.fuentes_finales:
            self.fuentes_finales["Default"] = "default"

        self.setup_ui()

    def setup_ui(self):
        # --- BARRA SUPERIOR ---
        top = tk.Frame(self.root, bg="#111", pady=10)
        top.pack(fill="x")
        
        tk.Label(top, text="🔍 TEMA:", bg="#111", fg="#00ff00", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        self.entry_ia = tk.Entry(top, width=15, font=("Arial", 11))
        self.entry_ia.pack(side="left", padx=5)
        
        # BOTÓN CONFIGURADO PARA 30 FOTOS
        tk.Button(top, text="TRAER 30 FOTOS ✨", bg="#7c3aed", fg="white", font=("Arial", 10, "bold"), command=self.start_multi_search).pack(side="left", padx=5)
        
        # NUEVOS BOTONES: AGREGAR DESDE PC Y REEMPLAZAR
        tk.Button(top, text="➕ AGREGAR PC", bg="#047857", fg="white", font=("Arial", 9, "bold"), command=self.agregar_foto_pc).pack(side="left", padx=4)
        tk.Button(top, text="🔄 REEMPLAZAR", bg="#b45309", fg="white", font=("Arial", 9, "bold"), command=self.reemplazar_clip).pack(side="left", padx=4)

        tk.Button(top, text="🗣️️ HISTORIA", bg="#065f46", fg="white", font=("Arial", 10, "bold"), command=self.open_text_window).pack(side="left", padx=6)
        
        tk.Label(top, text="Voz Microsoft:", bg="#111", fg="#38bdf8", font=("Arial", 9, "bold")).pack(side="left", padx=2)
        self.combo_voces = ttk.Combobox(top, textvariable=self.voz_sel, values=list(self.voces_disponibles.keys()), state="readonly", width=24)
        self.combo_voces.pack(side="left", padx=4)

        # BOTONES DE VOZ Y MUTE
        self.btn_grabar = tk.Button(top, text="🎙️ NARRAR", bg="#b91c1c", fg="white", font=("Arial", 9, "bold"), command=self.toggle_grabacion)
        self.btn_grabar.pack(side="left", padx=4)

        tk.Checkbutton(top, text="🔇 MUTE", variable=self.mute_activado, bg="#111", fg="#facc15", selectcolor="#222", font=("Arial", 9, "bold")).pack(side="left", padx=4)

        tk.Button(top, text="🎨 MINIATURA PRO", bg="#d97706", fg="white", font=("Arial", 9, "bold"), command=self.generar_kit_youtuber).pack(side="left", padx=6)
        tk.Button(top, text="📥 CREAR VIDEO", bg="#2563eb", fg="white", font=("Arial", 9, "bold"), command=self.descarga_total_sin_cortes).pack(side="left", padx=6)
        tk.Button(top, text="🗑 QUITAR", bg="#450a0a", fg="white", font=("Arial", 9, "bold"), command=self.quitar_clip).pack(side="right", padx=10)

        # MONITOR
        mid = tk.Frame(self.root, bg="#050505")
        mid.pack(expand=True, fill="both")
        self.mon_label = tk.Label(mid, bg="black", width=850, height=480)
        self.mon_label.pack(pady=10)
        
        play_frame = tk.Frame(mid, bg="#050505")
        play_frame.pack()
        tk.Button(play_frame, text="▶ PLAY PREVIEW", bg="#166534", fg="white", command=self.toggle_play).pack(side="left", padx=5)
        tk.Button(play_frame, text="⏹ STOP", bg="#991b1b", fg="white", command=self.stop_play).pack(side="left", padx=5)

        # --- TIMELINE CON SCROLLBAR ---
        timeline_frame = tk.Frame(self.root, bg="#0a0a0a")
        timeline_frame.pack(fill="x", side="bottom")
        
        self.scrollbar = ttk.Scrollbar(timeline_frame, orient="horizontal")
        self.scrollbar.pack(side="bottom", fill="x")
        
        self.canvas = tk.Canvas(timeline_frame, bg="#050505", height=160, highlightthickness=0, xscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="top", fill="x")
        self.scrollbar.config(command=self.canvas.xview)
        
        self.playhead = self.canvas.create_line(150, 0, 150, 160, fill="red", width=3)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    # ==============================================================
    # GENERADOR DE AUDIO CON VOCES DE MICROSOFT EDGE
    # ==============================================================
    def generar_audio_edge_sincrono(self, texto, ruta_salida):
        if not texto or not texto.strip():
            texto = "Bienvenidos a este video oficial."
        
        seleccion = self.voz_sel.get()
        voz_code = self.voces_disponibles.get(seleccion, "es-MX-DaliaNeural")

        async def _run():
            communicate = edge_tts.Communicate(texto, voz_code)
            await communicate.save(ruta_salida)

        try:
            asyncio.run(_run())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_run())

    # ==============================================================
    # GRABACIÓN DE VOZ PROPIA
    # ==============================================================
    def toggle_grabacion(self):
        if not self.grabando_voz:
            self.grabando_voz = True
            self.btn_grabar.config(text="⏹ DETENER NARRACIÓN", bg="#ef4444")
            threading.Thread(target=self._hilo_grabar, daemon=True).start()
        else:
            self.grabando_voz = False
            self.btn_grabar.config(text="🎙️ NARRAR", bg="#b91c1c")

    def _hilo_grabar(self):
        try:
            fs = 44100
            self.ruta_mi_voz = os.path.join(self.magic_folder, "mi_voz_narrada.wav")
            frames_grabados = []

            def callback(indata, frames, time, status):
                if self.grabando_voz:
                    frames_grabados.append(indata.copy())

            with sd.InputStream(samplerate=fs, channels=1, callback=callback):
                while self.grabando_voz:
                    time.sleep(0.1)
            
            if frames_grabados:
                audio_data = np.concatenate(frames_grabados, axis=0)
                if np.max(np.abs(audio_data)) < 0.001:
                    self.ruta_mi_voz = None
                    self.root.after(0, lambda: messagebox.showerror("❌ Error", "Micrófono bloqueado por Mac."))
                else:
                    sf.write(self.ruta_mi_voz, audio_data, fs)
                    self.root.after(0, lambda: messagebox.showinfo("✅ Éxito", "Narración grabada."))
            else:
                self.ruta_mi_voz = None
        except:
            self.grabando_voz = False
            self.root.after(0, lambda: self.btn_grabar.config(text="🎙️ NARRAR", bg="#b91c1c"))

    # ==============================================================
    # MOTOR DE BÚSQUEDA EXHAUSTIVO (ESTRICTAMENTE 30 FOTOS)
    # ==============================================================
    def start_multi_search(self):
        q = self.entry_ia.get().strip()
        if not q: return
        self.ultima_busqueda = q 
        self.clips = []
        self.canvas.delete("all")
        self.playhead = self.canvas.create_line(150, 0, 150, 160, fill="red", width=3)
        self.root.title(f"⌛ BUSCANDO 30 FOTOS DE: {q}...")
        threading.Thread(target=self.download_engine, args=(q,), daemon=True).start()

    def download_engine(self, q):
        headers = {"User-Agent": "Mozilla/5.0"}
        links_acumulados = []
        variaciones = [q, f"{q} hd wallpaper", f"{q} photography", f"{q} 4k"]
        
        for var in variaciones:
            if len(links_acumulados) >= 35: break
            try:
                url = f"https://www.bing.com/images/search?q={var.replace(' ', '+')}"
                html = requests.get(url, headers=headers, timeout=5, verify=False).text
                links = re.findall(r'murl&quot;:&quot;(.*?)&quot;', html)
                for l in links:
                    if l.startswith("http") and l not in links_acumulados:
                        links_acumulados.append(l)
            except:
                continue

        exitos = 0
        for url_foto in links_acumulados:
            if exitos >= 30: break  # <--- EXACTAMENTE 30 FOTOS
            try:
                res = requests.get(url_foto, headers=headers, timeout=4, verify=False)
                img_t = Image.open(BytesIO(res.content)).convert("RGB")
                p = os.path.join(self.magic_folder, f"foto_{int(time.time())}_{exitos}.jpg")
                img_t.save(p, "JPEG")
                self.root.after(0, lambda path=p: self.agregar_timeline(path))
                exitos += 1
            except:
                continue
        self.root.after(0, lambda: self.root.title(f"LISTO - {exitos} FOTOS CARGADAS"))

    def agregar_timeline(self, p):
        x = 150 if not self.clips else self.clips[-1]["x"] + 210
        img = Image.open(p); img.thumbnail((180, 100)); tk_t = ImageTk.PhotoImage(img)
        r_id = self.canvas.create_rectangle(x, 20, x+200, 120, outline="#00ff00")
        i_id = self.canvas.create_image(x+100, 70, image=tk_t)
        self.clips.append({"path": p, "x": x, "tk": tk_t, "rect_id": r_id, "img_id": i_id})
        
        self.canvas.config(scrollregion=(0, 0, x + 500, 160))
        self.update_preview(p)

    # ==============================================================
    # NUEVAS FUNCIONES: AGREGAR DESDE PC Y REEMPLAZAR
    # ==============================================================
    def agregar_foto_pc(self):
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes desde la computadora",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.webp")]
        )
        if files:
            for f in files:
                try:
                    img_t = Image.open(f).convert("RGB")
                    p = os.path.join(self.magic_folder, f"foto_pc_{int(time.time())}_{random.randint(100,999)}.jpg")
                    img_t.save(p, "JPEG")
                    self.agregar_timeline(p)
                except:
                    pass
            messagebox.showinfo("✅ Éxito", f"Se agregaron {len(files)} foto(s) desde tu computadora.")

    def reemplazar_clip(self):
        if self.selected_clip_index is not None:
            f = filedialog.askopenfilename(
                title="Seleccionar foto de reemplazo",
                filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.webp")]
            )
            if f:
                try:
                    img_t = Image.open(f).convert("RGB")
                    p = os.path.join(self.magic_folder, f"foto_rep_{int(time.time())}.jpg")
                    img_t.save(p, "JPEG")
                    
                    clip = self.clips[self.selected_clip_index]
                    clip["path"] = p
                    
                    # Actualizar miniatura en el canvas
                    img = Image.open(p)
                    img.thumbnail((180, 100))
                    tk_t = ImageTk.PhotoImage(img)
                    clip["tk"] = tk_t
                    self.canvas.itemconfig(clip["img_id"], image=tk_t)
                    
                    self.update_preview(p)
                    messagebox.showinfo("✅ Éxito", "Foto reemplazada correctamente.")
                except:
                    messagebox.showerror("❌ Error", "No se pudo reemplazar la foto.")
        else:
            messagebox.showwarning("⚠️ Aviso", "Primero haz clic sobre la foto en la línea de tiempo que deseas reemplazar.")

    # ==============================================================
    # MÓDULO DE MINIATURAS
    # ==============================================================
    def generar_kit_youtuber(self):
        if not self.clips: return
        idx = self.selected_clip_index if self.selected_clip_index is not None else 0
        foto_base = self.clips[idx]["path"]
        
        ed = tk.Toplevel(self.root)
        ed.title("EDITOR DE MINIATURAS PROFESIONAL")
        ed.geometry("950x700")
        ed.configure(bg="#1a1a1a")

        v_texto = tk.StringVar(value=f"LA VERDAD SOBRE {self.ultima_busqueda.upper()}")
        v_color_txt = tk.StringVar(value="#FFFF00")
        v_color_bar = tk.StringVar(value="#000000")
        v_fuente = tk.StringVar(value=list(self.fuentes_finales.keys())[0])
        
        v_v_stretch = tk.DoubleVar(value=1.5)
        v_h_stretch = tk.DoubleVar(value=1.0)
        v_pos_x = tk.IntVar(value=640)
        v_pos_y = tk.IntVar(value=600)
        
        v_mostrar_flecha = tk.BooleanVar(value=True)
        v_color_flecha = tk.StringVar(value="#FF0000")
        v_fx = tk.IntVar(value=800)
        v_fy = tk.IntVar(value=300)
        v_fw = tk.IntVar(value=250)
        v_fh = tk.IntVar(value=250)
        v_frot = tk.IntVar(value=45)

        v_blur = tk.IntVar(value=0)
        v_split_dark = tk.IntVar(value=0)

        self.img_lista_para_exportar = None

        frame_controles = tk.Frame(ed, bg="#1a1a1a")
        frame_controles.pack(side="left", fill="y", padx=20, pady=20)
        
        frame_preview = tk.Frame(ed, bg="#1a1a1a")
        frame_preview.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        lbl_preview = tk.Label(frame_preview, bg="black")
        lbl_preview.pack(expand=True)

        notebook = ttk.Notebook(frame_controles)
        notebook.pack(fill="both", expand=True)

        tab_texto = tk.Frame(notebook, bg="#222")
        tab_flecha = tk.Frame(notebook, bg="#222")
        tab_filtros = tk.Frame(notebook, bg="#222")
        notebook.add(tab_texto, text="📝 Texto")
        notebook.add(tab_flecha, text="↪️ Flecha")
        notebook.add(tab_filtros, text="✨ Filtros")

        def crear_imagen_flecha(color_hex):
            img_arr = Image.new("RGBA", (500, 500), (0,0,0,0))
            draw = ImageDraw.Draw(img_arr)
            c = ImageColor.getrgb(color_hex) + (255,)
            draw.arc([50, 150, 450, 550], start=180, end=270, fill=c, width=35)
            draw.polygon([(220, 110), (300, 150), (220, 190)], fill=c)
            return img_arr

        def renderizar_imagen():
            img = Image.open(foto_base).convert("RGBA").resize((1280, 720))
            if v_blur.get() > 0:
                img = img.filter(ImageFilter.GaussianBlur(radius=v_blur.get()))
            
            if v_split_dark.get() > 0:
                oscurecedor = Image.new("RGBA", (1280, 720), (0,0,0,0))
                d_osc = ImageDraw.Draw(oscurecedor)
                if v_split_dark.get() == 1:
                    d_osc.rectangle([0, 0, 640, 720], fill=(0,0,0,180))
                else:
                    d_osc.rectangle([640, 0, 1280, 720], fill=(0,0,0,180))
                img = Image.alpha_composite(img, oscurecedor)

            overlay = Image.new("RGBA", (1280, 720), (0,0,0,0))
            draw = ImageDraw.Draw(overlay)
            
            c_bar = ImageColor.getrgb(v_color_bar.get())
            draw.rectangle([0, 480, 1280, 720], fill=(c_bar[0], c_bar[1], c_bar[2], 210))
            
            f_path = self.fuentes_finales[v_fuente.get()]
            font = ImageFont.truetype(f_path, 100) if f_path != "default" else ImageFont.load_default()
            
            tmp = Image.new("RGBA", (4000, 1000), (0,0,0,0))
            d_tmp = ImageDraw.Draw(tmp)
            txt = v_texto.get()
            
            for o in range(-5, 6):
                for oo in range(-5, 6):
                    d_tmp.text((200+o, 200+oo), txt, font=font, fill="black")
            d_tmp.text((200, 200), txt, font=font, fill=v_color_txt.get())
            
            crop = tmp.crop(tmp.getbbox())
            if crop:
                new_w = max(1, int(crop.width * v_h_stretch.get())) 
                new_h = max(1, int(crop.height * v_v_stretch.get()))
                crop = crop.resize((new_w, new_h), Image.Resampling.LANCZOS)
                overlay.paste(crop, (v_pos_x.get() - crop.width//2, v_pos_y.get() - crop.height//2), crop)

            if v_mostrar_flecha.get():
                flecha_base = crear_imagen_flecha(v_color_flecha.get())
                flecha_base = flecha_base.resize((v_fw.get(), v_fh.get()), Image.Resampling.LANCZOS)
                flecha_base = flecha_base.rotate(v_frot.get(), expand=True, fillcolor=(0,0,0,0))
                overlay.paste(flecha_base, (v_fx.get(), v_fy.get()), flecha_base)
            
            img_final = Image.alpha_composite(img, overlay).convert("RGB")
            return img_final

        def actualizar_preview(*args):
            try:
                img_final = renderizar_imagen()
                self.img_lista_para_exportar = img_final
                img_final.thumbnail((640, 360)) 
                tk_img = ImageTk.PhotoImage(img_final)
                lbl_preview.config(image=tk_img)
                lbl_preview.image = tk_img
            except: pass

        tk.Entry(tab_texto, textvariable=v_texto, width=25, font=("Arial", 11)).pack(pady=5)
        ttk.Combobox(tab_texto, textvariable=v_fuente, values=list(self.fuentes_finales.keys()), state="readonly").pack(pady=5)
        tk.Scale(tab_texto, from_=0, to=1280, variable=v_pos_x, orient="horizontal", label="X Pos").pack()
        tk.Scale(tab_texto, from_=0, to=720, variable=v_pos_y, orient="horizontal", label="Y Pos").pack()
        tk.Scale(tab_texto, from_=0.2, to=5.0, resolution=0.1, variable=v_h_stretch, orient="horizontal", label="Ancho H").pack()

        tk.Checkbutton(tab_flecha, text="Mostrar Flecha", variable=v_mostrar_flecha, bg="#222", fg="white").pack(pady=5)
        tk.Scale(tab_flecha, from_=0, to=1280, variable=v_fx, orient="horizontal", label="X Flecha").pack()
        tk.Scale(tab_flecha, from_=0, to=360, variable=v_frot, orient="horizontal", label="Rotación").pack()

        tk.Scale(tab_filtros, from_=0, to=15, variable=v_blur, orient="horizontal", label="Blur").pack()

        def pt(): v_color_txt.set(colorchooser.askcolor()[1]); actualizar_preview()
        tk.Button(frame_controles, text="🎨 COLOR TEXTO", command=pt).pack(pady=5)

        def exportar():
            if self.img_lista_para_exportar:
                out = os.path.join(self.desktop, f"MINIATURA_{int(time.time())}.jpg")
                self.img_lista_para_exportar.save(out); subprocess.run(["open", out]); ed.destroy()

        tk.Button(frame_controles, text="📥 DESCARGAR", bg="#b91c1c", fg="white", font=("Arial", 11, "bold"), command=exportar).pack(pady=10)

        for var in [v_texto, v_fuente, v_v_stretch, v_h_stretch, v_pos_x, v_pos_y, v_mostrar_flecha, v_fx, v_frot, v_blur]:
            var.trace_add("write", actualizar_preview)
        
        actualizar_preview()

    # ==============================================================
    # RENDER DE VIDEO ROBUSTO CON ANIMACIONES EN CADA FOTO
    # ==============================================================
    def descarga_total_sin_cortes(self):
        if not self.clips: return
        p = filedialog.asksaveasfilename(defaultextension=".mp4", initialfile="video_animado_pro.mp4")
        if p: threading.Thread(target=self.run_render, args=(p,), daemon=True).start()

    def run_render(self, out_path):
        try:
            t = 3.5  # Duración por cada foto
            audio = None
            
            if not self.mute_activado.get():
                if self.ruta_mi_voz and os.path.exists(self.ruta_mi_voz):
                    audio = self.ruta_mi_voz
                elif self.full_story_text:
                    audio = os.path.join(self.magic_folder, "voz_edge_render.mp3")
                    self.generar_audio_edge_sincrono(self.full_story_text, audio)
                
                if audio and os.path.exists(audio):
                    try:
                        dur = float(subprocess.check_output(f"PATH=$PATH:/usr/local/bin:/opt/homebrew/bin ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '{audio}'", shell=True))
                        t = max(2.0, (dur + 1) / len(self.clips))
                    except:
                        pass

            n_frames = int(t * 25)

            # BANCO DE ANIMACIONES ROBUSTAS COMPATIBLES CON TODAS LAS FOTOS
            banco_animaciones = [
                f"zoompan=z='min(zoom+0.0015,1.3)':d={n_frames}:s=1280x720:fps=25",
                f"zoompan=z='max(zoom-0.0015,1.0)':d={n_frames}:s=1280x720:fps=25",
                f"zoompan=z='1.2':x='if(eq(on,1),0,x+1.2)':y='ih/2':d={n_frames}:s=1280x720:fps=25",
                f"zoompan=z='1.2':x='iw/2':y='if(eq(on,1),0,y+1.2)':d={n_frames}:s=1280x720:fps=25"
            ]

            lst = os.path.join(self.magic_folder, "l.txt")
            with open(lst, "w") as f:
                for i, c in enumerate(self.clips):
                    cp = os.path.join(self.magic_folder, f"v_{i}.mp4")
                    animacion_elegida = banco_animaciones[i % len(banco_animaciones)]
                    
                    m = f"scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,{animacion_elegida},fade=t=in:st=0:d=0.3,fade=t=out:st={max(0, t-0.3)}:d=0.3"
                    
                    cmd = f"PATH=$PATH:/usr/local/bin:/opt/homebrew/bin ffmpeg -framerate 25 -loop 1 -i '{c['path']}' -vf \"{m},format=yuv420p\" -t {t} -c:v libx264 -preset ultrafast -y '{cp}'"
                    subprocess.run(cmd, shell=True)
                    f.write(f"file 'v_{i}.mp4'\n")

            if not self.mute_activado.get() and audio and os.path.exists(audio):
                subprocess.run(f"PATH=$PATH:/usr/local/bin:/opt/homebrew/bin ffmpeg -f concat -safe 0 -i '{lst}' -i '{audio}' -c:v copy -c:a aac -shortest -y '{out_path}'", shell=True)
            else:
                subprocess.run(f"PATH=$PATH:/usr/local/bin:/opt/homebrew/bin ffmpeg -f concat -safe 0 -i '{lst}' -c:v copy -y '{out_path}'", shell=True)

            messagebox.showinfo("OK", "¡Video con todas las fotos y efectos generado sin pantallas negras!")
            subprocess.run(["open", os.path.dirname(out_path)])
        except:
            pass

    def update_preview(self, p):
        img = Image.open(p).resize((850, 480))
        self.tk_mon = ImageTk.PhotoImage(img); self.mon_label.config(image=self.tk_mon)

    def toggle_play(self):
        self.is_playing = True
        
        def reproducir_hilo():
            if not self.mute_activado.get():
                if self.ruta_mi_voz and os.path.exists(self.ruta_mi_voz):
                    subprocess.run(["afplay", self.ruta_mi_voz])
                elif self.full_story_text:
                    ruta_mp3 = os.path.join(self.magic_folder, "preview_edge.mp3")
                    self.generar_audio_edge_sincrono(self.full_story_text, ruta_mp3)
                    if os.path.exists(ruta_mp3) and self.is_playing:
                        subprocess.run(["afplay", ruta_mp3])

        threading.Thread(target=reproducir_hilo, daemon=True).start()
        self.run_play_engine()

    def stop_play(self):
        self.is_playing = False
        subprocess.run(["killall", "afplay"], stderr=subprocess.DEVNULL)

    def run_play_engine(self):
        if self.is_playing:
            self.playhead_x += 4
            self.canvas.coords(self.playhead, self.playhead_x, 0, self.playhead_x, 160)
            self.canvas.xview_moveto((self.playhead_x - 150) / max(1, self.canvas.bbox("all")[2]))
            for c in self.clips:
                if c["x"] <= self.playhead_x <= c["x"] + 200:
                    self.update_preview(c["path"])
            self.root.after(50, self.run_play_engine)

    def on_canvas_click(self, event):
        x = self.canvas.canvasx(event.x); self.playhead_x = x
        self.canvas.coords(self.playhead, x, 0, x, 160)
        for i, c in enumerate(self.clips):
            if c["x"] <= x <= c["x"] + 200:
                self.selected_clip_index = i; self.update_preview(c["path"])

    def quitar_clip(self):
        if self.selected_clip_index is not None:
            c = self.clips.pop(self.selected_clip_index)
            self.canvas.delete(c["rect_id"]); self.canvas.delete(c["img_id"])

    def open_text_window(self):
        t = tk.Toplevel(self.root)
        txt = scrolledtext.ScrolledText(t, width=60, height=15); txt.pack(padx=10, pady=10)
        if self.full_story_text: txt.insert("1.0", self.full_story_text)
        tk.Button(t, text="GUARDAR", command=lambda: [setattr(self, 'full_story_text', txt.get("1.0", "end-1c")), t.destroy()]).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk(); app = CapacitiumX_30Fotos_Pro(root); root.mainloop()
