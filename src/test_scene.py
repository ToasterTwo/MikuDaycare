import logic
import logic.creature
import logic.progress_bar
import logic.scene as scn
import logic.game_components as gcomp


def make()->scn.Scene:
    bar_shape = gcomp.Rectangle(dimensions=(100, 100), color = (0xff, 0, 0), position=(0, 0))
    bar_script = logic.progress_bar.ProgressBar(None, 10, 10, bar_shape, logic.progress_bar.BarMode.VERTICAL, logic.progress_bar.BarAligngment.BOTTOMRIGHT)
    bar_transform = gcomp.Transform(None, (300, 150), 0)
    happy_bar = gcomp.GameObject(bar_shape, bar_script, bar_transform)

    creature_brain = logic.creature.CreatureBehaviour(None, happy_bar)
    miku_image = gcomp.Image(path = "resources\images\pngegg.png")
    miku_transform = gcomp.Transform(None, (0,0), 0)
    miku = gcomp.GameObject(creature_brain, miku_image, miku_transform)

    main_scene = scn.Scene()
    main_scene.add_objects(happy_bar, miku)

    return main_scene