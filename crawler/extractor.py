class Extractor(object):
    TABLE_CLS = "product-specs"
    TABLE_ROW_CLS = "product-specs__spec display"

    def __init__(self):
        self.features_name = [
            "marca",
            "linha",
            "modelo",
            "chips",
            "câmera traseira",
            "câmera frontal",
            "tamanho da tela",
            "resolução",
            "velocidade do processador",
            "memória interna",
            "memória ram"
        ]

    def extract_obj(self, soup_obj):
        table = soup_obj.find("table", class_=self.TABLE_CLS)
        t_row = table.tbody.find_all("tr", class_=self.TABLE_ROW_CLS)
        final_obj = {}

        for row in t_row:
            data = row.find_all("td")
            key = str(data[0].string)
            value = str(data[1].string)
            if key.lower() in self.features_name:
                final_obj[key] = value

        return final_obj