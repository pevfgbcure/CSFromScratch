import os
from timeit import default_timer as timer

import pygame
from Chip8.vm import SCREEN_HEIGHT, SCREEN_WIDTH, VM  # type: ignore


def run(program_data: bytes, name: str):
    # Start Pygame, create the window, and load the sound.
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
    pygame.display.set_caption(f"Chip8 - {os.path.basename(name)}")
    bee_sound = pygame.mixer.Sound(
        os.path.dirname(os.path.realpath(__file__)) + "/bee.wav"
    )
    currently_playing_sound = False
    vm = VM(program_data)  # load the virtual machine with the program data.
    timer_accumulator = 0.0  # used to limit the timer to 60 Hz.
    # Main virtual machine loop.
    while True:
        frame_start = timer()
        vm.step()
        if vm.needs_redraw:
            pygame.surfarray.blit_array(screen, vm.display_buffer)
            pygame.display.flip()
