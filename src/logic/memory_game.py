from logic.game_components import *
import logic.context as context
import random as rand

class MemoryScript(Script):
    def __init__(self, parent:GameObject, button1: Rectangle, button2:Rectangle, button3:Rectangle, button4:Rectangle, fail_menu: GameObject,
                 score_display: Text, total_score_display: Text, current_score_display: Text):
        Script.__init__(self, parent)
        self._button1 = button1
        self._button2 = button2
        self._button3 = button3
        self._button4 = button4

        # 0 - playing, 1 - awaiting input, 2 - success animation and reset, 3 - failure animation, 4 - reset 5-wait to restart
        self._state = 0
        self._playback_timer = 0
        self._playback_delay = 1
        self._playback_counter = 0
        self._sequence = [rand.randint(1, 4)]
        self._button_lit = False
        self._input_sequence = []
        self._button_timers = [0., 0., 0., 0.]
        self._blink_time = 0.5
        self._blinks = 0
        self._score = 0
        self._session_score = 0 
        self._fail_menu = fail_menu
        self._score_display = score_display
        self._total_display = total_score_display
        self._current_display = current_score_display
    
    def init(self):
        self._button1._color = (127, 0, 0)
        self._button2._color = (0, 127, 0)
        self._button3._color = (0, 0, 127)
        self._button4._color = (127, 127, 0)
    
    def light_button(self, button_id):
        match button_id:
            case 1:
                self._button1._color = (255, 0, 0)
            case 2:
                self._button2._color = (0, 255, 0)
            case 3:
                self._button3._color = (0, 0, 255)
            case 4:
                self._button4._color = (255, 255, 0)

    def darken_button(self, button_id):
        match button_id:
            case 1:
                self._button1._color = (127, 0, 0)
            case 2:
                self._button2._color = (0, 127, 0)
            case 3:
                self._button3._color = (0, 0, 127)
            case 4:
                self._button4._color = (127, 127, 0)

    def update(self, delta_time):
        for i, timer in enumerate(self._button_timers):
            if timer < 0:
                self.darken_button(i+1)
                self._button_timers[i]=0

            else:
                self._button_timers[i]-=delta_time

        match self._state:
            case 0:
                self._playback_timer-=delta_time
                if self._playback_timer<=0:
                    if self._playback_counter<len(self._sequence):
                        bid = self._sequence[self._playback_counter]
                        self.light_button(bid)
                        self._playback_counter+=1
                        self._button_timers[bid-1] = self._playback_delay/2
                        self._playback_timer+=self._playback_delay

                    else:
                        self._input_sequence = []
                        self._state = 1

            
            case 1:
                if len(self._input_sequence) == len(self._sequence):
                    correct = True
                    for inp, real in zip(self._input_sequence, self._sequence):
                        if inp != real:
                            correct = False
                    
                    if correct:
                        self._state = 2
                        self._score += 1
                        self._session_score += 1
                        self._current_display._text = f"{self._score:03}"
                    else: 
                        self._playback_timer = self._playback_delay
                        self._state = 3
                        
            
            case 2:
                if self._playback_timer < 0:
                    if self._blinks<3:
                        for i in range(4):
                            self.light_button(i+1)
                            self._button_timers[i] = self._blink_time/2
                        self._playback_timer = self._blink_time
                        self._blinks+=1
                
                    elif self._blinks >= 3:
                        self._playback_timer = self._playback_delay
                        self._playback_counter = 0
                        self._blinks = 0
                        self._sequence.append(rand.randint(1, 4))
                        self._state = 0
                else:
                    self._playback_timer-=delta_time
            
            case 3:
                if self._playback_timer > 0:
                    self._button1._color = (255, 0 ,0)
                    self._button2._color = (255, 0 ,0)
                    self._button3._color = (255, 0 ,0)
                    self._button4._color = (255, 0 ,0)
                    self._playback_timer-=delta_time
                else:
                    self._playback_timer = self._playback_delay
                    self._state = 5
                    self._score_display._text = f"{self._score:03}"
                    self._total_display._text = f"{self._session_score:03}"
                    self._button1._parent._active = False
                    self._button2._parent._active = False
                    self._button3._parent._active = False
                    self._button4._parent._active = False
                    self._fail_menu.message("fail")
                    

            
            case 4:
                self._button1._parent._active = True
                self._button2._parent._active = True
                self._button3._parent._active = True
                self._button4._parent._active = True
                self._score = 0
                self._playback_counter = 0
                self._sequence = [rand.randint(1, 4)]
                self.init()
                self._state = 0
            
            case 5:
                pass

    def b1(self):
        if self._state == 1:
            self._input_sequence.append(1)
            self._button_timers[0] = self._blink_time
            self.light_button(1)
    
    def b2(self):
        if self._state == 1:
            self._input_sequence.append(2)
            self._button_timers[1] = self._blink_time
            self.light_button(2)



    
    def b3(self):
        if self._state == 1:
            self._input_sequence.append(3)
            self._button_timers[2] = self._blink_time
            self.light_button(3)




    def b4(self):
        if self._state == 1:
            self._input_sequence.append(4)
            self._button_timers[3] = self._blink_time
            self.light_button(4)

    def retry(self):
        self._state = 4
    
    def return_home(self):
        context.set_by_alias("main")
        context.global_vars["score"] = self._session_score
        context.global_vars["energy"] = self._session_score
        self._score = 0
        self._session_score = 0
