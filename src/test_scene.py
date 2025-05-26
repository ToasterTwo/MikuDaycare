import logic.scene as scn
import logic.progress_bar
import logic.creature

def make()->scn.Scene:

    return scn.from_json("resources/scenes/sample.json")
