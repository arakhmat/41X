import os
import pygame
import numpy as np

from keras.models import load_model
from air_hockey import AirHockey
from gym_air_hockey import DataProcessor

project_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    
    air_hockey = AirHockey()
    processor = DataProcessor()
    
    model = load_model('bottom_ai_model.h5')
    
    action = [0, 0]
    
    frames = np.zeros((1, 10, 128, 128, 3), dtype=np.float32)
    
    i = 0
    while True:

        if any([event.type == pygame.QUIT for event in pygame.event.get()]): break
        frame, _           = air_hockey.step(action)
        frame = processor.process_observation(frame)
        
        frames[0][1:] = frames[0][:-1]
        frames[0][0] = frame
        
        
        
        if i >= 5:
            action = np.argmax(model.predict(frames)[0])
#            print(frames)
        print(action)
        i += 1
        
    
    pygame.quit()
        