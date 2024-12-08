def load_styles(path):
    # Cargar colores
    with open("styles\colors.qss", "r") as colors_file:
        colors = colors_file.read()

    # Cargar estilos y reemplazar variables
    with open(path, "r") as styles_file:
        styles = styles_file.read()

    for line in colors.splitlines():
        if line.startswith("@"):
            var_name, var_value = line.split(":")
            styles = styles.replace(var_name.strip(), var_value.strip("; "))

    return styles