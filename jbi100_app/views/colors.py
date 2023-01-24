# GUI colours
global bg_colour
global card_colour
global txt_colour
global line_colour

# Marker colours
global marker_1 # Primary colour
global marker_2 # True colour
global marker_3 # False colour
global marker_4  
global marker_5
global marker_off # Disabled colour

global colour_gradient

# Word cloud colour function
global wc_colour_func

#Default values

bg_colour = "#121212"
card_colour = "#212121"
txt_colour = "#f1f1f1"
line_colour = "#424242"

marker_1 = "#548C2F"   # Green
marker_2 = "#A8D5E2"   # Light blue
marker_3 = "#F9A620"   # Orange
marker_4 = "#FFD449"   # Yellow
marker_5 = "#A8D5E2"   # Dark green
marker_off = "#a8a8a8" # Grey

colour_gradient = "Viridis" 

# Word cloud colour functions
def my_tf_color_func(dictionary):
    def my_tf_color_func_inner(
        word, random_state=None, **kwargs
    ):
        return "hsl(90, 50%%, %d%%)" % (dictionary[word])

    return my_tf_color_func_inner
#colour function for word cloud in colourblind mode
def my_tf_color_func_cb(dictionary):
    def my_tf_color_func_inner(
        word, random_state=None, **kwargs
    ):
        return "hsl(174, 37%%, %d%%)" % (dictionary[word])

    return my_tf_color_func_inner

wc_colour_func = my_tf_color_func



