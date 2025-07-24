import json
from PIL import Image, ImageDraw, ImageFont


# --- DADOS DA CRIATURA ---
ARQUIVO_FICHA_JSON = 'Dados.json'


with open(ARQUIVO_FICHA_JSON, 'r', encoding='utf-8') as f:
    ficha = json.load(f)

# --- CONFIGURAÇÕES DE ESTILO ---
WIDTH, HEIGHT = 800, 8000 # Começa com uma tela bem alta para caber todo o conteúdo
BG_COLOR = (255, 255, 255)
BOX_COLOR = (230, 230, 230)
HEADER_COLOR = (70, 70, 70)
TEXT_COLOR = (0, 0, 0)
FONT_PATH_BOLD = "arial.ttf"
FONT_PATH_REGULAR = "arial.ttf"

# --- INICIALIZAÇÃO DA IMAGEM ---
img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# --- FONTES ---
try:
    font_title = ImageFont.truetype(FONT_PATH_BOLD, 20)
    font_header = ImageFont.truetype(FONT_PATH_BOLD, 16)
    font_text = ImageFont.truetype(FONT_PATH_REGULAR, 14)
    font_text_bold = ImageFont.truetype(FONT_PATH_REGULAR.replace(".ttf", "bd.ttf"), 14)
except IOError:
    font_title = ImageFont.load_default()
    font_header = ImageFont.load_default()
    font_text = ImageFont.load_default()
    font_text_bold = ImageFont.load_default()

# --- FUNÇÕES AUXILIARES DE DESENHO ---
def draw_text(pos, text, font=font_text, fill=TEXT_COLOR, anchor="la"):
    draw.text(pos, text, font=font, fill=fill, anchor=anchor)

def draw_header_box(pos, size, text):
    x, y = pos
    w, h = size
    draw.rectangle([x, y, x + w, y + h], outline=TEXT_COLOR, fill=BOX_COLOR)
    draw_text((x + w / 2, y + h / 2), text, font=font_header, anchor="mm")

def draw_value_box(pos, size, label, value):
    x, y = pos
    w, h = size
    draw_header_box(pos, (w, h/2), label)
    draw_text((x + w / 2, y + h * 0.75), value, font=font_text, anchor="mm")

def wrap_text(text, font, max_width):
    lines = []
    words = text.split(' ')
    while len(words) > 0:
        line = ''
        while len(words) > 0 and font.getbbox(line + words[0])[2] <= max_width:
            line += words.pop(0) + ' '
        lines.append(line.strip())
    return lines

def draw_rich_text(start_pos, parts, y_offset=0):
    x, y = start_pos
    current_x = x
    for font, text in parts:
        draw_text((current_x, y), text, font=font)
        current_x += font.getbbox(text)[2]
    return y + y_offset

def calcular_modificador(valor):
    mod = (valor - 10) // 2
    return f"+{mod}" if mod >= 0 else str(mod)

# --- DESENHANDO A FICHA ---
y_cursor = 0

# NOME DA CRIATURA
draw.rectangle([40, 30, WIDTH - 40, 90], outline=TEXT_COLOR, width=1)
draw_text((50, 35), ficha["nome"].upper(), font=font_title, anchor="la")
draw_text((50, 72), ficha["tipo_subtipo_descritores_tamanho"], font=font_text)

# FUNÇÃO E ND
draw.rectangle([WIDTH - 240, 30, WIDTH - 40, 60], outline=TEXT_COLOR, width=1)
draw_header_box((WIDTH - 240, 30), (120, 30), "Função")
draw_header_box((WIDTH - 120, 30), (80, 30), "ND")
draw_text((WIDTH - 180, 45+30), ficha["funcao"], font=font_text, anchor="mm")
draw_text((WIDTH - 80, 45+30), ficha["nd"], font=font_text, anchor="mm")

y_cursor = 100

# PV, CA, RD, PROF, INICIATIVA
stats = [("PV", ficha["pv"]), ("CA", ficha["ca"]), ("RD", ficha["rd"]),
         ("PROFICIÊNCIA", ficha["proficiencia"]), ("INICIATIVA", ficha["iniciativa"])]
stat_box_width = (WIDTH - 80) / len(stats)
for i, (label, value) in enumerate(stats):
    draw_value_box((40 + i * stat_box_width, y_cursor), (stat_box_width, 50), label, value)

y_cursor += 60

# ATRIBUTOS
attrs = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]
attr_box_width = (WIDTH - 80) / len(attrs)
for i, attr in enumerate(attrs):
    attr_value = ficha[attr.lower()]
    mod_str = calcular_modificador(attr_value)
    display_text = f"{attr_value} ({mod_str})"
    draw_header_box((40 + i * attr_box_width, y_cursor), (attr_box_width, 25), attr)
    draw_text((40 + i * attr_box_width + attr_box_width/2, y_cursor + 40), display_text, font=font_text, anchor="mm")

y_cursor += 70

# --- SEÇÃO ADICIONAL ---
draw.rectangle([40, y_cursor, WIDTH - 40, y_cursor + 120], fill=BOX_COLOR, outline=TEXT_COLOR)
y_text = y_cursor + 10
draw_text((50, y_text), "SENTIDOS:", font=font_text_bold)
draw_text((150, y_text), ficha["sentidos"])
y_text += 30
draw_text((50, y_text), "MOVIMENTO:", font=font_text_bold)
draw_text((150, y_text), ficha["movimento"])
y_text += 30
draw_text((50, y_text), "PERÍCIAS:", font=font_text_bold)
draw_text((150, y_text), ficha["pericias"])
y_text += 30
draw_text((50, y_text), "IDIOMAS:", font=font_text_bold)
draw_text((150, y_text), ficha["idiomas"])

