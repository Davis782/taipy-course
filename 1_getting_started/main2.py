from taipy.gui import Gui
import taipy.gui.builder as tgb


values = [20, 40, 80]


def compute_data(decay: int) -> list:
    return [cos(i / 6) * exp(-i * decay / 600) for i in range(100)]


def slider_moved(state):
    state.data = compute_data(state.value)


with tgb.Page() as page:
    tgb.text(value="# Taipy Goodbye World Started", mode="md")
    # tgb.slider(value="{values}", on_change=slider_moved)
    # tgb.slider(value="{values}")
    tgb.slider(value="{values}", on_change=slider_moved)


# Create the GUI and run the app
gui = Gui(page).run(use_reloader=True)
gui.run(port=5050)
