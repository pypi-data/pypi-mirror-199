# still need to deal with the case LSCOLORS alredy exists in .bashrc
import os
import os.path

font_dict = {
    "bold": "1",
    "underlined": "4",
}

color_dict = {  # change
    "red": "31",
    "green": "32",
    "orange": "33",
    "blue": "34",
    "purple": "35",
    "cyan": "36",
    "grey": "37",
}


def get_color_code(color_string):
    return color_dict[color_string]


def get_font_code(font_string):
    return font_dict[font_string]


def get_full_path(curr_path):
    return os.path.expanduser(curr_path)


def config(color_c, font_c):
    return "di=" + font_c + ";" + color_c


def add_ls_colors(curr_text, text_add):
    output = curr_text + "\n" + "LS_COLORS=" + '"{}"'.format(text_add)
    return output


def replace_ls_colors(config_string):
    new_line = "LS_COLORS=" + '"{}"'.format(config_string)
    return new_line


def main(color, font):
    path = "~/.bashrc"

    full_path = get_full_path(path)
    color_code = get_color_code(color)
    font_code = get_font_code(font)

    curr_colors = os.popen("echo $LS_COLORS").read()  # make into function?
    print(curr_colors)
    config_string = config(color_code, font_code)
    print(config_string)

    bashrc = open(full_path, "r")
    data = bashrc.read()

    search_line = 'LS_COLORS='
    exists = False
    with open(full_path, 'r') as file:
        lines = file.readlines()
    with open(full_path, 'w') as file:
        for line in lines:
            if search_line in line:
                exists = True
                file.write(replace_ls_colors(config_string))
            else:
                file.write(line)

    if exists is False:
        print("does not exist")
        fin_data = add_ls_colors(data, config_string)
        with open(full_path, "w") as file:
            file.write(fin_data)

        return fin_data.splitlines()[-1]

    return replace_ls_colors(config_string)


if __name__ == "__main__":
    color = "cyan"
    font = "bold"
    main(color, font)
