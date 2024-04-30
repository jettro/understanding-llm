import ipywidgets as widgets
from itertools import cycle
from IPython.display import display, HTML, Javascript

def pretty_print_bytes(token_list, encoding):
    # List of 10 distinct colors
    colors = [
        "#708090",  # SlateGray
        "#B0C4DE",  # LightSteelBlue
        "#778899",  # LightSlateGray
        "#4682B4",  # SteelBlue
        "#5F9EA0",  # CadetBlue
        "#8FBC8F",  # DarkSeaGreen
        "#556B2F",  # DarkOliveGreen
        "#6B8E23",  # OliveDrab
        "#8B4513",  # SaddleBrown
        "#9932CC"   # DarkOrchid
    ]

    # Create a color iterator using cycle
    color_iter = cycle(colors)

    # Start the HTML string
    html_str = '<div style="display: flex; flex-wrap: wrap;">'
    
    # Loop through each byte and create a colored box for it.
    for token in token_list:
        color = next(color_iter)
        box = f'''
        <div style="margin: 5px; padding: 2px;">
            <div style="padding: 2px; background-color: {color}; 
                    border: 2px solid black; min-width: 30px; text-align: center; color: black">
                '{encoding.decode_single_token_bytes(token).decode('utf-8')}'
            </div>
            <span style="text-align: middle; margin: 5px">{token}</span>
        </div>
        '''
        html_str += box
    
    # End the HTML string
    html_str += '</div>'
    
    # Display the colored boxes
    display(HTML(html_str))


def print_byte(byte) -> str:
    return f"'{byte.decode('utf-8')}'"


def find_matching_tokens(search_string, vocabulary):
    byte_string = bytes(search_string, 'utf-8')
    exact_matches = [byte_string] if byte_string in vocabulary else []
    matches = [byte for index, byte in enumerate(vocabulary) if byte_string in byte]
    all_matches = exact_matches + matches

    return [print_byte(byte) for byte in all_matches[:10]]


def interactive_mode(encoding, vocabulary):
    input_box = widgets.Text(
        value='',
        placeholder='Type something',
        description='Search:',
        disabled=False
    )
    output_widget = widgets.Output()

    display(input_box, output_widget)

    def on_input_change(change):
        output_widget.clear_output()
        with output_widget:
            matches = find_matching_tokens(change['new'], vocabulary)
            if len(matches) > 0:
                encoded_input = encoding.encode(change['new'])
                pretty_print_bytes(encoded_input, encoding)
            for match in find_matching_tokens(change['new'], vocabulary):
                print(match)


    input_box.observe(on_input_change, names='value')