y_cursor += 130

# --- EXPERIÊNCIA ---
exp_box_width = (WIDTH - 80) / 2
box_height = 50

# Cabeçalho XP
draw_header_box((40, y_cursor), (WIDTH - 80, 25), "XP")
y_cursor += 25

# Box Coletivo
coletivo_x = 40
coletivo_y = y_cursor
draw.rectangle([coletivo_x, coletivo_y, coletivo_x + exp_box_width, coletivo_y + box_height], outline=TEXT_COLOR, width=1)
draw_text((coletivo_x + exp_box_width / 2, coletivo_y + 15), "COLETIVO", font=font_header, anchor="mm")
draw_text((coletivo_x + exp_box_width / 2, coletivo_y + 35), ficha["exp_coletivo"], font=font_text, anchor="mm")

# Box Individual
individual_x = 40 + exp_box_width
individual_y = y_cursor
draw.rectangle([individual_x, individual_y, individual_x + exp_box_width, individual_y + box_height], outline=TEXT_COLOR, width=1)
draw_text((individual_x + exp_box_width / 2, individual_y + 15), "INDIVIDUAL", font=font_header, anchor="mm")
draw_text((individual_x + exp_box_width / 2, individual_y + 35), ficha["exp_individual"], font=font_text, anchor="mm")

y_cursor += box_height + 10 # 50px for box, 10px for padding

def draw_section(y_start, title, content_list):
    y = y_start
    draw.rectangle([40, y, WIDTH - 40, y + 30], fill=HEADER_COLOR)
    draw_text((WIDTH/2, y + 15), title, font=font_header, fill="white", anchor="mm")
    y += 30
    
    content_y_start = y
    y += 10
    
    for item in content_list:
        if isinstance(item, dict): # Para Características e Ataques
            bold_part = f"{item['nome']}. "
            regular_part = item['descricao']
            full_text = bold_part + regular_part
            wrapped_lines = wrap_text(full_text, font_text, WIDTH - 100)
            
            for i, line in enumerate(wrapped_lines):
                if i == 0:
                    draw_rich_text((50, y), [(font_text_bold, bold_part), (font_text, line[len(bold_part):])])
                else:
                    draw_text((50, y), line)
                y += 20

        else: # Para Defesas e Runas
            parts = item.split(": ", 1)
            if len(parts) == 2:
                bold_part = f"{parts[0]}: "
                regular_part = parts[1]
                full_text = bold_part + regular_part
                wrapped_lines = wrap_text(full_text, font_text, WIDTH - 100)
                
                for i, line in enumerate(wrapped_lines):
                    if i == 0:
                        draw_rich_text((50, y), [(font_text_bold, bold_part), (font_text, line[len(bold_part):])])
                    else:
                        draw_text((50, y), line)
                    y += 20
            else:
                wrapped_lines = wrap_text(item, font_text, WIDTH - 100)
                for line in wrapped_lines:
                    draw_text((50, y), line)
                    y += 20
        y += 5 # Espaço entre itens

    # Desenha o contorno da seção de conteúdo
    draw.rectangle([40, content_y_start, WIDTH - 40, y], outline=TEXT_COLOR, width=1)
    return y + 10

# --- DEFESAS ---
defesas_content = [
    f"Salvaguardas: {ficha['salvaguardas']}",
    f"Resistência a danos: {ficha['resistencias_dano']}",
    f"Imunidade a danos: {ficha['imunidades_dano']}",
    f"Vulnerabilidade a danos: {ficha['vulnerabilidades_dano']}",
    f"Imunidade a condições: {ficha['imunidades_condicao']}"
]
y_cursor = draw_section(y_cursor, "DEFESAS", defesas_content)

# --- CARACTERÍSTICAS ---
y_cursor = draw_section(y_cursor, "CARACTERÍSTICAS", ficha["caracteristicas"])

# --- ATAQUES ---
y_cursor = draw_section(y_cursor, "ATAQUES", ficha["ataques"])

# --- REAÇÕES ---
reacoes_content = [
    {
        "nome": reacao["nome"],
        "descricao": f"Gatilho: {reacao['gatilho']}. Resposta: {reacao['resposta']}"
    }
    for reacao in ficha["reacoes"]
]
y_cursor = draw_section(y_cursor, "REAÇÕES", reacoes_content)

# --- RUNAS ---
runas_content = [
    f"Pulso Rúnico: {ficha['pulso_runico']}",
    f"Runas: {ficha['runas']}"
]
y_cursor = draw_section(y_cursor, "RUNAS", runas_content)


# --- RECURSOS ÉPICOS ---
epic_resources_content = [
    f"Carga de ações épicas por turno: {ficha['cargas_acoes_epicas_por_turno']}",
    f"Pontos de Resiliência: {ficha['pontos_resiliencia']}",
    f"Pontos gastos para resistir: {ficha['pontos_gastos_para_resistir']}"
]
y_cursor = draw_section(y_cursor, "RECURSOS ÉPICOS", epic_resources_content)


# --- SALVAR IMAGEM ---
# Adiciona um preenchimento na parte inferior para um melhor visual
final_height = y_cursor + 20 
# Corta a imagem para a altura calculada
img = img.crop((0, 0, WIDTH, final_height))

img_path = "Ficha-" + ficha['nome'].replace(" ", "-") + ".png"
img.save(img_path)

img_path