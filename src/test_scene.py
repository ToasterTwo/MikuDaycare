import logic
import logic.creature
import logic.progress_bar
import logic.scene as scn
import logic.game_components as gcomp


def make()->scn.Scene:
    bar_shape = gcomp.Rectangle(dimensions=(100, 10), color = (0xff, 0, 0), position=[0., 0.])
    bar_script = logic.progress_bar.ProgressBar(None, 10, 10, bar_shape, logic.progress_bar.BarMode.HORIZONTAL, logic.progress_bar.BarAligngment.TOPLEFT)
    bar_transform = gcomp.Transform(None, [0., 0.], 0)
    happy_bar = gcomp.GameObject(bar_shape, bar_script, bar_transform)

    creature_brain = logic.creature.CreatureBehaviour(None, happy_bar)
    miku_image = logic.creature.body_image
    miku_transform = gcomp.Transform(None, [200.,200.], 0)
    hair = logic.creature.hair_sprite
    eyes = logic.creature.eyes_sprite
    mouth = logic.creature.mouth_sprite
    left_arm = logic.creature.left_arm_sprite
    right_arm = logic.creature.right_arm_sprite


    miku = gcomp.GameObject(creature_brain,
                            miku_image, 
                            miku_transform, 
                            hair, 
                            eyes, 
                            mouth,
                            left_arm,
                            right_arm)

    main_scene = scn.Scene()
    main_scene.add_objects(happy_bar, miku, hair, eyes, mouth, left_arm, right_arm)

    return main_scene